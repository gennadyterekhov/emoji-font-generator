#!/usr/bin/env python3
"""
SVG to TTF Font Converter
Creates a TTF font file from SVG files in a specified directory.
"""

import os
import struct
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import OrderedDict

class SVGToTTF:
    def __init__(self, font_name="CustomFont", svg_dir="./svgs"):
        self.font_name = font_name
        self.svg_dir = svg_dir
        self.glyphs = OrderedDict()
        self.glyph_data = {}
        self.next_glyph_id = 1  # Start from 1, 0 is reserved for .notdef

    def parse_svg_path(self, svg_file):
        """Parse SVG file and extract path data"""
        try:
            tree = ET.parse(svg_file)
            root = tree.getroot()

            # Find path elements
            paths = []
            for elem in root.iter():
                if 'path' in elem.tag.lower():
                    if 'd' in elem.attrib:
                        paths.append(elem.attrib['d'])
                elif elem.tag.endswith('}path') or elem.tag == 'path':
                    if 'd' in elem.attrib:
                        paths.append(elem.attrib['d'])

            # If no path found, try to create a simple rectangle as fallback
            if not paths:
                # Check for viewBox or dimensions
                width = 1000
                height = 1000
                if 'viewBox' in root.attrib:
                    view_box = root.attrib['viewBox'].split()
                    if len(view_box) == 4:
                        width = float(view_box[2])
                        height = float(view_box[3])
                elif 'width' in root.attrib and 'height' in root.attrib:
                    width = float(root.attrib['width'].replace('px', ''))
                    height = float(root.attrib['height'].replace('px', ''))

                # Create a simple rectangle path
                paths.append(f"M0,0 L{width},0 L{width},{height} L0,{height} Z")

            return paths[0] if paths else None

        except Exception as e:
            print(f"Error parsing {svg_file}: {e}")
            return None

    def collect_glyphs(self):
        """Collect all SVG files and convert to glyph data"""
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
        for i, svg_file in enumerate(svg_files):
            char_code = 0xE000 + i  # Start from Private Use Area

            # Use filename (without extension) as character name
            char_name = os.path.splitext(svg_file)[0]

            full_path = os.path.join(self.svg_dir, svg_file)
            path_data = self.parse_svg_path(full_path)

            if path_data:
                self.glyphs[char_name] = {
                    'char_code': char_code,
                    'path': path_data,
                    'file': svg_file,
                    'width': 1000,  # Default advance width
                    'height': 1000
                }
                print(f"  Added: {char_name} -> U+{char_code:04X}")
            else:
                print(f"  Failed to parse: {svg_file}")

        return len(self.glyphs) > 0

    def calculate_checksum(self, data):
        """Calculate TrueType checksum (sum of all longwords)"""
        # Pad to multiple of 4
        if len(data) % 4 != 0:
            data += b'\0' * (4 - (len(data) % 4))

        # Sum all 32-bit words
        checksum = 0
        for i in range(0, len(data), 4):
            word = struct.unpack('>I', data[i:i+4])[0]
            checksum = (checksum + word) & 0xFFFFFFFF
        return checksum

    def create_head_table(self):
        """Create the 'head' table (font header)"""
        data = struct.pack('>I', 0x00010000)  # Version 1.0
        data += struct.pack('>I', 0x00010000)  # Font revision 1.0
        data += struct.pack('>I', 0)  # Checksum adjustment (placeholder)
        data += struct.pack('>I', 0x5F0F3CF5)  # Magic number
        data += struct.pack('>H', 0)  # Flags
        data += struct.pack('>H', 1000)  # Units per em
        data += struct.pack('>Q', 0)  # Created (placeholder)
        data += struct.pack('>Q', 0)  # Modified (placeholder)

        # Set bounds (default values)
        data += struct.pack('>h', 0)  # xMin
        data += struct.pack('>h', 0)  # yMin
        data += struct.pack('>h', 1000)  # xMax
        data += struct.pack('>h', 1000)  # yMax

        data += struct.pack('>H', 0)  # Mac style
        data += struct.pack('>H', 8)  # Lowest rec PPEM
        data += struct.pack('>h', 2)  # Font direction hint
        data += struct.pack('>h', 0)  # Index to loc format (short format)
        data += struct.pack('>h', 0)  # Glyph data format

        return data

    def create_maxp_table(self):
        """Create the 'maxp' table (maximum profile)"""
        num_glyphs = len(self.glyphs) + 1  # +1 for .notdef

        data = struct.pack('>I', 0x00010000)  # Version 1.0
        data += struct.pack('>H', num_glyphs)  # Num glyphs
        data += struct.pack('>H', 0)  # Max points (0 for composite glyphs)
        data += struct.pack('>H', 0)  # Max contours
        data += struct.pack('>H', 0)  # Max component points
        data += struct.pack('>H', 0)  # Max component contours
        data += struct.pack('>H', 0)  # Max zones
        data += struct.pack('>H', 0)  # Max twilight points
        data += struct.pack('>H', 0)  # Max storage
        data += struct.pack('>H', 0)  # Max function defs
        data += struct.pack('>H', 0)  # Max instruction defs
        data += struct.pack('>H', 0)  # Max stack elements
        data += struct.pack('>H', 0)  # Max size of instructions
        data += struct.pack('>H', 0)  # Max component elements
        data += struct.pack('>H', 0)  # Max component depth

        return data

    def create_hhea_table(self):
        """Create the 'hhea' table (horizontal header)"""
        data = struct.pack('>I', 0x00010000)  # Version 1.0
        data += struct.pack('>h', 1000)  # Ascender
        data += struct.pack('>h', -200)  # Descender
        data += struct.pack('>h', 0)  # Line gap
        data += struct.pack('>H', 1000)  # Advance width max
        data += struct.pack('>h', 0)  # Min left side bearing
        data += struct.pack('>h', 0)  # Min right side bearing
        data += struct.pack('>h', 1000)  # X max extent
        data += struct.pack('>h', 0)  # Caret slope rise
        data += struct.pack('>h', 1)  # Caret slope run
        data += struct.pack('>h', 0)  # Caret offset
        data += struct.pack('>h', 0)  # Reserved
        data += struct.pack('>h', 0)  # Reserved
        data += struct.pack('>h', 0)  # Reserved
        data += struct.pack('>h', 0)  # Reserved
        data += struct.pack('>h', 0)  # Metric data format
        data += struct.pack('>H', len(self.glyphs) + 1)  # Num hmtx entries

        return data

    def create_hmtx_table(self):
        """Create the 'hmtx' table (horizontal metrics)"""
        data = b''

        # Add metrics for all glyphs
        num_glyphs = len(self.glyphs) + 1

        # .notdef glyph
        data += struct.pack('>H', 1000)  # Advance width
        data += struct.pack('>h', 0)  # Left side bearing

        # Regular glyphs
        for glyph_name, glyph_info in self.glyphs.items():
            data += struct.pack('>H', 1000)  # Advance width
            data += struct.pack('>h', 0)  # Left side bearing

        return data

    def create_cmap_table(self):
        """Create the 'cmap' table (character to glyph mapping)"""
        # Format 4 subtable (Windows Unicode BMP)
        num_glyphs = len(self.glyphs) + 1
        num_segments = num_glyphs + 1  # +1 for end of segments

        # Prepare segment data
        start_codes = [0xFFFF]  # End of segments marker
        end_codes = [0xFFFF]
        id_deltas = [1]
        id_range_offsets = [0]

        # Add actual glyphs
        for glyph_info in self.glyphs.values():
            start_codes.insert(0, glyph_info['char_code'])
            end_codes.insert(0, glyph_info['char_code'])
            id_deltas.insert(0, 1)  # Simple 1:1 mapping
            id_range_offsets.insert(0, 0)

        # Build cmap table
        data = struct.pack('>H', 0)  # Version
        data += struct.pack('>H', 1)  # Number of tables

        # Platform ID, Encoding ID, Offset
        data += struct.pack('>H', 3)  # Platform ID (Windows)
        data += struct.pack('>H', 1)  # Encoding ID (Unicode BMP)
        data += struct.pack('>I', 12)  # Offset to subtable

        # Format 4 subtable
        subtable = struct.pack('>H', 4)  # Format
        subtable += struct.pack('>H', 16 + 8 * num_segments)  # Length
        subtable += struct.pack('>H', 0)  # Language
        subtable += struct.pack('>H', num_segments * 2)  # Seg count * 2
        subtable += struct.pack('>H', 0)  # Search range
        subtable += struct.pack('>H', 0)  # Entry selector
        subtable += struct.pack('>H', 0)  # Range shift

        # End codes
        for code in end_codes:
            subtable += struct.pack('>H', code)
        subtable += struct.pack('>H', 0)  # Reserved

        # Start codes
        for code in start_codes:
            subtable += struct.pack('>H', code)

        # ID deltas
        for delta in id_deltas:
            subtable += struct.pack('>h', delta)

        # ID range offsets
        for offset in id_range_offsets:
            subtable += struct.pack('>H', offset)

        # Glyph ID array (empty for this simple mapping)

        return data + subtable

    def create_glyf_table(self):
        """Create the 'glyf' table (glyph data)"""
        data = b''
        self.glyph_data['offsets'] = [0]  # Start with offset 0 for .notdef

        # Add .notdef glyph (empty)
        notdef_data = struct.pack('>h', 1)  # Number of contours
        notdef_data += struct.pack('>h', 0)  # xMin
        notdef_data += struct.pack('>h', 0)  # yMin
        notdef_data += struct.pack('>h', 1000)  # xMax
        notdef_data += struct.pack('>h', 1000)  # yMax
        data += notdef_data
        self.glyph_data['offsets'].append(len(data))

        # Add actual glyphs
        for glyph_name, glyph_info in self.glyphs.items():
            # Simple contour glyph (simplified - just a placeholder)
            # In a real implementation, you'd parse the SVG path properly
            glyph_data = struct.pack('>h', 1)  # Number of contours
            glyph_data += struct.pack('>h', 0)  # xMin
            glyph_data += struct.pack('>h', 0)  # yMin
            glyph_data += struct.pack('>h', 1000)  # xMax
            glyph_data += struct.pack('>h', 1000)  # yMax

            # Add a simple rectangle as fallback (this is simplified)
            # End points of contours
            glyph_data += struct.pack('>H', 3)  # End point index

            # Instructions length (0)
            glyph_data += struct.pack('>H', 0)

            # Coordinates for a rectangle
            glyph_data += struct.pack('>h', 0)  # x coordinate
            glyph_data += struct.pack('>h', 0)  # y coordinate
            glyph_data += struct.pack('>h', 1000)  # x coordinate
            glyph_data += struct.pack('>h', 0)  # y coordinate
            glyph_data += struct.pack('>h', 1000)  # x coordinate
            glyph_data += struct.pack('>h', 1000)  # y coordinate
            glyph_data += struct.pack('>h', 0)  # x coordinate
            glyph_data += struct.pack('>h', 1000)  # y coordinate

            # Flags (all points on curve)
            glyph_data += struct.pack('>B', 1) * 4

            data += glyph_data
            self.glyph_data['offsets'].append(len(data))

        return data

    def create_loca_table(self):
        """Create the 'loca' table (glyph offsets)"""
        data = b''
        for offset in self.glyph_data['offsets']:
            data += struct.pack('>H', offset // 2)  # Short format (divide by 2)
        return data

    def create_name_table(self):
        """Create the 'name' table (font naming information)"""
        # Name records
        records = []
        strings = []

        # Add name strings
        names = [
            (1, self.font_name.encode('utf-16be')),  # Font Family
            (2, b'\x00R\x00e\x00g\x00u\x00l\x00a\x00r'),  # Font Subfamily
            (4, self.font_name.encode('utf-16be')),  # Full Font Name
            (6, self.font_name.encode('utf-16be')),  # PostScript Name
        ]

        # Build strings data
        strings_data = b''
        for name_id, string in names:
            strings_data += string
            records.append({
                'platform_id': 3,
                'encoding_id': 1,
                'language_id': 0x409,
                'name_id': name_id,
                'length': len(string),
                'offset': len(strings_data) - len(string)
            })

        # Header
        data = struct.pack('>H', 0)  # Format
        data += struct.pack('>H', len(records))  # Count
        data += struct.pack('>H', 6 + 12 * len(records))  # Storage offset

        # Records
        for record in records:
            data += struct.pack('>H', record['platform_id'])
            data += struct.pack('>H', record['encoding_id'])
            data += struct.pack('>H', record['language_id'])
            data += struct.pack('>H', record['name_id'])
            data += struct.pack('>H', record['length'])
            data += struct.pack('>H', record['offset'])

        # String data
        data += strings_data

        return data

    def create_post_table(self):
        """Create the 'post' table (PostScript information)"""
        data = struct.pack('>I', 0x00020000)  # Version 2.0
        data += struct.pack('>I', 0)  # Italic angle
        data += struct.pack('>h', 0)  # Underline position
        data += struct.pack('>h', 0)  # Underline thickness
        data += struct.pack('>I', 0)  # Fixed pitch
        data += struct.pack('>I', 0)  # Min memory type 42
        data += struct.pack('>I', 0)  # Max memory type 42
        data += struct.pack('>I', 0)  # Min memory type 1
        data += struct.pack('>I', 0)  # Max memory type 1

        # Number of glyphs
        num_glyphs = len(self.glyphs) + 1
        data += struct.pack('>H', num_glyphs)

        # Glyph name indices (all 0 = .notdef for simplicity)
        for _ in range(num_glyphs):
            data += struct.pack('>H', 0)

        # No extra strings

        return data

    def create_os2_table(self):
        """Create the 'OS/2' table"""
        data = struct.pack('>H', 0)  # Version
        data += struct.pack('>h', 1000)  # xAvgCharWidth
        data += struct.pack('>H', 0)  # usWeightClass
        data += struct.pack('>H', 0)  # usWidthClass
        data += struct.pack('>H', 0)  # fsType
        data += struct.pack('>h', 1000)  # ySubscriptXSize
        data += struct.pack('>h', 1000)  # ySubscriptYSize
        data += struct.pack('>h', 0)  # ySubscriptXOffset
        data += struct.pack('>h', 0)  # ySubscriptYOffset
        data += struct.pack('>h', 1000)  # ySuperscriptXSize
        data += struct.pack('>h', 1000)  # ySuperscriptYSize
        data += struct.pack('>h', 0)  # ySuperscriptXOffset
        data += struct.pack('>h', 0)  # ySuperscriptYOffset
        data += struct.pack('>h', 0)  # yStrikeoutSize
        data += struct.pack('>h', 500)  # yStrikeoutPosition
        data += struct.pack('>h', 0)  # sFamilyClass
        data += struct.pack('B', 0) * 10  # panose
        data += struct.pack('>I', 0)  # ulUnicodeRange1
        data += struct.pack('>I', 0)  # ulUnicodeRange2
        data += struct.pack('>I', 0)  # ulUnicodeRange3
        data += struct.pack('>I', 0)  # ulUnicodeRange4
        data += struct.pack('>H', 0)  # achVendID
        data += struct.pack('>H', 0)  # fsSelection
        data += struct.pack('>H', 0x0020)  # usFirstCharIndex (space)
        data += struct.pack('>H', 0xFFFF)  # usLastCharIndex
        data += struct.pack('>h', 1000)  # sTypoAscender
        data += struct.pack('>h', -200)  # sTypoDescender
        data += struct.pack('>h', 0)  # sTypoLineGap
        data += struct.pack('>H', 1000)  # usWinAscent
        data += struct.pack('>H', 200)  # usWinDescent
        data += struct.pack('>I', 0)  # ulCodePageRange1
        data += struct.pack('>I', 0)  # ulCodePageRange2
        data += struct.pack('>h', 0)  # sxHeight
        data += struct.pack('>h', 0)  # sCapHeight
        data += struct.pack('>H', 0)  # usDefaultChar
        data += struct.pack('>H', 0)  # usBreakChar
        data += struct.pack('>H', 0)  # usMaxContext

        return data

    def create_ttf(self, output_file="custom_font.ttf"):
        """Create the final TTF file"""
        # Collect required tables
        tables = OrderedDict()
        tables['head'] = self.create_head_table()
        tables['hhea'] = self.create_hhea_table()
        tables['maxp'] = self.create_maxp_table()
        tables['OS/2'] = self.create_os2_table()
        tables['name'] = self.create_name_table()
        tables['cmap'] = self.create_cmap_table()
        tables['post'] = self.create_post_table()
        tables['glyf'] = self.create_glyf_table()
        tables['loca'] = self.create_loca_table()
        tables['hmtx'] = self.create_hmtx_table()

        # Calculate offsets and build table directory
        offset = 12 + 16 * len(tables)  # Offset table + directory entries
        table_entries = []

        for tag, data in tables.items():
            # Align to 4-byte boundary
            padding = (4 - (offset % 4)) % 4
            if padding:
                data = b'\0' * padding + data
                offset += padding

            checksum = self.calculate_checksum(data)
            table_entries.append({
                'tag': tag,
                'checksum': checksum,
                'offset': offset,
                'length': len(data)
            })
            offset += len(data)

        # Build offset table
        ttf_data = struct.pack('>I', 0x00010000)  # SFNT version 1.0
        ttf_data += struct.pack('>H', len(tables))  # Number of tables
        ttf_data += struct.pack('>H', 0)  # Search range
        ttf_data += struct.pack('>H', 0)  # Entry selector
        ttf_data += struct.pack('>H', 0)  # Range shift

        # Add table directory entries
        for entry in sorted(table_entries, key=lambda x: x['tag']):
            ttf_data += entry['tag'].encode('ascii')
            ttf_data += struct.pack('>I', entry['checksum'])
            ttf_data += struct.pack('>I', entry['offset'])
            ttf_data += struct.pack('>I', entry['length'])

        # Add table data
        current_offset = len(ttf_data)
        for entry in sorted(table_entries, key=lambda x: x['offset']):
            # Add padding if needed
            if current_offset < entry['offset']:
                ttf_data += b'\0' * (entry['offset'] - current_offset)
                current_offset = entry['offset']

            ttf_data += tables[entry['tag']]
            current_offset += len(tables[entry['tag']])

        # Calculate and set head table checksum adjustment
        file_checksum = self.calculate_checksum(ttf_data)
        checksum_adjustment = (0xB1B0AFBA - file_checksum) & 0xFFFFFFFF

        # Find and update head table checksum
        head_offset = None
        for entry in table_entries:
            if entry['tag'] == 'head':
                head_offset = entry['offset'] + 8  # Skip tag and checksum
                break

        if head_offset:
            # Replace checksum adjustment in head table
            ttf_data = (ttf_data[:head_offset] +
                        struct.pack('>I', checksum_adjustment) +
                        ttf_data[head_offset+4:])

        # Write to file
        with open(output_file, 'wb') as f:
            f.write(ttf_data)

        print(f"\nTTF file created successfully: {output_file}")
        print(f"Total glyphs: {len(self.glyphs)}")

def main():
    """Main function"""
    import sys

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

    print(f"SVG to TTF Converter")
    print(f"SVG directory: {svg_dir}")
    print(f"Output file: {output_file}")
    print(f"Font name: {font_name}")
    print("-" * 50)

    # Create font
    converter = SVGToTTF(font_name, svg_dir)

    if converter.collect_glyphs():
        converter.create_ttf(output_file)
    else:
        print("No glyphs collected. Please check your SVG files.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())