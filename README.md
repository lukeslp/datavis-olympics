# Summer Rings

[![Live Site](https://img.shields.io/badge/live-dr.eamer.dev-blue)](https://dr.eamer.dev/datavis/poems/olympics/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A rotating spiral of Summer Olympic medal counts from 1896 through 2024. Every Games gets its own ring layer — hover any arc to see that country's gold, silver, and bronze breakdown. The sidebar lets you filter by country or jump to a specific year.

## What It Shows

Each ring in the spiral represents one Summer Games. Arc length within a ring encodes total medals for that country in that year. Colors follow Olympic ring assignments per country — USA in blue, Germany in yellow, France in blue, China in red, and so on.

Hovering a segment surfaces the Games year, host city, and full medal tally for that country. Clicking a country in the sidebar isolates their history across all 32 Games, making it easy to see when a nation's dominance rose and fell.

## Interaction

- **Hover** any arc: country, year, host city, gold/silver/bronze counts appear in a tooltip
- **Click** a country in the sidebar to highlight only their arcs across all Games
- **All Countries** resets the filter
- **Featured countries** section gives quick access to the major Olympic powers

## Data

- **Coverage**: Summer Olympics 1896–2024 (Athens to Paris), 32 Games
- **Source**: `olympic_data_inline.js` — all medal-winning countries per Games
- **Country codes**: Historical transitions handled (URS/RUS/ROC, GDR/FRG/GER, EUN, etc.)

## Design

Light parchment theme (`#f6f2e8`) — intentionally different from the dark palette used across the rest of the poems collection. The Olympic rings color palette drives all country assignment: blue `#0077C8`, yellow `#D9A400`, green `#009F3D`, red `#DF0024`.

## Data Sources

Data compiled from Wikipedia Olympic medal tables and cross-validated against Olympedia.org. Covers all medal-winning countries for all 32 Summer Games, including the cancelled 1916/1940/1944 Games and the COVID-delayed 2020 Tokyo Games held in 2021.

## Tech Stack

Canvas 2D, vanilla JavaScript — no D3, no framework.

## Running Locally

```bash
cd /home/coolhand/html/datavis/poems/olympics
python3 -m http.server 8000
# Open http://localhost:8000/
```

---

By [Luke Steuber](https://lukesteuber.com) · [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) · [dr.eamer.dev](https://dr.eamer.dev)
