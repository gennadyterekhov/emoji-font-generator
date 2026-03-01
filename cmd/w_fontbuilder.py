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
from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib import SVGPath
import xml.etree.ElementTree as ET
from fontTools.fontBuilder import FontBuilder
from lirbantu.project import get_project_dir



def main():
    """Main function"""
    # Parse command line arguments
    projdir=get_project_dir()
    svg_dir = f'{projdir}/emojis/combined'
    output_file = "custom_font.ttf"
    font_name = "CustomFont"

    print(f"SVG to TTF Converter using fontTools")
    print(f"SVG directory: {svg_dir}")
    print(f"Output file: {output_file}")
    print(f"Font name: {font_name}")
    print("-" * 50)

    fb = FontBuilder(...)
    fb.setupGlyphOrder(...)
    fb.setupCharacterMap(...)
    fb.setupGlyf(...) #--or-- fb.setupCFF(...)
    fb.setupHorizontalMetrics(...)
    fb.setupHorizontalHeader()
    fb.setupNameTable(...)
    fb.setupOS2()
    fb.addOpenTypeFeatures(...)
    fb.setupPost()
    fb.save(...)


if __name__ == "__main__":
    exit(main())