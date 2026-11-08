"""Design coverage, reuse and statistical evidence checks for balanced RQ2."""
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy.stats import binomtest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"experiments"))
import balanced_null_study as study


class BalancedNullTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.configs,cls.pops,cls.arrays=study.build_design()

    def test_balanced_grid_and_original_ids(self):
        grid={(c["k"],c["profile"],c["n_p"],c["n_q"]) for c in study.base.build_design()[0]}
        for common in study.COMMON_MI:
            subset=[c for c in self.configs if c["common_mi"]==common]
            self.assertEqual(len(subset),120)
            self.assertEqual({(c["k"],c["profile"],c["n_p"],c["n_q"]) for c in subset},grid)
            self.assertTrue(all(c["mi_p"]==c["mi_q"]==common and c["delta"]==0 for c in subset))
        self.assertEqual({c["configuration_id"] for c in self.configs if c["record_source"]=="original"},study.original_ids())
        self.assertEqual(len({c["configuration_id"] for c in self.configs}),360)

    def test_population_targets_and_distinct_equal_mi_tables(self):
        for pop in self.pops.values():
            for side in "pq":
                p=np.array(pop["probability_"+side])
                self.assertTrue((p>0).all())
                np.testing.assert_allclose(p.sum(0),pop["margin_"+side],atol=1e-12)
                np.testing.assert_allclose(p.sum(1),pop["margin_"+side],atol=1e-12)
                self.assertAlmostEqual(pop["achieved_mi_"+side],pop["mi_"+side],places=10)
            p,q=self.arrays[pop["pair_id"]]
            if pop["profile"]=="different_skew":self.assertFalse(np.array_equal(p,q))
            else:np.testing.assert_array_equal(p,q)

    def test_independent_streams_for_the_two_new_levels(self):
        subset=[c for c in self.configs if c["k"]==4 and c["profile"]=="uniform" and
                c["n_p"]==1000 and c["record_source"]=="extension"]
        self.assertEqual(len({study.base.seed_for(c["configuration_id"],0,side)
                             for c in subset for side in "pq"}),4)

    def test_complete_results_and_wilson_intervals(self):
        if not (study.OUTPUT/"combined_audit.json").exists():self.skipTest("Run not complete")
        audit=json.loads((study.OUTPUT/"combined_audit.json").read_text())
        self.assertTrue(audit["passed"]);self.assertEqual(audit["pairs"],36000000)
        self.assertEqual(audit["new_pairs"],24000000);self.assertEqual(audit["reused_pairs"],12000000)
        self.assertEqual(audit["independently_reconstructed_pairs"],2880)
        rates=pd.read_csv(study.OUTPUT/"combined_rates.csv")
        rates=rates[rates.denominator.eq("all")]
        self.assertEqual(len(rates),720)
        for row in rates.itertuples():
            ci=binomtest(row.rejections,row.replicates).proportion_ci(method="wilson")
            self.assertAlmostEqual(row.rejection_low,ci.low,places=12)
            self.assertAlmostEqual(row.rejection_high,ci.high,places=12)
        old=pd.read_csv(study.original.OUTPUT/"rates.csv")
        old=old[old.denominator.eq("all")].set_index(["configuration_id","method"])
        for row in rates[rates.record_source.eq("original")].itertuples():
            previous=old.loc[(row.configuration_id,{"normal_wald":"wald","expanded_welch":"expanded"}[row.method])]
            self.assertEqual(row.rejections,previous.rejected)
            self.assertEqual(row.valid_replicates,previous.valid_count)
        paired=pd.read_csv(study.OUTPUT/"combined_paired.csv")
        paired=paired[paired.denominator.eq("all")]
        self.assertTrue(paired.only_expanded.eq(0).all())
        np.testing.assert_array_equal(paired.only_wald+paired.only_expanded+paired.both_reject+paired.neither_reject,100000)

    def test_display_coverage_and_diagnostic_selection(self):
        path=study.base.ROOT.parent/"Thesis Writeup/Welch MI/figures_rewrite/balanced_null_evidence.json"
        if not path.exists():self.skipTest("Figures not rendered")
        evidence=json.loads(path.read_text());all_ids=[]
        configs={c["configuration_id"]:c for c in self.configs}
        for data in evidence["figures"].values():
            ids=data["configurations"];self.assertEqual(len(ids),120)
            self.assertEqual({configs[key]["common_mi"] for key in ids},set(study.COMMON_MI))
            all_ids.extend(ids)
        self.assertEqual(len(all_ids),360);self.assertEqual(set(all_ids),set(configs))
        selected=[configs[key] for key in evidence["diagnostic_cases"]]
        self.assertEqual([(c["k"],c["profile"],c["n_p"]) for c in selected],list(study.DIAGNOSTIC_CASES))
        self.assertTrue(all(c["common_mi"]==.02 for c in selected))

    def test_manuscript_and_table_values_match_evidence(self):
        if not (study.OUTPUT/"combined_audit.json").exists():self.skipTest("Run not complete")
        thesis=study.base.ROOT.parent/"Thesis Writeup/Welch MI"
        source=(thesis/"chapters_rewrite/06_results.tex").read_text()
        body=source[source.index(r'\section{RQ2:'):source.index(r'\section{RQ3:')]
        for term in ["RedesignGridTolerance","redesign-case-rates","redesign-stronger-null","0.656","At A,","At B,"]:
            self.assertNotIn(term,body)
        rates=pd.read_csv(study.OUTPUT/"combined_rates.csv")
        rates=rates[rates.denominator.eq("all")]
        for k,profile,n,common,method in [(4,"uniform",20,.02,"normal_wald"),
            (4,"uniform",20,.02,"expanded_welch"),(4,"uniform",20,.3,"expanded_welch"),
            (16,"different_skew",1000,.005,"normal_wald"),(16,"different_skew",1000,.005,"expanded_welch")]:
            row,=rates[rates.k.eq(k)&rates.profile.eq(profile)&rates.n_p.eq(n)&
                np.isclose(rates.common_mi,common)&rates.method.eq(method)].to_dict("records")
            self.assertIn(f'{100*row["rejection_rate"]:.2f}\\%',body)
        weak_large=rates[rates.k.eq(16)&rates.n_p.eq(50000)&np.isclose(rates.common_mi,.005)]
        self.assertLess(weak_large.rejection_rate.max(),.04)
        table=(thesis/"figures_rewrite/balanced_null_diagnostics.tex").read_text()
        diag=pd.read_csv(study.OUTPUT/"combined_diagnostics.csv")
        for k,profile,n in study.DIAGNOSTIC_CASES:
            d,=diag[diag.k.eq(k)&diag.profile.eq(profile)&diag.n_p.eq(n)&np.isclose(diag.common_mi,.02)].to_dict("records")
            self.assertIn(f'{d["difference_bias"]/np.sqrt(d["observed_variance"]):.3f}',table)
            self.assertIn(f'{d["estimated_observed_ratio"]:.3f}',table)


if __name__=="__main__":unittest.main()
