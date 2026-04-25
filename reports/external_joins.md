# External-data joins — recommended next steps

Two external-data joins are recommended by the labor-economics review but require fetches outside this repo.

## 1. Felten / Raj / Seamans — AI Occupational Exposure (AIOE)

**Why:** correlate `capability_2026_median` per O*NET-SOC occupation with the AIOE index. Felten et al.'s scoring is the canonical occupation-level AI-exposure measure since 2021. Strong correlation = our drift study externally validates against an established measure; weak correlation = we're picking up something different (and we should explain what).

**Where to find:**
- Felten, Raj, Seamans (2021). *Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses.* Strategic Management Journal.
- Updated AIOE 2.0 dataset (2023): supplementary materials of follow-up paper. Search "Felten AIOE 2.0 replication."
- Direct contact: edward.felten@princeton.edu (paper's corresponding author).

**Join:** AIOE indexes by 6-digit SOC code; our `O*NET-SOC Code` is in `data/raw/task_statement_with_metadata.csv`. Aggregate `capability_2026_median` per occupation (mean across tasks), then Pearson/Spearman against AIOE.

**Expected output:** scatter plot + correlation coefficient. If r > 0.5 with AIOE, validates direction of drift. If r near 0, raises question.

## 2. Census ACS — demographic exposure

**Why:** the Low → Red migration touches occupations with specific demographic profiles. Without ACS join, claims about *which workers* are exposed are unsupported. Webb (2020), Acemoglu-Restrepo, and Eloundou et al. all do this join.

**Where to find:**
- IPUMS USA: https://usa.ipums.org/usa/ — extract OCC1990dd or OCC2018 + demographic vars (age, sex, race, education, income).
- Census ACS PUMS via Census Bureau API.

**Join:** ACS uses Census occupation codes; need a Census-OCC-to-O*NET-SOC crosswalk (BLS publishes one). Then aggregate exposed-worker-share by demographic.

**Expected output:** table — for each migration class, report % of exposed workers by gender / race / age / educational attainment.

## 3. (Optional) Anthropic Economic Index / Clio

**Why:** Tamkin et al. 2024 publish anonymized usage measurement showing where Claude is *actually deployed*. Cross-reference our predicted-capability with Clio's observed-deployment to expose deployment vs capability gap.

**Where:** https://www.anthropic.com/research/economic-index

---

These joins are non-trivial fetches and not blocking for the v1 release. Recommended as Phase 2.
