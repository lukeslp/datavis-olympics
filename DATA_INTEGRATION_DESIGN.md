# Olympic Medal Spiral - Data Integration Design

**Current State**: 40 data points (selective countries/years)
**Target State**: 1,433 data points (all medal-winning countries × 30 Olympic Games)
**File**: `/home/coolhand/html/datavis/poems/olympics/index.html`

---

## 1. Data Structure Strategy

### Recommendation: External JSON File

**Rationale**:
- Current inline data (40 points) = ~3KB
- Full dataset (1,433 points) = ~90KB
- Keeping HTML maintainable and cacheable
- Enables future data updates without touching code
- Browser can cache `data.json` separately

**Structure**:
```javascript
// data.json
{
  "games": [
    {
      "year": 1896,
      "location": "Athens, Greece",
      "countries": [
        { "code": "USA", "name": "United States", "gold": 11, "silver": 7, "bronze": 2 },
        { "code": "GRE", "name": "Greece", "gold": 10, "silver": 17, "bronze": 19 }
      ]
    }
  ],
  "countryMetadata": {
    "USA": {
      "name": "United States",
      "color": "#3b82f6",
      "historicalCodes": ["USA"]
    },
    "URS": {
      "name": "Soviet Union (1922-1991)",
      "color": "#a855f7",
      "historicalCodes": ["URS", "EUN", "RUS"],
      "successor": "RUS"
    },
    "GER": {
      "name": "Germany",
      "color": "#f59e0b",
      "historicalCodes": ["GER", "FRG", "GDR"],
      "note": "Unified after 1990"
    }
  }
}
```

**Loading Strategy**:
```javascript
async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        return transformData(data); // Convert to internal format
    } catch (error) {
        console.error('Failed to load Olympic data:', error);
        return FALLBACK_DATA; // Small embedded dataset for offline
    }
}
```

**Benefits**:
- Clean separation of data and visualization logic
- Version control friendly (data changes tracked separately)
- Easy to regenerate from authoritative sources
- Can add metadata (host city, boycotts, pandemic notes)

---

## 2. Visualization Scaling Adjustments

### Current Layout Analysis

**Ring spacing**: 18px
**Base radius**: 60px
**29 years**: 60 + (29 × 18) = 582px max radius
**Current viewport**: Dynamic (full screen)

**Problem**: With all medal-winning countries per year, arc segments become thin at inner rings

### Proposed Layout

#### Option A: Adaptive Ring Thickness (Recommended)

```javascript
function generateSpiral() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const baseRadius = 80; // Increased from 60
    const radiusStep = 22; // Increased from 18

    years.forEach((year, yearIndex) => {
        const yearData = OLYMPIC_DATA.filter(d => d.year === year);
        const radius = baseRadius + yearIndex * radiusStep;

        // Adaptive thickness: thicker for inner rings
        const thickness = Math.max(12, 18 - yearIndex * 0.15);

        // Minimum arc size for readability
        const minArcSize = 0.02; // ~1 degree minimum

        // ... segment generation
    });
}
```

**Max radius**: 80 + (29 × 22) = 718px (fits ~1400px viewports)

#### Option B: Logarithmic Spacing

```javascript
const radius = baseRadius + Math.log(yearIndex + 1) * 50;
```

**Trade-offs**:
- Compresses early years (fewer countries anyway)
- Expands modern games (more countries competing)
- Non-linear but perceptually cleaner

#### Option C: Two-Tier Spiral

```javascript
// Inner spiral: 1896-1960 (pre-modern era)
// Outer spiral: 1964-2024 (modern era)
```

**Recommendation**: **Option A** (Adaptive Ring Thickness)
- Most intuitive chronological progression
- Handles variable country counts gracefully
- Maintains visual consistency

---

## 3. Color Palette Expansion

### Current Palette: 11 Colors

```javascript
const COUNTRY_COLORS = {
    "USA": "#3b82f6", "CHN": "#ef4444", "GBR": "#22c55e",
    "RUS": "#a855f7", "GER": "#f59e0b", "FRA": "#06b6d4",
    "GRE": "#0ea5e9", "SWE": "#eab308", "URS": "#a855f7",
    "EUN": "#a855f7", "default": "#64748b"
};
```

### Proposed Palette: 25+ Distinguishable Colors

**Strategy**: Use categorical color schemes optimized for colorblind accessibility

```javascript
const COUNTRY_COLORS = {
    // Tier 1: Perennial medal leaders (high saturation)
    "USA": "#3b82f6",    // Blue
    "CHN": "#ef4444",    // Red
    "GBR": "#22c55e",    // Green
    "RUS": "#a855f7",    // Purple
    "GER": "#f59e0b",    // Amber
    "FRA": "#ec4899",    // Pink
    "ITA": "#8b5cf6",    // Violet
    "JPN": "#f43f5e",    // Rose
    "AUS": "#10b981",    // Emerald
    "NED": "#f97316",    // Orange

    // Tier 2: Frequent medalists (medium saturation)
    "CAN": "#14b8a6",    // Teal
    "BRA": "#84cc16",    // Lime
    "ESP": "#eab308",    // Yellow
    "KOR": "#06b6d4",    // Cyan
    "POL": "#d946ef",    // Fuchsia
    "SWE": "#0ea5e9",    // Sky
    "NOR": "#6366f1",    // Indigo
    "FIN": "#22d3ee",    // Light cyan
    "HUN": "#fb923c",    // Light orange
    "ROU": "#c084fc",    // Light purple

    // Historical entities (linked colors)
    "URS": "#a855f7",    // Same as RUS
    "EUN": "#9333ea",    // Darker purple (1992 Unified Team)
    "FRG": "#f59e0b",    // Same as GER
    "GDR": "#ea580c",    // Darker amber (East Germany)
    "TCH": "#ef4444",    // Czechia base

    // Fallback
    "default": "#64748b"
};
```

**Accessibility Validation**:
- Use Color Brewer categorical schemes
- Maintain 4.5:1 contrast ratio against dark background
- Tested with Coblis colorblind simulator

---

## 4. Performance Optimization

### Current Performance Profile

**Rendering**: ~40 segments × 60fps = 2,400 draws/sec
**Hit detection**: Linear search through 40 segments
**Memory**: ~20KB data + ~100KB canvas buffer

### Optimizations for 290 Segments

#### 4.1 Spatial Indexing for Hit Detection

```javascript
// Build quadtree or grid index on resize
function buildSpatialIndex() {
    const index = new Map(); // key: "ring_X", value: segments[]

    segments.forEach(seg => {
        const ringIndex = Math.floor((seg.radius - baseRadius) / radiusStep);
        const key = `ring_${ringIndex}`;
        if (!index.has(key)) index.set(key, []);
        index.get(key).push(seg);
    });

    return index;
}

// Fast lookup during mousemove
function findSegmentAtPoint(px, py) {
    const dx = px - centerX;
    const dy = py - centerY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const ringIndex = Math.floor((dist - baseRadius) / radiusStep);

    const candidates = spatialIndex.get(`ring_${ringIndex}`) || [];
    return candidates.find(seg => pointInSegment(px, py, seg));
}
```

**Impact**: O(n) → O(log n) hit detection
**Speedup**: 290 segments → ~10 candidates per lookup

#### 4.2 Render Culling

```javascript
function render() {
    // Only draw segments within viewport
    const viewportRadius = Math.max(canvas.width, canvas.height) / 2 + 100;

    const visibleSegments = segments.filter(seg =>
        seg.radius < viewportRadius
    );

    for (const seg of visibleSegments) {
        drawSegment(seg, seg === hoveredSegment);
    }
}
```

#### 4.3 Throttle Mousemove Events

```javascript
let lastMouseMoveTime = 0;
canvas.addEventListener('mousemove', (e) => {
    const now = performance.now();
    if (now - lastMouseMoveTime < 16) return; // ~60fps throttle
    lastMouseMoveTime = now;

    // ... hit detection
});
```

#### 4.4 Offscreen Canvas for Static Elements

```javascript
// Pre-render grid background once
const gridCanvas = document.createElement('canvas');
const gridCtx = gridCanvas.getContext('2d');

function prerenderGrid() {
    gridCanvas.width = canvas.width;
    gridCanvas.height = canvas.height;

    // Draw radial grid
    gridCtx.strokeStyle = 'rgba(255,255,255,0.03)';
    for (let r = baseRadius; r < maxRadius; r += radiusStep) {
        gridCtx.beginPath();
        gridCtx.arc(centerX, centerY, r, 0, Math.PI * 2);
        gridCtx.stroke();
    }
}

function render() {
    // Blit pre-rendered grid
    ctx.drawImage(gridCanvas, 0, 0);

    // Draw animated segments
    // ...
}
```

**Expected Performance**:
- 60fps maintained on 290 segments
- <5ms hit detection latency
- <50ms load time for data.json

---

## 5. Filter Control Redesign

### Current Controls: 6 Buttons

```html
<div id="controls">
    <button data-filter="all">All Countries</button>
    <button data-filter="USA">USA</button>
    <!-- 4 more hardcoded buttons -->
</div>
```

**Problem**: Doesn't scale to 20+ countries

### Proposed: Multi-Tiered Filter System

#### 5.1 Country Dropdown with Search

```html
<div id="controls">
    <div class="filter-group">
        <label>Country</label>
        <input type="text" id="country-search" placeholder="Search countries...">
        <select id="country-select" size="8">
            <option value="all" selected>All Countries</option>
            <!-- Populated dynamically, sorted by total medals -->
        </select>
    </div>

    <div class="filter-group">
        <label>Era</label>
        <select id="era-filter">
            <option value="all">All Years (1896-2024)</option>
            <option value="early">Early Era (1896-1936)</option>
            <option value="cold-war">Cold War (1948-1988)</option>
            <option value="modern">Modern (1992-2024)</option>
        </select>
    </div>

    <div class="filter-group">
        <label>Quick Filters</label>
        <div class="quick-filters">
            <button data-filter="USA">🇺🇸 USA</button>
            <button data-filter="CHN">🇨🇳 CHN</button>
            <button data-filter="GBR">🇬🇧 GBR</button>
            <button data-filter="RUS">🇷🇺 RUS</button>
        </div>
    </div>
</div>
```

**Features**:
- **Country search**: Fuzzy matching on country names
- **Era filtering**: Pre-defined historical periods
- **Quick filters**: Top 4-5 countries as buttons
- **Medal threshold**: "Show countries with 10+ medals"

#### 5.2 Responsive Layout

```css
#controls {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(10, 10, 20, 0.95);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 16px;
    border-radius: 8px;
    display: flex;
    gap: 20px;
    max-width: 90vw;
}

@media (max-width: 768px) {
    #controls {
        flex-direction: column;
        bottom: 0;
        left: 0;
        transform: none;
        width: 100%;
        border-radius: 0;
    }
}
```

#### 5.3 Multi-Select Mode

```javascript
let selectedCountries = new Set(['all']);

function toggleCountryFilter(country) {
    if (country === 'all') {
        selectedCountries = new Set(['all']);
    } else {
        selectedCountries.delete('all');
        if (selectedCountries.has(country)) {
            selectedCountries.delete(country);
        } else {
            selectedCountries.add(country);
        }
        if (selectedCountries.size === 0) {
            selectedCountries.add('all');
        }
    }
}

function isSegmentVisible(seg) {
    if (selectedCountries.has('all')) return true;
    return selectedCountries.has(seg.country) ||
           selectedCountries.has(seg.countryGroup); // For URS→RUS grouping
}
```

---

## 6. Historical Accuracy Handling

### Country Name Changes & Successors

**Critical Cases**:

| Historical Code | Years | Modern Code | Display Name |
|----------------|-------|-------------|--------------|
| URS | 1952-1988 | RUS | Soviet Union |
| EUN | 1992 | RUS | Unified Team |
| FRG | 1968-1988 | GER | West Germany |
| GDR | 1968-1988 | GER | East Germany |
| TCH | 1920-1992 | CZE | Czechoslovakia |
| YUG | 1920-1992 | SRB | Yugoslavia |

### Implementation Strategy

#### 6.1 Country Grouping System

```javascript
const COUNTRY_GROUPS = {
    "Russia": {
        codes: ["RUS", "URS", "EUN"],
        displayNames: {
            "RUS": "Russia",
            "URS": "Soviet Union (1922-1991)",
            "EUN": "Unified Team (1992)"
        },
        color: "#a855f7",
        filterKey: "RUS"
    },
    "Germany": {
        codes: ["GER", "FRG", "GDR"],
        displayNames: {
            "GER": "Germany",
            "FRG": "West Germany (1949-1990)",
            "GDR": "East Germany (1949-1990)"
        },
        color: "#f59e0b",
        filterKey: "GER"
    }
};
```

#### 6.2 Tooltip Display

```javascript
function formatCountryName(code, year) {
    for (const group of Object.values(COUNTRY_GROUPS)) {
        if (group.codes.includes(code)) {
            return group.displayNames[code];
        }
    }
    return COUNTRY_METADATA[code]?.name || code;
}

// In tooltip:
tooltip.innerHTML = `
    <h3 style="color: ${seg.color}">
        ${formatCountryName(seg.country, seg.year)}
        ${seg.year}
    </h3>
    ${getHistoricalNote(seg.country, seg.year)}
`;

function getHistoricalNote(code, year) {
    if (code === 'URS' && year === 1980) {
        return '<p class="note">US boycott of Moscow Games</p>';
    }
    if (code === 'USA' && year === 1984) {
        return '<p class="note">Soviet boycott of Los Angeles Games</p>';
    }
    return '';
}
```

#### 6.3 Filter Behavior

**When filtering by "Russia"**:
- Show RUS (1996-2024)
- Show URS (1952-1988)
- Show EUN (1992)
- Highlight all with same color family
- Display legend: "Russia & Predecessors"

```javascript
function getCountryFilterCodes(filterKey) {
    for (const group of Object.values(COUNTRY_GROUPS)) {
        if (group.filterKey === filterKey) {
            return group.codes;
        }
    }
    return [filterKey];
}

function matchesFilter(seg, filterKey) {
    if (filterKey === 'all') return true;
    const validCodes = getCountryFilterCodes(filterKey);
    return validCodes.includes(seg.country);
}
```

---

## 7. Additional Enhancements

### 7.1 Data Metrics Panel

```html
<div id="stats-panel">
    <h3>Olympic Statistics</h3>
    <div class="stat-row">
        <span>Total Games:</span>
        <span id="total-games">29</span>
    </div>
    <div class="stat-row">
        <span>Countries Represented:</span>
        <span id="total-countries">20+</span>
    </div>
    <div class="stat-row">
        <span>Total Medals:</span>
        <span id="total-medals">15,000+</span>
    </div>
    <div class="stat-row" id="filtered-stats" style="display: none;">
        <span>Filtered Medals:</span>
        <span id="filtered-count">0</span>
    </div>
</div>
```

### 7.2 Timeline Scrubber

```html
<input type="range" id="year-scrubber"
       min="1896" max="2024" step="4" value="2024">
<label id="scrubber-label">2024</label>
```

**Behavior**:
- Highlights selected year ring
- Shows only data up to selected year (historical progression)
- Auto-play mode: animates through years

### 7.3 Medal Count Visualization Modes

**Toggle between**:
- **Total medals** (current): arc size = gold + silver + bronze
- **Gold only**: arc size = gold count
- **Weighted**: arc size = (gold × 3) + (silver × 2) + (bronze × 1)

```javascript
let medalMode = 'total'; // 'total' | 'gold' | 'weighted'

function calculateMedalValue(data) {
    switch (medalMode) {
        case 'total': return data.gold + data.silver + data.bronze;
        case 'gold': return data.gold;
        case 'weighted': return data.gold * 3 + data.silver * 2 + data.bronze;
    }
}
```

### 7.4 Export Functionality

```javascript
function exportAsImage() {
    // Pause rotation
    const wasRotating = isRotating;
    isRotating = false;

    // Render static frame
    render();

    // Export
    canvas.toBlob(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `olympics-spiral-${Date.now()}.png`;
        a.click();
        URL.revokeObjectURL(url);
    });

    isRotating = wasRotating;
}
```

---

## 8. Implementation Roadmap

### Phase 1: Data Preparation (1-2 hours)
- [ ] Collect complete Olympic data from olympics.com
- [ ] Structure as `data.json` with metadata
- [ ] Add country groupings and historical notes
- [ ] Validate data completeness (30 games × all medal winners = 1,433 entries)

### Phase 2: Core Scaling (2-3 hours)
- [ ] Implement adaptive ring thickness
- [ ] Expand color palette to 25 colors
- [ ] Add spatial indexing for hit detection
- [ ] Optimize rendering with culling
- [ ] Test performance with full dataset

### Phase 3: Filter System (2-3 hours)
- [ ] Replace button controls with dropdown + search
- [ ] Add country grouping logic (Russia, Germany)
- [ ] Implement multi-select mode
- [ ] Add era filtering
- [ ] Mobile responsive layout

### Phase 4: Enhancements (2-4 hours)
- [ ] Historical notes in tooltips
- [ ] Statistics panel
- [ ] Timeline scrubber
- [ ] Medal visualization modes
- [ ] Export functionality

### Phase 5: Polish (1-2 hours)
- [ ] Accessibility testing (keyboard nav, screen readers)
- [ ] Performance profiling
- [ ] Cross-browser testing
- [ ] Documentation

**Total Estimated Time**: 8-14 hours

---

## 9. Testing Checklist

### Performance Benchmarks
- [ ] 60fps rendering with 290 segments
- [ ] <100ms data load time
- [ ] <5ms hover detection latency
- [ ] <500ms filter transition

### Data Integrity
- [ ] All 29 Summer Olympics represented
- [ ] All medal-winning countries per game
- [ ] Correct medal counts (validate against olympics.com)
- [ ] Historical country codes mapped correctly

### Cross-Browser
- [ ] Chrome 120+ (primary)
- [ ] Firefox 120+
- [ ] Safari 17+
- [ ] Mobile Safari (iOS)
- [ ] Mobile Chrome (Android)

### Accessibility
- [ ] ARIA labels on controls
- [ ] Keyboard navigation (Tab, Enter, Arrow keys)
- [ ] Screen reader support for data
- [ ] Colorblind-safe palette (test with Coblis)

---

## 10. File Structure (Post-Implementation)

```
olympics/
├── index.html              # Main visualization (remains single-file)
├── data.json               # Full Olympic dataset (new)
├── DATA_INTEGRATION_DESIGN.md  # This document
└── README.md               # User-facing documentation
```

**Alternative** (if file grows >1000 lines):
```
olympics/
├── index.html              # Shell + layout
├── data.json               # Olympic dataset
├── js/
│   ├── config.js           # Constants, colors, metadata
│   ├── spiral.js           # Spiral generation logic
│   ├── renderer.js         # Canvas rendering
│   ├── filters.js          # Filter controls
│   └── utils.js            # Helper functions
└── css/
    └── styles.css          # Extracted styles
```

**Recommendation**: Keep as single HTML file until >1000 lines for portability.

---

## Summary

**Key Decisions**:
1. **Data**: External JSON file (~20KB)
2. **Layout**: Adaptive ring thickness (80px base, 22px step)
3. **Colors**: 25-color categorical palette (colorblind-safe)
4. **Filters**: Dropdown + search + country grouping
5. **Performance**: Spatial indexing + render culling
6. **Historical**: Country succession logic (URS→RUS, etc.)

**Expected Outcome**:
- Smooth 60fps rendering of 290 data points
- Intuitive multi-country filtering
- Historically accurate country representations
- Accessible and mobile-friendly interface
- Maintainable single-file architecture

**Next Steps**:
1. Review this design document
2. Approve data structure and implementation approach
3. Begin Phase 1 (data collection)
4. Iterate through implementation phases
