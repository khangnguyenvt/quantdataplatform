# Alternative Data Guide for Quant Research
### Product Releases & Patents · Bank Stress Tests · Credit & Bond Issuance · Pharma & Clinical Trials

This guide maps each data category to (a) where to actually pull it — free and paid — and (b) concrete ways quants turn it into signal. General best practices for using this kind of data are at the end.

---

## 1. Product Releases & Patent Filings

### Where to find it
| Source | What you get | Cost |
|---|---|---|
| **USPTO Patent Public Search / PatentsView** | Full-text US patents & applications, bulk bulk-download API, assignee/inventor metadata | Free |
| **WIPO PATENTSCOPE** | Global PCT filings (140+ countries) — earliest signal of intent to file in multiple jurisdictions | Free |
| **EPO Espacenet** | European filings, family/citation data | Free |
| **USPTO TESS/TSDR (Trademark Search)** | New trademark applications — often filed before product names are public | Free |
| **FCC Equipment Authorization (Office of Engineering & Technology filings)** | Companies must certify wireless/RF hardware before sale — filings frequently leak unreleased hardware (this is how many Apple/Google device leaks originate) | Free |
| **SEC EDGAR (8-K, earnings call transcripts)** | Material product launch disclosures | Free |
| **App store metadata (Sensor Tower, data.ai/App Annie, Apptopia)** | App release notes, ranking shifts, download velocity as product-adoption proxy | Paid |
| **IFI Claims, PatSnap, Clarivate Derwent Innovation, Relecura** | Cleaned, deduped, citation-linked patent databases with analytics layers | Paid |
| **GitHub (public repos, release tags)** | For software/AI companies, commit velocity & release cadence | Free |

### Making it valuable to quant
- **Innovation-value factor**: Weight patent counts by forward citations (KPSS-style "patent value" methodology) — academic literature (Kogan, Papanikolaou, Seru, Stoffman) shows citation-weighted patent value predicts future stock returns better than raw counts. Build a long-short factor: high patent-value-growth vs. peers.
- **FCC filing arbitrage**: Screen FCC OET filings by assignee for unreleased hardware ahead of earnings — a genuine leading indicator for consumer hardware names before street estimates adjust.
- **NLP topic clustering** on patent abstracts/claims to detect emerging technology clusters (e.g., solid-state battery chemistry, specific AI chip architectures) before they show up in sell-side thematic notes — useful for early sector rotation and thematic basket construction.
- **Litigation risk overlay**: Cross-reference patent filings with PACER/Lex Machina IP litigation dockets to flag names with rising infringement exposure.
- **Trademark filing lead time**: New trademark filings can precede product announcements by 6–18 months — useful as a low-cost "watchlist trigger" for retail, consumer tech, and pharma brand names.

---

## 2. Banks & Finance: Stress Test Results

### Where to find it
| Source | What you get | Cost |
|---|---|---|
| **Federal Reserve — CCAR & DFAST results** (federalreserve.gov) | Annual stress capital buffer (SCB) results, hypothetical loss rates, post-stress capital ratios for all large US banks | Free |
| **EBA EU-wide stress test** (eba.europa.eu) | Same for EU banks | Free |
| **Bank of England stress test results** | Same for UK banks | Free |
| **FFIEC Central Data Repository / Call Reports** | Quarterly bank financials (all US banks, not just G-SIBs) | Free |
| **FDIC BankFind / Quarterly Banking Profile** | Aggregate + individual bank condition data | Free |
| **Company 10-K/10-Q, investor decks** | CET1, capital return plans announced immediately after CCAR | Free |
| **S&P Capital IQ Pro, SNL Financial** | Cleaned bank financials, peer comps, historical stress test archives | Paid |

### Making it valuable to quant
- **Excess-capital factor**: Rank banks by (post-stress CET1 minus regulatory minimum + Stress Capital Buffer). Historically, banks that clear with the widest buffer announce the largest buyback/dividend increases within days of results — an event-driven long bias into results week (typically late June under the Fed's cycle).
- **Scenario-sensitivity mapping**: The Fed publishes the macro scenario assumptions (unemployment path, GDP shock, house price decline, equity shock) alongside modeled bank losses. Reverse-engineer each bank's implied sensitivity to specific macro shocks to build macro hedges or relative-value pairs (e.g., banks with high CRE exposure vs. those without, under the stress scenario's real estate assumptions).
- **Cross-sectional relative value**: Compare stress-implied loss rates on similar loan books across banks — persistent underperformers vs. peers on stress loss-rates tend to trade at a valuation discount; can be a slow-moving fundamental screen.
- **CDS/options reaction study**: Build an event study around stress test release day to characterize typical bank CDS spread and equity implied-vol compression/expansion patterns, useful for structuring pre-event vol trades.

---

## 3. Credit, Bond & Bond Issuance Data

### Where to find it
| Source | What you get | Cost |
|---|---|---|
| **FINRA TRACE** | Near-real-time corporate bond transaction prices/volumes (the core public source for corporate bond microstructure) | Free (delayed tape) / Paid (real-time/historical bulk) |
| **SEC EDGAR (424B, FWP prospectus filings, S-1/S-3)** | New bond issuance terms, covenants, use of proceeds | Free |
| **MSRB EMMA** | Municipal bond issuance & trade data | Free |
| **TreasuryDirect.gov** | US Treasury auction calendar & results | Free |
| **FRED (St. Louis Fed)** | Credit spread indices (ICE BofA AAA/BAA/High Yield OAS), corporate bond yield series | Free |
| **Dealogic / LSEG (Refinitiv) league tables** | Bond issuance volumes by sector, underwriter, region | Paid |
| **Moody's / S&P / Fitch ratings actions** | Rating changes, outlook changes, watch-list placements (press releases often free; full research paid) | Mixed |
| **Bloomberg/Refinitiv Eikon terminals** | Full cross-asset credit data, CDS curves | Paid (institutional) |

### Making it valuable to quant
- **Bond microstructure alpha**: Use TRACE tick data to model post-large-trade price reversion/momentum in corporate bonds — thinner-traded issues show exploitable mean-reversion after block trades.
- **Issuance-supply model**: Track weekly/monthly issuance calendars (Dealogic or EDGAR 424B filings) as a supply-side input to a credit spread forecasting model — heavy forward issuance calendars tend to cheapen secondary spreads ahead of pricing.
- **Ratings-migration anticipation**: Build a quantitative model (financial ratios + market-implied signals like CDS/equity vol) to anticipate rating actions before the agencies announce them — trade the CDS-bond basis or capital structure arbitrage ahead of the public announcement.
- **Credit as a macro leading indicator**: Aggregate issuance volumes by sector as a proxy for corporate capex/financing intentions — a leading indicator that can feed into cross-asset macro models (equity sector rotation, rate views).
- **CDS-bond basis trades**: Combine TRACE bond spreads with CDS market data to identify basis dislocations for relative value credit strategies.

---

## 4. Pharma Data, Clinical Trials & Drug Discovery

### Where to find it
| Source | What you get | Cost |
|---|---|---|
| **ClinicalTrials.gov** | The core global registry — trial phase, status (recruiting/active/completed/terminated), enrollment counts, sponsor, primary/secondary endpoints, and **update history** (via the API) | Free |
| **EU CTIS / EudraCT** | EU trial registrations | Free |
| **WHO ICTRP** | Aggregates registries globally | Free |
| **FDA Drugs@FDA / Purple Book** | Approved drug/biologic database | Free |
| **FDA FAERS** | Adverse event reports — spike detection can flag safety-signal risk pre-headline | Free |
| **FDA advisory committee & PDUFA date calendars** | Binary decision-date calendar for pending approvals | Free (scattered across FDA site) / aggregated by **BioPharmCatalyst** |
| **PubMed / bioRxiv / medRxiv** | Peer-reviewed and preprint literature — earliest public trace of a discovery, often before any company press release | Free |
| **Company 8-K / press releases** | Topline trial readouts | Free |
| **Evaluate Pharma / EvaluateVantage, GlobalData Pharma, Clarivate Cortellis** | Cleaned trial databases, consensus probability-of-success benchmarks by phase/indication | Paid |

### Making it valuable to quant
- **Trial status-change scraping**: Poll the ClinicalTrials.gov API for status transitions (e.g., "Recruiting" → "Active, not recruiting" → "Completed" → "Terminated") and *completion date* changes. A trial quietly shifting from "Completed" to "Terminated," or a primary completion date slipping repeatedly, is a leading indicator of trouble well before an official press release.
- **Binary-event calendar trading**: Build a systematic PDUFA/advisory-committee-date calendar to structure options strategies (straddles/calibrated skew trades) around FDA decision dates — a well-known biotech catalyst-trading approach.
- **Enrollment-velocity tracking**: Compare actual vs. planned enrollment counts over time to forecast trial timeline slippage, which correlates with delayed data readouts and guidance risk.
- **Probability-of-success (PoS) modeling**: Build a historical base-rate model of trial success by phase + therapeutic indication + trial design features, then compare your model's implied PoS to the options market's implied probability (derived from at-the-money straddle pricing around the readout date) to find mispriced binary risk.
- **Preprint-to-patent-to-approval pipeline**: Chain bioRxiv/PubMed discovery → patent filing (Section 1) → clinical trial registration → FDA approval into one signal pipeline — academic discoveries often precede market awareness by 1–3 years, giving a long-horizon thematic edge in small/mid-cap biotech.
- **FAERS anomaly detection**: Statistical spike detection on adverse-event report volume for approved drugs as an early warning system for label changes, recalls, or litigation risk.

---

## Cross-Cutting Notes for Building These Into a Quant Pipeline

1. **Point-in-time integrity is everything.** For every dataset above, capture *when the data became publicly available*, not just the data's content date. Patent applications are often published 18 months after filing; clinical trial "last updated" timestamps differ from when a status change was actually knowable. Backtests built on retroactively-corrected data will look far better than any live strategy.
2. **Legal/compliance boundary.** All sources listed here are public. Be careful with anything that involves scraping behind paywalls/ToS violations, or informal "expert network" channels — that shifts from alternative data into potential MNPI territory, which is a securities-law problem, not a data problem.
3. **Vendor discovery layer.** If you want to shortcut building scrapers yourself, alt-data discovery platforms like **Eagle Alpha**, **Neudata**, and **Yipit Data** catalog and benchmark hundreds of vendors across exactly these categories (patents, biotech catalysts, credit data, etc.) and can save significant build time.
4. **Combine, don't use in isolation.** The highest-conviction signals in practice come from *fusing* categories — e.g., a patent filing (Section 1) + a clinical trial registration (Section 4) + an FDA PDUFA date, chained together, tells a fuller story than any single feed.
5. **NLP/LLM layer.** Nearly every source above is semi-structured text (filings, press releases, trial descriptions). A modest NLP/LLM extraction layer (entity linking assignee → ticker, status-change detection, sentiment on protocol amendments) is usually where most of the practical value is created, more than the raw data acquisition itself.

