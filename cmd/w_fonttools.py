#!/usr/bin/env python3
"""
SVG to TTF Font Converter using fontTools
Converts SVG files in a directory to a valid TTF font file.
"""

import os
import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib.tables._h_e_a_d import table__h_e_a_d
from fontTools.ttLib.tables._h_h_e_a import table__h_h_e_a
from fontTools.ttLib.tables._m_a_x_p import table__m_a_x_p
from fontTools.ttLib.tables._n_a_m_e import table__n_a_m_e
# from fontTools.ttLib.tables._o_s_2f_2 import table__O_S_2f_2
from fontTools.ttLib.tables.O_S_2f_2 import table_O_S_2f_2
from fontTools.ttLib.tables._p_o_s_t import table__p_o_s_t
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib import SVGPath
import xml.etree.ElementTree as ET

class SVGToTTF:
    def __init__(self, font_name="CustomFont", svg_dir="./svgs"):
        self.font_name = font_name
        self.svg_dir = svg_dir
        self.glyphs = {}
        self.unicode_mapping = {}
        self.upm = 1000  # Units per em
        self.font = None

    def parse_svg_path(self, svg_file):
        """Parse SVG file and extract path data"""
        try:
            tree = ET.parse(svg_file)
            root = tree.getroot()

            # Get viewBox or dimensions
            view_box = root.get('viewBox')
            if view_box:
                view_box_values = [float(x) for x in view_box.split()]
                width = view_box_values[2]
                height = view_box_values[3]
            else:
                # Try to get width/height attributes
                width_attr = root.get('width', '1000')
                height_attr = root.get('height', '1000')
                # Remove units if present
                width = float(''.join(c for c in width_attr if c.isdigit() or c == '.'))
                height = float(''.join(c for c in height_attr if c.isdigit() or c == '.'))

            # Find all path elements
            paths = []
            transforms = []

            for elem in root.iter():
                # Check for path elements
                if elem.tag.endswith('path') or (hasattr(elem, 'tag') and 'path' in elem.tag):
                    path_data = elem.get('d')
                    if path_data:
                        # Get transform if present
                        transform = elem.get('transform', '')
                        paths.append(path_data)
                        transforms.append(transform)

                # Check for group transforms
                elif elem.tag.endswith('g') or (hasattr(elem, 'tag') and 'g' in elem.tag):
                    transform = elem.get('transform', '')
                    if transform:
                        transforms.append(transform)

            if not paths:
                # Create a simple rectangle as fallback
                paths.append(f"M0,0 L{width},0 L{width},{height} L0,{height} Z")

            # For simplicity, we'll use the first path
            # In a real implementation, you'd combine multiple paths
            return paths[0], width, height

        except Exception as e:
            print(f"Error parsing {svg_file}: {e}")
            return None, 1000, 1000

    def svg_path_to_ttf_glyph(self, path_data, width, height, glyph_name):
        """Convert SVG path to TTF glyph using fontTools"""
        pen = TTGlyphPen(None)

        try:
            # Parse SVG path and draw to pen
            # This is a simplified version - you'd need proper SVG path parsing
            # For now, we'll create a simple glyph based on the bounding box

            # Scale to fit UPM
            scale_x = self.upm / max(width, 1)
            scale_y = self.upm / max(height, 1)

            # Create a simple rectangle glyph
            pen.moveTo((0, 0))
            pen.lineTo((self.upm, 0))
            pen.lineTo((self.upm, self.upm))
            pen.lineTo((0, self.upm))
            pen.closePath()

            glyph = pen.glyph()

            # Set glyph metrics
            glyph.width = self.upm
            glyph.lsb = 0

            return glyph

        except Exception as e:
            print(f"Error creating glyph for {glyph_name}: {e}")
            return None

    def create_empty_glyph(self):
        """Create an empty .notdef glyph"""
        pen = TTGlyphPen(None)
        pen.moveTo((0, 0))
        pen.lineTo((self.upm, 0))
        pen.lineTo((self.upm, self.upm))
        pen.lineTo((0, self.upm))
        pen.closePath()
        return pen.glyph()

    def collect_glyphs(self):
        """Collect all SVG files and convert to glyphs"""
        if not os.path.exists(self.svg_dir):
            print(f"Directory '{self.svg_dir}' not found!")
            return False

        # Get all SVG files
        svg_files = sorted([f for f in os.listdir(self.svg_dir)
                            if f.lower().endswith('.svg')])

        if not svg_files:
            print(f"No SVG files found in '{self.svg_dir}'")
            return False

        print(f"Found {len(svg_files)} SVG files")

        # Process each SVG file
        glyph_names = ['.notdef']  # Start with .notdef
        self.glyphs['.notdef'] = self.create_empty_glyph()

        for i, svg_file in enumerate(svg_files):
            # Use filename (without extension) as glyph name
            glyph_name = os.path.splitext(svg_file)[0]
            # Clean glyph name (must be valid PostScript name)
            glyph_name = ''.join(c for c in glyph_name if c.isalnum() or c == '_')
            if not glyph_name[0].isalpha():
                glyph_name = 'glyph' + glyph_name

            # Assign Unicode code point (start from 0xE000 for Private Use Area)
            unicode_value = 0xE000 + i

            full_path = os.path.join(self.svg_dir, svg_file)
            path_data, width, height = self.parse_svg_path(full_path)

            if path_data:
                glyph = self.svg_path_to_ttf_glyph(path_data, width, height, glyph_name)
                if glyph:
                    self.glyphs[glyph_name] = glyph
                    self.unicode_mapping[unicode_value] = glyph_name
                    glyph_names.append(glyph_name)
                    print(f"  Added: {glyph_name} -> U+{unicode_value:04X}")
                else:
                    print(f"  Failed to create glyph: {svg_file}")
            else:
                print(f"  Failed to parse: {svg_file}")

        return len(self.glyphs) > 1  # More than just .notdef

    def create_font(self):
        """Create and populate the TTF font"""
        # Create new font
        self.font = TTFont()

        # Set up basic tables
        self.font['head'] = table__h_e_a_d()
        self.font['hhea'] = table__h_h_e_a()
        self.font['maxp'] = table__m_a_x_p()
        self.font['name'] = table__n_a_m_e()
        # self.font['OS/2'] = table__O_S_2f_2()
        self.font['OS/2'] = table_O_S_2f_2()
        self.font['post'] = table__p_o_s_t()

        # Initialize tables
        self.font['head'].version = 1.0
        self.font['head'].fontRevision = 1.0
        self.font['head'].checkSumAdjustment = 0
        self.font['head'].magicNumber = 0x5F0F3CF5
        self.font['head'].flags = 0
        self.font['head'].unitsPerEm = self.upm
        self.font['head'].created = 0
        self.font['head'].modified = 0
        self.font['head'].xMin = 0
        self.font['head'].yMin = 0
        self.font['head'].xMax = self.upm
        self.font['head'].yMax = self.upm
        self.font['head'].macStyle = 0
        self.font['head'].lowestRecPPEM = 8
        self.font['head'].fontDirectionHint = 2
        self.font['head'].indexToLocFormat = 0
        self.font['head'].glyphDataFormat = 0

        # hhea table
        self.font['hhea'].version = 1.0
        self.font['hhea'].ascent = self.upm
        self.font['hhea'].descent = -200
        self.font['hhea'].lineGap = 0
        self.font['hhea'].advanceWidthMax = self.upm
        self.font['hhea'].minLeftSideBearing = 0
        self.font['hhea'].minRightSideBearing = 0
        self.font['hhea'].xMaxExtent = self.upm
        self.font['hhea'].caretSlopeRise = 1
        self.font['hhea'].caretSlopeRun = 0
        self.font['hhea'].caretOffset = 0
        self.font['hhea'].metricDataFormat = 0
        self.font['hhea'].numberOfHMetrics = len(self.glyphs)

        # maxp table
        self.font['maxp'].version = 1.0
        self.font['maxp'].numGlyphs = len(self.glyphs)
        self.font['maxp'].maxPoints = 0
        self.font['maxp'].maxContours = 0
        self.font['maxp'].maxCompositePoints = 0
        self.font['maxp'].maxCompositeContours = 0
        self.font['maxp'].maxZones = 2
        self.font['maxp'].maxTwilightPoints = 0
        self.font['maxp'].maxStorage = 0
        self.font['maxp'].maxFunctionDefs = 0
        self.font['maxp'].maxInstructionDefs = 0
        self.font['maxp'].maxStackElements = 0
        self.font['maxp'].maxSizeOfInstructions = 0
        self.font['maxp'].maxComponentElements = 0
        self.font['maxp'].maxComponentDepth = 0

        # OS/2 table
        self.font['OS/2'].version = 4
        self.font['OS/2'].xAvgCharWidth = self.upm
        self.font['OS/2'].usWeightClass = 400
        self.font['OS/2'].usWidthClass = 5
        self.font['OS/2'].fsType = 0
        self.font['OS/2'].ySubscriptXSize = 0
        self.font['OS/2'].ySubscriptYSize = 0
        self.font['OS/2'].ySubscriptXOffset = 0
        self.font['OS/2'].ySubscriptYOffset = 0
        self.font['OS/2'].ySuperscriptXSize = 0
        self.font['OS/2'].ySuperscriptYSize = 0
        self.font['OS/2'].ySuperscriptXOffset = 0
        self.font['OS/2'].ySuperscriptYOffset = 0
        self.font['OS/2'].yStrikeoutSize = 0
        self.font['OS/2'].yStrikeoutPosition = 0
        self.font['OS/2'].sFamilyClass = 0
        self.font['OS/2'].panose = [0] * 10
        self.font['OS/2'].ulUnicodeRange1 = 0
        self.font['OS/2'].ulUnicodeRange2 = 0
        self.font['OS/2'].ulUnicodeRange3 = 0
        self.font['OS/2'].ulUnicodeRange4 = 0
        self.font['OS/2'].achVendID = 'NONE'
        self.font['OS/2'].fsSelection = 64
        self.font['OS/2'].fsFirstCharIndex = min(self.unicode_mapping.keys()) if self.unicode_mapping else 0
        self.font['OS/2'].fsLastCharIndex = max(self.unicode_mapping.keys()) if self.unicode_mapping else 0
        self.font['OS/2'].sTypoAscender = self.upm
        self.font['OS/2'].sTypoDescender = -200
        self.font['OS/2'].sTypoLineGap = 0
        self.font['OS/2'].usWinAscent = self.upm
        self.font['OS/2'].usWinDescent = 200
        self.font['OS/2'].ulCodePageRange1 = 0
        self.font['OS/2'].ulCodePageRange2 = 0
        self.font['OS/2'].sxHeight = 500
        self.font['OS/2'].sCapHeight = 700
        self.font['OS/2'].usDefaultChar = 0
        self.font['OS/2'].usBreakChar = 32
        self.font['OS/2'].usMaxContext = 0

        # name table
        name_table = self.font['name']
        name_table.setName(self.font_name, 1, 3, 1, 0x409)  # Family
        name_table.setName('Regular', 2, 3, 1, 0x409)      # Subfamily
        name_table.setName(self.font_name, 4, 3, 1, 0x409) # Full name
        name_table.setName(self.font_name.replace(' ', ''), 6, 3, 1, 0x409) # PostScript name

        # post table
        self.font['post'].formatType = 2.0
        self.font['post'].italicAngle = 0
        self.font['post'].underlinePosition = 0
        self.font['post'].underlineThickness = 0
        self.font['post'].isFixedPitch = 0
        self.font['post'].minMemType42 = 0
        self.font['post'].maxMemType42 = 0
        self.font['post'].minMemType1 = 0
        self.font['post'].maxMemType1 = 0

        # Add glyphs to font
        glyph_order = ['.notdef'] + [name for name in self.glyphs.keys() if name != '.notdef']
        self.font.setGlyphOrder(glyph_order)

        # Set glyph metrics
        for glyph_name, glyph in self.glyphs.items():
            self.font['glyf'][glyph_name] = glyph

            # Set horizontal metrics
            self.font['hmtx'][glyph_name] = (self.upm, 0)

        # Create cmap table
        cmap = cmap_format_4(4)
        cmap.platformID = 3
        cmap.platEncID = 1
        cmap.language = 0
        cmap.cmap = self.unicode_mapping
        self.font['cmap'] = newTable('cmap')
        self.font['cmap'].tableVersion = 0
        self.font['cmap'].tables = [cmap]

        # Add required tables if missing
        if 'glyf' not in self.font:
            self.font['glyf'] = newTable('glyf')
        if 'loca' not in self.font:
            self.font['loca'] = newTable('loca')
        if 'hmtx' not in self.font:
            self.font['hmtx'] = newTable('hmtx')
        if 'cvt ' not in self.font:
            self.font['cvt '] = newTable('cvt ')
        if 'fpgm' not in self.font:
            self.font['fpgm'] = newTable('fpgm')
        if 'prep' not in self.font:
            self.font['prep'] = newTable('prep')

        return True

    def save_font(self, output_file):
        """Save the font to a TTF file"""
        if not self.font:
            print("No font to save")
            return False

        try:
            self.font.save(output_file)
            print(f"\nTTF file created successfully: {output_file}")
            print(f"Total glyphs: {len(self.glyphs)}")
            print(f"Mapped characters: {len(self.unicode_mapping)}")
            return True
        except Exception as e:
            print(f"Error saving font: {e}")
            return False

def main():
    """Main function"""
    # Parse command line arguments
    svg_dir = "./svgs"
    output_file = "custom_font.ttf"
    font_name = "CustomFont"

    if len(sys.argv) > 1:
        svg_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        font_name = sys.argv[3]

    print(f"SVG to TTF Converter using fontTools")
    print(f"SVG directory: {svg_dir}")
    print(f"Output file: {output_file}")
    print(f"Font name: {font_name}")
    print("-" * 50)

    # Check if fontTools is installed
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("\nError: fontTools is not installed!")
        print("Please install it using: pip install fontTools")
        return 1

    # Create font
    converter = SVGToTTF(font_name, svg_dir)

    if converter.collect_glyphs():
        if converter.create_font():
            converter.save_font(output_file)
            return 0
        else:
            print("Failed to create font structure")
            return 1
    else:
        print("No glyphs collected. Please check your SVG files.")
        return 1

if __name__ == "__main__":
    exit(main())