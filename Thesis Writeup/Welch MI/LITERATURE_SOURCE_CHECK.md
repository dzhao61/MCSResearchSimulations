# Targeted literature and contribution check

Checked 13 September and extended twice on 20 September 2026 for the active thesis. This is a source-level check
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
| [Hutcheson (1970), original article record](https://doi.org/10.1016/0022-5193(70)90124-4); [U.S. EPA technical manual reproduction, p. IV-2-22](https://www.epa.gov/sites/default/files/2014-10/documents/uaa-vol123.pdf) | Compares two Shannon diversity estimates with a Student statistic and assigns component degrees of freedom (n_1,n_2) in the Satterthwaite denominator. | Direct information-theoretic Welch predecessor. The thesis now identifies the (n_i) assignment explicitly and evaluates its MI analogue separately from the (n_i-1) Simple Welch ablation. It is not a derivation for the plug-in MI variance functional. |
| [Welch (1947), original article](https://academic.oup.com/biomet/article-pdf/34/1-2/28/553093/34-1-2-28.pdf); [Satterthwaite (1946), original record](https://www.jstor.org/stable/3002019) | Combining independently estimated variance contributions and matching a variance estimate to a scaled chi-squared law. | Supplies the architecture, not an exact finite-sample Student theorem for plug-in MI. |
| [Guha and Chothia (2014), original journal page](https://journals.sagepub.com/doi/10.1177/0008068320140103); [authors' working-paper PDF](https://www.cs.bham.ac.uk/~tpc/Papers/JC.pdf) | Uses MI between a pooled observation and its sample label to test whether two **continuous distributions are equal**. | Despite the title, this is not a test of \(I(P)=I(Q)\) for two within-population joint tables. |
| [Marinescu and Balcau (2025), original preprint](https://arxiv.org/abs/2502.17636) | Studies the second-order MI behaviour at one-table independence and its relation to classical tests; more generally, its Taylor approximation contains a normal term plus dependent chi-squared terms. | Supports separating the degenerate independence boundary from the positive-MI first-order comparison and motivates the discussion of quadratic effects near that boundary. It does not establish a two-sample Welch reference. |
| [Miller (1955), bibliographic chapter]; [Paninski (2003), original paper](https://www.cns.nyu.edu/pub/eero/paninski-infoEst-2003.pdf) | Leading entropy bias and wider finite-sample/sparse-support estimation issues. | Supports the fixed-support correction and its limitations, not universal sparse-sample calibration. |
| [Chung and Romano (2013), authors' paper](https://arxiv.org/abs/1304.5939) | Distinguishes exact exchangeability from studentized weak-null permutation inference. | Raw pooled-label permutation is not automatically exact under equal MI with \(P\ne Q\); not every permutation method fails. |
| [Kandasamy et al. (2015), original conference paper](https://papers.nips.cc/paper/5911-nonparametric-von-mises-estimators-for-entropies-divergences-and-mutual-informations) | General influence-function/von Mises tools for information functionals. | Background framework only; the categorical formulas are derived directly in the thesis. |
| [Berrett and Samworth (2021), original paper, Section 3(b)](https://arxiv.org/abs/2101.10880) | Uses a four-cell, margin-preserving perturbation as a sparse alternative in a categorical independence simulation. | Establishes provenance for the principal simulation direction. This thesis adapts the direction by prescribing separate margins for \(P\) and \(Q\) and numerically targeting their MI values. |
| [Pan and Wall (2002), publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1002/sim.1142); [Bell and McCaffrey (2002), official paper](https://www150.statcan.gc.ca/n1/pub/12-001-x/2002002/article/9058-eng.pdf); [Kauermann and Carroll (2001), author preprint](https://epub.ub.uni-muenchen.de/1579/1/paper_189.pdf) | Develop degrees-of-freedom or small-sample adjustments that account for variability in sandwich variance estimators. | These are important general precedents for estimating effective degrees of freedom from a non-classical variance estimator. They do not contain the categorical MI sensitivity derived here. |
| [Hutter (2002), original paper](https://arxiv.org/abs/cs/0112019); [Hutter and Zaffalon (2005), original paper](https://arxiv.org/abs/cs/0403025) | Derive moments and approximations for MI under a Dirichlet posterior. | Relevant higher-moment MI work, but Bayesian posterior uncertainty is distinct from the repeated-sampling two-sample test studied here. |
| [Roulston (1999), publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0167278998002693) | Studies finite-sample error and bias in empirical MI. | Supports the need to account for MI estimation error and the sensitivity of support corrections; it does not give the thesis's weak-null test. |
| [Hampel (1974), publisher record](https://www.tandfonline.com/doi/abs/10.1080/01621459.1974.10482962) | Establishes influence curves as derivatives of statistical functionals. | Provides the classical framework for the observation-level sensitivity used in Chapter 4. |
| [van der Vaart (1998), Cambridge record and contents](https://www.cambridge.org/core/books/asymptotic-statistics/A3C7DAD3F7E66A1FA60E9C8FE132EE1D) | Gives the functional delta method and von Mises calculus in Chapter 20. | Primary asymptotic reference for the functional expansion; Kandasamy et al. remain a secondary information-functional application. |
| [Fay and Graubard (2001), publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.0006-341X.2001.01198.x); [Imbens and Kolesar (2016), publisher record](https://doi.org/10.1162/REST_A_00552) | Develop and review small-sample Wald adjustments based on uncertain sandwich variance estimates and effective degrees of freedom. | Further protects the narrow gap claim: variance-estimator adjustments are established generally; the thesis contribution is the MI-specific sensitivity and evaluation. |
| [Drake and Guha (2014), journal record](https://doi.org/10.1080/02664763.2014.899325) | Develops an MI-based (k)-sample test for equality of discrete distributions. | Discrete counterpart to Guha and Chothia's different null; it is not a comparison of two within-population MI values. |
| [Janssen (1997), publisher record](https://doi.org/10.1016/S0167-7152(97)00043-6) | Establishes asymptotically valid studentized permutation tests for heterogeneous non-i.i.d. nulls, including Behrens--Fisher. | Historical weak-null permutation predecessor cited alongside Chung and Romano. |
| [Wilks (1938), original journal record](https://doi.org/10.1214/aoms/1177732360) | Establishes the large-sample likelihood-ratio reference for composite hypotheses. | Primary citation for the likelihood-ratio chi-squared limit in Appendix D. |
| [Barnett and Bossomaier (2012), APS record](https://doi.org/10.1103/PhysRevLett.109.138105); [Bossomaier et al. (2016), Springer record](https://doi.org/10.1007/978-3-319-43222-9) | Connect transfer entropy to a log-likelihood ratio and chi-squared asymptotics, and review the wider transfer-entropy setting. | Adjacent information-theoretic example of the likelihood-ratio principle in Appendix D, not evidence for a two-sample Welch law. |
| [Efron (1979), original journal record](https://doi.org/10.1214/aos/1176344552) | Introduces the bootstrap as a general resampling method. | Standard source for the brief bootstrap discussion; no bootstrap is claimed as part of the final comparison. |

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

The table below records the sources cited by the active manuscript after the
20 September review. A bibliography entry was accepted only when its metadata
could be reconciled with the original publisher, an author-hosted paper, or an
institutional research record. The claim column states the limited proposition
for which the thesis uses the source.

| Citation key | Metadata checked against | Claim used in the thesis | Disposition |
| --- | --- | --- | --- |
| `shannon1948` | Wiley records for Parts I and II, *Bell System Technical Journal* 27, pp. 379--423 and 623--656 | Entropy and MI foundations. | Retained as one conventional two-part entry; removed the misleading single-part DOI. |
| `miller1955` | Chapter record in Quastler (ed.), *Information Theory in Psychology*, pp. 95--100 | Leading plug-in entropy bias. | Retained. The thesis derives the corresponding MI term rather than attributing an MI theorem directly to Miller. |
| `satterthwaite1946` | JSTOR publisher record, *Biometrics Bulletin* 2(6), pp. 110--114, DOI 10.2307/3002019 | Moment matching for estimated variance components. | Retained. |
| `welch1947` | Oxford Academic original article, *Biometrika* 34(1--2), pp. 28--35 | Unequal-variance mean comparison and Student reference. | Retained. |
| `hutcheson1970` | Elsevier DOI record, *Journal of Theoretical Biology* 29(1), pp. 151--154; formula cross-checked against the U.S. EPA technical manual reproduction | Shannon-diversity Student comparison with component df (n_i). | Reclassified as a direct information-theoretic Welch predecessor. Its MI analogue is now a named post-review baseline; it remains distinct from the expanded MI-variance sensitivity. |
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
| `panwall2002` | Wiley record, *Statistics in Medicine* 21(10), pp. 1429--1441 | Approximate degrees of freedom for sandwich variance inference. | Added as the closest general moment-matching analogue. |
| `bell2002` | Official *Survey Methodology* paper, 28(2), pp. 169--181 | Small-sample degrees-of-freedom and variance adjustments. | Added as general precedent, with no claim that it treats MI. |
| `kauermann2001` | Author preprint and *JASA* record, 96(456), pp. 1387--1396 | Variability and coverage consequences of sandwich variance estimation. | Added to qualify the literature-gap claim. |
| `hutter2002`, `hutterzaffalon2005` | Original arXiv papers and proceedings/journal records | Higher posterior moments and approximations for discrete MI. | Added and distinguished from frequentist repeated sampling. |
| `roulston1999` | Elsevier record, *Physica D* 125(3--4), pp. 285--294 | Finite-sample MI error and bias. | Added as adjacent MI error work. |
| `hampel1974` | Taylor & Francis record, *JASA* 69(346), pp. 383--393 | Classical influence-curve framework. | Added beside the modern information-functional citation. |
| `wilson1927`, `brent1973`, `deming1940` | Original article/book records | Binomial score intervals, scalar root finding and iterative proportional fitting. | Added for methods used in the experiment. |
| `vanderVaart1998` | Cambridge University Press book record and Chapter 20 contents | Functional delta method and von Mises calculus. | Added as the primary asymptotic reference for the functional expansion. |
| `fay2001`, `imbens2016` | Wiley and MIT Press publisher records | Small-sample Wald and effective-df adjustments for uncertain robust variance estimators. | Added as further general methodological precedents. |
| `mora2011` | Wiley/SAGE publisher record, *Sociological Methodology* 41(1), pp. 159--194 | Peer-reviewed account of the mutual-information segregation index. | Added for subject context only; the thesis does not claim its test statistic is algebraically identical to Normal Wald. |
| `drake2014` | Taylor & Francis/Crossref record, *Journal of Applied Statistics* 41(9), pp. 2011--2027 | MI-based equality test for discrete distributions. | Added and explicitly distinguished from the equal-MI null. |
| `janssen1997` | Elsevier record, *Statistics & Probability Letters* 36(1), pp. 9--21 | Studentized permutation under heterogeneous weak nulls. | Added as the historical predecessor to the modern weak-null discussion. |
| `efron1979`, `wilks1938` | Project Euclid/IMS records | Bootstrap resampling and the likelihood-ratio chi-squared limit. | Added for methods discussed or used in Appendix D. |
| `barnett2012`, `bossomaier2016` | APS and Springer publisher records | Likelihood-ratio inference for transfer entropy and broader information-flow context. | Added as a closely related information-theoretic likelihood example, with the distinction from equal MI stated explicitly. |

Fresh exact-title and formula searches on 15 September included `"mutual
information" "Welch-Satterthwaite"`, `equal mutual information two sample
test`, `mutual information variance influence function`, and citation chasing
from Moddemeijer and Brillinger. They identified Moddemeijer (1999), which is
now included, but no paper directly combining the plug-in MI-variance
sensitivity with two Welch component degrees of freedom. This search outcome
supports only the narrow wording above, not a priority claim.

## Remaining bibliographic uncertainty

The accessible Mora--Ruiz-Castillo inference document is an author-uploaded
working paper. The peer-reviewed 2011 article is now cited for the index's
substantive context, but the manuscript does not assert that its inferential
statistic is algebraically identical to the thesis's Normal Wald baseline.

The Hutcheson metadata were checked against the original publisher record, but
the paywalled 1970 article text was not accessible in this audit. The (n_i)
degrees-of-freedom formula was cross-checked against independent technical and
textbook reproductions attributed to Hutcheson. This is sufficient to correct
the baseline description, but the audit does not quote an equation number from
the original paper.

A fully exhaustive database-level search would still be needed for a claim of
first priority. The active manuscript avoids that claim.

The earlier note that Moddemeijer's continuous-title paper should be excluded
from the discrete bias discussion was too strong: the original article says
the histogram bias and variance calculations apply to discrete systems. The
active draft now credits it directly.
