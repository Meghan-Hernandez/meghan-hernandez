# US Grain Cooperative — EUR Receivable FX Hedge Model · Technical Specification


| Field | Value |
|------|------|
| **Created by** | Meghan Hernandez |
| **Updated by** | Meghan Hernandez |
| **Date Created** | 2026-11-06 |
| **Date Updated** | 2026-11-13 |
| **Version** | 1.3 |
| **LLM Used** | Copilot SDK in VS Code; Claude |
| **Role** | Treasury Analyst |
| **Audience** | CFO / Director of Treasury |
| **Companion Workbook** | Grain-cooperative hedge build |
| **Stage 2 Brief** | [2026-10-30-grain-cooperative-hedge-brief.md](../../docs/briefs/2026-10-30-grain-cooperative-hedge-brief.md) |

---

## 1. Problem Statement

The U.S. grain cooperative expects to receive EUR 6,900,000 from a Portuguese feed manufacturer in 182 days, around April 29, 2027. The cooperative's reporting and decision currency is USD, so EUR/USD appreciation would increase the realized dollar proceeds while EUR/USD depreciation would reduce them.

The objective is to protect the USD value of the receivable and to quantify what each protection costs or gives up. The decision sits with the CFO, who will choose among a forward, a money-market hedge, and a put option.



## 2. Inputs (Known Variables)

All inputs should be exposed as workbook named ranges on the Inputs tab. Values below are indicative placeholders dated 29 Oct 2026, replaced with sourced Stage 4 values. Market inputs (spot, forward, rates, premia) are the only cells an analyst should adjust for scenario work. Their source and access details belong on the Notes & Assumptions tab.

### 2.1 Core Inputs

| Standardized Name | Description | Unit | Indicative placeholder (29 Oct 2026) | Stage 4 source |
|-------------------|-------------|------|-------------------|----------------|
| `FC_AMT` | Foreign-currency receivable | EUR | 6,900,000 | Invoice to the Portuguese buyer (ERP receivables ledger) |
| `S0_in` | Spot EUR/USD at inception | USD per EUR | 1.1191 | EURUSD spot from one named provider, timestamped |
| `F0_in` | Quoted forward EUR/USD to settlement | USD per EUR | 1.1705 | Bank indicative 182-day forward for the settlement date |
| `R_USD` | USD interest rate over the horizon | Annual rate | 4.216% | CME Term SOFR 6M |
| `R_FC` | EUR interest rate over the horizon | Annual rate | 2.960% | 6-month Euribor fixing (EMMI / ECB) |
| `T_DAYS` | Days to settlement | Days | 182 (April 29, 2027) | Invoice due date minus `VAL_DATE` |
| `VAL_DATE` | Valuation Date | Date | 29 Oct 2026 | Date and time of the Stage 4 data pull |
| `BASIS` | Day-count denominator | Days | 360 (USD / EUR) | CME Term SOFR and EMMI Euribor methodology (both ACT/360) |
| `K_PUT` | EUR put strike | USD per EUR | = `S0_in` (1.1191) | Equal to live S0_in; confirm against the bank’s option quote |
| `K_CALL` | EUR call strike | USD per EUR | = `S0_in` (1.1191) | Equal to live S0_in; confirm against the bank’s option quote |
| `PREM_PUT` | Put premium | USD per EUR | 0.0194 | Bank quote for a 182-day at-the-money EUR put |
| `PREM_CALL` | Call premium | USD per EUR | 0.0296 | Bank quote for a 182-day at-the-money EUR call |


### 2.2 Derived / Intermediate Values

| Name | Description | Source |
|------|-------------|--------|
| `DF_USD` | USD maturity growth factor | `1 + R_USD × T_DAYS / BASIS` |
| `DF_FC` | EUR maturity growth factor | `1 + R_FC × T_DAYS / BASIS` |
| `FV_PREM_PUT` | Settlement-date value of the put premium | `−PREM_PUT × FC_AMT × DF_USD` |
| `FV_PREM_CALL` | Future value of call premium at settlement | `−PREM_CALL × FC_AMT × DF_USD` |
| `S_T_grid` | Settlement-date EUR/USD sensitivity grid | `S0_in` × (1 + k × 0.01), k = −5 to +5. |
| `USD_NO_HEDGE` | USD proceeds under no hedge | `S_T × FC_AMT` |


### 2.3 Workbook Tab Architecture

The workbook uses the following tabs, in this order:

| Tab | Purpose |
|-----|---------|
| Cover | Scenario 12 grain-cooperative (EUR 6,900,000 received in 182 days); author, date, version; data-provenance block naming each input’s source and marking all values indicative placeholders dated 29 Oct 2026 until Stage 4; points to Notes & Assumptions |
| Legend | Explain the workbook's color convention: yellow = inputs, blue = assumptions, green = formulas, gray = outputs, applied on every tab. |
| Inputs | Named-range inputs with unit, indicative value, and Stage 4 source; the only tab where analysts adjust market inputs |
| Forward | Calculate and display the forward hedge's locked USD proceeds from the receivable amount and quoted forward rate. |
| Money Market | Three separate cells: EUR borrowing, USD conversion at spot, USD investment; then the parity comparison with the forward |
| Options | Put and call: premiums in `USD (FV_PREM_PUT, FV_PREM_CALL)`; put proceeds `USD_PUT` and call result `USD_CALL_NE`T as functions of `S_T`; `USD_FLOOR_PUT`. |
| Sensitivity | Show the settlement-rate grid, strategy proceeds, hedge-profit measures, winner labels, summary metrics, and proceeds chart. |
| Check | Every §6.3 check computed live with PASS / REVIEW status |
| Notes & Assumptions | Record assumptions, constraints, and market-data provenance, including each source/provider, access timestamp, and units when Stage 4 populates the inputs. |



## 3. Assumptions & Constraints

- **Quote convention:** EUR/USD is quoted in USD per EUR. A higher rate means EUR appreciation and therefore greater USD proceeds on a receivable.
- **Exposure:** Static full-notional EUR receivable; partial, layered, and dynamic hedging are outside scope.
- **Horizon:** The horizon is the known 182-day exposure; single maturity model. Both money-market legs use the applicable day-count denominator.
- **Day-count basis:** Default `BASIS` = 360 days for USD and EUR. 
- **Forward:** The forward strategy locks the quoted EUR/USD rate on the full receivable and pays no stated upfront premium.
- **Money market:** The cooperative borrows the present value of the EUR receivable, converts the borrowed euros to USD at spot, and invests the USD proceeds to settlement.
- **Option:** The premium is paid upfront and quoted per EUR. The put strategy fixes a USD floor below which exercise can prevent EUR/USD depreciation from reducing proceeds, while preserving exposure to appreciation above the strike.
- **Parity:** The money-market result is compared with the forward result. Parity passes if `USD_PARITY_GAP_PCT` ≤ 0.05% (about USD 3,885); otherwise the status is REVIEW. With the placeholder inputs the gap is USD 306,351 (3.94%), so REVIEW is expected.
- **Option premium:** Paid upfront in USD, quoted per 1 EUR (no contract multiplier). It is expressed as a negative cash flow carried forward at `R_USD` to put it on the same footing as settlement-date proceeds.
- **Cash timing:** The option premium is carried forward at the USD rate so settlement-date proceeds are comparable across strategies.
- **Costs and risk:** Base-case calculations exclude bid-ask spreads, taxes, accounting designation, credit risk, counterparty exposure, and transaction costs.
- **Transaction costs & bid-ask spreads:** Excluded from the base case; a sensitivity candidate.
- **Tax/accounting treatment:** Excluded. Pre-tax cash outcomes only.
- **Sensitivity:** Settlement rates are varied deterministically; probabilities, implied-volatility distributions, and probability weights are not used.
- **Scenario construction:** Future spot `S_T` is varied deterministically across a grid; no probability weights or implied volatility distribution. 
- **Data status:** Market inputs are indicative placeholders dated 29 Oct 2026; source, provider, timestamp and units are recorded when Stage 4 replaces them.



## 4. Calculation Flow
Written in named range pseudocode for a receivable. `S_T` is the spot rate on the date the euros arrive.

### Step 1 — Derived inputs

1. `DF_USD = 1 + R_USD × T_DAYS / BASIS`
2. `DF_FC = 1 + R_FC × T_DAYS / BASIS`
3. `FV_PREM_PUT = −PREM_PUT × FC_AMT × DF_USD`
4. `FV_PREM_CALL = −PREM_CALL × FC_AMT × DF_USD`


### Step 2 — Forward hedge

- Borrowing and investment mechanics do not apply.
- `USD_FWD = FC_AMT × F0_in`
- The result is constant across the settlement-rate grid.

### Step 3 — Money-market hedge

1. Present-value EUR borrowing: `FC_AMT / DF_FC`
2. USD conversion at inception: `(FC_AMT / DF_FC) × S0_in`
3. USD maturity proceeds: `USD_MM = (FC_AMT / DF_FC) × S0_in × DF_USD`
4. At settlement, the receivable repays the EUR borrowing exactly.

**Parity check:** Parity passes if `USD_PARITY_GAP_PCT` ≤ 0.05% (about USD 3,885). Otherwise the status is REVIEW. The absolute and percentage differences should be shown as separate check outputs.

### Step 4 — Option hedge

- Upfront premium: `PREM_PUT × FC_AMT`
- Settlement proceeds for each rate in the grid:
  - `USD_PUT(S_T) = MAX(S_T, K_PUT) × FC_AMT + FV_PREM_PUT`
- The piecewise formula can be restated as `S_T × FC_AMT + MAX(0, (K_PUT − S_T) × FC_AMT) + FV_PREM_PUT`.
- Call (reference leg, not one of the four strategies):
  - Upfront premium: `CALL_PREM_USD = PREM_CALL × FC_AMT`
  - Net result at settlement: `USD_CALL_NET(S_T) = MAX(0, S_T − K_CALL) × FC_AMT + FV_PREM_CALL`
  - Break-even: `BE_CALL = K_CALL − FV_PREM_CALL / FC_AMT`

### Step 5 — Sensitivity table

For each settlement rate in `S_T_grid`:

| Column | Formula |
|--------|---------|
| No hedge | `USD_NO_HEDGE = S_T × FC_AMT` |
| Forward | `USD_FWD`, constant |
| Money market | `USD_MM`, constant |
| EUR put | `USD_PUT(S_T)` |
| Call leg (reference, not charted)| `USD_CALL_NET(S_T)` |
| Forward hedge profit | `USD_FWD − USD_NO_HEDGE` |
| Money-market hedge profit | `USD_MM − USD_NO_HEDGE` |
| Put hedge profit | `USD_PUT(S_T) − USD_NO_HEDGE` |
| Overall winner including no hedge | `ARGMAX` of the four settlement proceeds |
| Best active hedge | `ARGMAX` of forward, money-market, and put proceeds |

### Step 6 — Summary metrics

- `USD_FLOOR_PUT = MIN(USD_PUT)` across `S_T_grid`.
- `USD_BASE_k = USD_k` evaluated at `S_T = S0_in` for each strategy.
- `USD_PARITY_GAP = USD_FWD − USD_MM`.
- `USD_PARITY_GAP_PCT = USD_PARITY_GAP / USD_MM`.



## 5. Outputs

| Output | Description | Format | Purpose |
|--------|-------------|--------|---------|
| Input panel | Named-range inputs, units, and values | Inputs tab | Single source of truth |
| Strategy summary | Forward, money-market, unhedged-at-spot, put-at-spot, and put-floor results | Top of sensitivity tab | Executive comparison |
| Sensitivity table | USD proceeds across settlement EUR/USD rates | Core table | Show rate-state outcomes |
| Hedge-profit columns | Strategy proceeds less no-hedge proceeds | Core table | Isolate incremental hedge value |
| Winner labels | Overall winner and best active hedge by rate | Two label columns | Provide quick-read result |
| Sensitivity chart | USD proceeds versus settlement EUR/USD | Embedded on Sensitivity tab | Show certainty, optionality, and exposure |
| Source and timestamp log | Market-data provenance | Notes & Assumptions tab | Audit Stage 4 population |

### 5.1 Computed Base-Case Values

Calculated from the §2.1 scenario values using simple-interest growth factors and 360-day bases. USD amounts are rounded to the nearest dollar; the scenario inputs remain unvalidated pending Stage 4 sourcing.

| Strategy | USD Proceeds |
|----------|-------------:|
| No hedge at spot | $7,721,790 |
| Forward | $8,076,450 |
| Money market | $7,770,099 |
| EUR put | $7,585,077 |
| Put floor over the sensitivity grid | $7,585,077 |

The put and the floor match because the strike is at the money (`K_PUT` = `S0_in`).

## 6. Model Review — What Worked & What to Improve

### 6.1 What Worked

- The specification separates known scenario facts, market inputs, derived values, calculations, outputs, and audit checks.
- The money-market calculation supplies an independent covered-interest-rate parity benchmark.
- The put formula represents the decision-relevant floor while retaining upside.

### 6.2 Known Risks to Improve During Build

- Confirm that any quoted interest rates and forward points use a consistent 182-day convention.
- Confirm whether the put premium is cash-settled upfront or financed differently.
- Parity threshold (0.05%) is built in; confirm it still flags REVIEW after Stage 4.
- Verify that settlement rates and linked formulas refresh correctly when market inputs are replaced.

### 6.3 Auditability Checklist

- Every core input has the standardized named range in §2.1: all 12 present.
- Every formula uses named ranges, with no bare cell references: 0 bare references.
- `FC_AMT` is EUR 6,900,000 and `T_DAYS` is 182.
- Forward: `USD_FWD`= 8,076,450
- Money Market: 6,798,268 EUR → 7,607,941 USD → 7,770,099.
- Put proceeds at its strike equal `K_PUT × FC_AMT + FV_PREM_PUT`= 7,721,790 − 136,713 = 7,585,077.
- Premium sign: `FV_PREM_PUT` = −136,713; `FV_PREM_CALL` = −208,593.
- Call leg: `USD_CALL_NET` = −208,593 at or below the strike and 177,496 at +5%; `BE_CALL` = 1.1493.
- Parity: gap = USD 306,351 (3.94%), so the status is REVIEW, which is expected with these placeholders.
- Grid: 11 rows, from 1.0631 to 1.1751.
- Input cells are yellow, assumptions blue, formulas green, and outputs gray, matching the Legend tab.
- All market inputs identify source and access timestamp in the Notes & Assumptions tab.



## 7. Sensitivity Plan

- **Grid:** settlement EUR/USD spans `S0_in` × (1 + k × 0.01), k = −5 to +5
- **Strategies plotted:** no hedge, forward, money market, and EUR put.
- **Primary chart:** line chart with settlement EUR/USD on the horizontal axis and USD proceeds on the vertical axis.
- **Expected visual shapes:** the forward and money-market proceeds are horizontal; no hedge is linear through the origin; the put is piecewise-linear with a kink at the strike.
- **Secondary analysis:** show hedge-profit values versus no hedge to identify where each strategy adds or subtracts value.
- **Decision interpretation:** the put can provide the lowest proceeds floor only after the future-value premium is included; this is the trade-off between certainty, premium cost, and retained appreciation.



## 8. Limitations & Next Steps

This specification does not incorporate implied-volatility-based option pricing because premia are scenario inputs rather than Black-Scholes outputs. It also excludes bid-ask spreads, transaction costs, credit and settlement risk, taxes, accounting treatment, partial hedges, portfolio effects, and multiple settlement dates.

Stage 4 will populate sourced market inputs and refresh all formulas. Stage 5 will use the resulting proceeds, parity evidence, sensitivity chart, and premium-adjusted put floor to recommend a hedge to the cooperative's treasury decision-maker. Before finalizing that recommendation, the refreshed inputs must be validated against their stated source and timestamp.



## 9. Writing a Strong Specification

> The specification should function as a handoff document, not a lab notebook.

- All scenario facts and sourced inputs should be explicit.
- Market values, source names, and access timestamps should remain easy to audit.
- Calculation steps should be reproducible from named ranges alone.
- Workbook outputs should be traceable to the formulas in §4 and the validations in §6.

## 10. How This Sets Up Stages 3–5

| What's Written in Stage 2 | What It Enables in Stages 3–5 |
|---------------------------|----------------------------|
| Standardized named ranges with precise definitions | AI uses standardized variable names; no improvisation |
| Step-by-step calculation flow | AI generates correct, auditable hedge formulas |
| Model review and improvement notes (§6.2) | AI builds the *improved* version, not just a replica |
| Explicit output requirements + chart spec | AI produces the exact tables, chart, and memo sections needed |
| Base-case output values (§5.1) | Regression checkpoints for the refined model |


## Appendix A — Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1 | 2026-11-06 | Meghan Hernandez | Initial draft |
| 1.0 | 2026-11-06 | Meghan Hernandez | Reworked the specification for the grain-cooperative EUR receivable scenario. |
| 1.1 | 2026-11-13 | Meghan Hernandez | Added workbook tab architecture and aligned input and data-source documentation locations. |
| 1.2 | 2026-11-13 | Meghan Hernandez | Calculated forward, money-market, and sensitivity-grid put-floor proceeds from the §2.1 scenario inputs. |
| 1.3 | 2026-11-13 | Meghan Hernandez | Added a Stage 4 source column to the §2.1 inputs table, with source placeholders pending validation. |
