# Market-Data Memo: Scenario 12 `grain-cooperative`
Date as-of: 2026-10-30 (market close)\
Date retrieved: 2026-11-20\
Time and time zone: 5:30pm HST\
Author: Meghan Hernandez\
Workbook version: 1.0\
Spec version: 1.0


## 1. Purpose
This memo records the source, timestamp and logic for every live input that replaces the Stage 3 placeholders, so an auditor (or a reader who has only this memo and the spec) can re-pull every number.

## 2. Conventions
- Quote convention: USD per EUR (a higher rate means EUR appreciation)
- Day-count basis: 360 for both USD and EUR; `BASIS` = 360
- Interest treatment: simple (non-compounded), ACT/360 growth factors `DF_USD` = 1 + `R_USD` x `T_DAYS/BASIS` and `DF_FC` = 1 + `R_FC` x `T_DAYS/BASIS`
- Currency of results: USD at the settlement date
- Settlement date: 2027-04-30 (`VAL_DATE` 2026-10-30 + 182 days)

## 3. Input table
| Input | Value | Source | URL | As-of | Notes |
|---|---|---|---|---|---|
| FC_AMT | 6,900,000 EUR | Scenario 12 invoice terms | n/a | 2026-10-30 | From scenario |
| S0_in | 1.1160 | Investing.com EUR/USD historical data, close for Oct 30, 2026 (range 1.1136 to 1.1215) | https://www.investing.com/currencies/eur-usd-historical-data | 2026-10-30 close | Cross-checks: ECB reference rate 1.1172; Yahoo Finance USD/EUR close 0.8942 (about 1.1183 inverted). Sources differ by up to 0.0023 (0.2%). |
| F0_in | 1.1705 | Scenario bank quote, kept as given | n/a | 2026-10-30 | Never replaced by my own rate; no requote requested
| R_USD | 4.25% | FRED series DGS6MO (market yield on U.S. Treasury securities at 6-month constant maturity, investment basis), source Federal Reserve Board H.15 | https://fred.stlouisfed.org/series/DGS6MO | 2026-10-30 | Bond-equivalent yield on a 365-day year, used as published in a 360-day simple-interest model (known simplification) |
| R_FC | 2.992% | 6-month Euribor fixing | https://euriborrates.com/term-comparison/euribor-6m | 2026-10-30 | Aggregator sources (euriborrates.com, and a second aggregator, urbo.lt); the primary EMMI fixing was not checked |
| T_DAYS | 182 | Scenario, SETTLE_DATE minus VAL_DATE | n/a | 2026-10-30 | Calendar days |
| VAL_DATE | 2026-10-30 | Date of the market-data pull | n/a | n/a | Start date of Stage 4 |
| BASIS | 360 | CME Term SOFR and EMMI Euribor methodology, both ACT/360 | n/a | n/a | Convention |
| K_PUT | 1.1160 (= S0_in) | Scenario convention: at the money | n/a | 2026-10-30 | Equal to live S0_in |
| K_CALL | 1.1160 (= S0_in) | Scenario convention: at the money | n/a | 2026-10-30 | Equal to live S0_in |
| PREM_PUT | 0.0194 USD per EUR | Scenario-given | n/a | n/a | Assumption (see Section 6) |
| PREM_CALL | 0.0296 USD per EUR | Scenario-given | n/a | n/a | Assumption (see Section 6) |

### 3A. Placeholders replaced and live check figures

Stage 2 and Stage 3 were built on indicative placeholders dated 29 Oct 2026. The live values below replace them. A reader working from the spec and this memo should use the live values.

| Input | Spec placeholder (29 Oct 2026) | Live value (30 Oct 2026) | Changed? |
|---|---|---|---|
| `S0_in` | 1.1191 | 1.1160 | Yes |
| `R_USD` | 4.216% | 4.25% | Yes |
| `R_FC` | 2.960% | 2.992% | Yes |
| `VAL_DATE` | 2026-10-29 | 2026-10-30 | Yes |
| `SETTLE_DATE` | 2027-04-29 | 2027-04-30 | Yes |
| `K_PUT` | 1.1191 (= S0_in) | 1.1160 (= S0_in) | Yes |
| `K_CALL` | 1.1191 (= S0_in) | 1.1160 (= S0_in) | Yes |
| `F0_in` | 1.1705 | 1.1705 | No (bank quote kept as given) |
| `PREM_PUT` | 0.0194 | 0.0194 | No (scenario-given) |
| `PREM_CALL` | 0.0296 | 0.0296 | No (scenario-given) |
| `FC_AMT` | 6,900,000 | 6,900,000 | No |
| `T_DAYS` | 182 | 182 | No |
| `BASIS` | 360 | 360 | No |

Calculated from the live inputs before loading the workbook, using `DF_USD` = 1.021486 and `DF_FC` = 1.015126. These replace the placeholder figures in spec Section 6.3 and are confirmed or corrected in Sections 7 and 8 after loading.

| Output | Placeholder figure (spec) | Live figure |
|---|---|---|
| Unhedged proceeds at spot (`S0_in` x `FC_AMT`) | 7,721,790 | 7,700,400 |
| Forward proceeds (`USD_FWD`) | 8,076,450 | 8,076,450 |
| Money market: EUR borrowed (`FC_AMT` / `DF_FC`) | 6,798,268 | 6,797,184 |
| Money market: USD today (x `S0_in`) | 7,607,941 | 7,585,658 |
| Money-market proceeds (`USD_MM`) | 7,770,099 | 7,748,644 |
| CIP-implied forward (`F_CIP`) | 1.1261 | 1.1230 |
| Parity gap in USD (`USD_FWD` minus `USD_MM`) | 306,351 | 327,806 |
| Parity gap as % of `USD_MM` | 3.94% | 4.23% |
| Parity status | REVIEW | REVIEW |
| `FV_PREM_PUT` | -136,713 | -136,736 |
| `FV_PREM_CALL` | -208,593 | -208,628 |
| Put floor (`USD_FLOOR_PUT`) | 7,585,077 | 7,563,664 |
| Call break-even (`BE_CALL`) | 1.1493 | 1.1462 |
| Sensitivity grid, first and last `S_T` | 1.0631 / 1.1751 | 1.0602 / 1.1718 |

Parity stays at REVIEW because the quoted forward (1.1705) is about 4.9% above spot, which current rates do not support. The status is not changed to make a check pass.

## 4. Rate choices
### R_USD
- Instrument chosen: FRED DGS6MO, 6-month Treasury constant maturity.
- Why this instrument: A risk-free 6-month USD rate that matches the 182-day horizon and is forward-looking, which parity needs. Alternatives considered and not used: 180-day average SOFR (FRED SOFR180DAYAVG, 3.718% on Oct 30; backward-looking, so a weak input for a forward-looking parity check).
- Day-count and tenor match to `T_DAYS`: 365-day bond-equivalent yield used as published; converting to ACT/360 would give about 4.19% and widen the parity gap by about USD 2,200, which does not change the conclusion.

### R_FC
- Instrument chosen: 6-month Euribor fixing.
- Why this instrument: Standard EUR money-market reference at a tenor matching `T_DAYS`.
- Day-count and tenor match to `T_DAYS`: ACT/360, no adjustment needed.

## 5. Forward quote and CIP comparison
`F0_in` stays the bank's quote and is never replaced by my own rate.

`F_CIP` = `S0_in` x (1 + `R_USD` x `T_DAYS/BASIS`) / (1 + `R_FC` x `T_DAYS/BASIS`)

| Measure | Value |
|---|---|
| `DF_USD` | 1.021486 |
| `DF_FC` | 1.015126 |
| Bank forward quote (`F0_in`) | 1.1705 |
| CIP-implied forward (`F_CIP`) | 1.1230 |
| Gap as a rate (`F0_in` minus `F_CIP`) | 0.0475 |
| Forward proceeds `USD_FWD` | 8,076,450 |
| Money-market proceeds `USD_MM` | 7,748,644 |
| EUR borrowed | 6,797,184 |
| USD today | 7,585,658 |
| Gap in USD (`USD_FWD` minus `USD_MM`) | 327,806 |
| Gap as % of `USD_MM` | 4.23% |
| Parity tolerance 0.05% of `USD_MM` | about USD 3,874 |
| Parity status | REVIEW |

The gap is far larger than the parity tolerance, so the parity status is REVIEW.

Interpretation / requote requested: The quoted forward is about 4.9% above spot, which today's rates do not support. The gap is a finding about the quote, not a model error. Requote requested: No.

Sensitivity: with ECB spot 1.1172 the gap is about USD 319,000; each 0.1 percentage point change in R_USD moves the gap by about USD 3,800.

## 6. Option premiums
`PREM_PUT` and `PREM_CALL` are scenario-given assumptions, kept because retail option quotes are unreliable. Source: scenario 12.

## 7. Workbook population
| Named range | Cell entered | Value entered | Entered through input cell only? (Y/N) |
|---|---|---|---|
| S0_in | D7 | 1.1160 | Y |
| R_USD | D9 | 0.0425 | Y |
| R_FC | D10 | 0.02992 | Y |
| VAL_DATE | D12 | 2026-10-30 | Y |

## 8. Checks after loading live data
| Check | Result | Notes |
|---|---|---|
| Parity check status | REVIEW | Shown on the Check tab after Excel recalculation |
| Parity gap in USD and % | 327,806 USD / 4.23% | Against USD_MM of 7,748,644 |
| Sensitivity grid recentred on new spot | Y | Endpoints are 1.0602 and 1.1718 |
| Chart redraws | Y | Chart series cache reflects the recalculated sensitivity grid |
| Formula error cells | None observed | No formula-error values in the saved workbook after recalculation |
| Failed check: Money-market EUR borrowing | FAIL | 6,797,184 versus typed check reference 6,798,268 |
| Failed check: Money-market USD conversion | FAIL | 7,585,658 versus typed check reference 7,607,941 |
| Failed check: Money-market USD investment | FAIL | 7,748,644 versus typed check reference 7,770,099 |
| Failed check: Put proceeds at strike | FAIL | 7,563,664 versus typed check reference 7,585,077 |
| Failed check: Put premium future value | FAIL | -136,736 versus typed check reference -136,713 |
| Failed check: Call premium future value | FAIL | -208,628 versus typed check reference -208,593 |
| Failed check: Call net at or below strike | FAIL | -208,628 versus typed check reference -208,593 |
| Failed check: Call net at +5% | FAIL | 176,392 versus typed check reference 177,496 |
| Failed check: Call break-even rate | FAIL | 1.1462 versus typed check reference 1.1493 |
| Failed check: Absolute parity gap | FAIL | 327,806 versus typed check reference 306,351 |
| Failed check: Parity gap percentage | FAIL | 4.23% versus typed check reference 3.94% |
| Failed check: Grid lower endpoint | FAIL | 1.0602 versus typed check reference 1.0631 |
| Failed check: Grid upper endpoint | FAIL | 1.1718 versus typed check reference 1.1751 |
| Check status after my manual fixes | PASS except parity REVIEW | All checks PASS except parity status, which stays REVIEW. The parity status was not changed to make a check pass. |
| Parity status after fixes | REVIEW | Gap USD 327,806 (4.23%) unchanged |

## 9. Structural fixes
| What broke | Why (root cause) | What I changed | Commit |
|---|---|---|---|
| 13 Check-tab checks failed after loading live data. | Each check compared a live value with a figure typed inside its status formula from the Stage 2 placeholders (Stage 3 audit finding 7). | Refreshed the typed figures to the live figures calculated independently before loading: 6,797,184; 7,585,658; 7,748,644; 7,563,664; -136,736; -208,628; -208,628; 176,392; 1.1462; 327,806; 4.23%; 1.0602; 1.1718. No live formula, status rule or input was changed. | [hash] |
| Cover, Notes, Inputs and Check text still said placeholder, 29 Oct 2026, CME Term SOFR and pending Stage 4. | Text written at Stage 3 for placeholder data. | Updated to live sources, as-of date and retrieval time (text cells only). | [hash] |
| Manual-check cells already said 'verified' before I had inspected the workbook. | Written by the build tool. | Reworded as pending sign-off, then signed off by me on 2026-11-20 after inspection. | [hash] |

Documented fixes are not penalised; finding them is the exercise.

## 10. FX Hedging Lab cross-check
| Output | My workbook | FX Lab | Difference | Resolution |
|---|---|---|---|---|
| Forward proceeds | 8,076,450 | 8,076,450 | 0 | Match |
| Money-market proceeds | 7,748,644 | 7,748,644 | 0 | Match (borrowed EUR 6,797,184 and USD today 7,585,658 also match) |
| Put floor (net of premium) | 7,563,664 | 7,566,540 | 2,876 | Convention difference, not an error: the lab deducts the premium at face value (133,860); the workbook carries it to settlement at R_USD (136,736) per spec Section 3. |
| CIP-implied forward | 1.1230 | 1.1230 | 0 | Match |

Lab: https://adamwstauffer.github.io/ai-lms/fxlab.html. Corrected run on 2026-11-20 at 10:00 pm HST, with inputs `FC_AMT` 6,900,000; `S0_in` 1.1160; `F0_in 1.1705`; `R_USD` 4.25 (percent); `R_FC` 2.992 (percent); `T_DAYS 182`; `K_PUT 1.1160`; `PREM_PUT` 0.0194; `K_CALL` 1.1160; `PREM_CALL` 0.0296.

Sensitivity grid: the lab's eleven rows run from S_T 1.0602 to 1.1718 and match the workbook's grid. The unhedged column matches (7,315,380 at -5% to 8,085,420 at +5%). Forward and money-market proceeds are flat. The forward is the best hedge in every row; unhedged is best only at +5%.

Parity gap: the lab shows -USD 327,806 (implied minus quoted forward). The workbook shows +USD 327,806 (forward minus money market). Same size, opposite sign. The lab's red parity message is generic; per Section 5 the gap is a finding about the quoted forward, not a formula error.

First run (recorded because it showed a discrepancy): I entered R_USD and R_FC as decimals (0.0425 and 0.02992). The lab's rate fields are in percent, so it read them as 0.0425% and 0.02992% and returned EUR 6,898,956 borrowed, USD 7,699,235 converted, USD 7,700,890 invested, an implied forward of 1.1161 and a parity gap of -USD 375,560. This was an input-unit error in the lab, not a workbook error. I re-ran with 4.25 and 2.992.

Resolution of the put difference: the workbook follows spec Section 3 (premium carried to settlement at R_USD: 133,860 x 1.021486 = 136,736). The lab deducts 133,860 at face value; the difference is 133,860 x 0.021486 = 2,876. At +1% the lab shows 7,643,544, which is 7,777,404 minus 133,860, which confirms this. I kept the workbook's convention. [Instructor guidance: Not asked.]

## 11. Limitations and assumptions
- R_USD is the FRED DGS6MO bond-equivalent yield (365-day basis) used as published in a 360-day simple-interest model. Converting to ACT/360 gives about 4.19% and widens the parity gap by about USD 2,200.
- Spot sources differ by up to 0.0023 (0.2%). I used the Investing.com close (1.1160); using the ECB fix (1.1172) puts the parity gap at about USD 319,000.
- R_FC (2.992%) comes from aggregator sites, not directly from the EMMI fixing.
- The forward (1.1705), option premiums and invoice amount are scenario-given, not market-sourced. The parity gap depends on the forward, and its status is REVIEW unless a requote changes it.
- Market data for 2026-10-30 was retrieved after the fact (2026-11-20) from public web pages, not a live terminal.
- Model simplifications: simple interest, no bid-ask spreads, fees, credit or counterparty risk, single maturity, European options at the money.
- The put floor follows the spec convention of carrying the premium to settlement at R_USD. The FX Lab deducts the premium at face value, a USD 2,876 difference.
