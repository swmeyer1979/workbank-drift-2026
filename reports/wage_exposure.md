# Wage-bill exposure

Joins occupation mean annual wage (BLS via WORKBank metadata, M2024) and occupation employment to the 2026 zone migration table.
Reported per migration class. Occupation-deduped (one occupation may host many tasks; counted once).

**In-scope coverage:** 104 occupations / 22.3M workers / $1977494.53T wage bill.

## Migration class — wage and employment exposure

| migration | n occupations | workers (M) | wage bill ($B) | mean wage ($) |
|---|---:|---:|---:|---:|
| R&D->Green | 48 | 5.82 | 578640.08 | 112,918,333 |
| Low->Red | 52 | 9.39 | 849643.55 | 102,078,462 |
| Green->R&D | 3 | 0.33 | 33242.41 | 105,405,000 |
| Red->Low | 3 | 1.82 | 95100.36 | 154,370,000 |
| R&D->R&D | 9 | 1.81 | 114063.75 | 99,315,000 |
| Low->Low | 4 | 0.18 | 12533.83 | 87,910,000 |
| Green->Green | 94 | 21.45 | 1900396.93 | 96,290,000 |
| Red->Red | 79 | 19.42 | 1558215.64 | 84,905,085 |

## Headline numbers

- **Low→Red**: 52 occupations, 9.4M workers, **$849643.55T wage bill** affected. Tasks workers did not want automated, frontier crossed threshold anyway.
- **R&D→Green**: 48 occupations, 5.8M workers, **$578640.08T wage bill** affected. Tasks workers wanted automated; capability now delivers.

## Top 20 occupations by exposed wage bill (any migration)

| occupation | wage bill ($B) | workers (K) | mean wage ($) |
|---|---:|---:|---:|
| Computer and Information Systems Managers | 121435.90 | 646.0 | 187,990,000 |
| Secretaries and Administrative Assistants, Except  | 82789.74 | 1737.8 | 47,640,000 |
| Medical and Health Services Managers | 77933.14 | 565.8 | 137,730,000 |
| Bookkeeping, Accounting, and Auditing Clerks | 75729.16 | 1455.8 | 52,020,000 |
| Human Resources Specialists | 73149.09 | 917.5 | 79,730,000 |
| Computer Systems Analysts | 55733.69 | 497.8 | 111,960,000 |
| Computer User Support Specialists | 45311.68 | 697.2 | 64,990,000 |
| Personal Financial Advisors | 43333.60 | 270.5 | 160,210,000 |
| Medical Secretaries and Administrative Assistants | 37866.04 | 830.8 | 45,580,000 |
| Human Resources Managers | 34586.65 | 215.5 | 160,480,000 |
| Sales Representatives, Wholesale and Manufacturing | 33660.86 | 293.9 | 114,520,000 |
| Network and Computer Systems Administrators | 32236.10 | 318.6 | 101,190,000 |
| Training and Development Specialists | 32204.35 | 436.6 | 73,760,000 |
| Mechanical Engineers | 31566.54 | 286.8 | 110,080,000 |
| Production, Planning, and Expediting Clerks | 23261.70 | 385.0 | 60,420,000 |
| Information Security Analysts | 22918.59 | 179.4 | 127,730,000 |
| Public Relations Specialists | 22534.18 | 280.6 | 80,310,000 |
| Producers and Directors | 16601.46 | 145.3 | 114,280,000 |
| Graphic Designers | 14700.38 | 214.3 | 68,610,000 |
| Purchasing Managers | 12237.18 | 81.2 | 150,630,000 |

## Caveats

- Mean annual wage is from the upstream BLS M2024 join provided in WORKBank metadata. Stored as $1000s; converted to dollars here.
- Employment is total occupation-level US employment, not the share of that occupation's wage bill exposed to the migrating tasks. A pessimistic upper-bound interpretation.
- A finer-grained estimate would weight by task `Importance × Frequency × Relevance` to apportion an occupation's wage bill across its tasks; see `reports/weighted_aggregation.md`.