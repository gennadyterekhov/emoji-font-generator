#!/usr/bin/env python3
"""
SVG to TTF Font Converter using fontTools
Converts SVG files in a directory to a valid TTF font file.
"""


from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from lirbantu.project import get_project_dir
def drawTestGlyph(pen):
    pen.moveTo((100, 100))
    pen.lineTo((100, 1000))
    pen.qCurveTo((200, 900), (400, 900), (500, 1000))
    pen.lineTo((500, 100))
    pen.closePath()

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

    fb = FontBuilder(1024, isTTF=True)
    fb.setupGlyphOrder([".notdef", ".null", "space", "A", "a"])
    fb.setupCharacterMap({32: "space", 65: "A", 97: "a"})
    advanceWidths = {".notdef": 600, "space": 500, "A": 600, "a": 600, ".null": 0}

    familyName = "HelloTestFont"
    styleName = "TotallyNormal"
    version = "0.1"

    nameStrings = dict(
        familyName=dict(en=familyName, nl="HalloTestFont"),
        styleName=dict(en=styleName, nl="TotaalNormaal"),
        uniqueFontIdentifier="fontBuilder: " + familyName + "." + styleName,
        fullName=familyName + "-" + styleName,
        psName=familyName + "-" + styleName,
        version="Version " + version,
    )

    pen = TTGlyphPen(None)
    drawTestGlyph(pen)
    glyph = pen.glyph()
    glyphs = {".notdef": glyph, "space": glyph, "A": glyph, "a": glyph, ".null": glyph}
    fb.setupGlyf(glyphs)
    metrics = {}
    glyphTable = fb.font["glyf"]
    for gn, advanceWidth in advanceWidths.items():
        metrics[gn] = (advanceWidth, glyphTable[gn].xMin)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=824, descent=-200)
    fb.setupNameTable(nameStrings)
    fb.setupOS2(sTypoAscender=824, usWinAscent=824, usWinDescent=200)
    fb.setupPost()
    fb.save("test.ttf")


if __name__ == "__main__":
    exit(main())