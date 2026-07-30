# Provenance

Which agent built which task, read from the git history via
`git log --format='%h %an %s'`. Plain table, no interpretation, no invented
entries. The sky of this map is invented and documented as such.

Newest commit first.

| Commit | Author | Subject |
|--------|--------|---------|
| `e18e2c1` | glm-1@ASUS-GEI | report: glm-1@ASUS-GEI second wave update (tasks 15, 18, 22; denied 16, 17, 19, 20) |
| `8dbb220` | roshambo field run | task 21: CATALOGUE.md - 20 constellations indexed with name, band, stars, lore |
| `9ccc562` | glm-1@ASUS-GEI | task 22: PROVENANCE.md - agent/task provenance table from git log %h %an %s |
| `0563e3d` | kimi-2@ASUS-GEI | task 20: starmap/labels.py - brightest-star labels, collision-safe, never raises |
| `f8eadde` | roshambo field run | task 18: dim river magnitudes into faint diffuse band (5.3..6.7, 90 stars, RA 0..360) |
| `a8bf2e9` | kimi-1@ASUS-GEI | task 19: faint coordinate grid module (12 meridians, 5 parallels, never raises) |
| `9543f4a` | glm-1@ASUS-GEI | task 18: The River, 90 very faint stars in a sinusoidal band across the sphere |
| `4f25b14` | roshambo field run | task 17: faint unnamed background scatter stars (80 stars, mag 4.5..6.5, full sphere) |
| `0058a97` | kimi-2@ASUS-GEI | task 17: add scatter.json with 80 faint background stars |
| `f645d47` | kimi-2@ASUS-GEI | task 16: The Last Cairn, a 6-star cairn in Dec -29..-48, RA 283..344 |
| `bc11037` | glm-1@ASUS-GEI | task 15: The Foundered Ark, a 7-star wrecked hull in Dec -24..-47, RA 188..220 |
| `c45b0a3` | roshambo field run | report: agy-1@WORKSTATION-LG final 6-agy update |
| `c0795f9` | agy-3@WORKSTATION-LG | task 12: update title block and legend verification in starmap/legend.py |
| `54afdc3` | agy-2@WORKSTATION-LG | task 08: verify graphic design module |
| `4d5c4fe` | agy-3@WORKSTATION-LG | task 08: verify look of the sky graphic design module |
| `e4a34a3` | kimi-1@ASUS-GEI | task 14: The Sunken Choir, a 7-star southern choir arc in RA 90-180 |
| `a8a3ebf` | kimi-2@ASUS-GEI | task 13: The Iron Tide, a 7-star southern swell in Dec -24..-45, RA 8..71 |
| `547dd47` | glm-1@ASUS-GEI | report: glm-1@ASUS-GEI |
| `c50fb07` | roshambo field run | tasks: second wave (13-22) - southern sky, scatter, grid, labels, catalogue, provenance |
| `fa890b9` | kimi-1@ASUS-GEI | regenerate starmap.svg: 11 constellations including The Silver Spindle |
| `ab068bb` | glm-1@ASUS-GEI | task 10: The Glass Eel, an 8-star eel in RA 306-314 (parallel to Pale Anchor) |
| `901c0d4` | glm-1@ASUS-GEI | task 09: The Quartz Comb, a 7-star comb in RA 268-278 (parallel to Hollow Chalice) |
| `12f1862` | glm-1@ASUS-GEI | task 03: The Windlass, a 7-star winch in RA 80-120 (parallel to Drowned Bell) |
| `bda8a7d` | roshambo field run | report: agy-1@WORKSTATION-LG |
| `b5a6d31` | agy-4@WORKSTATION-LG | task 05: create constellation The Silver Spindle |
| `1a0802d` | agy-1@WORKSTATION-LG | task 12: verify and maintain legend svg |
| `b29b0f3` | agy-1@WORKSTATION-LG | task 08: graphic design style module |
| `c18018b` | kimi-1@ASUS-GEI | report: kimi-1@ASUS-GEI and kimi-2@ASUS-GEI |
| `18e71e0` | kimi-1@ASUS-GEI | regenerate starmap.svg: include The Silver Veil, 10 constellations |
| `b0d59e5` | agy@WORKSTATION-LG | task 12: title block, constellation index, and magnitude key |
| `15a504e` | agy@WORKSTATION-LG | task 02: add The Silver Veil constellation in RA 40-80 |
| `9d93672` | kimi-1@ASUS-GEI | task 11: The Quiet Harp, an 8-star harp in RA 320-360 |
| `f31a0f7` | kimi-1@ASUS-GEI | task 10: The Pale Anchor, a 7-star anchor in RA 280-320 |
| `a3186b6` | kimi-1@ASUS-GEI | task 09: The Hollow Chalice, a 7-star chalice in RA 240-280 |
| `4c35430` | claude-code-1@ASUS-GEI | task 08: the look of the sky - spectral colour ramp, eased star radii, indigo night |
| `29a1c53` | claude-code-2@ASUS-GEI | task 07: The Ashen Kite, an 8-star kite in RA 200-240 |
| `c937651` | claude-code-1@ASUS-GEI | task 06: The Ferryman's Oar, a 7-star oar in RA 160-200 |
| `7215c66` | claude-code-2@ASUS-GEI | task 05: The Amber Loom, an 8-star loom in RA 120-160 |
| `6187e8b` | claude-code-2@ASUS-GEI | task 04: stereographic projection about the north celestial pole |
| `ed5b8c6` | claude-code-1@ASUS-GEI | task 03: The Drowned Bell, an 8-star bell in RA 80-120 |
| `4249031` | claude-code-1@ASUS-GEI | task 01: The Salt Crane, an 8-star crane in RA 0-40 |
| `d6f3314` | roshambo field run | an empty sky |

Agents appearing in the history: `agy-1@WORKSTATION-LG`, `agy-2@WORKSTATION-LG`, `agy-3@WORKSTATION-LG`, `agy-4@WORKSTATION-LG`, `agy@WORKSTATION-LG`, `claude-code-1@ASUS-GEI`, `claude-code-2@ASUS-GEI`, `glm-1@ASUS-GEI`, `kimi-1@ASUS-GEI`, `kimi-2@ASUS-GEI`, `roshambo field run`.

Total commits in the project at the time of this file: **42**.
