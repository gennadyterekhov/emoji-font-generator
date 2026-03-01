import os
import subprocess
import tempfile
from pathlib import Path

from fontTools.misc.transform import Scale
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib import SVGPath
from fontTools.ttLib import TTFont

from emoji_font_generator.config.config import get_ai_dictionary, get_lirbantu_font_filename
from emoji_font_generator.project import get_project_dir


def replace_ligature(ligature):
    ligature = ligature.replace('á', 'a')
    ligature = ligature.replace('í', 'i')
    ligature = ligature.replace('ú', 'u')
    ligature = ligature.replace('é', 'e')
    ligature = ligature.replace('ó', 'o')
    ligature = ligature.replace(' ', '')
    ligature = ligature.replace('?', '')
    ligature = ligature.replace('(', '')
    ligature = ligature.replace(')', '')
    return ligature


def add_ligatures_practical(input_font, ligature_dict, output_font):
    """
    Use fonttools with feature file approach
    """

    # Create a feature file for OpenType ligatures
    feature_content = """languagesystem DFLT dflt;
languagesystem latn dflt;

feature liga {
"""

    for ligature, svg_file in ligature_dict.items():
        if ',' in ligature:
            continue
        ligature = replace_ligature(ligature)
        # Format: ligature name is the glyph name, components are space-separated
        # The ligature name should match a glyph name in the font
        components = ' '.join(ligature)  # This creates "f i" from "fi"
        feature_content += f"    sub {components} by {ligature};\n"

    feature_content += "} liga;\n"

    print("Generated feature file content:")
    print(feature_content)

    # Write feature file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False) as f:
        f.write(feature_content)
        feature_file = f.name

        # Use fonttools to add features
        cmd = [
            'fonttools', 'feaLib', '-o', output_font,
            feature_file, input_font
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Font saved to {output_font}")
        except subprocess.CalledProcessError as e:
            print(f"Error adding features: {e}")
            print(f"stderr: {e.stderr}")
            print(f"stdout: {e.stdout}")
        finally:
            os.unlink(feature_file)


def add_ligatures_with_glyph_check(input_font, ligature_dict, output_font):
    """
    Check glyph names exist and create proper feature syntax
    """

    # First, load the font to see what glyphs are available
    font = TTFont(input_font)

    # Get all glyph names
    glyph_names = set(font.getGlyphOrder())

    print(f"Font has {len(glyph_names)} glyphs")

    # Create feature content
    feature_content = """languagesystem DFLT dflt;
languagesystem latn dflt;

feature liga {
"""

    missing_glyphs = []
    valid_ligatures = 0

    for ligature, svg_file in ligature_dict.items():
        ligature = replace_ligature(ligature)
        print('Checking ligature', ligature)
        # Check if ligature glyph exists
        if ligature not in glyph_names:
            missing_glyphs.append(ligature)
            continue

        # Format depends on what your ligature strings represent
        # Option 1: If ligature is like "f_i" (glyph names with underscores)
        if '_' in ligature:
            components = ligature.replace('_', ' ')
        else:
            # Option 2: If ligature is like "fi" (need to split into individual glyphs)
            # This assumes each character maps to a glyph name
            components = ' '.join(ligature)

        feature_content += f"    sub {components} by {ligature};\n"
        valid_ligatures += 1

    feature_content += "} liga;\n"

    print(f"\nValid ligatures to add: {valid_ligatures}")
    if missing_glyphs:
        print(f"Missing glyphs (first 10): {missing_glyphs[:10]}")

    print("\nGenerated feature content:")
    print(feature_content)

    # Write feature file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False) as f:
        f.write(feature_content)
        feature_file = f.name

    # Use fonttools to add features
    cmd = [
        'fonttools', 'feaLib', '-o', output_font,
        feature_file, input_font
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Success! Font saved to {output_font}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

        # Show the exact line where error occurred
        error_lines = e.stderr.split('\n')
        for line in error_lines:
            if ':' in line and 'ERROR' in line:
                parts = line.split(':')
                if len(parts) >= 3:
                    line_num = int(parts[1])
                    print(f"\nError at line {line_num}")
                    # Show the problematic line
                    feature_lines = feature_content.split('\n')
                    if line_num <= len(feature_lines):
                        print(f"Line {line_num}: {feature_lines[line_num - 1]}")
    finally:
        os.unlink(feature_file)



def add_svg_ligatures_to_font(input_font_path, ligature_dict, output_font_path):
    """
    Add SVG ligature glyphs to a font and create ligature substitutions

    Args:
        input_font_path: Path to input TTF/OTF font
        ligature_dict: Dictionary mapping ligature names to SVG file paths
        output_font_path: Path to save modified font
    """
    # Load the font
    font = TTFont(input_font_path)
    #font.setFontRevision('Nu Lirbantu With Emoji hieroglyphs in ligatures')

    # Get font metrics
    upm = font['head'].unitsPerEm
    ascender = font['hhea'].ascent
    descender = font['hhea'].descent

    # Get existing glyph tables
    glyf = font['glyf']
    hmtx = font['hmtx']

    # Track new glyphs and their components for ligature rules
    new_glyphs = []
    ligature_rules = []

    for ligature_name, svg_path in ligature_dict.items():
        if ',' in ligature_name:
            continue
        ligature_name = replace_ligature(ligature_name)
        if not Path(svg_path).exists():
            print(f"SVG file {svg_path} does not exist")
            continue

        print(f"Processing {ligature_name}...")

        # Parse ligature components (e.g., "f_i" -> ["f", "i"])
        components = ligature_name.split('_') if '_' in ligature_name else list(ligature_name)

        # Convert SVG to glyph outline
        glyph, advance_width = svg_to_glyph_with_picosvg(
            font,
            svg_path,
            upm,
            ascender,
            descender,
            #is_ttf=True  # Set to False for CFF fonts
        )

        # Add glyph to font
        add_glyph_to_font(font, ligature_name, glyph, advance_width)
        new_glyphs.append(ligature_name)

        # Store ligature rule
        ligature_rules.append((components, ligature_name))

    # Add ligature substitutions to GSUB table
    add_ligature_substitutions(font, ligature_rules)

    # Save the font
    font.save(output_font_path)
    print(f"Font saved to {output_font_path}")

def svg_to_glyph(font,svg_path, upm, ascender, descender, is_ttf=True):
    """
    Convert SVG file to glyph outline using fontTools.svgLib.SVGPath [citation:3][citation:6]
    """
    # Parse SVG and get its dimensions
    svg = SVGPath(svg_path)

    # Get SVG dimensions from viewBox or fallback to parsing
    root = svg.root
    viewBox = root.get('viewBox')

    if viewBox:
        x, y, width, height = map(float, viewBox.split())
    else:
        # Fallback: try to get width/height attributes
        width = float(root.get('width', 1000))
        height = float(root.get('height', 1000))
        x = y = 0

    # Calculate scale to fit font UPM
    # Scale so height matches font's ascender-descender range
    font_height = ascender - descender
    scale = font_height / height

    # Create transformation to position glyph correctly
    # Flip Y axis (SVG Y increases downward, font Y increases upward)
    transform = Scale(scale, -scale).translate(-x, -height)

    # Create appropriate pen based on font type [citation:4]
    if is_ttf:
        # For TrueType (quadratic curves)
        glyph_pen = TTGlyphPen(font.getGlyphSet())
    else:
        # For CFF (cubic curves) - would need T2CharStringPen
        from fontTools.pens.t2CharStringPen import T2CharStringPen
        glyph_pen = T2CharStringPen(upm, None)

    # Wrap pen with transform
    transform_pen = TransformPen(glyph_pen, transform)

    # Draw SVG onto the pen
    svg.draw(transform_pen)

    # Get the glyph and calculate advance width
    if is_ttf:
        glyph = glyph_pen.glyph()
        # Calculate advance width based on scaled SVG width
        advance_width = int(width * scale)
    else:
        glyph = glyph_pen.getCharString()
        advance_width = int(width * scale)

    return glyph, advance_width
def svg_to_glyph_with_picosvg(font,svg_path, upm, ascender, descender):
    """
    Convert SVG to glyph using picosvg for better path handling
    """
    from picosvg.svg import SVG as picoSVG
    from fontTools.pens.t2CharStringPen import T2CharStringPen
    from fontTools.pens.transformPen import TransformPen

    # Read and normalize SVG
    with open(svg_path, 'r', encoding='utf-8-sig') as f:
        svg_content = f.read()

    # Convert to picosvg format (normalizes paths, removes transforms)
    picosvg = picoSVG.fromstring(svg_content).topicosvg()

    # Get viewBox
    x, y, width, height = picosvg.view_box()

    # Calculate scale
    font_height = ascender - descender
    scale = font_height / height

    # Create pen for CFF outlines (cubic curves)
    # pen = T2CharStringPen(upm, None)
    pen = TTGlyphPen(font.getGlyphSet())
    transform = Scale(scale, -scale).translate(-x, -height)
    transform_pen = TransformPen(pen, transform)

    # Draw
    svg_pen = SVGPath(None)
    svg_pen.root = picosvg.svg_root
    svg_pen.draw(transform_pen)

    # glyph = pen.getCharString()
    glyph = pen.glyph()
    advance_width = int(width * scale)

    return glyph, advance_width
def add_glyph_to_font(font, glyph_name, glyph, advance_width):
    """
    Add a new glyph to the font [citation:7]
    """
    # Update glyph order
    glyph_order = list(font.getGlyphOrder())
    if glyph_name not in glyph_order:
        glyph_order.append(glyph_name)
        font.setGlyphOrder(glyph_order)

    # Add to glyf table
    font['glyf'][glyph_name] = glyph

    # Get left side bearing (minimum X coordinate)
    if hasattr(glyph, 'xMin'):
        lsb = glyph.xMin
    else:
        lsb = 0

    # Add to horizontal metrics
    font['hmtx'][glyph_name] = (advance_width, lsb)

def add_ligature_substitutions_old(font, ligature_rules):
    """
    Add OpenType ligature substitutions to GSUB table
    """
    # Ensure GSUB table exists
    if 'GSUB' not in font:
        from fontTools.ttLib.tables import G_S_U_B_
        font['GSUB'] = G_S_U_B_.table_G_S_U_B_()

    # Create feature file content
    feature_content = """languagesystem DFLT dflt;
languagesystem latn dflt;

feature liga {
"""

    for components, ligature_name in ligature_rules:
        # Format: sub [component1] [component2] ... by ligature_name;
        comp_str = ' '.join(components)
        feature_content += f"    sub {comp_str} by {ligature_name};\n"

    feature_content += "} liga;\n"

    # Write temporary feature file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False) as f:
        f.write(feature_content)
        feature_file = f.name

    # Compile and add features
    from fontTools.feaLib.builder import addOpenTypeFeatures
    try:
        addOpenTypeFeatures(font, feature_file)
        print("Ligature features added successfully")
    except Exception as e:
        print(f"Error adding features: {e}")
        print("Feature content:")
        print(feature_content)
    finally:
        os.unlink(feature_file)

def add_ligature_substitutions(font, ligature_rules):
    """
    Add OpenType ligature substitutions to GSUB table - CORRECTED VERSION
    """
    # Ensure GSUB table exists - this creates a proper table_G_S_U_B_ instance
    if 'GSUB' not in font:
        from fontTools.ttLib.tables import G_S_U_B_
        font['GSUB'] = G_S_U_B_.table_G_S_U_B_()

    # Get the GSUB table
    gsub = font['GSUB']
    if 'GSUB' in font:
        print(dir(font['GSUB']))  # Shows available methods/attributes
    # print(dir(gsub))  # Shows available methods/attributes
    # IMPORTANT: The table_G_S_U_B_ object itself is the table
    # You don't access a .table attribute - the object IS the table

    # The correct way to add features is using feaLib.builder
    # Don't try to manually manipulate GSUB tables

    # Create feature file content
    feature_content = """languagesystem DFLT dflt;
languagesystem latn dflt;

feature liga {
"""

    for components, ligature_name in ligature_rules:
        comp_str = ' '.join(components)
        feature_content += f"    sub {comp_str} by {ligature_name};\n"

    feature_content += "} liga;\n"

    # Write temporary feature file
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False) as f:
        f.write(feature_content)
        feature_file = f.name

    # Use addOpenTypeFeatures to properly build the GSUB table
    from fontTools.feaLib.builder import addOpenTypeFeatures
    try:
        addOpenTypeFeatures(font, feature_file)
        print("Ligature features added successfully")
    except Exception as e:
        print(f"Error adding features: {e}")
        print("Feature content:")
        print(feature_content)
    finally:
        os.unlink(feature_file)

def get_ligatures_map():
    rootdir = get_project_dir()
    dct = get_ai_dictionary()
    liga = {}
    for wf_info in dct:
        liga[wf_info["lirbantu"]] = f'{rootdir}/emojis/combined/{wf_info["wordform"]}.svg'
    return liga


# Usage
ligatures = {
    "fi": "path/to/fi.svg",
    "fl": "path/to/fl.svg",
    "ffi": "path/to/ffi.svg",
    # ... 383 more ligatures
}

rootdir = get_project_dir()

ligatures = get_ligatures_map()
output_filename = f'{rootdir}/output/nu_lirbantu_w_ligatures.ttf'
add_svg_ligatures_to_font(get_lirbantu_font_filename(), ligatures, output_filename)
