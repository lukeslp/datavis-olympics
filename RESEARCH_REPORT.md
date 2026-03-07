# Olympic Medal Data Research Report

**Date**: 2026-01-06
**Project**: Olympic Medal Spiral Visualization
**Location**: `/home/coolhand/html/datavis/poems/olympics/`

---

## Executive Summary

This report provides comprehensive research on authoritative Olympic medal data sources, data structure recommendations, and documentation of historical country code changes for the Olympic Medal Spiral visualization covering Summer Olympic Games from 1896 to 2024.

**Key Findings**:
- Multiple validated data sources identified (Wikipedia, Olympedia, Kaggle datasets)
- 30 Summer Olympic Games held from 1896-2024 (excluding 1916, 1940, 1944 cancellations)
- Complex country code evolution documented (15+ special cases)
- Recommended JSON structure with all medal-winning countries per Games
- Data maintenance strategy for future Olympics (2028, 2032+)

---

## Authoritative Data Sources

### Primary Sources (Recommended)

| Source | Coverage | Format | Accuracy | Access |
|--------|----------|--------|----------|--------|
| **Wikipedia Medal Tables** | 1896-2024 | HTML tables | High (peer-reviewed) | Free, no API |
| **Olympedia.org** | 1896-2024 | Web interface | Highest (official archive) | Free, filterable by year |
| **Kaggle: Summer Olympics Medals** | 1896-2024 | CSV | High | Free (requires account) |
| **Olympics.com** | 1896-2024 | Web/JSON | Official IOC | Free, limited API |

### Dataset Details

#### 1. Wikipedia Individual Medal Tables
- **URLs**: Individual pages per Olympic year
  - Example: `https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table`
  - Pattern: `https://en.wikipedia.org/wiki/[YEAR]_Summer_Olympics_medal_table`
- **Coverage**: Complete medal tables for all 30 Summer Olympics
- **Pros**:
  - Detailed footnotes explaining medal reallocations
  - Historical context for country changes
  - All medal-winning countries with exact counts
- **Cons**:
  - No official API (requires scraping)
  - Manual extraction needed per year

#### 2. Olympedia.org Statistics
- **URL**: `https://www.olympedia.org/statistics/medal/country`
- **Coverage**: 1896-2024, filterable by Games, sport, discipline
- **Pros**:
  - Official Olympic historical database (successor to sports-reference.com)
  - Maintained by OlyMADmen (Olympic historians)
  - Interactive filtering by year
- **Cons**:
  - No direct API
  - Requires web scraping or manual compilation

#### 3. Kaggle: Summer Olympics Medals (1896-2024)
- **URL**: `https://www.kaggle.com/datasets/stefanydeoliveira/summer-olympics-medals-1896-2024`
- **Size**: ~3.9 MB CSV
- **Structure**: Athlete-level data (NOT pre-aggregated by country)
- **Columns**: `player_id`, `Name`, `Sex`, `Team`, `NOC`, `Year`, `Season`, `City`, `Sport`, `Event`, `Medal`
- **Pros**:
  - Complete 1896-2024 coverage
  - Includes 2024 Paris Games
  - Downloadable CSV format
- **Cons**:
  - Requires aggregation (medals are per-athlete, not per-country)
  - Need to count medals per NOC/Year combination
- **License**: CC BY-NC-SA 4.0

#### 4. GitHub: Olympics-Dataset (KeithGalli)
- **URL**: `https://github.com/KeithGalli/Olympics-Dataset`
- **Coverage**: 1896-2022 (pre-2024)
- **Files**: `results/results.csv`, `athletes/bios.csv`
- **Source**: Scraped from Olympedia.org
- **Cons**: Does not include 2024 Paris Games

### Secondary Sources

- **Olympics.com Official Results**: Official but no historical API
- **Statista**: Aggregate statistics (requires subscription for full data)
- **Topendsports.com**: Medal tallies, good for validation
- **Figshare Historical Dataset**: 1896-2016 scraped from sports-reference.com (archived)

---

## Data Validation & Accuracy

### Cross-Source Validation Strategy

1. **Primary Reference**: Wikipedia individual medal tables (most accessible, peer-reviewed)
2. **Validation**: Cross-check against Olympedia.org filters
3. **Modern Games (2000-2024)**: Verify with Olympics.com official tables
4. **Early Games (1896-1920)**: Extra scrutiny due to historical inconsistencies

### Known Data Anomalies

| Games | Issue | Resolution |
|-------|-------|------------|
| **1896 Athens** | No standardized medal ceremonies | Some sources vary on silver/bronze counts |
| **1900 Paris** | Mixed Olympic/Exposition events | Use IOC-recognized medal counts only |
| **1904 St. Louis** | USA dominated (239 medals) | Accurate but skewed (few international competitors) |
| **1908 London** | Host nation rule changes | GBR total (146) legitimate under period rules |
| **2008 Beijing** | Doping reallocations | Use post-2024 corrected counts |
| **2012 London** | Ongoing doping cases | Wikipedia tables updated through Aug 2024 |

### Medal Reallocation Notes

Many historical medal counts have been revised due to:
- Doping disqualifications (especially 2000-2016 Games)
- Historical investigations
- IOC retroactive decisions

**Recommendation**: Use Wikipedia tables (current through August 2024) as they incorporate these changes.

---

## Historical Country Code Changes

### Critical Country Transitions

#### 1. **Russia / Soviet Union**

| Period | Code | Name | Notes |
|--------|------|------|-------|
| 1900-1912 | RUS | Russian Empire | Pre-revolution |
| 1952-1991 | URS | Soviet Union (USSR) | Dominant Cold War power |
| 1992 | EUN | Unified Team | Post-USSR transition (ex-Baltic states) |
| 1994-2017 | RUS | Russia | Independent Russian Federation |
| 2018 | OAR | Olympic Athletes from Russia | Doping sanctions |
| 2020-2022 | ROC | Russian Olympic Committee | Continued sanctions |
| 2024 | AIN | Individual Neutral Athletes | Ukraine conflict sanctions |

**Visualization Approach**:
- Display URS/EUN/ROC under "Russia" filter
- Annotate with historical context tooltip

#### 2. **Germany**

| Period | Code | Name | Notes |
|--------|------|------|-------|
| 1896-1936 | GER | Germany | Pre-WWII unified |
| 1952 | GER/SAA | West Germany + Saarland | Brief separate Saarland team |
| 1956-1964 | EUA | United Team of Germany | Combined East/West (French: Équipe unifiée d'Allemagne) |
| 1968-1988 | FRG | West Germany | Federal Republic of Germany |
| 1968-1988 | GDR | East Germany | German Democratic Republic |
| 1992-present | GER | Germany | Post-reunification |

**Visualization Approach**:
- Merge GER + FRG + GDR under "Germany" filter
- Show EUA separately with annotation
- Color-code by period if needed

#### 3. **Yugoslavia / Successor States**

| Period | Code | Name | Successor States |
|--------|------|------|------------------|
| 1920-1991 | YUG | Yugoslavia | - |
| 1992 | IOP | Independent Olympic Participants | Transitional (under sanctions) |
| 1996-2003 | YUG | Federal Republic of Yugoslavia | Serbia + Montenegro only |
| 2004-2006 | SCG | Serbia and Montenegro | - |
| 2008-present | SRB | Serbia | Independent |
| 1992-present | CRO | Croatia | Independent since 1992 |
| 1992-present | SLO | Slovenia | Independent since 1992 |
| 1992-present | BIH | Bosnia and Herzegovina | Independent since 1992 |
| 1992-present | MKD | North Macedonia | Independent since 1992 |
| 2008-present | MNE | Montenegro | Independent since 2008 |

**Note**: Kosovo (KOS) joined as independent NOC in 2016.

#### 4. **Czechoslovakia**

| Period | Code | Name | Notes |
|--------|------|------|-------|
| 1920-1992 | TCH/CZS | Czechoslovakia | IOC used both codes |
| 1992 | ČSFR | Czech and Slovak Federative Republic | Final Olympics |
| 1994-present | CZE | Czech Republic (Czechia) | "Velvet Divorce" split |
| 1994-present | SVK | Slovakia | - |

#### 5. **Australasia**

| Period | Code | Name | Composition |
|--------|------|------|-------------|
| 1908, 1912 | ANZ | Australasia | Australia + New Zealand combined |
| 1920-present | AUS | Australia | Separate teams thereafter |
| 1920-present | NZL | New Zealand | - |

**Historical Note**: Won 12 medals in two Games (notably 1908 Rugby gold).

#### 6. **Other Notable Changes**

- **China**: ROC (1932-1948, now Taiwan) → PRC/CHN (1952, then 1984-present)
- **Korea**: Unified Team (COR) at 2018 Winter Olympics only
- **Hong Kong**: HKG (separate NOC since 1952, continues post-1997)
- **Great Britain**: GBR consistent, but includes Northern Ireland (not IRL)
- **Netherlands Antilles**: AHO (dissolved 2011, athletes now compete for individual islands)

---

## Recommended Data Structure

### JSON Format (Year-Country Aggregation)

```json
{
  "olympics": [
    {
      "year": 1896,
      "host_city": "Athens",
      "host_country": "Greece",
      "cancelled": false,
      "medal_table": [
        {
          "rank": 1,
          "country": "United States",
          "noc": "USA",
          "gold": 11,
          "silver": 7,
          "bronze": 2,
          "total": 20
        },
        {
          "rank": 2,
          "country": "Greece",
          "noc": "GRE",
          "gold": 10,
          "silver": 18,
          "bronze": 19,
          "total": 47
        }
        // ... all medal-winning countries
      ]
    },
    {
      "year": 1900,
      "host_city": "Paris",
      "host_country": "France",
      "cancelled": false,
      "medal_table": [
        // ... all medal-winning countries
      ]
    },
    // ... all Olympics through 2024
    {
      "year": 1916,
      "host_city": "Berlin",
      "host_country": "Germany",
      "cancelled": true,
      "reason": "World War I",
      "medal_table": []
    }
  ],
  "metadata": {
    "last_updated": "2026-01-06",
    "source": "Wikipedia Olympic Medal Tables",
    "validation_sources": ["Olympedia.org", "Olympics.com"],
    "notes": "Medal counts current through August 2024 including doping reallocations"
  },
  "country_mapping": {
    "URS": {
      "name": "Soviet Union",
      "years": [1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988],
      "successor": "RUS",
      "notes": "Dissolved 1991"
    },
    "EUN": {
      "name": "Unified Team",
      "years": [1992],
      "predecessor": "URS",
      "successor": "RUS",
      "notes": "Post-Soviet transition team (ex-Baltic states)"
    },
    // ... other country transitions
  }
}
```

### Alternative: Flat Array (Current Implementation)

```json
[
  { "year": 1896, "country": "USA", "gold": 11, "silver": 7, "bronze": 2 },
  { "year": 1896, "country": "GRE", "gold": 10, "silver": 18, "bronze": 19 },
  // ... continues
]
```

**Pros**: Simple, minimal
**Cons**: No metadata, host city info, or country transition documentation

---

## Data Gaps & Special Cases

### Cancelled Olympics

| Year | Host City | Reason |
|------|-----------|--------|
| 1916 | Berlin, Germany | World War I |
| 1940 | Tokyo, Japan (then Helsinki) | World War II |
| 1944 | London, United Kingdom | World War II |

**Visualization**: Include as grayed-out rings or skip entirely

### Early Olympics Participation Issues

- **1896**: Only 14 nations participated
- **1900, 1904**: Part of World's Fair expositions, some events not considered "Olympic"
- **1904**: Dominated by USA (hosted in St. Louis, few international competitors)
- **1906**: "Intercalated Games" in Athens - no longer recognized by IOC

### Medal-Winner Definition

- Some early Olympics had fewer than 10 medal-winning nations
- 1896: Only 10 nations won medals (some tied)
- Recommendation: Include all medal-winning nations (early Games often have fewer entries)

---

## Implementation Recommendations

### Data Collection Approach

**Option 1: Manual Compilation (Recommended for Initial Build)**
1. Scrape or manually extract Wikipedia medal tables for each year
2. Include all medal-winning countries per Games
3. Export to JSON with recommended structure
4. Validate against Olympedia.org filters

**Estimated Time**: 4-6 hours for all 30 Games

**Option 2: Kaggle Dataset Processing**
1. Download CSV from Kaggle dataset
2. Aggregate medals by Year + NOC
3. Rank by total medals per year (no top-10 filter)
4. Export to JSON

**Python script**:
```python
import pandas as pd

# Load athlete-level data
df = pd.read_csv('summer_olympics_medals.csv')

# Filter medal winners only (exclude "No medal")
medals_df = df[df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]

# Count medals by Year, NOC, Medal type
medal_counts = medals_df.groupby(['Year', 'NOC', 'Medal']).size().unstack(fill_value=0)

# Calculate totals and rank
medal_counts['Total'] = medal_counts.sum(axis=1)
medal_counts['Rank'] = medal_counts.groupby('Year')['Total'].rank(ascending=False)

# Use all medal-winning countries per year
all_per_year = medal_counts

# Export to JSON
all_per_year.to_json('olympic_medals_all.json', orient='records')
```

**Option 3: Olympedia Web Scraping**
- Most accurate historical source
- Requires Beautiful Soup / Selenium
- More complex but highest quality

### Keeping Data Updated

#### For Future Olympics (2028 Los Angeles, 2032 Brisbane)

**Immediate Update Process** (within days of Games conclusion):
1. Check Olympics.com official medal table
2. Cross-reference with Wikipedia (usually updated within 24 hours)
3. Add new year entry to JSON
4. Validate rankings by total medals

**3-Month Post-Games Review**:
- Check for doping disqualifications
- Medal reallocations
- Update JSON with corrected counts

**Automated Monitoring** (Optional):
- GitHub Actions workflow to check Wikipedia page updates
- Scrape official Olympics.com API (if available)
- Generate pull request with new data

#### Data Maintenance Schedule

| Frequency | Task |
|-----------|------|
| **Every 4 years** | Add new Olympic Games data (2028, 2032, etc.) |
| **Annually** | Check for historical medal reallocations (doping cases) |
| **Ad-hoc** | Update for major IOC decisions (country code changes, Russia sanctions, etc.) |

---

## Data Quirks & Special Handling

### Medal Counting Methods

**Two Official Methods**:

1. **IOC Method** (used by Olympics.com): Rank by gold medals, then silver, then bronze
   - Example: Country with 10 gold > country with 5 gold + 20 silver

2. **Total Medal Method** (used by some media): Rank by total medals
   - Example: Country with 50 total medals > country with 40 total (regardless of gold count)

**Recommendation**: Use IOC method (gold-first ranking) but display total for tooltip

### Ties

When countries tie in all medal categories:
- Early Olympics: No tiebreaker (shared rank)
- Modern approach: Alphabetical by IOC code
- **Visualization**: Show both at same rank, adjust arc sizes equally

### Team vs. Individual Sports

- Team sports (basketball, volleyball) award one medal per team
- Individual sports award medals per athlete
- **Data source consistency**: Use official IOC counts (already aggregated correctly)

### Mixed-NOC Teams

- Early Olympics allowed mixed-nationality teams (rowing, etc.)
- These medals not counted toward any nation
- Listed as "Mixed team" (ZZX code in some databases)
- **Recommendation**: Exclude from visualization (rare, complicates narrative)

---

## Validation Checklist

Before finalizing data:

- [ ] All 30 Summer Olympics represented (1896-2024)
- [ ] Cancelled Olympics (1916, 1940, 1944) handled appropriately
- [ ] All medal-winning countries per Games validated against Wikipedia
- [ ] Country code mapping complete (URS→RUS, GDR→GER, etc.)
- [ ] Medal counts include post-2024 doping reallocations
- [ ] JSON structure includes metadata (last updated, sources)
- [ ] Spot-check 5 random Olympics against Olympedia.org
- [ ] USA medal counts validated (most consistent for comparison)
- [ ] 2024 Paris data confirmed from official Olympics.com

---

## Sample Data Extract

### 1896 Athens (First Modern Olympics)

| Rank | Country | NOC | Gold | Silver | Bronze | Total |
|------|---------|-----|------|--------|--------|-------|
| 1 | United States | USA | 11 | 7 | 2 | 20 |
| 2 | Greece | GRE | 10 | 18 | 19 | 47 |
| 3 | Germany | GER | 6 | 5 | 2 | 13 |
| 4 | France | FRA | 5 | 4 | 2 | 11 |
| 5 | Great Britain | GBR | 2 | 3 | 2 | 7 |
| 6 | Hungary | HUN | 2 | 1 | 3 | 6 |
| 7 | Austria | AUT | 2 | 1 | 2 | 5 |
| 8 | Australia | AUS | 2 | 0 | 0 | 2 |
| 9 | Denmark | DEN | 1 | 2 | 3 | 6 |
| 10 | Switzerland | SUI | 1 | 2 | 0 | 3 |

### 2024 Paris (Most Recent)

| Rank | Country | NOC | Gold | Silver | Bronze | Total |
|------|---------|-----|------|--------|--------|-------|
| 1 | United States | USA | 40 | 44 | 42 | 126 |
| 2 | China | CHN | 40 | 27 | 24 | 91 |
| 3 | Japan | JPN | 20 | 12 | 13 | 45 |
| 4 | Australia | AUS | 18 | 19 | 16 | 53 |
| 5 | France | FRA | 16 | 26 | 22 | 64 |
| 6 | Netherlands | NED | 15 | 7 | 12 | 34 |
| 7 | Great Britain | GBR | 14 | 22 | 29 | 65 |
| 8 | South Korea | KOR | 13 | 9 | 10 | 32 |
| 9 | Italy | ITA | 12 | 13 | 15 | 40 |
| 10 | Germany | GER | 12 | 13 | 8 | 33 |

---

## Next Steps

1. **Decide on data collection method** (manual Wikipedia scraping vs. Kaggle dataset processing)
2. **Create comprehensive JSON file** with all 30 Olympics
3. **Implement country code mapping** for filter functionality (Russia includes URS/EUN/ROC)
4. **Add metadata layer** (host cities, cancelled Games annotations)
5. **Create data update script** for 2028 Los Angeles Olympics
6. **Document visualization color scheme** for country consistency across years

---

## Resources & Links

### Data Sources
- [Wikipedia: All-time Olympic Games medal table](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table)
- [Wikipedia: Category - Summer Olympics medal tables](https://en.wikipedia.org/wiki/Category:Summer_Olympics_medal_tables)
- [Olympedia: Medals by country](https://www.olympedia.org/statistics/medal/country)
- [Kaggle: Summer Olympics Medals (1896-2024)](https://www.kaggle.com/datasets/stefanydeoliveira/summer-olympics-medals-1896-2024)
- [GitHub: Olympics-Dataset (KeithGalli)](https://github.com/KeithGalli/Olympics-Dataset)
- [Olympics.com: Official Results Database](https://www.olympics.com/en/olympic-games/olympic-results)
- [Topendsports: Olympic Medal Tallies](https://www.topendsports.com/events/summer/medal-tally/all-time-all.htm)

### Country Code References
- [Olympedia: Soviet Union (URS)](https://www.olympedia.org/countries/URS)
- [Olympedia: Unified Team (EUN)](https://www.olympedia.org/countries/EUN)
- [Wikipedia: Russia at the Olympics](https://en.wikipedia.org/wiki/Russia_at_the_Olympics)
- [Wikipedia: Germany at the Summer Olympics](https://en.wikipedia.org/wiki/Germany_at_the_Summer_Olympics)
- [Wikipedia: Yugoslavia at the Olympics](https://en.wikipedia.org/wiki/Yugoslavia_at_the_Olympics)
- [Wikipedia: Unified Team at the Olympics](https://en.wikipedia.org/wiki/Unified_Team_at_the_Olympics)
- [Olympics Wiki: List of IOC country codes](https://olympics.fandom.com/wiki/List_of_IOC_country_codes)

### Research Articles
- [Figshare: Olympic history dataset (1896-2016)](https://figshare.com/articles/dataset/Olympic_history_longitudinal_data_scraped_from_www_sports-reference_com/6121274)
- [Taylor & Francis: Olympic medalists 1896-2016](https://www.tandfonline.com/doi/full/10.1080/17445647.2021.1996475)

---

**Report Compiled By**: Luke Steuber (via Claude Code research orchestration)
**Last Updated**: 2026-01-06
**Status**: Ready for implementation
