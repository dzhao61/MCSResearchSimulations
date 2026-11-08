# Thesis flow revision

Completed on 2 November 2026 after the requested review of conjunctions and
reading flow. The [sample review](SAMPLE_THESIS_FLOW_REVIEW_2026-11-02.md)
records the passages examined in all three reference theses. Their
transferable techniques are now included in the
[research-prose guide](RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md).

## Approach

The review covered the abstract, Chapters 1–7 and both appendices. Revisions
were selective: identify the relationship between ideas, arrange the ideas
in an intelligible order, then choose a connector that states that
relationship without strengthening the evidence. Sentence length and
conjunction frequency were not targets.

## Changes made

| Passage | Revision and purpose |
| --- | --- |
| Abstract, final paragraph | Put the unchanged estimation bias before its possible wrong-direction consequence, with an explicit referent. Retained the three-paragraph structure. |
| Chapter 2, leading MI bias | Put the sparse-sample qualification beside the approximation it limits, before the historical connections. |
| Chapter 3, motivation for Expanded Welch | Move from existing degrees-of-freedom assignments to their limitation for MI, then to the proposed response. |
| Chapter 4, first-order mean | Make the zero-mean linear term's implication for bias explicit. |
| Chapter 5, construction and evaluation | Clarify fixed population margins versus fluctuating sample proportions; state the two-sided power convention with the power definition; connect repetition counts and sample sizes through their different roles. |
| Chapter 6, null diagnostics | Keep the unchanged bias with the excessive rejection it helps explain, retaining the qualification that it is a partial explanation. |
| Chapter 6, power | Keep early irregularities with their interpretation, separate the table-size comparison from the overall curve description, and discuss small-sample calculation failures before recovery at larger samples. |
| Chapter 7, main findings | Connect underestimated means to the degrees-of-freedom consequence, connect apparent association to its role in the sample-based calculation, and order the power discussion from smaller to larger samples. |

Chapter 1 and the appendices required no further edits. Section 2.3,
Section 6.1 and the recently revised Sections 7.2–7.3 were retained
unchanged. Short definitions and useful mathematical steps were preserved.
All edited passages were reread with their surrounding prose after revision.

## Verification

- Compared against a snapshot taken immediately before this flow pass,
  preserving earlier pending work.
- Displayed equations and complete figure/table blocks are byte-identical.
  Inline mathematics, numerical values, citations and references are
  preserved, with some prose reordered.
- Section headings and environment counts are unchanged. The abstract's
  first two paragraphs are unchanged and its three-paragraph structure is
  retained.
- All 18 active TeX files have balanced braces and environments. All
  references to 137 labels and all 46 cited bibliography keys resolve;
  no duplicate labels were found.
- The paragraph-style check and `git diff --check` pass. The regional
  spelling scan found no listed US variants in active authored prose;
  TeX commands were excluded from that scan.
- All three reference PDFs are unchanged. Existing thesis PDFs and delivery
  files retain their previous sizes and modification times.

No PDF was rebuilt and no commit or push was made for this pass. The checks
verify source preservation and consistency; visual verification of a new
PDF remains part of the next requested rebuild.
