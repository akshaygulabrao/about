---
title: "Expected Value of a Mega Millions Ticket in CA"
author: "Akshay Gulabrao"
date : "2025 October 27"
bibliography: library.bib
link-citations: true
---

California hosts 3 main lotteries, Mega Millions, PowerBall, and SuperLotto. 

In MegaMillions, each ticket is $5. You pick 5 white balls from 1–70 plus a single Mega Ball from 1–25. In addition, each ticket comes with an integer multiplier of 2,3,4,5, or 10, which multiplies every prize except the jackpot by your multiplier. 

| Matching Numbers           | Odds 1 in |
|----------------------------|-----------|
| All 5 of 5 and Mega        | 290,472,336 |
| All 5 of 5                 | 12,629,232 |
| Any 4 of 5 and Mega        | 893,762 |
| Any 4 of 5                 | 38,860 |
| Any 3 of 5 and Mega        | 13,966 |
| Any 3 of 5                 | 608 |
| Any 2 of 5 and Mega        | 666 |
| Any 1 of 5 and Mega        | 86 |
| None of 5, only Mega       | 36 |
| **Overall odds of winning** | **1 in 23.08** |

| Multiplier | Frequency | Odds 1 in |
|------------|-----------|-----------|
| 2X         | 15 of 32  | 2.14 |
| 3X         | 10 of 32  | 3.20 |
| 4X         | 4 of 32   | 8 |
| 5X         | 2 of 32   | 16 |
| 10X        | 1 of 32   | 32 |

Source: [California Lottery Mega Millions](https://www.calottery.com/en/draw-games/mega-millions#section-content-4-3)

## Prizes
5 numbers + mega: 415,300,000
5 numbers : 3,057,767
4 numbers + mega : 20,520
4 numbers: 363
3 numbers + mega: 216
3 numbers: 10
2 #'s mega: 10
1 # + mega: 6
mega: 5

### Expected value of one ticket

Using the published odds and Megaplier frequencies above, the probability of each outcome is simply the reciprocal of its “1 in” value. For every non-jackpot prize I take the expected payout over the Megaplier distribution (2X 15/32, 3X 10/32, 4X 4/32, 5X 2/32, 10X 1/32). Tax assumptions: prizes under $600 remain untaxed per your instruction, 4-number wins (with or without Mega) follow the standard 24% federal withholding, and the 5-number (Match 5) prize faces a 55% effective tax. The listed jackpot amount is already net of tax, so I use it as-is. The table below shows the conditional expected payout for each match pattern (already averaged over the multiplier where applicable) and its contribution to the ticket’s expected return.

| Outcome            | Odds (1 in …) | Expected payout after tax (USD) | EV contribution (USD) |
|--------------------|--------------:|--------------------------------:|----------------------:|
| 5 numbers + Mega   |     290,472,336 | 415,300,000.00 | 1.43 |
| 5 numbers          |      12,629,232 | 4,127,985.45 | 0.33 |
| 4 numbers + Mega   |         893,762 | 46,785.60 | 0.05 |
| 4 numbers          |          38,860 | 827.64 | 0.02 |
| 3 numbers + Mega   |          13,966 | 541.08 | 0.04 |
| 3 numbers          |             608 | 30.00 | 0.05 |
| 2 numbers + Mega   |             666 | 30.00 | 0.05 |
| 1 number + Mega    |              86 | 18.00 | 0.21 |
| Only Mega          |              36 | 15.00 | 0.42 |

Adding the contributions yields an expected payout of roughly **$2.59** per ticket. After subtracting the $5 ticket price, the expected value of playing Mega Millions under these assumptions is about **−$2.41**.

### Calculation details

The “Game Odds” table (`lottery_EV.md:13-24`) supplies every probability via `P(outcome) = 1 / (listed odds)`. The raw prize amounts are the ones you placed just above (`lottery_EV.md:36-45`). All multipliers use the frequencies provided in the “Multiplier Odds” table (`lottery_EV.md:26-32`), so `P(multiplier) = frequency / 32`. Below is the step-by-step math for each outcome.

#### 5 numbers + Mega
- Probability: `1 / 290,472,336`.
- Net payout (already post-tax in your source list): `$415,300,000`.
- EV contribution: `(1 / 290,472,336) × 415,300,000 = $1.4297`.

#### 5 numbers (Match 5)

| Multiplier | Gross payout (USD) | Tax rate | Net payout (USD) | Weight |
|------------|-------------------:|---------:|-----------------:|-------:|
| 2X | 6,115,534 | 55% | 2,751,990.30 | 15/32 |
| 3X | 9,173,301 | 55% | 4,127,985.45 | 10/32 |
| 4X | 12,231,068 | 55% | 5,503,980.60 | 4/32 |
| 5X | 15,288,835 | 55% | 6,879,975.75 | 2/32 |
| 10X | 30,577,670 | 55% | 13,759,951.50 | 1/32 |

Weighted expected payout: `Σ weight × net = $4,127,985.45`.  
Probability: `1 / 12,629,232`.  
Contribution: `(1 / 12,629,232) × 4,127,985.45 = $0.3269`.

#### 4 numbers + Mega

| Multiplier | Gross payout | Tax rate | Net payout | Weight |
|------------|-------------:|---------:|-----------:|-------:|
| 2X | 41,040 | 24% | 31,190.40 | 15/32 |
| 3X | 61,560 | 24% | 46,785.60 | 10/32 |
| 4X | 82,080 | 24% | 62,380.80 | 4/32 |
| 5X | 102,600 | 24% | 77,976.00 | 2/32 |
| 10X | 205,200 | 24% | 155,952.00 | 1/32 |

Weighted expected payout: `$46,785.60`.  
Probability: `1 / 893,762`.  
Contribution: `$46,785.60 / 893,762 = $0.0523`.

#### 4 numbers

| Multiplier | Gross payout | Tax rate | Net payout | Weight |
|------------|-------------:|---------:|-----------:|-------:|
| 2X | 726 | 24% | 551.76 | 15/32 |
| 3X | 1,089 | 24% | 827.64 | 10/32 |
| 4X | 1,452 | 24% | 1,103.52 | 4/32 |
| 5X | 1,815 | 24% | 1,379.40 | 2/32 |
| 10X | 3,630 | 24% | 2,758.80 | 1/32 |

Weighted expected payout: `$827.64`.  
Probability: `1 / 38,860`.  
Contribution: `$827.64 / 38,860 = $0.0213`.

#### 3 numbers + Mega

| Multiplier | Gross payout | Tax rate | Net payout | Weight |
|------------|-------------:|---------:|-----------:|-------:|
| 2X | 432 | 0% | 432.00 | 15/32 |
| 3X | 648 | 24% | 492.48 | 10/32 |
| 4X | 864 | 24% | 656.64 | 4/32 |
| 5X | 1,080 | 24% | 820.80 | 2/32 |
| 10X | 2,160 | 24% | 1,641.60 | 1/32 |

Weighted expected payout: `$541.08`.  
Probability: `1 / 13,966`.  
Contribution: `$541.08 / 13,966 = $0.0387`.

#### 3 numbers

| Multiplier | Gross payout | Tax | Net payout | Weight |
|------------|-------------:|----:|-----------:|-------:|
| 2X | 20 | 0% | 20.00 | 15/32 |
| 3X | 30 | 0% | 30.00 | 10/32 |
| 4X | 40 | 0% | 40.00 | 4/32 |
| 5X | 50 | 0% | 50.00 | 2/32 |
| 10X | 100 | 0% | 100.00 | 1/32 |

Weighted expected payout: `$30.00`.  
Probability: `1 / 608`.  
Contribution: `$30.00 / 608 = $0.0493`.

#### 2 numbers + Mega

Same multiplier math as “3 numbers,” so the expected payout is `$30.00`.  
Probability: `1 / 666`.  
Contribution: `$30.00 / 666 = $0.0450`.

#### 1 number + Mega

| Multiplier | Gross payout | Tax | Net payout | Weight |
|------------|-------------:|----:|-----------:|-------:|
| 2X | 12 | 0% | 12.00 | 15/32 |
| 3X | 18 | 0% | 18.00 | 10/32 |
| 4X | 24 | 0% | 24.00 | 4/32 |
| 5X | 30 | 0% | 30.00 | 2/32 |
| 10X | 60 | 0% | 60.00 | 1/32 |

Weighted expected payout: `$18.00`.  
Probability: `1 / 86`.  
Contribution: `$18.00 / 86 = $0.2093`.

#### Only Mega

| Multiplier | Gross payout | Tax | Net payout | Weight |
|------------|-------------:|----:|-----------:|-------:|
| 2X | 10 | 0% | 10.00 | 15/32 |
| 3X | 15 | 0% | 15.00 | 10/32 |
| 4X | 20 | 0% | 20.00 | 4/32 |
| 5X | 25 | 0% | 25.00 | 2/32 |
| 10X | 50 | 0% | 50.00 | 1/32 |

Weighted expected payout: `$15.00`.  
Probability: `1 / 36`.  
Contribution: `$15.00 / 36 = $0.4167`.

Summing all nine EV contributions:

```
1.4297 + 0.3269 + 0.0523 + 0.0213 + 0.0387 + 0.0493 + 0.0450 + 0.2093 + 0.4167 ≈ 2.59
```

That total is the expected payout per ticket. Subtracting the $5 ticket cost gives the overall expected value:

```
2.59 − 5.00 ≈ −2.41
```
