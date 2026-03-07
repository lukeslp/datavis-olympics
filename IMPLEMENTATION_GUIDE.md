# Olympic Medal Data Implementation Guide

**Project**: Olympic Medal Spiral Visualization
**Date**: 2026-01-06
**Location**: `/home/coolhand/html/datavis/poems/olympics/`

---

## Quick Start

### Files Generated

1. **RESEARCH_REPORT.md** - Comprehensive research on data sources, country codes, and special cases
2. **sample_data.json** - Example JSON structure with 5 complete Olympics + metadata
3. **IMPLEMENTATION_GUIDE.md** - This file (integration instructions)

### Recommended Next Steps

1. **Choose data collection method** (see options below)
2. **Expand sample_data.json** to include all 30 Summer Olympics
3. **Update index.html** to consume JSON instead of inline JavaScript array
4. **Implement country code mapping** for filters (URS→RUS, GDR→GER, etc.)
5. **Add historical annotations** (cancelled Games, boycotts, etc.)

---

## Data Collection Options

### Option 1: Manual Wikipedia Scraping (Recommended)

**Best for**: Highest accuracy, complete control over data

**Process**:
1. Visit each Wikipedia medal table page
   - Pattern: `https://en.wikipedia.org/wiki/[YEAR]_Summer_Olympics_medal_table`
   - Example: `https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table`
2. Extract all medal-winning countries with medal counts
3. Add to JSON following `sample_data.json` structure
4. Cross-validate with Olympedia.org filters

**Time estimate**: 4-6 hours for all 30 Olympics

**Wikipedia URLs to scrape**:
```
1896: https://en.wikipedia.org/wiki/1896_Summer_Olympics_medal_table
1900: https://en.wikipedia.org/wiki/1900_Summer_Olympics_medal_table
1904: https://en.wikipedia.org/wiki/1904_Summer_Olympics_medal_table
1908: https://en.wikipedia.org/wiki/1908_Summer_Olympics_medal_table
1912: https://en.wikipedia.org/wiki/1912_Summer_Olympics_medal_table
1920: https://en.wikipedia.org/wiki/1920_Summer_Olympics_medal_table
1924: https://en.wikipedia.org/wiki/1924_Summer_Olympics_medal_table
1928: https://en.wikipedia.org/wiki/1928_Summer_Olympics_medal_table
1932: https://en.wikipedia.org/wiki/1932_Summer_Olympics_medal_table
1936: https://en.wikipedia.org/wiki/1936_Summer_Olympics_medal_table
1948: https://en.wikipedia.org/wiki/1948_Summer_Olympics_medal_table
1952: https://en.wikipedia.org/wiki/1952_Summer_Olympics_medal_table
1956: https://en.wikipedia.org/wiki/1956_Summer_Olympics_medal_table
1960: https://en.wikipedia.org/wiki/1960_Summer_Olympics_medal_table
1964: https://en.wikipedia.org/wiki/1964_Summer_Olympics_medal_table
1968: https://en.wikipedia.org/wiki/1968_Summer_Olympics_medal_table
1972: https://en.wikipedia.org/wiki/1972_Summer_Olympics_medal_table
1976: https://en.wikipedia.org/wiki/1976_Summer_Olympics_medal_table
1980: https://en.wikipedia.org/wiki/1980_Summer_Olympics_medal_table
1984: https://en.wikipedia.org/wiki/1984_Summer_Olympics_medal_table
1988: https://en.wikipedia.org/wiki/1988_Summer_Olympics_medal_table
1992: https://en.wikipedia.org/wiki/1992_Summer_Olympics_medal_table
1996: https://en.wikipedia.org/wiki/1996_Summer_Olympics_medal_table
2000: https://en.wikipedia.org/wiki/2000_Summer_Olympics_medal_table
2004: https://en.wikipedia.org/wiki/2004_Summer_Olympics_medal_table
2008: https://en.wikipedia.org/wiki/2008_Summer_Olympics_medal_table
2012: https://en.wikipedia.org/wiki/2012_Summer_Olympics_medal_table
2016: https://en.wikipedia.org/wiki/2016_Summer_Olympics_medal_table
2020: https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table
2024: https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table
```

### Option 2: Kaggle Dataset Processing

**Best for**: Automated approach, programmatic validation

**Dataset**: https://www.kaggle.com/datasets/stefanydeoliveira/summer-olympics-medals-1896-2024

**Python Script** (`process_kaggle_data.py`):

```python
import pandas as pd
import json
from collections import defaultdict

# Load Kaggle dataset
df = pd.read_csv('summer_olympics_medals_1896_2024.csv')

# Filter medal winners only
medals_df = df[df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]

# Group by Year and NOC, count medals by type
medal_counts = medals_df.groupby(['Year', 'NOC', 'Medal']).size().unstack(fill_value=0)

# Reset index to make Year and NOC columns
medal_counts = medal_counts.reset_index()

# Calculate totals
medal_counts['Total'] = medal_counts[['Gold', 'Silver', 'Bronze']].sum(axis=1)

# Rank by total medals, then gold/silver/bronze for tie-breaks
medal_counts = medal_counts.sort_values(
    ['Year', 'Total', 'Gold', 'Silver', 'Bronze'],
    ascending=[True, False, False, False, False]
)
medal_counts['RankTotal'] = medal_counts.groupby('Year')['Total'].rank(method='min', ascending=False)

# Use all medal-winning countries per year
all_per_year = medal_counts

# Build JSON structure
olympics_data = {"olympics": [], "metadata": {}, "country_mapping": {}}

for year in sorted(all_per_year['Year'].unique()):
    year_data = all_per_year[all_per_year['Year'] == year].sort_values(
        ['Total', 'Gold', 'Silver', 'Bronze'],
        ascending=False
    )

    medal_table = []
    for _, row in year_data.iterrows():
        medal_table.append({
            "rank_total": int(row['RankTotal']),
            "country": row['Team'],  # You may need country name mapping
            "noc": row['NOC'],
            "gold": int(row['Gold']),
            "silver": int(row['Silver']),
            "bronze": int(row['Bronze']),
            "total": int(row['Total'])
        })

    olympics_data['olympics'].append({
        "year": int(year),
        "host_city": "",  # Add manually or from separate dataset
        "host_country": "",
        "cancelled": False,
        "medal_table": medal_table
    })

# Add metadata
olympics_data['metadata'] = {
    "format_version": "1.0",
    "last_updated": "2026-01-06",
    "source": "Kaggle: Summer Olympics Medals (1896-2024)",
    "total_olympics": len(olympics_data['olympics'])
}

# Export to JSON
with open('olympic_medals_complete.json', 'w', encoding='utf-8') as f:
    json.dump(olympics_data, f, indent=2, ensure_ascii=False)

print(f"Exported {len(olympics_data['olympics'])} Olympics to olympic_medals_complete.json")
```

**Additional Requirements**:
- Manual addition of host cities (not in Kaggle dataset)
- Country name mapping (NOC codes may differ)
- Cancelled Games insertion (1916, 1940, 1944)

### Option 3: Web Scraping (Advanced)

**Best for**: Automated updates, future-proofing

**Python Script** (Beautiful Soup + Wikipedia):

```python
import requests
from bs4 import BeautifulSoup
import json

def scrape_olympic_medals(year):
    """Scrape Wikipedia medal table for a given Olympic year"""
    url = f"https://en.wikipedia.org/wiki/{year}_Summer_Olympics_medal_table"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find medal table (usually first sortable table)
    table = soup.find('table', {'class': 'wikitable'})

    medals = []
    rows = table.find_all('tr')[1:]  # Skip header, keep all medal-winning rows

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            noc = cols[0].text.strip()
            gold = int(cols[1].text.strip())
            silver = int(cols[2].text.strip())
            bronze = int(cols[3].text.strip())

            medals.append({
                "noc": noc,
                "gold": gold,
                "silver": silver,
                "bronze": bronze,
                "total": gold + silver + bronze
            })

    medals.sort(key=lambda m: (m["total"], m["gold"], m["silver"], m["bronze"]), reverse=True)
    for i, medal in enumerate(medals, start=1):
        medal["rank_total"] = i

    return medals

# Scrape all Olympics
olympic_years = [
    1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936,
    1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984,
    1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024
]

olympics_data = {"olympics": []}

for year in olympic_years:
    print(f"Scraping {year}...")
    medals = scrape_olympic_medals(year)

    olympics_data['olympics'].append({
        "year": year,
        "medal_table": medals
    })

# Save to JSON
with open('scraped_olympic_medals.json', 'w') as f:
    json.dump(olympics_data, f, indent=2)

print("Scraping complete!")
```

**Note**: Wikipedia's HTML structure may vary. Test on multiple years and adjust selectors as needed.

---

## Updating index.html

### Current Implementation

The existing `index.html` has medals hardcoded in JavaScript:

```javascript
const OLYMPIC_DATA = [
    { year: 1896, country: "USA", gold: 11, silver: 7, bronze: 2 },
    { year: 1896, country: "GRE", gold: 10, silver: 17, bronze: 19 },
    // ... more entries
];
```

### Recommended Changes

**1. Load JSON via fetch**:

```javascript
let OLYMPIC_DATA = [];
let COUNTRY_MAPPING = {};

async function loadOlympicData() {
    try {
        const response = await fetch('olympic_medals_complete.json');
        const data = await response.json();

        // Transform nested structure to flat array for compatibility
        OLYMPIC_DATA = data.olympics.flatMap(olympiad =>
            olympiad.medal_table.map(country => ({
                year: olympiad.year,
                country: country.noc,
                gold: country.gold,
                silver: country.silver,
                bronze: country.bronze
            }))
        );

        COUNTRY_MAPPING = data.country_mapping || {};

        console.log(`Loaded ${OLYMPIC_DATA.length} medal records from ${data.olympics.length} Olympics`);

        // Initialize visualization after data loads
        generateSpiral();
        render();
    } catch (error) {
        console.error('Failed to load Olympic data:', error);
    }
}

// Call on page load
loadOlympicData();
```

**2. Update filter buttons to handle country transitions**:

```javascript
// Enhanced filter to include historical codes
const FILTER_MAPPINGS = {
    'RUS': ['RUS', 'URS', 'EUN', 'ROC'],  // Russia includes Soviet Union, Unified Team, ROC
    'GER': ['GER', 'FRG', 'GDR', 'EUA'],   // Germany includes West/East Germany, United Team
    'USA': ['USA'],
    'CHN': ['CHN'],
    'GBR': ['GBR']
};

function drawSegment(seg, highlight = false) {
    const filterCodes = FILTER_MAPPINGS[currentFilter] || [currentFilter];

    if (currentFilter !== 'all' && !filterCodes.includes(seg.country)) {
        ctx.globalAlpha = 0.15;  // Dim non-matching countries
    } else {
        ctx.globalAlpha = 1;
    }

    // ... rest of drawing code
}
```

**3. Add host city annotations**:

```javascript
// In tooltip display
if (hoveredSegment) {
    const olympiad = data.olympics.find(o => o.year === hoveredSegment.year);

    tooltip.innerHTML = `
        <h3 style="color: ${seg.color}">${seg.country} - ${seg.year}</h3>
        <p style="font-size: 10px; color: #666;">${olympiad.host_city}, ${olympiad.host_country}</p>
        <div class="medals">
            <div class="medal-count"><span style="color: #ffd700">🥇</span> ${seg.gold}</div>
            <div class="medal-count"><span style="color: #c0c0c0">🥈</span> ${seg.silver}</div>
            <div class="medal-count"><span style="color: #cd7f32">🥉</span> ${seg.bronze}</div>
        </div>
        <div class="stat"><span>Total Medals</span><span>${seg.total}</span></div>
        ${olympiad.notes ? `<p style="font-size: 9px; color: #888; margin-top: 8px;">${olympiad.notes}</p>` : ''}
    `;
}
```

**4. Handle cancelled Olympics**:

```javascript
// In spiral generation
years.forEach((year, yearIndex) => {
    const olympiad = data.olympics.find(o => o.year === year);

    if (olympiad.cancelled) {
        // Draw grayed-out ring with no segments
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.stroke();

        // Add tooltip annotation for cancelled Games
        segments.push({
            year,
            cancelled: true,
            reason: olympiad.reason,
            centerX,
            centerY,
            radius,
            startAngle: 0,
            endAngle: Math.PI * 2
        });
    } else {
        // Regular medal table rendering
        // ... existing code
    }
});
```

---

## Country Code Mapping Implementation

### Filter Button Updates

**Replace hardcoded buttons**:

```html
<div id="controls">
    <button class="control-btn active" data-filter="all">All Countries</button>
    <button class="control-btn" data-filter="USA">USA</button>
    <button class="control-btn" data-filter="CHN">China</button>
    <button class="control-btn" data-filter="GBR">Great Britain</button>
    <button class="control-btn" data-filter="RUS" title="Includes USSR, Unified Team, ROC">Russia *</button>
    <button class="control-btn" data-filter="GER" title="Includes West/East Germany">Germany *</button>
</div>
```

### Dynamic Country Colors

**Update COUNTRY_COLORS to handle transitions**:

```javascript
const COUNTRY_COLORS = {
    // Modern codes
    "USA": "#3b82f6",
    "CHN": "#ef4444",
    "GBR": "#22c55e",
    "RUS": "#a855f7",
    "GER": "#f59e0b",
    "FRA": "#06b6d4",
    "JPN": "#ec4899",
    "AUS": "#10b981",
    "ITA": "#14b8a6",
    "KOR": "#6366f1",

    // Historical codes (map to modern equivalents)
    "URS": "#a855f7",  // Soviet Union → Russia color
    "EUN": "#a855f7",  // Unified Team → Russia color
    "ROC": "#a855f7",  // Russian Olympic Committee → Russia color
    "FRG": "#f59e0b",  // West Germany → Germany color
    "GDR": "#f59e0b",  // East Germany → Germany color
    "EUA": "#f59e0b",  // United Team of Germany → Germany color
    "YUG": "#84cc16",  // Yugoslavia
    "TCH": "#f97316",  // Czechoslovakia
    "ANZ": "#10b981",  // Australasia → Australia color

    "default": "#64748b"
};
```

---

## Data Validation Checklist

Before deploying:

- [ ] All 30 Summer Olympics present (1896-2024)
- [ ] Cancelled Olympics (1916, 1940, 1944) included with `cancelled: true`
- [ ] All medal-winning countries per Games (or fewer if no medals awarded)
- [ ] Medal counts validated against Wikipedia for 5 random Olympics
- [ ] Country code mapping tested (filter "Russia" shows URS, EUN, ROC)
- [ ] Host cities filled for all Olympics
- [ ] 2024 Paris data confirmed against official Olympics.com
- [ ] Metadata `last_updated` field reflects current date
- [ ] JSON validates (use `jsonlint.com` or `jq`)

---

## Future Updates (2028, 2032+)

### Automated Update Script

**`update_olympics.py`**:

```python
import json
from datetime import datetime

def add_new_olympics(year, host_city, host_country, medal_table):
    """
    Add a new Olympic Games to the JSON file

    Args:
        year: int - Olympic year
        host_city: str - Host city name
        host_country: str - Host country name
        medal_table: list - All medal-winning countries with medal counts
    """
    # Load existing data
    with open('olympic_medals_complete.json', 'r') as f:
        data = json.load(f)

    # Check if year already exists
    if any(o['year'] == year for o in data['olympics']):
        print(f"Warning: {year} Olympics already exists. Updating...")
        data['olympics'] = [o for o in data['olympics'] if o['year'] != year]

    # Add new Olympics
    new_olympics = {
        "year": year,
        "host_city": host_city,
        "host_country": host_country,
        "cancelled": False,
        "medal_table": medal_table
    }

    data['olympics'].append(new_olympics)
    data['olympics'].sort(key=lambda x: x['year'])

    # Update metadata
    data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    data['metadata']['total_olympics'] = len([o for o in data['olympics'] if not o.get('cancelled')])

    # Save
    with open('olympic_medals_complete.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully added {year} {host_city} Olympics!")

# Example usage for 2028 Los Angeles
medal_table_2028 = [
    {"rank": 1, "country": "United States", "noc": "USA", "gold": 45, "silver": 40, "bronze": 38, "total": 123},
    # ... all medal-winning countries (update after Games conclude)
]

add_new_olympics(2028, "Los Angeles", "United States", medal_table_2028)
```

### Update Timeline

| Date | Action |
|------|--------|
| **Olympic closing ceremony** | Scrape official Olympics.com medal table |
| **+1 day** | Add to JSON, validate against Wikipedia |
| **+3 months** | Re-check for doping reallocations, update if needed |
| **+1 year** | Final validation, mark as stable |

---

## Testing

### Local Development

1. **Start local server**:
   ```bash
   cd /home/coolhand/html/datavis/poems/olympics
   python3 -m http.server 8000
   ```

2. **Open in browser**:
   ```
   http://localhost:8000/
   ```

3. **Test filters**:
   - Click "Russia" - should show URS (1952-1988), EUN (1992), RUS (1996+), ROC (2020)
   - Click "Germany" - should show GER, FRG, GDR, EUA
   - Hover over segments - tooltip should display host city

4. **Validate data**:
   - Check browser console for "Loaded X medal records from 30 Olympics"
   - Verify no 404 errors for JSON file
   - Inspect spiral for cancelled Games (grayed rings for 1916, 1940, 1944)

### Production Deployment

The project is already served at `https://dr.eamer.dev/datavis/poems/olympics/`

After updating JSON:
1. Commit changes to git repository
2. Caddy automatically serves updated files (no restart needed)
3. Hard refresh browser (Ctrl+Shift+R) to bypass cache

---

## Troubleshooting

### JSON Not Loading

**Symptom**: Blank visualization, console error "Failed to load Olympic data"

**Solutions**:
- Check file path is correct (`olympic_medals_complete.json` in same directory as `index.html`)
- Validate JSON syntax with `jq` or online validator
- Ensure local server is running (not `file://` protocol)
- Check browser console for CORS errors

### Country Filter Not Working

**Symptom**: Clicking "Russia" doesn't show Soviet Union medals

**Solution**: Verify `FILTER_MAPPINGS` includes all historical codes:
```javascript
'RUS': ['RUS', 'URS', 'EUN', 'ROC', 'OAR', 'AIN']
```

### Missing Olympics

**Symptom**: Visualization shows gaps or fewer than 30 rings

**Solution**:
- Check JSON has all years 1896-2024 (excluding cancelled)
- Verify `olympics` array length in browser console
- Ensure `generateSpiral()` is called after data loads

---

## Performance Optimization

### Large Dataset Considerations

With 30 Olympics × 10 countries = 300+ data points:

1. **Canvas rendering**: Already efficient (current implementation uses requestAnimationFrame)
2. **Data loading**: Async fetch prevents blocking page load
3. **Future scaling**: If adding Winter Olympics or expanding to top 20 countries, consider:
   - Lazy loading (load visible rings only)
   - WebGL rendering for smoother animations
   - Service Worker caching for offline access

---

## Additional Features (Optional Enhancements)

### 1. Time Slider

Allow users to scrub through Olympic history:

```html
<input type="range" id="year-slider" min="1896" max="2024" step="4" value="2024">
<span id="slider-year">2024</span>
```

```javascript
document.getElementById('year-slider').addEventListener('input', (e) => {
    const year = parseInt(e.target.value);
    document.getElementById('slider-year').textContent = year;

    // Highlight only the selected year's ring
    currentYear = year;
    render();
});
```

### 2. Comparison Mode

Compare two countries side-by-side:

```javascript
let comparisonMode = false;
let comparedCountries = [];

function toggleComparison(country) {
    if (comparedCountries.includes(country)) {
        comparedCountries = comparedCountries.filter(c => c !== country);
    } else if (comparedCountries.length < 2) {
        comparedCountries.push(country);
    }

    if (comparedCountries.length === 2) {
        comparisonMode = true;
        showComparisonStats(comparedCountries[0], comparedCountries[1]);
    }
}
```

### 3. Export Functionality

Allow users to download medal data:

```javascript
function exportData(format = 'json') {
    const dataStr = format === 'json'
        ? JSON.stringify(OLYMPIC_DATA, null, 2)
        : convertToCSV(OLYMPIC_DATA);

    const blob = new Blob([dataStr], { type: format === 'json' ? 'application/json' : 'text/csv' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `olympic_medals.${format}`;
    link.click();
}
```

---

## Summary

### Completed Deliverables

✅ **RESEARCH_REPORT.md** - Comprehensive data source analysis
✅ **sample_data.json** - Example JSON structure with 5 Olympics
✅ **IMPLEMENTATION_GUIDE.md** - This integration guide

### Next Actions

1. **Data Collection**: Choose method (manual Wikipedia, Kaggle, or scraping)
2. **JSON Expansion**: Complete all 30 Olympics in `olympic_medals_complete.json`
3. **Code Integration**: Update `index.html` to load JSON via fetch
4. **Country Mapping**: Implement filter mappings for URS→RUS, GDR→GER, etc.
5. **Testing**: Validate visualization with complete dataset
6. **Documentation**: Add data source attribution in info panel

### Maintenance Plan

- **2028 Los Angeles Olympics**: Add new data within 1 week of closing ceremony
- **Annual Review**: Check Wikipedia for doping reallocations
- **Every 4 years**: Update JSON with latest Summer Olympics

---

**Guide Compiled By**: Luke Steuber
**Last Updated**: 2026-01-06
**Ready For**: Implementation
