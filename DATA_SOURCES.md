# Olympic Medal Data Sources

## Data Collection Summary

**Generated**: January 6, 2026
**Dataset**: 1,433 entries covering 30 Summer Olympic Games (1896-2024)
**Countries**: 159 nations represented
**Total Medals**: 17,906 (5,816 gold, 5,787 silver, 6,303 bronze)

## Methodology

### Data Source
- **Primary Source**: Wikipedia Olympic medal tables for individual years
  - Each year has dedicated medal table page (e.g., "1896 Summer Olympics medal table")
  - Data compiled from IOC (International Olympic Committee) database
  - All medal-winning countries extracted per Olympic Games (ranked by total medals)

### Data Collection Process
1. **Automated Scraping**: Python script (`fetch_olympic_data.py`) using BeautifulSoup
2. **Years Covered**: All Summer Olympics from 1896-2024 (excluding canceled 1916, 1940, 1944)
3. **Country Normalization**: IOC country codes applied consistently
4. **Historical Transitions Handled**:
   - USSR (URS) → Unified Team (EUN, 1992) → Russia (RUS)
   - West Germany (FRG) + East Germany (GDR) → Unified Germany (GER)
   - Czechoslovakia (TCH) → Czech Republic (CZE)
   - Yugoslavia (YUG) → Serbia (SRB)

### Data Validation
- Cross-referenced against Olympics.com official records
- Verified 2024 Paris Olympics data against live results
- Validated historical records against IOC archives
- Country code consistency enforced throughout dataset

## Key Data Points

### Top 10 Most Frequent Countries
| Rank | Country | Appearances (out of 30) |
|------|---------|-------------------------|
| 1    | FRA     | 30                      |
| 2    | GBR     | 30                      |
| 3    | USA     | 29                      |
| 4    | DEN     | 29                      |
| 5    | SUI     | 29                      |
| 6    | HUN     | 28                      |
| 7    | AUS     | 28                      |
| 8    | BEL     | 28                      |
| 9    | ITA     | 28                      |
| 10   | SWE     | 28                      |

### Data Characteristics
- **Average entries per year**: ~48 countries
- **Most dominant performance**: USA 1904 (77 gold, 234 total medals)
- **Most recent**: Paris 2024 (USA and China tied at 40 gold each)

## Country Code Reference

### Major Powers
- **USA**: United States (consistent throughout)
- **CHN**: China (Olympic debut 1984)
- **GBR**: Great Britain (host 1908, 1948, 2012)
- **URS**: Soviet Union (1952-1988)
- **RUS**: Russia (post-1991, includes ROC for 2020)
- **GER**: Germany (unified, and post-1990)
- **FRG**: West Germany (1968-1988)
- **GDR**: East Germany (1968-1988)

### Frequent European Nations
- **FRA**: France
- **ITA**: Italy
- **HUN**: Hungary
- **SWE**: Sweden
- **FIN**: Finland
- **POL**: Poland
- **NED**: Netherlands
- **NOR**: Norway
- **DEN**: Denmark
- **SUI**: Switzerland
- **AUT**: Austria
- **BEL**: Belgium
- **ESP**: Spain
- **ROU**: Romania
- **TCH**: Czechoslovakia
- **BUL**: Bulgaria
- **UKR**: Ukraine
- **SRB**: Serbia/Yugoslavia

### Other Nations
- **JPN**: Japan
- **AUS**: Australia
- **CAN**: Canada
- **KOR**: South Korea
- **CUB**: Cuba
- **TUR**: Turkey
- **RSA**: South Africa
- **NZL**: New Zealand
- **GRE**: Greece

## Data Limitations

1. **All Medal Winners**: Each Olympic Games includes every medal-winning country (ranked by total medals)
2. **Historical Accuracy**: Early Olympics (1896-1920) had different medal systems and counting methods
3. **Country Transitions**: Some historical transitions are simplified (e.g., all Soviet medals counted as URS)
4. **Mixed Teams**: 1900 Paris included "Mixed" teams which were excluded from this dataset

## Update Process

To update with future Olympic Games:

```bash
# Run the fetch script
python3 fetch_olympic_data.py

# Verify new data
python3 -c "import json; data = json.load(open('olympic_medals_data.json')); print(f'{len(data)} entries')"

# Regenerate inline JavaScript
python3 -c "import json; data = json.load(open('olympic_medals_data.json')); compact = [{'year': d['year'], 'country': d['country'], 'gold': d['gold'], 'silver': d['silver'], 'bronze': d['bronze']} for d in data]; open('olympic_data_inline.js', 'w').write('const OLYMPIC_DATA = ' + json.dumps(compact, separators=(',', ':')) + ';')"
```

## References

- [Wikipedia: All-time Olympic Games medal table](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table)
- [Wikipedia: Individual Summer Olympics medal tables](https://en.wikipedia.org/wiki/[YEAR]_Summer_Olympics_medal_table)
- [Olympics.com: Official Olympic Records](https://olympics.com)
- [IOC Database](https://www.olympic.org)

## Citation

```bibtex
@dataset{olympic_medals_2026,
  title={Summer Olympic Games Medal Data (1896-2024)},
  author={Compiled from Wikipedia and IOC sources},
  year={2026},
  url={https://dr.eamer.dev/datavis/poems/olympics/},
  note={All medal-winning countries per Olympic Games, sourced from Wikipedia Olympic medal tables}
}
```
