---
title: "Expected Value of a Mega Millions Ticket in California: A Post-Restructure Analysis"
date: 2025-11-09
draft: false
tags: ["math", "probability", "economics"]
math: true
---

## 1. Introduction

The expected return of a state lottery ticket has been studied since at least Cook and Clotfelter's *Selling Hope* ([1989](https://scholar.google.com/scholar?q=Cook+Clotfelter+Selling+Hope+state+lotteries+1989)), with the consistent finding that nominal expected value is negative, but that under high-rollover jackpots the gap can narrow — or briefly invert — when jackpot-splitting and taxes are ignored. Thaler and Ziemba ([1988](https://doi.org/10.1257/jep.2.2.161)) surveyed parimutuel anomalies of this kind. Cook and Clotfelter ([1993](https://scholar.google.com/scholar?q=Cook+Clotfelter+peculiar+scale+economies+lotto+1993)) documented a convex sales response to jackpot size; Matheson and Grote ([2007](https://scholar.google.com/scholar?q=Matheson+Grote+jackpot+fatigue+lotto)) documented attenuation of that response over time ("jackpot fatigue").

In April 2025 the Mega Millions consortium [restructured the game](https://www.megamillions.com/how-to-play.aspx): the ticket price rose from $2 to $5, the gold-ball urn shrank from 1–25 to 1–24, an automatic prize multiplier replaced the previously optional Megaplier, and prize amounts shifted across all tiers. Prior EV estimates in the literature predate this restructure. This note recomputes the per-ticket expected value of a Mega Millions ticket purchased in California under the new rules, modeling explicitly: (i) jackpot splitting, (ii) the cash-versus-annuity election, and (iii) federal tax liability — noting that California exempts all California State Lottery prizes from state and local tax under [Government Code §8880.68](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=8880.68).

## 2. Game parameters

Each $5 ticket selects five white balls from 1–70 and one gold "Mega" ball from 1–24. The base jackpot probability is therefore \(1 / \big[\binom{70}{5} \cdot 24\big] = 1/290{,}472{,}336\). Published odds and prize amounts for each tier (source: [California Lottery](https://www.calottery.com/en/draw-games/mega-millions#section-content-4-3)):

| Tier \(T\)          | Odds (1 in)   | Base prize \(\pi_T\) |
|---------------------|--------------:|---------------------:|
| 5 of 5 + Mega       |  290,472,336  | jackpot \(J\)        |
| 5 of 5              |   12,629,232  | $1,000,000           |
| 4 of 5 + Mega       |      893,762  | $10,000              |
| 4 of 5              |       38,860  | $500                 |
| 3 of 5 + Mega       |       13,966  | $200                 |
| 3 of 5              |          606  | $10                  |
| 2 of 5 + Mega       |          693  | $10                  |
| 1 of 5 + Mega       |           89  | $7                   |
| Mega only           |           37  | $5                   |
| **Any prize**       |   **1 in 23** |                      |

Each ticket also draws an automatic multiplier \(M \in \{2, 3, 4, 5, 10\}\), applied to every non-jackpot prize, with

$$
\Pr(M = m) = \tfrac{15}{32},\ \tfrac{10}{32},\ \tfrac{4}{32},\ \tfrac{2}{32},\ \tfrac{1}{32} \quad \text{for } m = 2, 3, 4, 5, 10,
$$

giving \(\mathbb{E}[M] = 3.0\).

## 3. Model

For a single ticket purchased independently of the rest of the drawing, expected value is

$$
\mathrm{EV}(J, N) \;=\; \sum_T \Pr(T) \cdot \mathbb{E}\!\left[X_T \mid J, N\right] \;-\; c,
$$

where \(c = \$5\) is the ticket cost, \(J\) is the advertised (30-year graduated annuity) jackpot, \(N\) is the total number of tickets sold for the drawing, and \(X_T\) is the post-tax payout at tier \(T\).

### 3.1 Non-jackpot tiers

Net payout at a non-jackpot tier \(T\) given multiplier \(M\) is \(X_T = (1 - \tau_T)\, M\, \pi_T\). Conditional on tier \(T\), payout is independent of \(N\), so

$$
\mathbb{E}[X_T] \;=\; (1 - \tau_T)\, \mathbb{E}[M]\, \pi_T \;=\; 3\,(1 - \tau_T)\, \pi_T.
$$

### 3.2 Jackpot splitting

A winning ticket shares the jackpot equally with all other tickets in the same drawing that match all six numbers. Conditional on the focal ticket winning, the number of *other* winning tickets is well-approximated by

$$
W \mid \text{focal wins} \;\sim\; \mathrm{Poisson}(\lambda), \qquad \lambda = (N-1)\,p \approx N p,
$$

with \(p = 1/290{,}472{,}336\). The focal ticket's expected jackpot share, given it wins, is then

$$
\mathbb{E}\!\left[\frac{1}{1 + W}\right] \;=\; \sum_{k=0}^{\infty} \frac{1}{k+1} \cdot \frac{\lambda^k e^{-\lambda}}{k!} \;=\; \frac{1 - e^{-\lambda}}{\lambda}.
$$

So the expected pre-tax dollar share is \(J \cdot (1 - e^{-\lambda}) / \lambda\). Ticket sales depend on the jackpot; following Cook and Clotfelter (1993) we treat \(N\) as an increasing function of \(J\) and use the linear approximation

$$
N(J) \;\approx\; N_0 + \beta J,
$$

with baseline \(N_0 = 20{,}000{,}000\) tickets and slope \(\beta = 0.3\) tickets per dollar of advertised jackpot. These are not estimated from a clean published time series — Mega Millions does not release one — and §4 reports sensitivity to both.

### 3.3 Cash vs. annuity

The advertised jackpot \(J\) is the 30-year graduated annuity. The cash option is the present value of that annuity at the rate at which the consortium can purchase the annuity contract, currently about half of the headline number. Let \(J_{\text{cash}} = \alpha J\) with \(\alpha \approx 0.50\). The annuity's internal rate of return is approximately 4%; a winner with personal discount rate above 4% prefers cash. We assume the winner takes cash, giving an effective pre-tax jackpot of \(\alpha J\).

### 3.4 Taxes

Federal income tax treats gambling winnings as ordinary income ([IRS Publication 525](https://www.irs.gov/pub/irs-pdf/p525.pdf)). A jackpot winner is placed in the top federal bracket of 37% on dollars above approximately $626,350 (single filer, 2025 thresholds); at jackpot scale essentially the entire receipt is in that top bracket, so 37% is also the effective rate, not just the marginal one. Two surtaxes that often appear in "what does a top earner really pay" discussions do **not** apply here:

- The 3.8% Net Investment Income Tax does not reach gambling winnings — they are ordinary income, not net investment income under [IRC §1411](https://www.law.cornell.edu/uscode/text/26/1411).
- The 0.9% Additional Medicare Tax does not reach gambling winnings either — it applies only to earned income (wages and self-employment).

California exempts all California State Lottery prizes from state and local tax under [Government Code §8880.68](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=8880.68) ("No state or local taxes shall be imposed upon… Any prize awarded by the lottery"); see also the Franchise Tax Board's [guidance on gambling income](https://www.ftb.ca.gov/file/personal/income-types/gambling.html). California is one of a small number of states with this carve-out, and the exemption is what allows the model to use a federal-only rate. The 24% IRS withholding on lottery winnings above $5,000 ([Form W-2G](https://www.irs.gov/forms-pubs/about-form-w-2-g)) is withholding, not liability; the remaining 13 percentage points are due at filing.

We use effective rates:

- \(\tau_T = 0.37\) at the jackpot and Match-5 tiers (winner is firmly in the top federal bracket).
- \(\tau_T = 0.24\) at the 4+Mega and 4-of-5 tiers (winner plausibly in the 24% bracket after windfall).
- \(\tau_T = 0\) at tiers below the $600 W-2G reporting threshold, as a simplifying assumption. Liability technically applies; sensitivity in §4.

**Headline-to-pocket walkthrough.** For the $415.3M advertised jackpot, ignoring jackpot splitting:

| Step              | Amount             | What eats the gap                   |
|-------------------|-------------------:|-------------------------------------|
| Advertised annuity | $415.3M           | —                                   |
| Cash option        | $207.6M           | Annuity-to-cash discount (\(\alpha = 0.50\)) |
| After federal tax  | $130.8M           | 37% federal                          |
| After CA state tax | $130.8M           | 0% (Government Code §8880.68)       |
| **% of headline**  | **~31.5%**        |                                     |

This matches the popular "they take about two-thirds" intuition, but distributes that loss across two parameters (\(\alpha\) and \(\tau_J\)) rather than rolling it into one inflated tax number. A ticket bought in New York instead — where state and city taxes stack — would face federal 37% + state ~10.9% + NYC ~3.9% ≈ 52% on the cash option, pocketing only ~24% of the advertised number. CA is meaningfully more favorable.

## 4. Results

### 4.1 Point estimate

For the November 9, 2025 drawing with advertised jackpot \(J = \$415.3\text{M}\):

$$
\lambda \;=\; \frac{20\text{M} + 0.3 \cdot 415.3\text{M}}{290.47\text{M}} \;=\; \frac{144.6\text{M}}{290.47\text{M}} \;=\; 0.498.
$$

The expected share of the cash jackpot, given the focal ticket wins, is

$$
\alpha J \cdot \frac{1 - e^{-\lambda}}{\lambda} \;=\; 0.50 \cdot 415.3\text{M} \cdot 0.787 \;=\; \$163.4\text{M}.
$$

After the 37% federal rate, the expected post-tax share is $103.0M. The contribution of the jackpot tier to ticket EV is therefore \(\$103.0\text{M}/290.47\text{M} \approx \$0.354\).

Combining with the non-jackpot tiers (Table 1):

| Tier               | Probability      | Base \(\pi_T\) | After tax & multiplier | EV contribution |
|--------------------|-----------------:|---------------:|-----------------------:|----------------:|
| 5+Mega (jackpot)   |  1/290,472,336   | $103.0M (eff.) | —                     | $0.354          |
| 5 of 5             |  1/12,629,232    | $1,000,000     | $1,890,000             | $0.150          |
| 4+Mega             |  1/893,762       | $10,000        | $22,800                | $0.026          |
| 4                  |  1/38,860        | $500           | $1,140                 | $0.029          |
| 3+Mega             |  1/13,966        | $200           | $600                   | $0.043          |
| 3                  |  1/606           | $10            | $30                    | $0.050          |
| 2+Mega             |  1/693           | $10            | $30                    | $0.043          |
| 1+Mega             |  1/89            | $7             | $21                    | $0.236          |
| Mega only          |  1/37            | $5             | $15                    | $0.405          |
| **Total payout**   |                  |                |                        | **$1.34**       |

Subtracting the $5 ticket cost,

$$
\boxed{\mathrm{EV} \;\approx\; 1.34 - 5.00 \;=\; -\$3.66}.
$$

This is substantially worse than the −$2.41 obtained when jackpot splitting, cash discounting, and the 37% marginal rate are all neglected, and confirms the qualitative pattern reported in earlier literature: ignoring splitting and the cash discount overstates the jackpot tier's contribution by roughly a factor of three.

### 4.2 Break-even analysis

Let \(J^*\) denote the advertised jackpot at which \(\mathrm{EV}(J^*, N(J^*)) = 0\). Under the base parameters, the jackpot-tier contribution saturates as \(J \to \infty\): as \(\lambda\) grows, \((1 - e^{-\lambda})/\lambda \to 1/\lambda = 290.47\text{M}/N(J)\), so

$$
\lim_{J \to \infty} \big[\text{jackpot EV contribution}\big] \;=\; \frac{\alpha\, (1 - \tau_J)}{\beta} \;=\; \frac{0.50 \cdot 0.63}{0.3} \;\approx\; \$1.05.
$$

The asymptotic ticket EV is therefore \(1.05 + 0.98 - 5.00 \approx -\$2.97\). **No finite advertised jackpot makes the ticket fair under the base model.** This is the central result: the demand response to jackpot size is itself the mechanism that prevents +EV — every dollar added to the jackpot draws in tickets faster than it raises the focal ticket's expected share.

If \(\alpha\) is held at 1 (treat the advertised annuity as cash) and \(\tau_J = 0\) (ignore federal tax), the saturation jumps to \(1/\beta \approx \$3.33\), with asymptotic EV \(\approx -\$0.69\) — still negative. Only by zeroing the demand response (\(\beta = 0\)) does the calculation cross zero, at \(J^* \approx \$1.1\text{B}\), recovering the textbook "break-even Powerball" figure that has appeared widely in popular treatments.

### 4.3 Sensitivity to ticket-sales calibration

Varying \(\beta\) at fixed \(J = \$415.3\text{M}\):

| \(\beta\) (tickets/$) | \(N(\$415\text{M})\) | \(\lambda\) | Jackpot EV contrib. | Ticket EV |
|----------------------:|---------------------:|------------:|--------------------:|----------:|
| 0.1                   |  62M                 | 0.214       | $0.413              | −$3.60    |
| 0.2                   | 103M                 | 0.356       | $0.385              | −$3.63    |
| 0.3 (base)            | 145M                 | 0.498       | $0.354              | −$3.66    |
| 0.5                   | 228M                 | 0.785       | $0.297              | −$3.72    |

The sign of EV is insensitive to \(\beta\); the magnitude moves by only $0.12 across this range.

### 4.4 Sensitivity to discount factor \(\alpha\) and tax \(\tau_J\)

| \(\alpha\) | \(\tau_J\) | Jackpot EV contrib. | Ticket EV |
|-----------:|-----------:|--------------------:|----------:|
| 0.50       | 0.37       | $0.354 (base)       | −$3.66    |
| 0.50       | 0.24       | $0.427              | −$3.59    |
| 0.60       | 0.37       | $0.425              | −$3.59    |
| 1.00       | 0.00       | $1.124              | −$2.90    |

The ticket is robustly negative-EV across all plausible combinations.

## 5. Discussion

Negative expected value alone does not explain why people decline a fair bet; here it must explain why people *accept* an unfair one. Three families of model are standard:

- **Friedman and Savage** ([1948](https://doi.org/10.1086/256692)) propose that the utility function is locally convex over a band of large gains. A consumer who is risk-averse over typical income variation can simultaneously prefer a small-probability large-gain gamble to its expected value, if the gamble's payoff lies in the convex region. Whether the Mega Millions cash-option payout (a few hundred million dollars) sits in such a region depends on the consumer's full utility function and is not directly testable.
- **Prospect theory** (Kahneman and Tversky [1979](https://doi.org/10.2307/1914185)) replaces the linear probability in expected utility with a weighting function \(w(p)\) that systematically overweights small probabilities. Under typical parameter estimates, \(w(1/290\text{M})\) is several orders of magnitude larger than \(1/290\text{M}\), easily enough to rationalize a $5 ticket against a fair-bet baseline.
- **Consumption value of hope** (Conlisk [1993](https://doi.org/10.1007/BF01072614)) treats the act of holding a ticket as a consumption good, independent of outcome. Under this view the ticket is not a gamble at all but a purchase whose product is the experience of anticipating a win; the negative EV is the price.

The point estimate of −$3.66 is at the unfavorable end of what a Friedman-Savage convex region can comfortably justify but sits well within prospect-theory-weighted utility under standard \(w(p)\) parameters. The empirical literature on lottery demand has tended toward the prospect-theoretic and consumption-good interpretations rather than the Friedman-Savage one.

## 6. Limitations

The ticket-sales calibration \(N(J)\) is the weakest link in this model. Mega Millions does not publish drawing-level sales as a clean time series, and post-restructure data is thin (the $5-per-ticket regime has been in effect only since April 2025). The qualitative conclusion — no finite jackpot crosses break-even — is robust to plausible variation in \(\beta\), but the specific point estimate of EV at any particular jackpot is uncertain at the level of roughly $0.20. The tax model also assumes a single winner with no offsetting deductions; a winner with large itemized deductions or who structures the receipt through a trust may face a lower effective rate, but not by enough to change the sign of EV.

## References

- California Lottery. "Mega Millions." [calottery.com](https://www.calottery.com/en/draw-games/mega-millions).
- Mega Millions. "How to Play." [megamillions.com](https://www.megamillions.com/how-to-play.aspx).
- Internal Revenue Service. *Publication 525: Taxable and Nontaxable Income.* [irs.gov/pub/irs-pdf/p525.pdf](https://www.irs.gov/pub/irs-pdf/p525.pdf).
- Internal Revenue Service. *Form W-2G: Certain Gambling Winnings.* [irs.gov/forms-pubs/about-form-w-2-g](https://www.irs.gov/forms-pubs/about-form-w-2-g).
- California Government Code §8880.68 (California State Lottery Act of 1984). [leginfo.legislature.ca.gov](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=8880.68).
- California Franchise Tax Board. "Gambling — Personal income types." [ftb.ca.gov](https://www.ftb.ca.gov/file/personal/income-types/gambling.html).
- Internal Revenue Code §1411 (Net Investment Income Tax). [law.cornell.edu](https://www.law.cornell.edu/uscode/text/26/1411).
- Friedman, M., and Savage, L. J. (1948). "The Utility Analysis of Choices Involving Risk." *Journal of Political Economy* 56(4): 279–304. [doi:10.1086/256692](https://doi.org/10.1086/256692).
- Kahneman, D., and Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica* 47(2): 263–291. [doi:10.2307/1914185](https://doi.org/10.2307/1914185).
- Thaler, R. H., and Ziemba, W. T. (1988). "Anomalies: Parimutuel Betting Markets." *Journal of Economic Perspectives* 2(2): 161–174. [doi:10.1257/jep.2.2.161](https://doi.org/10.1257/jep.2.2.161).
- Conlisk, J. (1993). "The Utility of Gambling." *Journal of Risk and Uncertainty* 6(3): 255–275. [doi:10.1007/BF01072614](https://doi.org/10.1007/BF01072614).
- Cook, P. J., and Clotfelter, C. T. (1989). *Selling Hope: State Lotteries in America.* Harvard University Press. [Google Scholar](https://scholar.google.com/scholar?q=Cook+Clotfelter+Selling+Hope+state+lotteries+1989).
- Cook, P. J., and Clotfelter, C. T. (1993). "The Peculiar Scale Economies of Lotto." *American Economic Review* 83(3): 634–643. [Google Scholar](https://scholar.google.com/scholar?q=Cook+Clotfelter+peculiar+scale+economies+lotto+1993).
- Matheson, V. A., and Grote, K. R. (2007). "Examining the 'Halo Effect' in Lotto Games." *Applied Economics Letters.* [Google Scholar](https://scholar.google.com/scholar?q=Matheson+Grote+jackpot+fatigue+lotto).
