import subprocess
import tempfile
import os

from lirbantu.config.config import get_ai_dictionary, get_lirbantu_font_filename
from lirbantu.project import get_project_dir
from fontTools.ttLib import TTFont, newTable


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
add_ligatures_with_glyph_check(get_lirbantu_font_filename(), ligatures, output_filename)
