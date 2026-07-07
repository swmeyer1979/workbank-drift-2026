# Wage-bill exposure

Joins occupation mean annual wage and occupation employment from WORKBank metadata to the 2026 zone migration table. Reported per migration class. Occupation-deduped within each migration class; one occupation may appear in multiple classes when different tasks moved differently.

**In-scope coverage:** 104 occupations / 22.3M workers / $1,977.5B wage bill.

## Migration class - wage and employment exposure

| migration | n occupations | workers (M) | wage bill ($B) | mean wage ($) |
|---|---:|---:|---:|---:|
| R&D->Green | 46 | 5.71 | 570.9 | 99,944 |
| Low->Red | 52 | 9.39 | 849.6 | 90,482 |
| Green->R&D | 3 | 0.33 | 33.2 | 101,426 |
| Red->Low | 2 | 0.08 | 12.3 | 158,806 |
| R&D->R&D | 13 | 3.06 | 191.9 | 62,619 |
| Low->Low | 4 | 1.04 | 79.2 | 75,826 |
| Green->Green | 94 | 21.45 | 1,900.4 | 88,589 |
| Red->Red | 79 | 19.42 | 1,558.2 | 80,218 |

## Headline numbers

- **Low→Red**: 52 occupations, 9.4M workers, **$850B wage bill** affected. Tasks workers did not want automated crossed the capability threshold.
- **R&D→Green**: 46 occupations, 5.7M workers, **$571B wage bill** affected. Tasks workers wanted automated now clear the capability threshold.

## Top 20 occupations by exposed wage bill (any migration)

| occupation | wage bill ($B) | workers (K) | mean wage ($) |
|---|---:|---:|---:|
| Computer and Information Systems Managers | 121.4 | 646.0 | 187,990 |
| Secretaries and Administrative Assistants, Except Legal, Medical, and Executive | 82.8 | 1,737.8 | 47,640 |
| Medical and Health Services Managers | 77.9 | 565.8 | 137,730 |
| Human Resources Specialists | 73.1 | 917.5 | 79,730 |
| Computer Systems Analysts | 55.7 | 497.8 | 111,960 |
| Computer User Support Specialists | 45.3 | 697.2 | 64,990 |
| Personal Financial Advisors | 43.3 | 270.5 | 160,210 |
| Medical Secretaries and Administrative Assistants | 37.9 | 830.8 | 45,580 |
| Human Resources Managers | 34.6 | 215.5 | 160,480 |
| Sales Representatives, Wholesale and Manufacturing, Technical and Scientific Products | 33.7 | 293.9 | 114,520 |
| Network and Computer Systems Administrators | 32.2 | 318.6 | 101,190 |
| Training and Development Specialists | 32.2 | 436.6 | 73,760 |
| Mechanical Engineers | 31.6 | 286.8 | 110,080 |
| Production, Planning, and Expediting Clerks | 23.3 | 385.0 | 60,420 |
| Information Security Analysts | 22.9 | 179.4 | 127,730 |
| Public Relations Specialists | 22.5 | 280.6 | 80,310 |
| Producers and Directors | 16.6 | 145.3 | 114,280 |
| Graphic Designers | 14.7 | 214.3 | 68,610 |
| Purchasing Managers | 12.2 | 81.2 | 150,630 |
| Insurance Claims and Policy Processing Clerks | 11.9 | 229.1 | 51,980 |

## Caveats

- Mean annual wage and employment come from the upstream BLS M2024 join provided in WORKBank metadata.
- Employment is total occupation-level U.S. employment, not the share of that occupation's wage bill exposed to the migrating tasks. This is an upper-bound exposure view.
- A finer-grained estimate would weight each occupation's wage bill by task importance, frequency, and relevance.
