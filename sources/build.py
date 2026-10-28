"""Build the three Lisin families from their editable UFO sources."""
import argparse
import os
from pathlib import Path

from fontmake.font_project import FontProject
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables.ttProgram import Program

ROOT = Path(__file__).resolve().parents[1]


def finish(path):
    font = TTFont(path, recalcTimestamp=False)
    style = font["name"].getDebugName(2)
    bold, italic = "Bold" in style, "Italic" in style
    for name_id in (16, 17, 21, 22, 25):
        font["name"].removeNames(nameID=name_id)
    buildStatTable(font, [
        {"tag": "wght", "name": "Weight", "ordering": 0, "values": [
            {"value": 700 if bold else 400, "name": "Bold" if bold else "Regular",
             "flags": 0 if bold else 2}]},
        {"tag": "ital", "name": "Italic", "ordering": 1, "values": [
            {"value": int(italic), "name": "Italic" if italic else "Roman",
             "flags": 0 if italic else 2, **({} if italic else {"linkedValue": 1})}]}])
    font["prep"] = newTable("prep")
    font["prep"].program = Program()
    font["prep"].program.fromBytecode(bytes.fromhex("b801ff85b0048d"))
    font["head"].created = font["head"].modified = 3875990400
    font.save(path)
    assert font["name"].getDebugName(9) == "Enchante"
    assert abs(font["head"].fontRevision - 1.001) < 1 / 65536


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("studio", "logic", "cadre"))
    args = parser.parse_args()
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1793145600")
    for family in ([args.family] if args.family else ["studio", "logic", "cadre"]):
        sources = sorted((ROOT / "sources" / family).glob("*.ufo"))
        assert len(sources) == 4, family
        destination = ROOT / "fonts" / "ttf" / family
        FontProject().run_from_ufos([str(p) for p in sources], output=("ttf",),
                                   output_dir=str(destination), use_production_names=False,
                                   reverse_direction=False, remove_overlaps=False)
        for path in destination.glob("*.ttf"):
            finish(path)
        print(f"Built {family}: four TTF styles", flush=True)


if __name__ == "__main__":
    main()
