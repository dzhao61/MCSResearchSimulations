# Targeted literature and contribution check

Checked 13 September and extended 15 September 2026 for the active thesis. This is a source-level check
of close methodological predecessors, not proof that no earlier paper contains
the same formula. Search terms included combinations of *categorical mutual
information*, *asymptotic variance*, *two-sample comparison*, *equal mutual
information*, *influence function of variance*, *Welch*, and *Satterthwaite*.
Titles alone were not treated as evidence of a matching hypothesis.

| Original source inspected | What it establishes | Relation to this thesis |
| --- | --- | --- |
| [Moddemeijer (1989), original paper, Section 4 and Equation 4.11](https://ris.utwente.nl/ws/portalfiles/portal/6737096/Moddemeijer89on.pdf) | A leading histogram-MI variance proportional to the variance of pointwise log dependence, and a leading MI bias term. The author explicitly states that the calculations also apply to discrete systems. | Direct predecessor for the **MI estimator's variance** and bias. The thesis must not claim either leading formula as new. The paper does not present the thesis's two-component Welch degrees of freedom. |
| [Moddemeijer (1999), institutional publication record and abstract](https://research.rug.nl/en/publications/a-statistic-to-estimate-the-variance-of-the-histogram-based-mutua/) | Extends estimation of the sampling variance of histogram MI from independent to dependent observation pairs by first estimating the variance of a sample mean under serial dependence. | Important adjacent work now cited in Chapter 2. Its target is \(\operatorname{Var}(\widehat I)\) under dependent observations, not the sampling variance of the plug-in estimate of \(V\), nor a two-sample Welch--Satterthwaite reference. |
| [Brillinger (2004), author's paper, Section 3.2.2](https://www.stat.berkeley.edu/~brill/Papers/MIBJPS.pdf) | Gives the discrete non-null asymptotic MI variance as the probability-weighted variance of the cell log ratio divided by sample size; contrasts the chi-squared independence boundary. | Especially close to the thesis's \(V(P)/n\). It is now cited where that formula is introduced. |
| [Mora and Ruiz-Castillo (2009), author-uploaded working paper](https://www.researchgate.net/publication/4724169_The_statistical_properties_of_the_Mutual_Information_index_of_multigroup_segregation) | Develops inference for an MI-based segregation index and discusses pairwise comparisons across groups and periods. Its basic index is estimated from a flexible multinomial table. | Establishes that **comparing MI-like values** is not a new question. It does not present the expanded Welch degrees of freedom studied here. The accessible full text is author-uploaded; check later versions if making a detailed comparison. |
| [Hutcheson (1970), original article record](https://doi.org/10.1016/0022-5193(70)90124-4) | A t-type comparison of Shannon diversity. | Predecessor for comparing nonlinear information functionals, but not a derivation for this MI variance functional. |
| [Welch (1947), original article](https://academic.oup.com/biomet/article-pdf/34/1-2/28/553093/34-1-2-28.pdf); [Satterthwaite (1946), original record](https://www.jstor.org/stable/3002019) | Combining independently estimated variance contributions and matching a variance estimate to a scaled chi-squared law. | Supplies the architecture, not an exact finite-sample Student theorem for plug-in MI. |
| [Guha and Chothia (2014), original journal page](https://journals.sagepub.com/doi/10.1177/0008068320140103); [authors' working-paper PDF](https://www.cs.bham.ac.uk/~tpc/Papers/JC.pdf) | Uses MI between a pooled observation and its sample label to test whether two **continuous distributions are equal**. | Despite the title, this is not a test of \(I(P)=I(Q)\) for two within-population joint tables. |
| [Marinescu and Balcau (2025), original preprint](https://arxiv.org/abs/2502.17636) | Studies the second-order MI behaviour at one-table independence and its relation to classical tests. | Supports separating the degenerate independence boundary from the positive-MI first-order comparison. It does not establish a two-sample Welch reference. |
| [Miller (1955), bibliographic chapter]; [Paninski (2003), original paper](https://www.cns.nyu.edu/pub/eero/paninski-infoEst-2003.pdf) | Leading entropy bias and wider finite-sample/sparse-support estimation issues. | Supports the fixed-support correction and its limitations, not universal sparse-sample calibration. |
| [Chung and Romano (2013), authors' paper](https://arxiv.org/abs/1304.5939) | Distinguishes exact exchangeability from studentized weak-null permutation inference. | Raw pooled-label permutation is not automatically exact under equal MI with \(P\ne Q\); not every permutation method fails. |
| [Kandasamy et al. (2015), original conference paper](https://papers.nips.cc/paper/5911-nonparametric-von-mises-estimators-for-entropies-divergences-and-mutual-informations) | General influence-function/von Mises tools for information functionals. | Background framework only; the categorical formulas are derived directly in the thesis. |
| [Berrett and Samworth (2021), original paper, Section 3.2](https://arxiv.org/abs/2101.10880) | Uses a four-cell, margin-preserving perturbation as a sparse alternative in a categorical independence simulation. | Establishes provenance for the principal simulation direction. This thesis adapts the direction by prescribing separate margins for \(P\) and \(Q\) and numerically targeting their MI values. |

## Defensible contribution statement

The thesis combines established first-order categorical MI inference with an
explicit observation-level sensitivity of the **plug-in MI variance**, uses
that sensitivity to form two Welch--Satterthwaite component degrees of
freedom, and evaluates the resulting test against Normal Wald across fixed
equal-MI and unequal-MI multinomial populations. This is a contribution in
derivation, construction, and empirical assessment. It is **not** a claim to
have introduced MI variance, two-sample MI comparison, or a new exact
Student law. The searches above found no directly matching published
MI-variance-sensitivity-plus-Welch construction, but absence from these
searches is not a proof of first priority.

## Active citation audit

The table below records every source cited by the active manuscript after the
15 September review. A bibliography entry was accepted only when its metadata
could be reconciled with the original publisher, an author-hosted paper, or an
institutional research record. The claim column states the limited proposition
for which the thesis uses the source.

| Citation key | Metadata checked against | Claim used in the thesis | Disposition |
| --- | --- | --- | --- |
| `shannon1948` | Wiley records for Parts I and II, *Bell System Technical Journal* 27, pp. 379--423 and 623--656 | Entropy and MI foundations. | Retained as one conventional two-part entry; removed the misleading single-part DOI. |
| `miller1955` | Chapter record in Quastler (ed.), *Information Theory in Psychology*, pp. 95--100 | Leading plug-in entropy bias. | Retained. The thesis derives the corresponding MI term rather than attributing an MI theorem directly to Miller. |
| `satterthwaite1946` | JSTOR publisher record, *Biometrics Bulletin* 2(6), pp. 110--114, DOI 10.2307/3002019 | Moment matching for estimated variance components. | Retained. |
| `welch1947` | Oxford Academic original article, *Biometrika* 34(1--2), pp. 28--35 | Unequal-variance mean comparison and Student reference. | Retained. |
| `hutcheson1970` | Elsevier DOI record, *Journal of Theoretical Biology* 29(1), pp. 151--154 | A t-type comparison of Shannon diversity. | Retained as an analogy, not as an MI derivation. |
| `moddemeijer1989` | Original institutional PDF, *Signal Processing* 16(3), pp. 233--248 | Leading histogram-MI bias and non-null variance; explicit applicability to discrete systems. | Retained and credited directly. |
| `moddemeijer1999` | Institutional publication record and abstract, *Signal Processing* 75(1), pp. 51--63 | MI sampling-variance estimation for dependent observation pairs. | Added so adjacent variance-estimation work is not omitted. |
| `paninski2003` | Author-hosted original paper, *Neural Computation* 15(6), pp. 1191--1253 | Fixed-alphabet asymptotics and sparse-sample limitations of plug-in information estimates. | Retained. |
| `brillinger2004` | Author-hosted paper, *Brazilian Journal of Probability and Statistics* 18(2), pp. 163--183 | Discrete non-null MI variance and the chi-squared independence boundary. | Retained; author PDF added to the bibliography. |
| `kandasamy2015` | Official NeurIPS proceedings, pp. 397--405 | Influence-function and von Mises framework for information functionals. | Retained as general background; missing pages added to the bibliography. |
| `mora2009` | Author-uploaded Universidad Carlos III working paper 09-84 | Inference and comparisons for an MI-based segregation index. | Retained with deliberately limited wording. |
| `guha2014` | SAGE journal record and authors' paper, *Calcutta Statistical Association Bulletin* 66(1--2), pp. 39--54 | MI pooled-label test of equality of two continuous distributions. | Retained and explicitly distinguished from equal within-population MI. |
| `marinescu2025` | Original arXiv record 2502.17636 | Second-order MI behaviour at the one-table independence boundary. | Retained as a preprint and labelled as such in the bibliography. |
| `chung2013` | *Annals of Statistics* record and authors' arXiv paper, 41(2), pp. 484--507 | Raw permutation under a strong null versus studentized permutation under weak parameter nulls. | Retained; wording says studentization works for some weak-null comparisons rather than universally. |
| `berrett2021` | Royal Society/Crossref record, *Proceedings of the Royal Society A* 477(2256), article 20210549 | Four-cell margin-preserving sparse alternative for contingency-table simulation. | Added to identify the precedent for the principal population direction and to delimit the thesis's adaptations. |

Fresh exact-title and formula searches on 15 September included `"mutual
information" "Welch-Satterthwaite"`, `equal mutual information two sample
test`, `mutual information variance influence function`, and citation chasing
from Moddemeijer and Brillinger. They identified Moddemeijer (1999), which is
now included, but no paper directly combining the plug-in MI-variance
sensitivity with two Welch component degrees of freedom. This search outcome
supports only the narrow wording above, not a priority claim.

## Remaining bibliographic uncertainty

The accessible Mora--Ruiz-Castillo document is an author-uploaded working
paper and the exact relationship of its later versions to the 2009 version
would need confirmation before making a more detailed comparison. A fully
exhaustive database-level search would still be needed for a claim of first
priority. The active manuscript avoids both claims.

The earlier note that Moddemeijer's continuous-title paper should be excluded
from the discrete bias discussion was too strong: the original article says
the histogram bias and variance calculations apply to discrete systems. The
active draft now credits it directly.
