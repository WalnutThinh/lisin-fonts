# Quality assurance

Tested on 28 October 2026 using FontBakery 1.1.0 and the complete `googlefonts`
profile with network checks enabled. This candidate does **not** pass the
entire profile and is submitted for initial design/eligibility review.

| Family, four styles each | PASS | WARN | FAIL | ERROR | SKIP | INFO |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lisin Studio | 377 | 60 | 4 | 0 | 427 | 25 |
| Lisin Logic | 377 | 60 | 4 | 0 | 427 | 25 |
| Lisin Cadre | 377 | 60 | 4 | 0 | 427 | 25 |

Counts are check results across each family, not percentages of supported
characters. A skipped check is not a passed check. Catalog metadata,
variable-font and unrelated-script conditions account for many skips.

## Unresolved failing check

`googlefonts/glyphsets/shape_languages` fails once per style. Its >80% glyphset
coverage heuristic tests languages for which this project has not completed
an orthography. The reports list missing characters in Bambara, Dyula, Fanti,
Fulah, Hausa, Akuapem Twi and Yoruba. Characters include:

`Ɓ ɓ Ɗ ɗ Ɛ ɛ Ɔ ɔ Ƙ ƙ Ɲ ɲ Ƴ ƴ ʼ` and combining vertical line below `U+0329`.

These are real coverage gaps. The current project does not claim complete
support for these languages. We request guidance on the necessary coverage
before inclusion; no check has been disabled or reclassified to hide this.
The report labels the last evaluated glyphset in its message, so the label
alone is not a reliable description of the affected language group.

## Completed engineering and regression checks

- Twelve TTFs build from twelve editable UFO sources.
- All styles cover 100% of GF Latin Core.
- Each style passes 429 NFC/NFD equivalent-character checks, plus Vietnamese
  text samples with tone marks, horn/breve/circumflex and `di dị dĩ dỉ`.
- The approved default advances, bearings and Unicode mappings are preserved.
- Default glyph outlines were compared with the approved pre-release fonts.
  Reordered quadratic segments in four Regular glyphs have zero outline XOR
  area; all other default outline records are unchanged.
- Tabular numeral alternates now share one advance across all four styles
  within each family. Regular/Bold/Italic/Bold Italic metadata is checked.
- Naming, version 1.000, static STAT and smart-dropout checks pass.
- Specimens were rendered from the candidate TTFs using HarfBuzz/FreeType
  and visually inspected; they are not generated-image approximations.

## Warnings and remaining review

Remaining warnings include outline directions/short segments, inherited
unreachable alternates, some soft-dotted combinations outside the completed
Vietnamese mappings, missing dotted circle, GDEF classification of the horn
mark, math-symbol widths, unregistered ENCH vendor ID, language metadata,
vertical-metric recommendations and catalog-only documentation/subsets.
These warnings still require designer/onboarder review; this is not a clean
FontBakery certification. Word, Adobe, Safari and physical print are not
certified by the command-line and specimen checks.

## Reproduce

```sh
python sources/build.py
python sources/check.py
fontbakery check-googlefonts 'fonts/ttf/studio/*.ttf' --json studio.json
fontbakery check-googlefonts 'fonts/ttf/logic/*.ttf' --json logic.json
fontbakery check-googlefonts 'fonts/ttf/cadre/*.ttf' --json cadre.json
```

The full-profile commands currently return a failing exit status for the
coverage item above. [Machine-readable summary](fontbakery-summary.json).
