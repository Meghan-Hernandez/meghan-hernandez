# EUR 6.9M receivable: hedge recommendation

**To:** CFO  
**From:** Meghan Hernandez  
**Date:** 2026-11-23  
**Re:** EUR 6.9M receivable: hedge recommendation

> **Decision requested:** Approve a full EUR 6,900,000 forward hedge at 1.1705 only if the bank confirms it as a firm, executable quote; if the bank does not confirm, approve the money-market hedge instead.

## A. Exposure summary

The cooperative expects a EUR 6,900,000 receivable from a Portuguese feed manufacturer on 2027-04-30, 182 days after 2026-10-30. The reporting currency is USD, and the live spot rate is 1.1160 USD per EUR. At spot, the receivable is worth USD 7,700,400, and each 0.01 move in EURUSD changes its proceeds by USD 69,000.

Because the cooperative is fully exposed to EUR depreciation and appreciation, the hedge decision concerns both the protected USD value and the opportunity cost or optionality given up. Unhedged proceeds would range from USD 7,315,380 at 1.0602 to USD 8,085,420 at 1.1718. The active hedge choices differ in certainty, cost, and flexibility.

## B. Hedge outcomes

| Strategy | Locked or floor USD | What you give up or pay |
|---|---:|---|
| Unhedged at spot | 7,700,400 | No hedge premium; retains all EUR/USD gains and losses |
| Forward at 1.1705 | 8,076,450 locked | Gives up EUR appreciation above the forward and no premium is stated |
| Money market | 7,748,644 locked | Gives up EUR appreciation above the money-market outcome; no option premium |
| EUR put, strike 1.1160 | 7,563,664 floor | Premium of USD 133,860 today and USD 136,736 at settlement |
| EUR call, reference | -208,628 at or below strike; 176,392 at +5% | Premium of USD 204,240 today and USD 208,628 at settlement; reference leg only |

The forward locks USD 8,076,450, which is USD 376,050 above unhedged proceeds at spot and USD 327,806 above the money-market hedge. It also exceeds the put floor by USD 512,786.

The money-market hedge locks USD 7,748,644, USD 48,244 above unhedged proceeds at spot. Its mechanics are: borrow EUR 6,797,184, convert it to USD 7,585,658 at spot, and invest that amount to USD 7,748,644 at settlement. The inputs use 4.25% for USD and 2.992% for EUR under ACT/360.

The EUR put has a floor of USD 7,563,664 and net proceeds of USD 7,563,664 at 1.0602 and 1.1160 and USD 7,948,684 at 1.1718. The premium is USD 133,860 today and USD 136,736 at settlement, about 1.8% of the receivable's spot value.

The EUR call is not a hedge for this long-EUR receivable. It netted USD -208,628 at or below 1.1160 and USD 176,392 at 1.1718 after its USD 208,628 settlement-date premium cost. Its break-even rate is 1.1462.

## C. Sensitivity interpretation

If the euro falls, the forward provides the highest locked proceeds of the active hedges. At 1.0602, the put reaches its floor of USD 7,563,664, while the forward remains at USD 8,076,450 and the money-market lock remains at USD 7,748,644. The put therefore gives up certainty below the money-market lock but adds protection beyond the euro-depreciation state.

If the euro rises, the put preserves some appreciation above the 1.1160 strike while the forward and money-market hedge remain locked. The put beats the money-market lock only above 1.1428, 2.4% above spot. The put beats the forward only above 1.1903, 6.7% above spot and outside the +/-5% grid.

Within the grid, the forward is the best active hedge at every tested spot. Unhedged proceeds beat the forward only above 1.1705, 4.9% above spot; in the grid, unhedged wins only at 1.1718, where it produces USD 8,085,420 versus USD 8,076,450 for the forward. The tradeoff is therefore between full settlement certainty, the money-market alternative, and the put's retained upside.

## D. Recommendation

I recommend a forward hedge on the full EUR 6,900,000, but only if the bank confirms 1.1705 as a firm, executable 182-day quote. The forward locks the highest supported proceeds in the grid and removes the settlement-date EUR/USD exposure. It is USD 327,806 above the money-market hedge and exceeds the put floor by USD 512,786, while avoiding the put's premium cost. The recommendation should not proceed on an unconfirmed quote.

The bank's 1.1705 quote and the CIP-implied forward of 1.1230 do not agree. The gap is 0.0475 per EUR, or USD 327,806 on the receivable, equal to 4.23% of money-market proceeds. The quote is about 4.9% above spot, while the interest-rate differential supports only about 0.6% over 182 days. Parity tolerance is 0.05%, about USD 3,874, so the gap is about 85 times the tolerance and the status is REVIEW.

The 1.1705 quote is identical to the scenario's 29 Oct placeholder and implies a spot of about 1.163 at today's rates, so it looks like it was struck at an older, higher spot and not refreshed.

No bank or instructor requote was requested, and no requote answer is available. This does not change the ranking, but it determines execution: approve the forward now only after firm confirmation. Until the quote is firm, act with the money-market hedge, which locks USD 7,748,644. Gap sensitivity does not change the conclusion: using the ECB spot of 1.1172 gives a gap of about USD 319,000, and converting R_USD to ACT/360 widens it by about USD 2,200.

## E. Executive justification

The forward provides the strongest cash-flow stability and budget certainty for the full receivable, but only at the confirmed quote. The money-market hedge provides a locked USD result with no bank-forward reliance and is the appropriate fallback if the forward is not firm. The put provides flexibility, but it costs USD 136,736 at settlement and trails the money-market lock below 1.1428. The call does not add protection for a long-EUR receivable.

The decision should preserve the objective of a predictable 2027-04-30 cash flow without selecting a hedge based on an unverified forward quote. Confirming the quote first controls execution risk while preserving the stated fallback.

## What would change this recommendation

- A requote near 1.1230 would reduce the forward and money-market choice to certainty versus optionality; a firm forward at or near the CIP level could remain appropriate because it would closely match the money-market lock.
- A confirmed EUR-bullish view and willingness to accept or pay for retained upside could support the put, especially where proceeds above 1.1428 matter.
- A liquidity or accounting need to retain full EUR appreciation could favor unhedged exposure, but unhedged proceeds are lower than the forward within the grid until rates above 1.1705.

## Next steps

- Treasury team: request a firm, executable 182-day forward quote from the bank within the next 1 business day.
- Bank treasury: confirm the 1.1705 quote or provide a timestamped requote within the next 1 business day.
- CFO: approve the forward if confirmed, or approve the money-market hedge fallback before 2027-04-30.

The main limits are that the forward and option premiums are scenario-given rather than market-sourced, R_FC comes from aggregator sites rather than directly from EMMI, and spot sources differ by up to 0.0023. The market data was retrieved after the fact on 2026-11-20 for the 2026-10-30 close, and the analysis uses simple interest with no bid-ask spreads, fees, credit or counterparty risk.

**Supporting documents**

- [Stage 5 validation analysis](../../analysis/2026-11-23-grain-cooperative-validation-analysis.md)
- [Market-data memo](../../data/2026-11-19-grain-cooperative-market-data-memo.md)
- [FX hedge workbook](../../capabilities/fx-hedging/model_workbook.xlsx)
