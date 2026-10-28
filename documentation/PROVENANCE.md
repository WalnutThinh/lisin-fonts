# Provenance and engineering notes

## Upstream and modifications

- Upstream: Instrument Serif, Copyright 2022 The Instrument Serif Project Authors,
  licensed under SIL OFL 1.1. Original project:
  <https://github.com/Instrument/instrument-serif>.
- Libelier was the name of earlier internal studies derived from that upstream.
- Lisin Studio and Lisin Logic evolved from the Facette and Texte studies.
  Their approved public pre-release version is 0.211.
- Lisin Cadre adds a more upright slab-serif document style and revised tone marks.
  Its approved public pre-release version is 0.321.
- The `approved-source-manifest.json` file records the precise input font hashes.

This project preserves inherited copyright. Enchante is credited for its Lisin
modifications, not as the sole original author of the entire inherited design.
The UFO files make the current outline and layout sources directly editable.

## AI tools

OpenAI Codex assisted with design exploration, scripted outline construction,
accent positioning, spacing adjustments, font packaging, testing and documentation.
Enchante provided art direction and reviewed working font specimens.
Neither the use of AI nor the inherited origin is concealed in this submission.

## Version 1.000 preparation

The submission build standardizes font naming and version metadata, records
Enchante as the designer of the modifications, adds static STAT data and smart
dropout instructions, and gives tabular numeral alternates a shared advance
width across the four styles of each family. The default proportional text
advances and the approved base outlines are retained and regression-checked.

The font is unhinted apart from rasterizer dropout setup; this is not a claim
of manual TrueType hinting. Production application fonts are outside this repository.

## Review scope

Version 1.001 extends all twelve styles with thirty previously missing
characters and a dotted circle. The new outlines use the existing Lisin drawing
vocabulary; no additional third-party font outlines were imported. Combining
mark placement is added for the new bases. Existing outlines and advances are
unchanged from 1.000. License notices retain both upstream and Enchante credits.

Google Fonts admission requires design review in addition to licensing and QA.
The project requests an assessment of its suitability as three new derivative
families. This repository does not imply endorsement by Google or Instrument.
