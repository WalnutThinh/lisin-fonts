# Quality assurance

Candidate 1.001 was tested on 28 October 2026 using FontBakery 1.1.0 and the
complete `googlefonts` profile with network checks enabled. There are no
FAIL or ERROR results. Warnings and manual-review requirements remain;
this is still an initial design/eligibility submission.

| Family, four styles each | PASS | WARN | FAIL | ERROR | SKIP | INFO |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lisin Studio | 401 | 56 | 0 | 0 | 411 | 25 |
| Lisin Logic | 401 | 56 | 0 | 0 | 411 | 25 |
| Lisin Cadre | 401 | 56 | 0 | 0 | 411 | 25 |

Counts are check results across each family, not percentages of supported
characters. A skipped check is not a passed check. Catalog metadata,
variable-font and unrelated-script conditions account for many skips.

## Resolved language-coverage check

The 1.000 candidate failed `googlefonts/glyphsets/shape_languages` once per
style for missing characters in Bambara, Dyula, Fanti, Fulah, Hausa,
Akuapem Twi and Yoruba:

`Ɓ ɓ Ɗ ɗ Ɛ ɛ Ɔ ɔ Ƙ ƙ Ɲ ɲ Ƴ ƴ ʼ` and combining vertical line below `U+0329`.

All sixteen characters are now present. Fourteen auxiliary characters named
in the same check's warnings and a dotted circle were also added. See
[coverage details and actual-font proofs](COVERAGE.md). This check now
**passes in all twelve styles**, without disabling or reclassifying checks.
Passing coverage does not replace native-reader design review.

## Completed engineering and regression checks

- Twelve TTFs build from twelve editable UFO sources.
- All styles cover 100% of GF Latin Core.
- Each style passes 431 NFC/NFD equivalent-character checks, plus Vietnamese
  text samples with tone marks, horn/breve/circumflex and `di dị dĩ dỉ`.
- The approved default advances, bearings and Unicode mappings are preserved.
- Default glyph outlines were compared with the approved pre-release fonts.
  Reordered quadratic segments in four Regular glyphs have zero outline XOR
  area; all other default outline records are unchanged.
- Tabular numeral alternates now share one advance across all four styles
  within each family. Regular/Bold/Italic/Bold Italic metadata is checked.
- All 670 pre-existing outlines, metrics and 616 mappings in each style
  remain unchanged from candidate 1.000. New marks have zero advance and
  tested attachment positions without vertical collisions in the samples.
- All twelve 1.001 TTFs reproduce byte-for-byte in a second independent build.
- Naming, version 1.001, static STAT and smart-dropout checks pass.
- Specimens were rendered from the candidate TTFs using HarfBuzz/FreeType
  and visually inspected; they are not generated-image approximations.

## Warnings and remaining review

Remaining warnings include outline directions/short segments, inherited
unreachable alternates, some soft-dotted combinations outside the completed
Vietnamese mappings, GDEF classification of the horn
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

The full-profile commands return exit status 0 with the warnings above.
[Machine-readable summary](fontbakery-summary.json).
