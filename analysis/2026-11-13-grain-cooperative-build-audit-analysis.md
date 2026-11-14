# Stage 3 Build Audit: Scenario 12 `grain-cooperative`
**Date:** 2026-11-13 \
**Auditor:** Meghan Hernandez\
**Workbook:** `capabilities/fx-hedging/model.xlsx` (EUR 6,900,000 receivable, 182 days) \
 **Spec:** `capabilities/fx-hedging/spec.md` (v1.4 for build 1, v1.5 for build 2) \
**Build tool:** Copilot in VS Code (agent mode), built from the committed spec. I used Claude to help review it.

## 1. What I did
I audited the workbook twice. Build 1 came from spec v1.4. After I found problems, I fixed the spec (v1.5) and had the tool rebuild it, which is build 2.

For each build I:

- listed the named ranges and the cell each one points to
- looked at every formula for pasted numbers and typed constants
- compared the outputs to the check figures in the spec (§5.1 and §6.3)
- changed inputs on a copy and recalculated it (forward rate 1.10, spot 1.20, grid half-width 3)
- checked the colours against the Legend tab

**Verification status:** I ran the recalculations on copies in LibreOffice. In Excel (Ctrl+Alt+F9) I confirmed: no errors in either build, the parity status for `F0_in` = 1.10, the grid and strikes move when `S0_in` = 1.20. 

## 2. Does build 2 meet the contract?

| Contract item | Result |
|---|---|
| Named ranges (12 core inputs plus `PARITY_TOLERANCE`, `STEP_FRAC`, `GRID_HALF`) | Yes. Each is on the right Inputs cell, 25 names in total. |
| Formulas only | Yes. Typed numbers are only on Inputs and Notes (the assumptions). |
| Cover with provenance | Yes. Placeholders are marked indicative and dated 29 Oct 2026. |
| Legend and colours | Yes. Yellow inputs, blue assumptions, green formulas, gray outputs. |
| Forward, money market (three cells), put and call | Yes, but the money-market steps aren't chained (finding 5). |
| Sensitivity table (±5%, 1% steps) and chart | Yes. 11 formula-driven rows and a four-line chart. |
| Live checks | Yes. One shows REVIEW and I left it that way (see §4). |

## 3. Findings

### Finding 1: The parity test missed negative gaps (build 1), fixed

- **Checked:** the parity status formula, and what it does when the forward is below the money-market result.
- **Found:** the formula `=IF(USD_PARITY_GAP_PCT<=PARITY_TOLERANCE,"PASS","REVIEW")` had no absolute value. When I set `F0_in` to 1.10, the gap was −USD 180,099 (−2.3%) and the status still said **PASS**. This came from my spec wording ("parity passes if `USD_PARITY_GAP_PCT` ≤ 0.05%").
- **What I did:** changed spec §3 to use the absolute value against a named `PARITY_TOLERANCE`, committed it, and rebuilt. Build 2 now shows **REVIEW** for the same test (gap −2.32%).

### Finding 2: The checks compared formulas to themselves (build 1), fixed

- **Checked:** what each check on the Check tab was actually comparing.
- **Found:** `CHECK_GRID_ROW_COUNT` compared a typed 11 to itself. The put-at-strike check compared the put formula to a near copy of itself. None of the checks used the spec figures (8,076,450 and 7,585,077), so they could only fail if a name broke.
- **What I did:** added a rule to spec §6.3 that every check compares a live value to the typed spec figure (±1 USD, ±0.0001 for rates) and counts the real grid rows. In build 2 the checks now fail when inputs change. For example, `S0_in` = 1.20 flags the typed figures, which is what should happen.

### Finding 3: Disguised constants and too many names (build 1), fixed

- **Checked:** the Name Manager and the formulas on the Inputs and Sensitivity tabs.
- **Found:** over 230 names, including `ZERO_VALUE`, `ONE_VALUE`, `GRID_BASE_MULTIPLIER` and eleven `GRID_IDX_*`cells, plus a name for every grid cell. Formulas looked like `=R_USD*T_DAYS/BASIS+ONE_VALUE` instead of the spec's `1 + R_USD × T_DAYS / BASIS`.
- **What I did:** added spec rules that ban named 0 and 1 and limit names to inputs, derived values and headline results. Build 2 has 25 names and plain formulas.

### Finding 4: A possible `#VALUE!` error in the audit cell (build 1), resolved

- **Checked:** I recalculated build 1 and looked for error cells.
- **Found:** `Check!B41` mixed text results ("PASS") into an `AND`, and it returned `#VALUE!` in LibreOffice. Excel's `AND`ignores text, so it might do the same thing there. The stored value said PASS.
- **What I did:** moved the formula-reference checks to the manual block (spec §6.3). Build 2 recalculates with 0 errors. *I haven't confirmed how Excel treats the original cell.*

### Finding 5: The money-market steps aren't chained (build 2), open

- **Checked:** the three cells on the Money Market tab.
- **Found:** step 2 recomputes `(FC_AMT/DF_FC)*S0_in` on its own, and step 3 recomputes the whole chain. `USD_MM`repeats step 3's formula. So a change in one step wouldn't flow into the next. The values are right (6,798,268 → 7,607,941 → 7,770,099).

### Finding 6: The checks re-derive numbers instead of reading the model (build 2), open

- **Checked:** the borrowing, conversion, put-at-strike and call checks.
- **Found:** they recalculate their own formulas on the Check tab (for example `=FC_AMT/DF_FC`) and never read the Money Market or Options cells. If those tabs were broken, the checks would still pass. My naming limit in v1.5 played a part, because those cells weren't named.

### Finding 7: Typed numbers inside the check formulas (build 2), open

- **Checked:** the formulas on the Check tab.
- **Found:** the reference figures and tolerances are typed inside the formulas, for example `ABS(USD_FWD-8076450)<=1`and `COUNT(S_T_grid)=11`.

### Finding 8: `GRID_HALF` can't really be changed (build 2), open

- **Checked:** I set `GRID_HALF` to 3 on a copy.
- **Found:** the 11 rows ran from 1.0855 to 1.1974, which isn't centered on spot, and the grid-endpoint checks failed.

### Finding 9: The manual checks were filled in by the AI (build 2), open

- **Checked:** the three non-numeric items (formula references, colours, source timestamps).
- **Found:** the cells already say "Manually verified" and "Build audit confirms…". The build tool wrote that before I had looked at the workbook. There's no sign-off cell and no overall status cell.

### Finding 10: The grid formulas are hard to read (build 2), open, low priority

- **Checked:** the Sensitivity grid formulas.
- **Found:** they use `ROW()-MIN(ROW(S_T_grid))` with `INDEX`. It works, but it's hard to follow.

## 4. Check figures and the parity result
| Check | Spec figure | Build 2 | Status |
|---|---:|---:|---|
| Forward (`USD_FWD`) | 8,076,450 | 8,076,450 | PASS |
| Money-market EUR borrowing | 6,798,268 | 6,798,268 | PASS |
| Money-market USD conversion | 7,607,941 | 7,607,941 | PASS |
| Money-market USD investment (`USD_MM`) | 7,770,099 | 7,770,099 | PASS |
| Put at strike / floor | 7,585,077 | 7,585,077 | PASS |
| `FV_PREM_PUT` / `FV_PREM_CALL` | −136,713 / −208,593 | −136,713 / −208,593 | PASS |
| Call net at +5% | 177,496 | 177,496 | PASS |
| `BE_CALL` | 1.1493 | 1.1493 | PASS |
| Grid endpoints | 1.0631 / 1.1751 | 1.0631 / 1.1751 | PASS |
| Parity gap | USD 306,351 (3.94%) | USD 306,351 (3.94%) | **REVIEW** |

The parity check shows **REVIEW**, and I did not force it to pass. The quoted forward (1.1705) is about USD 306,351 higher than the money-market result (7,770,099). At spot 1.1191, covered interest parity implies a forward of about 1.1261. So this is a problem with the scenario's forward input, not a formula error.

## 5. What this means for Stage 4

- The typed reference figures on the Check tab are placeholders for 29 Oct 2026. They'll fail when I load live data, so they need to be refreshed at the same time.
- The parity result will only change if a live dealer forward quote replaces 1.1705.
- Open findings 5 to 10 should be fixed in the spec and rebuilt before Stage 4, so the live data doesn't carry them forward.

## 6. Commit log
| Commit | Change |
|---|---|
| [hash] | Build 1: generated workbook from spec v1.4 |
| [hash] | Spec v1.5: absolute-value parity, named assumptions, no named 0/1, checks against typed figures, named-range scope |
| [hash] | Build 2: regenerated workbook from spec v1.5 |
| [hash] | Audit note and prompt log |
