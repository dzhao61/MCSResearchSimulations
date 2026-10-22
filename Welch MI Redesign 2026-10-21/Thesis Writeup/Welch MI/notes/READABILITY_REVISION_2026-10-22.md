# Readability revision — 22 October 2026

## Writing guidance reviewed

Reviewed the prior thesis sessions available in the local session history, including the 13 October sentence-cohesion discussion and the 18–19 October clarity reviews. The user's guidance permits longer sentences when they clarify a connection, while rejecting run-on sentences and unnecessary mental load. Earlier comments ask for the purpose of degrees of freedom before their definition, clear topic sentences, and separation of ideas when a paragraph becomes disorganised.

Read the current AGENTS instructions and the writing guidance in WRITING_STYLE_GUIDE.md, EXEMPLAR_REVIEW_NOTES.md, THESIS_REWRITE_PLAN.md, NARRATIVE_REVIEW_2026-10-11.md, REVIEW_BATCH_2026-10-18.md and PROSE_REVIEW_2026-10-21.md. The older guide marks its numerical examples as historical. Its general writing advice is applied together with the newer user instructions, particularly the permission to use varied, connected sentences rather than enforce sentence-length targets.

The relevant principles are:

- Start with the scientific question and known populations, then introduce the quantities the comparison needs.
- Explain what changes and what that change does; define technical terms and symbols before relying on them.
- Give one main idea to a paragraph. Use conjunctions to connect a result to its reason without accumulating independent ideas.
- Avoid repeating a design as an overview, a table, detailed descriptions and another summary. Cut framing that adds neither explanation nor evidence.
- Keep the main evaluation distinct from diagnostic and supporting comparisons. Complete an explanation before changing the population construction or sample allocation.
- Retain intermediate derivation steps where they help the reader. Section 2.3 remains the benchmark; the original core theory is protected.
- Keep captions short, plots readable and the manuscript scientifically self-contained through its appendices.

## Applied changes

Chapter 5 now starts from known population tables, retains the worked construction example, and develops the approximation checks, false-positive comparison and power comparison in that order. Normal Wald, Expanded Welch and the sample-size rule form the main comparison. The fixed moment reference has an explicit diagnostic role. Formal first-order/moment/reference definitions and their algebra are retained in Appendix B. The null-SD power grid notation is also defined there, after its role has been explained in ordinary language.

Chapter 6 groups approximation accuracy, false positives and power as the main sequence. The scaled mean-error sweep, detailed shared-estimator table and complete construction/allocation interpretations are located beside their appendix displays. The main text retains the mechanisms and selected numerical evidence. The nominal and calibrated comparisons remain separate and their different questions are explicit.

Chapter 7 develops implications without repeating the full set of rates and settings. The introduction, conclusion and abstract have been aligned with the simpler hierarchy. The equations and evidence required to reproduce the experiment remain in the manuscript or appendices. No simulation, estimator, population, reference fitting or statistical reporting calculation has changed.

The pre-edit manuscript and PDF are preserved in archive/before_readability_pass_2026-10-22.zip. Chapters 2–4 and Appendix A remain byte-identical. The original workspace and historical working drafts remain unchanged.

## Verification

The final PDF is 104 pages, compared with 109 before this pass. Chapters 5, 6 and 7 occupy 6, 13 and 3 pages respectively (previously 9, 15 and 4): 22 pages rather than 28. Chapter 5 starts on printed page 34 and Chapter 6 on printed page 40. The complete main text is 57 pages, compared with 64 before this pass. Plot dimensions and core derivation sources are unchanged.

All 268 local tests pass (216 experiment, 27 estimator, 17 application, 8 packaging). All 178 extracted-package tests pass (134 experiment, 27 estimator, 17 application). The isolated source archive compiles without LaTeX warnings and has extracted PDF text identical to the delivery PDF. The final archive consistency check passes. Rendered pages were inspected, including the changed contents, main-text sequence, relocated tables and appendix calculations. A repeated closing application paragraph and duplicate p-value display were removed after layout review; the existing Chapter 4 p-value formula is referenced instead.

All 30,042 pre-copy original files again match their SHA-256 hashes. Protected copied theory sources and historical PDFs remain byte-identical. REDESIGN_VERIFICATION.json records the current page count and PDF checksum. The previous independent audit of the unchanged experiment retains its 4,416 reconstructed pairs.
