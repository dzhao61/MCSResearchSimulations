# Professor Meeting Package

Recommended reading order:

1. `BRIEF.md`: two-page research proposal and current evidence.
2. `SLIDES.md`: concise meeting deck.
3. `NEXT_STEPS.md`: decisions requested and work plan.
4. `../ADVERSARIAL_AUDIT.md`: detailed correctness and risk audit.

Run the local demonstration from the simulations root:

```bash
.venv/bin/python DifferentialMI/experiments/run_professor_demo.py
```

The command runs unit tests, repeats the JIDT unit audit and UCI case study,
and collates the saved broad results. It does not rerun the three-minute
288,000-replicate refinement screen.

