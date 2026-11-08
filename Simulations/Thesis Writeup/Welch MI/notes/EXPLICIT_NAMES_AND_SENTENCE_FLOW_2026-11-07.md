# Explicit names and sentence flow, 7 November 2026

The user authorised planning and applying the preceding naming, quantity
clarification and sentence-flow recommendations where they clearly improve
the thesis, followed by verification, a PDF rebuild and the standing push.

## Decisions before editing

1. Name the Wald test and Expanded Welch test explicitly when either is a
   prose subject, object or possessive. Replace comparisons that leave the
   reader to supply a cutoff, rate, power or set of rejections. Retain
   compact figure/table labels, mathematical notation and attributive names
   that already identify an object, such as Wald p-value.
2. Keep the ordinary Welch degrees-of-freedom comparison distinct from the
   ordinary Welch test for population means. The MI comparison substitutes
   degrees of freedom into the shared MI statistic.
3. Apply the seven quantity clarifications: distinguish estimated MI from
   population MI at independence; explain the sign counted in two-sided
   power; name the false-positive rates being compared; identify power beside
   its percentages; explain positive/negative-tail rejections by the sign of
   the estimated difference; distinguish agreement between tests from rates
   near 5%; and name both kinds of positive variance in the limitations.
4. Apply the six sentence-flow changes after checking their full paragraphs:
   separate the introductory comparisons from the variables varied; separate
   the two distributional requirements from their independence condition;
   separate variance trends from their effect on the ratio; distinguish the
   three bias cases in the discussion; separate small-sample calculation
   failures from the large-sample power comparison; and separate simulation
   assessment from the application's illustrative role.
5. Preserve useful short definitions, algebraic steps and causal explanations.
   Do not add sections, benchmarks, results, new notation or new analyses.

These edits remove missing referents or separate distinct explanatory tasks.
They do not target a sentence length or require a general rewrite. The only
change within the protected Section 2.3 is the specifically approved sentence
about a positive plug-in MI estimate when population MI is zero.

## Verification plan

- Compare against the saved source snapshot, checking displayed equations,
  numerical evidence, citations, labels, references, tables and figure sizing.
- Reread all changed paragraphs for meaning, flow and Australian English.
- Review every remaining use of the two short test names in active prose.
- Run paragraph-style checks and the existing thesis-consistency and
  application tests. Check the source diff for whitespace errors.
- Build with `--no-push`, inspect the rendered abstract and changed pages,
  check references and delivery consistency, then use `push_build()`.

## Completed edits and verification

Applied the naming pass, all seven quantity clarifications and all six
sentence-flow changes. Contextual rereading also corrected a comparison
between a p-value and a distribution: Chapter 4 now explicitly compares the
two p-values obtained from their respective reference distributions. The
power-summary sentence in Chapter 6 was divided after the general comparison
so that fuller test names did not crowd its numerical example. The abstract
retains its three paragraphs and useful short explanatory sentences.

- Only ten active manuscript sources changed. Before building, all other
  6,668 snapshotted tracked files were unchanged, including code, experimental
  evidence, figures, historical drafts and presentations.
- All displayed mathematics, table contents, figure commands and sizing,
  citations, labels and cross-references are identical to the source snapshot.
  All numerical values are preserved. Inline mathematics is unchanged apart
  from repeating the existing `1/n` rate when explaining the variance ratio.
- Section 2.3 is otherwise byte-for-byte unchanged after the explicitly
  approved estimate/population sentence substitution.
- Reread the changed passages for scientific meaning, sentence flow, explicit
  referents and Australian English. Remaining short test names are definitions,
  references to the name itself, compact labels or attributive names that
  already identify their objects.
- All five thesis-consistency tests and all five application tests pass.
  Paragraph-style checks and `git diff --check` pass.
- Built with `package_deliverables.py --no-push`. The PDF remains 109 pages,
  with no LaTeX formatting or reference warnings. The abstract remains on
  one page. The bibliography still contains 43 cited works.
- Visually inspected all 52 pages whose text or pagination changed, using
  rendered contact sheets and larger views of the abstract and introductory
  passages. Equations, tables, headings, plots and page margins remain clear.
- The final visual pass rephrased the conclusion's agreement sentence,
  retaining its larger-sample condition and the comparison with 5%. This
  removed a one-word last line and kept the following power-summary paragraph
  together. Rebuilt the delivery files and reviewed the affected conclusion
  pages 86--88 again.
- All 175 source cross-references resolve against 153 unique labels.
- Packaging verified and reused the unchanged experiment supplement. The
  refreshed source archive matches every current source input, and the
  compiled, main and named delivery PDFs match their recorded checksum.

PDF SHA-256:
`cdcb3dd1aa0930460d9d83f4f2bafd340e3fe5c7e9a4d3b6a137ab544c7cf052`.

The verified build is ready for the standing scoped commit-and-push step.
