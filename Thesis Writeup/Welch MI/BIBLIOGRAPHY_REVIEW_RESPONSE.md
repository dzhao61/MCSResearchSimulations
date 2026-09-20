# Response to bibliography and literature assessment

Reviewed 20 September 2026 against publisher records, original or
author-hosted papers where available, the active manuscript and a new paired
simulation baseline. The assessment was substantially fair. Its most important
point was that Hutcheson (1970) is a direct information-theoretic
Welch--Satterthwaite predecessor rather than only a loose analogy.

## Accepted corrections

| Assessment point | Response |
| --- | --- |
| The four-cell alternative was called standard | Corrected to the minimal four-violation alternative used by Berrett and Samworth, Section 3(b). No field-wide standard is claimed. |
| Brillinger's priority was unclear | Chapter 2 now says that Brillinger attributes the non-null variance to Moddemeijer and presents the independence chi-squared limit alongside it. |
| Hutcheson's component df are the sample sizes | Accepted. Chapter 2 now gives the formula, the gap statement distinguishes Hutcheson's (n_i) assignment from ordinary Welch's (n_i-1), and the introduction and baseline chapter use the same history. |
| Hutcheson should be an empirical baseline | Added to the post-review follow-up as `hutcheson_welch`, using exactly the same corrected MI statistic, plug-in standard error, table pairs and fixed populations as the other reference ablations. |
| Influence-function foundations were thin | van der Vaart (1998, Chapter 20) is now cited with Hampel (1974); Kandasamy et al. remain a secondary information-functional application. |
| General Satterthwaite/sandwich precedents were incomplete | Fay and Graubard (2001) and Imbens and Kolesar (2016) were added beside Pan and Wall, Bell and McCaffrey, and Kauermann and Carroll. The novelty claim is limited to the MI-specific sensitivity and its evaluation. |
| Marinescu and Balcau were described too narrowly | Chapter 2 now states their broader normal-plus-quadratic expansion, and Chapter 7 uses it cautiously as a possible explanation for behaviour near independence. |
| The G-test limit needed a primary source | Appendix D now cites Wilks (1938). Barnett and Bossomaier (2012) and Bossomaier et al. (2016) supply a related information-theoretic likelihood-ratio connection. |
| Related discrete and resampling literature was missing | Drake and Guha (2014), Janssen (1997), Mora and Ruiz-Castillo (2011), and Efron (1979) were added with limited, problem-specific wording. |

## Empirical consequence

The historical correction does not change the thesis conclusion. Across the
809 post-review configurations, Hutcheson-style (n_i) and Simple Welch
(n_i-1) produce identical rejection rates in 494 cases. Their mean absolute
difference is 0.00047. The maximum difference is 0.01235 in the deliberately
extreme (5\times5), (n_P=n_Q=5) alternative, where changing a component df
from 4 to 5 is proportionally large. Both fixed-df references remain much
closer to Wald than the complete Expanded Welch correction in the low-MI
regimes that drive the main finding.

The confirmatory run remains frozen. The Hutcheson comparison is explicitly
labelled as a post-review explanatory follow-up and does not replace any of the
3,111 confirmatory configurations.

## Qualified or declined points

- Guha and Chothia's metadata are not uncertain: the official SAGE record
  confirms volume 66, issues 1--2, pages 39--54, and DOI
  `10.1177/0008068320140103`. No correction was needed.
- The audit did not establish that Mora and Ruiz-Castillo's comparison statistic
  is algebraically identical to this thesis's Normal Wald statistic. The thesis
  therefore cites their prior MI-index inference without asserting identity.
- Panzeri--Treves was not added because the final estimator uses the declared
  fixed-support Miller correction and does not implement that alternative.
- Lizier (2014) was not added merely to enlarge the bibliography. The directly
  relevant transfer-entropy likelihood paper and the field book are now cited.
- No first-priority claim is made. The source search narrows the contribution
  but cannot prove that no earlier paper contains the same MI sensitivity.

## Verification boundary

The Hutcheson article metadata were verified from the original Elsevier/PubMed
record. Its full paywalled text was not available in this audit, so the
(n_i)-based formula was cross-checked against independent technical and
textbook reproductions attributed to Hutcheson rather than quoted with an
original equation number. This limitation is recorded in
`LITERATURE_SOURCE_CHECK.md`.
