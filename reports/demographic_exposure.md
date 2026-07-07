# Demographic exposure analysis

For each migration class, this report shows the employment-weighted demographic share of exposed occupations. Source: BLS Current Population Survey Annual Averages Table 11, stored locally as `data/raw/bls_race_gender.csv`.

Coverage: 50/104 WORKBank occupations matched on cleaned title to BLS CPS.

## Side-by-side: migration class vs demographic shares (employment-weighted)

| migration | n occs | workers (M) | Women % | White % | Black/AA % | Asian % | Hispanic % |
|---|---:|---:|---:|---:|---:|---:|---:|
| R&D->Green | 16 | 4.25 | 51.0% | 79.1% | 9.2% | 8.0% | 13.4% |
| Low->Red | 23 | 7.35 | 65.5% | 78.6% | 10.5% | 7.4% | 13.7% |
| Green->Green | 45 | 18.20 | 60.4% | 77.3% | 11.4% | 7.8% | 14.1% |
| Red->Red | 42 | 16.43 | 62.4% | 77.6% | 11.5% | 7.3% | 14.6% |

## U.S. workforce baseline (BLS CPS, all 16+ workers, 2024)

- Women: 47.1% · White: 76.3% · Black/AA: 12.8% · Asian: 7.0% · Hispanic: 19.4%

## Reading guide

- A migration class with above-baseline share of a demographic indicates that group is over-exposed to that drift pattern.
- Hispanic ethnicity overlaps with race per BLS methodology, so columns can sum above 100%.
- Capability is not deployment; exposure here means 2026 frontier capability crossed the threshold.

## Caveats

- BLS CPS occupation strings do not always match WORKBank O*NET-SOC titles. 54 occupations remain unmatched.
- Publication-grade demographic analysis should use IPUMS USA ACS PUMS with explicit SOC codes.
