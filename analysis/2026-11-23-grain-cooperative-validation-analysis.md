# Validation analysis: Scenario 12 grain-cooperative

**Date:** 2026-11-23  
**Author:** Meghan Hernandez  
**LLM tool and model:** Claude AI, Sonnet 5.5  
**Run date and time:** 2026-11-23 at 4:30pm (HST)  
**Documents given to the LLM:** [Technical specification](../capabilities/fx-hedging/spec.md); [Market-data memo](../data/2026-11-19-grain-cooperative-market-data-memo.md).   
**Answers to question 3:** The LLM received only the spec and market-data memo: yes. The run was changed or coached in any way: no.

## 1. Independent LLM run (Part 1)

A fresh Claude AI, Sonnet 5.5 session received only the technical specification and the market-data memo, with no workbook results and no mid-run coaching. The LLM applied the memo's live values rather than the spec's 29 October placeholders and concluded that the cooperative should hedge the full EUR 6,900,000 receivable with the forward only if 1.1705 is confirmed as a firm, executable quote, otherwise falling back to the money-market hedge. See [Appendix A](#appendix-a-raw-llm-output).

## 2. Comparison table (LLM vs workbook)

| Output | LLM result | Workbook result | Difference (LLM minus workbook) | Matches within USD 1 (or 0.0001 for rates)? | Diagnosis |
|---|---:|---:|---:|---|---|
| Unhedged at S_T = 1.0602 | 7,315,380 USD | 7,315,380 USD | 0 USD | Yes | Match |
| Unhedged at S_T = 1.1160 | 7,700,400 USD | 7,700,400 USD | 0 USD | Yes | Match |
| Unhedged at S_T = 1.1718 | 8,085,420 USD | 8,085,420 USD | 0 USD | Yes | Match |
| Forward proceeds | 8,076,450 USD | 8,076,450 USD | 0 USD | Yes | Match |
| Money market step 1: EUR borrowed | 6,797,184 EUR | 6,797,184 EUR (cached 6,797,184.280093905) | -0.280 EUR | Yes | Match |
| Money market step 2: USD at spot | 7,585,658 USD | 7,585,657.656584798 USD | 0.343 USD | Yes | Match |
| Money market step 3: USD invested | 7,748,644 USD | 7,748,643.939845030 USD | 0.060 USD | Yes | Match |
| Put premium | 133,860 USD | 133,860 USD | 0 USD | Yes | Match |
| Put premium future value | -136,736 USD | -136,736.130833333 USD | 0.131 USD | Yes | Match |
| Put net at S_T = 1.0602 | 7,563,664 USD | 7,563,663.869166668 USD | 0.131 USD | Yes | Match |
| Put net at S_T = 1.1160 | 7,563,664 USD | 7,563,663.869166668 USD | 0.131 USD | Yes | Match |
| Put net at S_T = 1.1718 | 7,948,684 USD | 7,948,683.869166668 USD | 0.131 USD | Yes | Match |
| Put floor | 7,563,664 USD | 7,563,663.869166668 USD | 0.131 USD | Yes | Match |
| Call premium | 204,240 USD | 204,240 USD | 0 USD | Yes | Match |
| Call premium future value | -208,628 USD | -208,628.323333333 USD | 0.323 USD | Yes | Match |
| Call net at S_T = 1.0602 | -208,628 USD | -208,628.323333333 USD | 0.323 USD | Yes | Match |
| Call net at S_T = 1.1160 | -208,628 USD | -208,628.323333333 USD | 0.323 USD | Yes | Match |
| Call net at S_T = 1.1718 | 176,392 USD | 176,391.676666667 USD | 0.323 USD | Yes | Match |
| Call break-even rate | 1.1462 USD per EUR | 1.146235988888889 USD per EUR | -0.000035988889 USD per EUR | Yes | Match |
| CIP-implied forward | 1.1230 USD per EUR | 1.1230 USD per EUR (cached 1.1230) | 0.0000 USD per EUR | Yes | Match |
| Parity gap in USD | 327,806 USD | 327,806.060154971 USD | -0.060 USD | Yes | Match |
| Parity gap in % | 4.23% | 4.230495848045% | -0.000495848045 (fraction) | Yes | Match |
| Core named ranges present | 12/12, all sourced values | 12 core inputs plus derived and headline named ranges in workbook | N/A | Structural check reported; workbook supplies the named values | Match |
| No bare cell references / colour legend | Not testable, REVIEW | Workbook check reports no bare formula references and manually verified legend | N/A | N/A | Match |
| FC_AMT and T_DAYS check | 6,900,000 EUR and 182 days; PASS | 6,900,000 EUR and 182 days; PASS | 0 / 0 | Yes | Match |
| Forward check | 8,076,450; PASS | 8,076,450; PASS | 0 USD | Yes | Match |
| Money-market EUR borrowing check | 6,797,184; PASS against live figure | 6,797,184 EUR; PASS | 0 EUR | Yes | Match |
| Money-market USD conversion check | 7,585,658; PASS against live figure | 7,585,658 USD; PASS | 0 USD | Yes | Match |
| Money-market USD investment check | 7,748,644; PASS against live figure | 7,748,644 USD; PASS | 0 USD | Yes | Match |
| Put proceeds at strike check | 7,563,664; PASS against live figure | 7,563,664 USD; PASS | 0 USD | Yes | Match |
| Put premium future value check | -136,736; PASS against live figure | -136,736 USD; PASS | 0 USD | Yes | Match |
| Call premium future value check | -208,628; PASS against live figure | -208,628 USD; PASS | 0 USD | Yes | Match |
| Call net at or below strike check | -208,628; PASS against live figure | -208,628 USD; PASS | 0 USD | Yes | Match |
| Call net at +5% check | 176,392; PASS against live figure | 176,392 USD; PASS | 0 USD | Yes | Match |
| Break-even check | 1.1462; PASS against live figure | 1.1462 USD per EUR; PASS | 0 USD per EUR | Yes | Match |
| Absolute parity gap check | 327,806; PASS against live figure | 327,806 USD; PASS | 0 USD | Yes | Match |
| Parity gap percentage check | 4.23%; PASS against live figure | 4.23%; PASS | 0.00 percentage points | Yes | Match |
| Parity status check | REVIEW | REVIEW | N/A | Status matches | Match |
| Grid row count check | 11; PASS | 11; PASS | 0 | Yes | Match |
| Grid lower endpoint check | 1.0602; PASS against live figure | 1.0602; PASS | 0.0000 | Yes | Match |
| Grid upper endpoint check | 1.1718; PASS against live figure | 1.1718; PASS | 0.0000 | Yes | Match |
| Market inputs carry source and timestamp | REVIEW; memo provides provenance | Workbook manual check is confirmed | N/A | N/A | Match |

No unmatched numerical or status result required a proposed diagnosis.

The ambiguities and assumptions reported by the LLM were:

1. Placeholder versus live inputs: the memo §3A says live values replace the spec §2.1 placeholders dated 29 October 2026.
2. Dates: the spec §2.1 gives 29 October 2026 and 29 April 2027, while memo §2 gives 30 October 2026 and 30 April 2027.
3. Version labels: the spec header identifies v1.3 while the memo identifies spec v1.0 and the change log differs.
4. R_USD source: the spec §2.1 names CME Term SOFR 6M, while memo §3 and §4 select FRED DGS6MO.
5. R_FC source: the spec §2.1 names EMMI/ECB 6-month Euribor, while memo §3 says it used aggregator sources and did not check the primary fixing.
6. Spot: spec §2.1 gives 1.1191; memo §3 records 1.1160 plus ECB and Yahoo cross-checks.
7. Forward quote: spec §2.1 and memo §3 both give 1.1705, while memo §5 says it remains bank-quoted and is not replaced or requoted.
8. Option premia: spec §2.1 and memo §6 treat 0.0194 and 0.0296 as scenario-given assumptions rather than market-repriced quotes.
9. Premium timing: spec §3 and §4 carry the premium forward at R_USD; memo §10 also records the FX Lab's face-value convention as different.
10. Parity tolerance in dollars: spec §3 gives a 0.05% absolute percentage test and memo §5 calculates approximately USD 3,874 from the live money-market proceeds.
11. Structural checks: spec §6.3 requires named ranges and formula/reference checks; memo §8 and §9 discuss workbook checks that cannot be repeated from the documents alone.
12. Check wording: spec §6.3 prohibits checking a formula against a copy of itself; memo §8 and §9 describe refreshing typed references to independently calculated live figures.
13. Out-of-scope items: spec §3 excludes partial hedges, bid-ask spreads, taxes, counterparty risk and probability weights.

## 3. Hand verification

Hand calculations done with a calculator, no spreadsheet. I carried full precision through each calculation and rounded only at the end. 'Reconciled' means my hand result agrees with the workbook value within rounding (USD 1 for dollar amounts, 0.0001 for rates), or the difference is explained.

Live inputs: FC_AMT 6,900,000 EUR; S0_in 1.1160; F0_in 1.1705; R_USD 4.25%; R_FC 2.992%; T_DAYS 182; BASIS 360; K_PUT 1.1160; PREM_PUT 0.0194.

Intermediate factors (show these as a short list above the table):
- T_DAYS / BASIS = 182 / 360 = 0.505556
- R_FC x T_DAYS / BASIS = 0.02992 x 0.505556 = 0.015126, so DF_FC = 1.015126
- R_USD x T_DAYS / BASIS = 0.0425 x 0.505556 = 0.021486, so DF_USD = 1.021486

Table:

| # | Outcome | Arithmetic (named-range notation, live inputs) | My calculator result | Workbook value | Difference (workbook minus mine) | Reconciled? |
|---|---|---|---|---|---|---|
| 1 | Forward proceeds | FC_AMT x F0_in = 6,900,000 x 1.1705 | 8,076,450 USD | 8,076,450 USD | 0 | Y |
| 2 | Money market step 1: borrow EUR | FC_AMT / (1 + R_FC x T_DAYS / BASIS) = 6,900,000 / 1.015126 | 6,797,184.28 EUR | 6,797,184 EUR | -0.28 | Y (rounding) |
| 3 | Money market step 2: convert at spot | borrowed EUR x S0_in = 6,797,184.28 x 1.1160 | 7,585,657.66 USD | 7,585,658 USD | 0.34 | Y (rounding) |
| 4 | Money market step 3: invest USD | USD today x (1 + R_USD x T_DAYS / BASIS) = 7,585,657.66 x 1.021486 | 7,748,643.94 USD | 7,748,644 USD | 0.06 | Y (rounding) |
| 5 | Put premium: paid today, then carried to settlement | PREM_PUT x FC_AMT = 0.0194 x 6,900,000 = 133,860; FV_PREM_PUT = -133,860 x 1.021486 | -136,736.13 USD | -136,736 USD | 0.13 | Y (rounding) |
| 6 | Put net proceeds at S_T = 1.0602 | MAX(S_T, K_PUT) x FC_AMT + FV_PREM_PUT = MAX(1.0602, 1.1160) x 6,900,000 - 136,736.13 = 7,700,400 - 136,736.13 | 7,563,663.87 USD | 7,563,664 USD | 0.13 | Y (rounding) |
| 7 | CIP-implied forward | S0_in x (1 + R_USD x T_DAYS / BASIS) / (1 + R_FC x T_DAYS / BASIS) = 1.1160 x 1.021486 / 1.015126 | 1.122992 USD per EUR | 1.1230 | 0.000008 | Y (rounding) |
| 8 | CIP parity gap in USD | (F0_in - implied forward) x FC_AMT = (1.1705 - 1.122992) x 6,900,000 | 327,806 USD | 327,806 USD | 0 | Y |

Under the table add these notes:
- "Row 6: S_T = 1.0602 is 0.95 x S0_in. It is below K_PUT, so MAX(S_T, K_PUT) returns the strike, the put is exercised, and the proceeds equal the put floor (7,563,664)."
- "Row 8: using the rounded forward 1.1230 instead of 1.122992 gives 327,750, a USD 56 difference. I used the unrounded value."
- "All eight outcomes reconcile to the workbook within rounding; the workbook is consistent with the hand calculations."

## 4. Spec retrospective

**What the LLM got right.** The fresh run reproduced every numeric output within USD 1 (0.0001 on rates): unhedged proceeds, forward, the three money-market steps, put and call premiums and future values, the put floor, the call break-even, the CIP-implied forward and the parity gap. The calculation flow in spec Section 4 (named ranges, ACT/360 simple interest, premium carried at R_USD) was precise enough to rebuild without help. It also reported the check failures against the old spec figures and the passes against the live ones, and left the parity status at REVIEW.

**Independence caveat.** The run was less independent than it looks. The memo I handed over contains expected results: Section 3A lists the live check figures, and Sections 5, 8, 9 and 10 report the forward, money-market proceeds, put floor, parity gap and which checks failed. The LLM referred to these sections. Matching the workbook therefore shows that the spec and memo are consistent with each other, not that the spec alone reproduces the model. A stricter test would give the LLM a memo without expected outputs.

**What it had to guess or reconcile, and the spec gap behind each**
1. **Placeholder versus live inputs, and dates (spec 2.1 vs memo 2 and 3A).** The spec carried 29 Oct 2026 values and a 29 Apr 2027 settlement as if they were the inputs. The LLM had to infer from memo Section 3A that live values override them. Gap: the spec never said its numbers were replaceable or which document wins.
2. **Version labels.** The spec header said v1.3 while its change log ran to 1.5, and the memo cited spec v1.0. Gap: no version control between the documents, so the LLM could not tell whether it had the right spec.
3. **Rate sources.** Spec 2.1 named CME Term SOFR 6M and the EMMI/ECB Euribor; the memo used FRED DGS6MO and aggregator Euribor. Gap: the spec named instruments instead of giving a selection rule (matching tenor, forward-looking, basis documented). It had no rule for a rate on a different day count: DGS6MO is a 365-day bond-equivalent yield, and the spec assumes ACT/360 (about 4.19% on that basis).
4. **Spot and forward.** Spec spot was 1.1191, the memo's was 1.1160, and the forward stayed at 1.1705, about 4.9% above spot. The LLM treated the forward as unconfirmed and recommended it only if the bank confirms a firm quote, otherwise the money-market hedge. It also added a put-call parity cross-check of its own. Gap: the spec had no rule for what a parity break (REVIEW) should do to the recommendation. The LLM's caution was its own judgement.
5. **Premium timing.** Spec Section 3 carries the premium to settlement at R_USD; the memo records that the FX Lab deducts it at face value, a USD 2,876 difference. Gap: the spec stated the convention without a reason or the alternative, so a reader could not tell it was deliberate.
6. **Parity tolerance.** The spec gave 0.05% but not its base. The spec's USD figure (about 3,885) and the memo's (3,874) differ because they use different proceeds. Gap: the base and the dollar equivalent were left unspecified.
7. **Checks.** Spec 6.3 forbids checking a formula against a copy of itself, but the memo describes typed reference figures refreshed after loading live data. Several 6.3 checks (named ranges, colours, bare references, source timestamps) cannot be tested from two documents, so the LLM marked them REVIEW. Gap: the spec put placeholder-based reference figures inside the checks, and 13 failed at Stage 4. It also did not separate checks a reader of the documents can run from checks that need the workbook.
8. **Summary signs.** The LLM's summary showed the premium future values unsigned (136,736 and 208,628) while its arithmetic used negatives. Gap: the spec gave a formula but no output format.

**What v2 of the spec would say differently**
- Mark every Section 2.1 value as a replaceable placeholder, say that the memo wins when the two disagree, and cross-reference version numbers in both documents.
- Replace named instruments with a rate-selection rule, and add a conversion step (or a stated simplification) for rates quoted on a 365-day basis.
- Add a decision rule: if market parity shows REVIEW, say whether the forward can be recommended before a requote, and how to size the gap.
- Define the parity tolerance's base and give a dollar formula.
- State the premium convention, the reason for it, and the face-value alternative with its USD impact.
- Split the checks into figures an outside reader can verify, with reference values generated independently and refreshed at Stage 4, and workbook-inspection checks (names, colours, references, timestamps) that a document reader is not expected to run.
- Fix the output format (signs, units) and keep expected results out of any document handed to an independent run.

## Appendix A: Raw LLM output

Link: [raw output](./2026-11-23-grain-cooperative-llm-raw-output.md)
