"""Check Unicode shaping, real styles and tabular digits in the built fonts."""
import json
import unicodedata as ud
from pathlib import Path

import glyphsets
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parents[1]
EXTENDED = "ƁɓƊɗƐɛƆɔƘƙƝɲƳƴʼ\u0329◌ĿŀſʻǤǥŦŧƷʒǮǯƟɵ"


def check_extension(tt, font):
    cmap = tt.getBestCmap()
    glyphs = tt.getGlyphSet()
    def bounds(name):
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        return pen.bounds
    assert all(ord(char) in cmap for char in EXTENDED)
    assert tt["hmtx"][cmap[0x329]][0] == 0
    for char in EXTENDED[:14] + "eonm◌ĿŀſǤǥŦŧƷʒǮǯƟɵ":
        left, bottom, right, top = bounds(cmap[ord(char)])
        for mark in ("\u0301", "\u0300", "\u0303", "\u0329"):
            buffer = hb.Buffer()
            buffer.add_str(char + mark)
            buffer.guess_segment_properties()
            hb.shape(font, buffer)
            if len(buffer.glyph_infos) == 1:
                continue  # Existing Latin precomposed substitutions are checked below.
            assert len(buffer.glyph_infos) == 2, (char, mark)
            pos = buffer.glyph_positions[-1]
            assert pos.x_advance == 0, (char, mark, "mark adds spacing")
            ml, mb, mr, mt = bounds(tt.getGlyphName(buffer.glyph_infos[-1].codepoint))
            x = buffer.glyph_positions[0].x_advance + pos.x_offset
            assert left - 65 < x + (ml + mr) / 2 < right + 65
            if mark == "\u0329":
                assert mt + pos.y_offset < bottom, (char, "below-mark collision")
            else:
                assert mb + pos.y_offset > top, (char, "above-mark collision")


def shape(font, text, features=None):
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(font, buffer, features or {})
    assert all(info.codepoint for info in buffer.glyph_infos), text
    return [(i.codepoint, p.x_advance, p.y_advance, p.x_offset, p.y_offset)
            for i, p in zip(buffer.glyph_infos, buffer.glyph_positions)]


def main():
    results = []
    for family in ("studio", "logic", "cadre"):
        paths = sorted((ROOT / "fonts" / "ttf" / family).glob("*.ttf"))
        assert len(paths) == 4
        widths, styles = set(), set()
        for path in paths:
            tt = TTFont(path)
            font = hb.Font(hb.Face(path.read_bytes()))
            font.scale = (tt["head"].unitsPerEm,) * 2
            hb.ot_font_set_funcs(font)
            check_extension(tt, font)
            cmap, pairs = tt.getBestCmap(), 0
            for cp in cmap:
                text = chr(cp)
                decomposed = ud.normalize("NFD", text)
                if text != decomposed and all(ord(c) in cmap for c in decomposed):
                    assert shape(font, text) == shape(font, decomposed), (path.name, hex(cp))
                    pairs += 1
            assert pairs >= 429, path.name
            for sample in ("rõ ràng ngược ngưỡng yễu mươu hạy ngẫy ngỗ",
                           "Những điều giản dị. Nghĩ kỹ trước khi viết.",
                           "di dị dĩ dỉ í ì ĩ ỉ ị #001 #095 0123456789"):
                assert shape(font, sample) == shape(font, ud.normalize("NFD", sample))
            for digit in "0123456789":
                widths.add(shape(font, digit, {"tnum": True})[0][1])
            style = tt["name"].getDebugName(2)
            styles.add(style)
            assert tt["name"].getDebugName(1) == "Lisin " + family.title()
            assert tt["name"].getDebugName(9) == "Enchante"
            assert tt["OS/2"].usWeightClass == (700 if "Bold" in style else 400)
            assert bool(tt["OS/2"].fsSelection & 1) == ("Italic" in style)
            assert abs(tt["head"].fontRevision - 1.001) < 1 / 65536
            coverage = glyphsets.get_glyphsets_fulfilled(tt)["GF_Latin_Core"]["percentage"]
            assert coverage == 1, (path.name, coverage)
            results.append({"file": path.name, "canonical_pairs": pairs,
                            "latin_core_coverage": coverage, "extension_characters": len(EXTENDED)})
        assert len(widths) == 1, (family, widths)
        assert styles == {"Regular", "Bold", "Italic", "Bold Italic"}
    print(json.dumps({"status": "PASS", "fonts": results}, indent=2))


if __name__ == "__main__":
    main()
