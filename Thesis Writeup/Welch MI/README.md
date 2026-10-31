# Main Welch MI thesis deliverable

Latest built PDF: **107 pages**, rebuilt on 31 October 2026 with the new
abstract, Chapters 1–4 prose revision and consistency review, and three
peer research-question labels throughout the thesis. Compilation,
references and paragraph style pass with no LaTeX warnings. The abstract
fits on one page, and 49 changed or boundary pages were rendered and
visually reviewed. No manuscript or formatting change was needed during
the build. The main and named PDFs, source archive and checksums are
current; the unchanged 25,010-file experiment supplement was reused after
inventory, size and timestamp checks.

Included in the requested rebuild, 31 October 2026: the abstract now follows
the current prose guidelines, connecting the problem, first-order
variance-sensitivity contribution, evaluation and empirical judgment in
four paragraphs. It includes the increased conservatism where rejection
is already too low and the dependence of calibrated power gains on the
fitting population. Its claims agree with Chapters 6–7, and source/style
checks and the five existing consistency tests pass. See
`notes/ABSTRACT_GUIDELINES_REWRITE_2026-10-31.md`.

Included in the requested rebuild, 31 October 2026: the Chapters 1–4 prose
revision is complete. It clarifies referents and literature connections,
connects assumptions and substitutions to their consequences, and removes
one repeated explanation of the shared statistic. All literature coverage,
mathematical displays, numerical evidence and citations are retained.
Section 2.3, Figure 2.1's discussion and Section 4.4's worked example and
algorithm are byte-identical to the preceding source. Source consistency,
paragraph style and the five existing thesis-consistency tests pass. The
PDF includes these edits and the subsequent consistency review. See
`notes/CHAPTERS_1_4_PROSE_REVISION_2026-10-31.md`.

The preceding **108-page** PDF was rebuilt on 31 October 2026 with the Chapters 5–7 sentence-construction revision and complete Section 6.4 rewrite. Compilation, references, paragraph style and visual review of the changed pages passed. Table 5.5 was anchored before its interpretation, and removing a repeated application closing sentence avoided a nearly empty page while retaining the final qualification. Typography, numerical evidence, equations and figure assets were unchanged.

Included in the requested rebuild, 31 October 2026: the sentence-construction principles now apply to Chapters 5–7. Chapter 5 connects construction choices, parameter definitions and evaluation steps; Chapter 7 connects findings, mechanisms and limits. Chapter 6 receives a lighter continuity review, retaining already clear definitions, numerical-setting lists and Figure 6.1's three row paragraphs. Earlier chapters, mathematical expressions, displays, numerical evidence, citations and typography are unchanged. Source checks and the five existing numerical-consistency tests pass. The requested rebuild now includes these edits in the main/named PDF and source archive. See `notes/CHAPTERS_5_7_SENTENCE_FLOW_2026-10-31.md`.

Also included in the requested rebuild: Section 6.4 has been rewritten as a complete application narrative, moving from the scientific comparisons and data to estimation, testing and interpretation. It explains the ten month rows through the absence of January and April, introduces the exploratory family before results, keeps the month conclusion with its Holm adjustment, and connects the weekend result to its small estimated degrees of freedom. Both tables, the worked equation and all numerical evidence are preserved. Five thesis-consistency tests and eleven application-data/calculation tests pass. See `notes/SECTION_6_4_FRESH_REWRITE_2026-10-31.md`.

Included in the requested rebuild, 31 October 2026: research questions now use three peer labels—RQ1 for variance-approximation accuracy, RQ2 for false-positive rates under equal MI, and RQ3 for nominal and calibrated power. The Introduction's nested question list is replaced by three questions, and Chapters 5–7 use the matching headings. The design overview now refers to three research questions. Scientific results and calculations are unchanged. The PDF, contents and source archive include the revised labels.

The submitted manuscript contains Appendix A's mathematical derivations and Appendix B's essential experimental details. The exact previous eleven-page C, its table sources and pre-reduction B source are preserved under `WelchSatterthwaiteMI/supplementary_displays/additional_results_2026_10_30/`. Chapter 6 retains local diagnostic support for its explanations; the separate sparse-alternative direction analysis is supplementary only. See `notes/APPENDIX_REDUCTION_2026-10-30.md` for the implementation and checks. The delivery refresh includes the changed experimental supplement, with new checksums.

The earlier 31 October revision connects related sentences and setup passages more naturally, with particular attention to calibration and the application. Its Figure 6.1 discussion, nominal-power panel interpretations, displays, numerical evidence and typography were preserved. The corresponding rebuild included those edits in the main/named PDF and source archive, reusing the verified supplement. See `notes/CHAPTER_6_CONTINUITY_2026-10-31.md`.

The subsequent sentence-level revision on 31 October applies the sample-derived construction and progression principles throughout Chapter 6. It connects detached explanations, comparisons and figure reminders while preserving the three Figure 6.1 row paragraphs, mathematical expressions, displays, values and qualifications. The workspace writing preferences and current Chapter 6 guide now include these principles. The latest requested rebuild includes the revision in the main/named PDF and source archive. The previously verified 25,010-file supplement is reused after confirming its inventory, sizes, exact input timestamps and archive size/timestamp are unchanged. See `notes/CHAPTER_6_SENTENCE_FLOW_2026-10-31.md`.

Source update, 31 October 2026: the examiner is assumed to receive only the submitted PDF. Manuscript directions to the unsubmitted experiment supplement have been removed from Chapters 4–6 and B, together with promises of unreported analyses and a secondary numerical-validation claim whose details were external. The construction comparison now points to the submitted thesis. Internal evidence packages remain preserved for project work. Writing instructions now enforce this reading boundary. The requested 31 October rebuild includes these changes in the main/named PDF and source archive; see `notes/EXAMINER_READING_BOUNDARY_2026-10-31.md`.

Included in the requested 31 October rebuild: the Chapter 6 punctuation review recasts mechanical colon/semicolon joins while retaining useful lists, equations and parallel comparisons. The workspace preferences and chapter guide now explain these principles. All displays, mathematical expressions, values and references are preserved; see `notes/CHAPTER_6_PUNCTUATION_2026-10-31.md`.

For interim review builds, use the lighter checks described in `AGENTS.md`.
The full packaging and independent-build review below remains the final-delivery
procedure. PDF builds still require an explicit request.

Successful direct `latexmk` builds of `main.tex` now run a post-build hook
that refreshes the named PDF in `deliverables/`, source archive, experiment
supplement and checksums. It uses the completed PDF without compiling again,
checks paragraph style and rejects incomplete builds or LaTeX warnings.
The ordinary packaging command suppresses the hook internally to publish
only once. Historical draft builds do not trigger the delivery hook. The
standalone source archive remains independent of this workspace hook.

This is the main thesis folder following promotion on 24 October 2026. The previous baseline, including its code, evidence and thesis, is preserved under the workspace root's `Archive/Welch MI baseline 2026-10-24/`. The current source is `main.tex`; `main.pdf` is generated by `python3 package_deliverables.py`. Run `python3 package_deliverables.py --check` after packaging.

Current delivery files are in `deliverables/`: `Daniel_Zhao_Welch_MI_Thesis.pdf`, `Daniel_Zhao_Welch_MI_Thesis_Source.zip` and `Daniel_Zhao_Welch_MI_Experiment_Supplement.zip`, with checksums. This restores the former main-version delivery structure. Working Draft v3, the previous main files and previous named delivery files are preserved in `archive/before_main_deliverable_2026-10-24/`. Older working drafts remain historical snapshots.

Chapters 5/6 present the 366-setting experiment, independent moment fitting, approximation checks and nominal/calibrated power. The full-deliverable revision adds explicit target definitions, derivation steps for moment combination and uncertainty, interval-bearing tables, readable validity panels and quantitative supporting interpretations. Introduction, abstract, discussion, conclusion and experimental appendices have been reconciled with that evidence. Chapter 2 (including Section 2.3), Chapter 3, Chapter 4 and the core Appendix A derivations are preserved.

The 22 October revision adds a six-case calibration-population sensitivity check, makes mean estimated component df relative to sampling-moment targets visible, and replaces the printed signed correlation with centered-magnitude rank correlation. Calibrated-power claims now state their dependence on the fitting null. Chapter 6 contains a compact sensitivity table; the detailed rates and cross-null validation formerly in Appendix C are now supplementary. The pre-revision source and PDF are saved in `archive/before_calibration_sensitivity_2026-10-22.zip`.

The experiment code and evidence sit under the workspace root's WelchSatterthwaiteMI folder, alongside DifferentialMI and PracticalMIExploration. All source imports and packaging resolve to those promoted main folders. Older paths through `Welch MI Redesign 2026-10-21/` remain available as compatibility links.

The appendix reduction on 23 October shortened the manuscript from 108 to 95 pages. At that stage, Appendix C retained diagnostics, calibration sensitivity, rejection directions and Holm adjustment. The complete previous 19-page Appendix C, its source, plots and tables are preserved under `WelchSatterthwaiteMI/supplementary_displays/full_additional_results/` in the experiment supplement. Appendices A and B were unchanged in that revision.

The 24 October revision brings seven definitions and setting reminders forward in Chapters 5-6 and Appendix C. It distinguishes moment fitting from rejection-threshold calibration and introduces the application selection and signed difference before their results. The manuscript remains 95 pages; the review is recorded in `notes/INFORMATION_ORDER_REVIEW_2026-10-24.md`.

The 25 October rewrite develops Section 5.1 more gradually, explaining the category probabilities, independent and copying choices, fixed population margins, target-MI search and numerical example before comparing the margin regimes. The added exposition brings the manuscript to 96 pages. The population formulas, settings and numerical results are unchanged; see `notes/SECTION_5_1_REWRITE_2026-10-25.md`.

The subsequent Chapter 5 presentation revision adds parameter-grid, calibration-population and performance-measure tables, displays the power grid and sampling-moment target, and lists the three sampling roles. The focus-setting table now includes the fitted null standard deviations. These displays bring the manuscript to 97 pages; population settings, test rules, experiment code and results are unchanged. See `notes/CHAPTER_5_VISUAL_REVISION_2026-10-25.md`.

The 25 October scope reduction removes the sample-size degrees-of-freedom comparator from the main manuscript, figures and tables. The comparison is now Expanded Welch versus Normal Wald, with the fixed moment reference retained as a diagnostic. All existing numerical evidence and the preceding four-rule displays are preserved in the experiment supplement. No simulations or bootstrap samples were rerun. The manuscript remains 97 pages; see `notes/COMPARATOR_SCOPE_REDUCTION_2026-10-25.md`.

The later 25 October exposition revision applies the Section 5.1 approach to Sections 5.2–5.5: it separates the two variance concepts, explains the independently fitted moment reference, works through a concrete power alternative, and introduces calibration as a sequence of fitting and evaluation steps. Section 5.1, all previous equations and tables, the experiment and its results are unchanged. The additional explanation brings the thesis to 98 pages; see `notes/CHAPTER_5_EXPOSITION_REVISION_2026-10-25.md`.

The final Section 5.1 trim on 25 October removes the bias-cancellation preview and the redundant restatement about increasing table size. The construction now ends with the distinction between identical tables and distinct tables with equal MI. Bias cancellation remains explained beside the results and in the discussion. The manuscript remains 98 pages; see `notes/SECTION_5_1_TRIM_2026-10-25.md`.

The Chapter 6 readability revision on 25 October separates findings from plot instructions, distinguishes the variance estimator’s sampling mean from its first-order approximation, and removes repeated explanations of calibration and the power curve at B. The application receives a light prose trim. All numerical evidence, figures, tables, equations and scientific qualifications are retained. The manuscript remains 98 pages; see `notes/CHAPTER_6_READABILITY_REVISION_2026-10-25.md`.

The Chapter 5 heading revision on 25 October labels the population construction as Setup, the approximation checks as RQ1, false-positive and power comparisons as RQ2, and sampling/uncertainty as shared evaluation. Only the five section headings change; body text, numbering and scientific content are unchanged. The manuscript remains 98 pages; see `notes/CHAPTER_5_HEADING_REVISION_2026-10-25.md`.

The subsequent chapter-title revision identifies Chapter 3 as an overview of the shared two-sample MI test and Wald baseline, and Chapter 4 as the detailed derivation of Expanded Welch–Satterthwaite. Only the two chapter titles change; mathematical content and labels remain unchanged. The manuscript remains 98 pages; see `notes/CHAPTERS_3_4_TITLE_REVISION_2026-10-25.md`.

The later Chapter 6 structural revision on 25 October introduces the variance quantities in a compact symbol guide, separates moment accuracy from its consequences for degrees of freedom, and explains the null, power and calibration comparisons before presenting their numerical results. Chapters 5–6 now use simulation repetitions for draws of two count tables and explain paired comparisons as methods evaluated on the same data. Existing symbols are used consistently after definition. All existing displayed equations, figure assets, numerical results and scientific qualifications are retained. The manuscript is now 99 pages; Chapter 6 is 14 pages. See `notes/CHAPTER_6_STRUCTURE_TERMINOLOGY_2026-10-25.md`.

The 26 October results-display revision checks every results subsection in Chapter 6 and Appendix C. The moment plot is split between mean/sampling-variance checks and component degrees of freedom; the calibrated-power graph is moved into Chapter 6. Compact tables accompany the broad-grid ranges, null-grid classification, selected shared-estimator diagnostics, higher-MI null comparisons, association constructions and sample allocations. Appendix C tabulates scaled mean-error ranges and wrong-direction rejection counts. Prose interprets these displays instead of repeating all their values. The thesis is now 102 pages (63 pages of main text), including a second page in the list of tables. All experiment data and existing numerical analyses are unchanged; see `notes/RESULTS_DISPLAY_REVIEW_2026-10-26.md`.

The additional result displays can be regenerated from saved CSV summaries with `python figures_rewrite/focused_results_displays.py`. Its `--results` argument accepts the `WelchSatterthwaiteMI/results/approximation_redesign` folder from the experiment supplement. This command does not run simulations or bootstrap sampling; the generated evidence JSON records the input hashes and table values.

The subsequent Section 6.1.1 revision removes the printed range table, which mixed extrema across settings and interrupted the interpretation of the different-skew graph. Three focused paragraphs now explain the mean ratios, the opposite errors of the population and sample-based sampling-variance predictions, and the remaining mean error at large sample sizes. One 16×16 population provides a consistent numerical walkthrough. The graph and its interpretation fit together on printed page 45; the thesis remains 102 pages. The range-table source is retained but is no longer printed. See `notes/SECTION_6_1_1_GRAPH_INTERPRETATION_2026-10-26.md`.

The later 26 October consistency audit makes all approximation and standard-error ratios use the observed benchmark divided by its prediction. Component degrees of freedom use the simulated moment target divided by the approximation. Related tables, examples, Chapters 5 and 7, Appendices B and C and both figure reporters follow those definitions. Confidence-band endpoints are reciprocated in reverse order; the unchanged CSV fields retain their original orientation. Symbolic ratio legends and ordinary decimal y-axis ticks make the agreement value of one explicit. Power axes now use the correct signed quantity, −Δ/σ₀ (or −Δ for unstandardised displays). The thesis is 103 pages, including 64 pages of main text and 17 pages in Chapter 6. No simulations, fitting batches or bootstrap draws were rerun. See `notes/CHAPTER_6_RATIO_CONSISTENCY_2026-10-26.md`.

The subsequent common-benchmark revision on 26 October supersedes the preceding observed/predicted display convention. Each estimate or approximation is divided by the quantity it is assessed against: population V for the mean coefficient, observed sampling variance for both variance predictions, and the sampling-moment target for both component-df approximations. Shared squared-standard-error diagnostics use the observed variance of the MI difference. Figures 6.1–6.2 use matching vertical scales for P and Q, descriptive axis labels and mathematical line-style legends. Related examples, tables, Chapters 5/7 and Appendices B/C follow these definitions; no simulated data or bootstrap results change. The thesis remains 103 pages. See `notes/COMMON_BENCHMARK_RATIOS_2026-10-26.md`.

The subsequent Section 6.4 reduction on 26 October folds the construction finding into Section 6.2.1 and moves the detailed construction table and sample-allocation analysis to the two-page supplement `WelchSatterthwaiteMI/supplementary_displays/construction_allocation/`. The former standalone section is removed; the application is now Section 6.4 and its results are Table 6.8. The introduction, design summary, discussion and conclusion now follow that narrower main narrative. Scientific construction details remain in Appendix B. The thesis is 102 pages (63 pages of main text; Chapter 6 is 16 pages). No experiment, estimator, simulation output, figure asset or numerical table source changes. See `notes/SECTION_6_4_REDUCTION_2026-10-26.md`.

The later approximation-plot revision on 26 October separates Figure 6.1 into mean, population variance-prediction and average sample variance-prediction rows. Figure 6.2 separates population first-order df and mean estimated df into two rows, with shared scales. The simplified Figure 6.3 keeps four informative df curves and names the near-independence prediction explicitly. Nine full near-independence diagnostic plots, including the median, percentile band and local moment-target prediction, are retained in the experiment supplement. Row references and interpretations in Section 6.1 and Appendix B match the figures. The taller figures bring the manuscript to 103 pages (64 pages of main text; Chapter 6 is 17 pages). No experiments or numerical results change. See `notes/APPROXIMATION_PLOT_SIMPLIFICATION_2026-10-26.md`.

The subsequent Section 6.4 application rewrite on 26 October defines P and Q separately for each predictor, establishes month as the main example and weekend as the weak-association comparison, and presents the MI difference and standard error before the p-values. Table 6.8 now gives corrected MI, the difference, standard error and shared statistic; Table 6.9 gives p-values and Expanded Welch degrees of freedom. The text explains the reference distributions and low weekend df, retaining all numerical results, data construction details and the six-comparison Holm adjustment. The application still occupies two pages and the thesis remains 103 pages. See `notes/SECTION_6_4_APPLICATION_REWRITE_2026-10-26.md`.

The 27 October research-question labels distinguish RQ2.1 (false-positive rates) from RQ2.2 (nominal and calibrated power). The Introduction defines these as the two parts of RQ2; Chapters 5 and 6 use the corresponding labels in their section headings, and the conclusion identifies the answers explicitly. RQ1 remains the approximation question. The manuscript remains 103 pages; no scientific results or experiment settings change.

The 27 October source revision merges the former Chapters 7 and 8 into Chapter 7, Conclusions, in `chapters_rewrite/07_conclusions.tex`. Section 7.1 answers RQ1, RQ2.1 and RQ2.2; Sections 7.2 and 7.3 consolidate limitations and future work. The former sources are preserved in `archive/before_conclusion_merge_2026-10-27.zip`. The Introduction and main entry point follow the new structure. At the user's request, the PDF and delivery packages have not been rebuilt and still show the previous chapter structure; their page counts describe the last build. See `notes/CONCLUSION_MERGE_2026-10-27.md`.

The subsequent 27 October formatting revision uses flush-left body paragraphs throughout, retaining 0.25em paragraph spacing. The shared preamble applies the rule to every chapter and appendix. Packaging checks the policy before compilation; `python3 package_deliverables.py --check-style` runs the source check alone. No PDF or delivery package has been rebuilt for this change.

The 27 October fixed-reference scope reduction removes the third testing rule from the active thesis prose, figures and tables, retaining the RQ1 sampling-moment targets, moment decomposition and focused-power null SDs. Its definition, combination identity, original comparison assets and unchanged numerical evidence are preserved under `WelchSatterthwaiteMI/supplementary_displays/fixed_moment_reference/`. Reporting scripts now regenerate two-test views. No simulation, fitting batch or bootstrap was rerun, and the thesis PDF/delivery archives remain unchanged pending the user's rebuild request. See `notes/FIXED_REFERENCE_SUPPLEMENT_MOVE_2026-10-27.md`.

The subsequent 27 October appendix reduction leaves Appendix A with the two unchanged near-independence derivations. The zero-mean proof moves beside its use in Chapter 4, and the zero-component equation moves beside the validity rule in Appendix B. Appendix B now has eight sections: supplementary-only grids, repeated setup and auxiliary uncertainty derivations move out or are condensed. Exact main settings, root tolerances, inclusion rules, moment-target decomposition and bootstrap pairing remain. Full relocated calculations and supplementary grids are preserved under `WelchSatterthwaiteMI/supplementary_displays/supporting_calculations/`. The PDF and delivery archives are unchanged; see `notes/APPENDICES_A_B_REDUCTION_2026-10-27.md`.

The later 27 October Section 6.4 revision states the month and weekend application questions separately, introduces the visitor groups and outcome before a compact X/Y/P/Q table, and moves the six-comparison Holm adjustment after the two shopping results. Numerical tables and the month-statistic equation are unchanged. The PDF/delivery files remain the previous build. See `notes/SECTION_6_4_QUESTIONS_2026-10-27.md`.

The later 27 October Section 6.3.2 revision explains why power is compared after matching false-positive rates, how calibration changes the decision threshold, and what the achieved null rates and A example show before introducing sensitivity to the fitting population. The new heading is Power after matching false-positive rates. All figure/table blocks and existing numerical findings are unchanged. The PDF and delivery files remain the previous build; see `notes/SECTION_6_3_2_EXPLANATION_2026-10-27.md`.

The 27 October abstract rewrite states the comparison and derivation directly, retains a brief near-independence finding and the shopping application, and summarises false-positive and power results without detailed settings. Calibrated power is explained through matching false-positive rates at a chosen equal-MI population. The PDF and delivery files remain the previous build; see `notes/ABSTRACT_REWRITE_2026-10-27.md`.

The requested 27 October rebuild incorporates all preceding source revisions. The main thesis is now 97 pages, with 64 pages of main text; Chapter 6 is 17 pages, Appendix A five pages, Appendix B nine pages and Appendix C five pages. All paragraphs are flush left. Formatting review shortened three crowded headings, kept the A power walkthrough together, and placed the application null hypothesis within its notation table. Both new supplementary documents are compiled and visually checked. The current named delivery files are refreshed together; earlier statements about deferred builds describe the historical source-edit stages. Future rebuilds still wait for the user's explicit request. See `notes/PDF_REBUILD_FORMAT_REVIEW_2026-10-27.md`.

The subsequent requested build on 27 October incorporates the abstract language pass, the parallel Section 6.2 subsections and the motivation added to Sections 2.3–2.4. The manuscript is 98 pages (65 pages of main text; Chapter 6 is 18 pages). Formatting and references compile without warnings. The direct-build delivery hook refreshes the named delivery set without a second TeX compilation. Future rebuilds still wait for an explicit request.

The requested 28 October mechanism rebuild incorporates the first-reader and display revisions and the evidence-backed explanations of the Chapter 6 curves. The manuscript has 102 pages, including 67 pages of main text; Chapter 6 occupies 19 pages and Appendices A/B/C occupy 5/9/7 pages. Formatting-only table placement changes keep introductions, displays and interpretation in reading order without changing values, font sizes or figure dimensions. The named delivery files and source/supplement archives are refreshed together. Earlier deferred-build statements above describe historical source-edit stages. Future builds continue to wait for an explicit request. See `notes/MECHANISM_PDF_BUILD_2026-10-28.md`.

The subsequent requested panel/table-analysis build on 28 October has 106 pages, including 69 pages of main text. Chapter 6 occupies 21 pages and Appendices A/B/C occupy 5/9/9 pages. Compact spacing around the three application tables and a shorter, equivalent Holm-adjustment paragraph remove a nearly empty trailing page. The fitted-null-SD table now precedes its interpretation. Font sizes, page margins, numerical evidence and figure dimensions are preserved. The named delivery files and archives are refreshed together. See `notes/PANEL_TABLE_PDF_BUILD_2026-10-28.md`.

## Build an extracted source archive

The source archive builds independently with TeX Live and latexmk. From its root, create `build/chapters_rewrite` and `build/appendices_rewrite`, then run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The packaging commands above apply to the full main workspace, where the experiment folders and packaging script are present.
