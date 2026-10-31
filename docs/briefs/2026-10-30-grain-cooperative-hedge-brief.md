---
type: brief                # "brief" for the Stage 1 executive brief; "memo" for the Stage 5 decision memo
title: "Hedging the EUR 6.9 M Portugese Feed Receivable"
scenario: "grain-cooperative"               # your scenario slug, e.g. beef-processor
date: 2026-10-30
hypothesis: "I expect the quoted 1.1705 forward to beat the hedge by about USD 306K becauses the forward rate is way higher than the 1.1261 interest rates."             # Stage 1 only: "I expect X because Y"
llm_used: "Claude"               # the LLM you used, or "None"
---
---


# Hedging the EUR 6.9 M Portuguese Feed Receivable

**Created by:** Meghan Hernandez  
**Updated by:** Meghan Hernandez  
**Date Created:** 2026-10-29  
**Date Updated:** 2026-10-30  
**Version:** 1.0\
**LLM Used:** Claude

---

## Executive Summary ##
The U.S. grain cooperative will recieve EUR 6,900,000 from a Portuguese feed manufacturer around April 29, 2027 (182 days out). At today's spot of 1.1191 the EUR will roughly equal to about USD 7.72 million. Every cent moved in EURUSD will change our proceeds by USD 69,000.


This project compares the three ways to protect the cash: a forward contract, a money-market hedge, and a put option. I expect the model to show that the quoted forward, 1.1705, will be far above what the current interest rates support, about 1.1261. A recommendation will come later in Stage 5. 

---

## Background & Objectives
The problem is that we invoiced in euros, so we carry the currency risk. With the invoice being 182 days in the future, currency values will fluctuate constantly. If the euro weakens, we will recieve fewer USD. This past year the euro has been experiencing a downward trend agaisnt the USD by about 4% due to all the regional political pressure. The 52 week range has a low consistent at about 1.1130 and the high varies but roughly around 1.2042. The swing could be about USD 590k to 630k.

The primary objective is to decide how to lock in or protect the USD value of the payment. The second objective is the compare the cost and trade offs of each headge in dollars, and test whether the quoted forward and option prices are consistent with the live market data stage. 

---

## Methods
For the first way to protect the cash is a forward contract. It would sell EUR 6.9 M forward at 1.1705. The pro is that it is simple with no upfront costs and it fixes the dollar amount. The con is that it gives up gains if the euro rises and it is a binding contract.

For the second way to protect would be the money market. It would borrow euros today, convert at spot, and invest the dollars. The pro would be that it would be built from our own bank lines. The cone is the use of credit lines and bank spreads add costs.

The last option to protect the money is the put option. It would buy the right to sell EUR at 1.1191 for USD 0.0194 per EUR so about USD 134k. The pro is that it seta a floor and keeps the upside. The con is it costs money upfront and the floor sits below today's spot.

The EUR call (prmium 0.0296) protects someone who must buy euros, so it doesn't hedge a recievable.

The hypotheis is that the forward will lock about USD 8.08M, and the money market hedge about USD 7.77M. THat gap is about USD 360k. THe put will set a floor near 1.099 or USD 7.59M. I expect the gape because the quoted forward is about 4.4 cents above the parity-implied forward of 1.1261.
How I would know I was wrong is if a refreshed forward quote or the stage 4 data brings the forward and money market results within about USD 20K of each other.


---

## Limitations & Next Steps
**Next Steps**\
Stage 2: Draft and design the workbook for the model specification\
Stage 3: AI-Assisted build and audit the workbook\
Stage 4: Market data and population with live inputs\
Stage 5: Validate and the decision memo

