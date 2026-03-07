#!/usr/bin/env python3
"""
Fetch Olympic medal data for Summer Olympics (1896-2024)
Scrapes Wikipedia medal tables for all medal-winning countries per year
Output: JSON file with complete historical data
"""

import json
import re
import time
from typing import Dict, List, Optional, Set

import requests
from bs4 import BeautifulSoup

# Summer Olympic years (excluding canceled 1916, 1940, 1944)
SUMMER_OLYMPICS_YEARS = [
    1896, 1900, 1904, 1908, 1912,
    1920, 1924, 1928, 1932, 1936,
    1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992,
    1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024
]

NOC_CODES_URL = "https://en.wikipedia.org/wiki/List_of_IOC_country_codes"

# Country name overrides for medal table labels that differ from IOC naming.
ALIAS_MAPPINGS = {
    "United States": "USA",
    "Great Britain": "GBR",
    "Russia": "RUS",
    "Soviet Union": "URS",
    "USSR": "URS",
    "China": "CHN",
    "Unified Team": "EUN",
    "United Team of Germany": "EUA",
    "West Germany": "FRG",
    "East Germany": "GDR",
    "Czechoslovakia": "TCH",
    "Czech Republic": "CZE",
    "Czechia": "CZE",
    "Yugoslavia": "YUG",
    "FR Yugoslavia": "YUG",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "Iran": "IRI",
    "Syria": "SYR",
    "Vietnam": "VIE",
    "Chinese Taipei": "TPE",
    "Taiwan": "TPE",
    "Formosa": "TPE",
    "Hong Kong": "HKG",
    "Trinidad and Tobago": "TTO",
    "Congo": "CGO",
    "DR Congo": "COD",
    "Cote d'Ivoire": "CIV",
    "Ivory Coast": "CIV",
    "Cape Verde": "CPV",
    "Eswatini": "SWZ",
    "North Macedonia": "MKD",
    "Macedonia": "MKD",
    "Republic of the Congo": "CGO",
    "United Arab Emirates": "UAE",
    "Russian Olympic Committee": "RUS",
    "Olympic Athletes from Russia": "RUS",
    "Individual Neutral Athletes": "RUS",
    "ROC": "RUS",
    "OAR": "RUS",
    "AIN": "RUS",
    "Independent Olympic Athletes": "IOA",
    "Independent Olympic Participants": "IOP",
    "Refugee Olympic Team": "EOR",
}

EXCLUDED_ENTRIES = {"Totals", "Total", "Mixed team", "Mixed"}


def clean_country_name(country_name: str) -> str:
    """Normalize medal table country names by removing footnotes/parentheticals."""
    name = country_name.replace("\xa0", " ").strip()
    name = re.sub(r"\s*\([^)]*\)", "", name)
    name = re.sub(r"\[[^\]]+\]", "", name)
    name = re.sub(r"[†‡*]", "", name)
    name = re.split(r"\s+From\s+", name, maxsplit=1)[0]
    name = re.split(r"\s+from\s+", name, maxsplit=1)[0]
    name = re.split(r"\s+Now\s+", name, maxsplit=1)[0]
    name = re.sub(r"\s+", " ", name).strip()
    return name


def extract_noc_mappings() -> Dict[str, str]:
    """Fetch IOC code mappings from Wikipedia and normalize for medal tables."""
    response = requests.get(NOC_CODES_URL, headers={"User-Agent": "Olympic Data Collector (Educational)"})
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    def find_table(required_headers: List[str]) -> Optional[BeautifulSoup]:
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            if all(header in headers for header in required_headers):
                return table
        return None

    mapping: Dict[str, str] = {}

    def add_mapping(code: str, name: str) -> None:
        cleaned = clean_country_name(name)
        if cleaned:
            mapping[cleaned] = code

    current_table = find_table(["Code", "National Olympic Committee"])
    if current_table:
        for row in current_table.find_all("tr")[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) < 2:
                continue
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(" ", strip=True)
            add_mapping(code, name)

    special_table = find_table(["Code", "Nation/Team"])
    if special_table:
        for row in special_table.find_all("tr")[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) < 2:
                continue
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(" ", strip=True)
            add_mapping(code, name)

    former_table = find_table(["Code", "Nation (NOC)"])
    if former_table:
        for row in former_table.find_all("tr")[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) < 2:
                continue
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(" ", strip=True)
            add_mapping(code, name)

    for alias, code in ALIAS_MAPPINGS.items():
        mapping[clean_country_name(alias)] = code

    return mapping


def normalize_country(country_name: str, noc_mappings: Dict[str, str], unknown: Set[str]) -> str:
    """Convert country name to IOC code using IOC mappings and aliases."""
    cleaned = clean_country_name(country_name)
    if cleaned in EXCLUDED_ENTRIES:
        return ""
    if cleaned in noc_mappings:
        return noc_mappings[cleaned]
    unknown.add(cleaned)
    return cleaned[:3].upper()

def parse_medal_value(value: str) -> Optional[int]:
    cleaned = re.sub(r"[^\d]", "", value)
    return int(cleaned) if cleaned else None


def fetch_year_medals(
    year: int,
    noc_mappings: Dict[str, str],
    unknown: Set[str],
    top_n: Optional[int] = None,
) -> List[Dict]:
    """Fetch medal-winning countries for a specific Olympic year from Wikipedia."""
    url = f"https://en.wikipedia.org/wiki/{year}_Summer_Olympics_medal_table"

    print(f"Fetching {year}... ", end='', flush=True)

    try:
        response = requests.get(url, headers={'User-Agent': 'Olympic Data Collector (Educational)'})
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the medal table (usually the first sortable table)
        table = soup.find('table', class_='wikitable')

        if not table:
            print(f"⚠️  No table found")
            return []

        medals = []
        rows = table.find_all('tr')[1:]  # Skip header

        for row in rows:
            cols = row.find_all(['td', 'th'])

            if len(cols) < 4:
                continue

            # Extract country name (usually in first or second column)
            country_cell = cols[0] if cols[0].name == 'th' else cols[1]
            country_name = country_cell.get_text(" ", strip=True)

            # Skip totals/host nation rows
            if 'Total' in country_name or 'Host' in country_name:
                continue
            if clean_country_name(country_name) in EXCLUDED_ENTRIES:
                continue

            try:
                # Medal counts are typically in columns: [Rank], Country, Gold, Silver, Bronze, Total
                gold = parse_medal_value(cols[-4].get_text(strip=True))
                silver = parse_medal_value(cols[-3].get_text(strip=True))
                bronze = parse_medal_value(cols[-2].get_text(strip=True))

                if gold is None or silver is None or bronze is None:
                    continue

                country_code = normalize_country(country_name, noc_mappings, unknown)
                if not country_code:
                    continue

                medals.append({
                    'year': year,
                    'country': country_code,
                    'country_name': clean_country_name(country_name),
                    'gold': gold,
                    'silver': silver,
                    'bronze': bronze,
                    'total': gold + silver + bronze
                })
            except (ValueError, IndexError) as e:
                print(f"⚠️  Error parsing row: {e}")
                continue

        medals.sort(
            key=lambda d: (d['total'], d['gold'], d['silver'], d['bronze'], d['country_name']),
            reverse=True,
        )
        if top_n is not None:
            medals = medals[:top_n]
        for idx, medal in enumerate(medals, start=1):
            medal['rank_total'] = idx

        print(f"✓ {len(medals)} countries")
        return medals

    except requests.RequestException as e:
        print(f"❌ Error: {e}")
        return []

def main():
    """Fetch all Olympic medal data and save to JSON"""
    all_medals = []
    unknown_countries: Set[str] = set()
    noc_mappings = extract_noc_mappings()

    print("Fetching Olympic Medal Data (1896-2024)")
    print("=" * 50)

    for year in SUMMER_OLYMPICS_YEARS:
        medals = fetch_year_medals(year, noc_mappings, unknown_countries)
        all_medals.extend(medals)
        time.sleep(1)  # Be nice to Wikipedia servers

    print("=" * 50)
    print(f"Total entries: {len(all_medals)}")

    if unknown_countries:
        print("\n⚠️  Unmapped countries (check aliases/mappings):")
        for name in sorted(unknown_countries):
            print(f"  - {name}")

    # Save to JSON
    output_file = 'olympic_medals_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_medals, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data saved to {output_file}")

    # Print summary statistics
    countries = set(m['country'] for m in all_medals)
    print(f"✓ Countries represented: {len(countries)}")
    print(f"✓ Years covered: {len(SUMMER_OLYMPICS_YEARS)}")

    # Show sample
    print("\nSample data (2024):")
    for medal in all_medals[-5:]:
        print(f"  {medal['country']}: {medal['gold']}🥇 {medal['silver']}🥈 {medal['bronze']}🥉")

if __name__ == '__main__':
    main()
