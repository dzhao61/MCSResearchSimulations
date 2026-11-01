"""Full-grid, signed-gap and reused-evidence checks for the power extension."""
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy.stats import binomtest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"experiments"))
import mi_gap_power_study as study


class MiGapPowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.configs,cls.pops,cls.arrays=study.build_design()

    def test_all_gaps_cover_the_same_full_grid(self):
        original,_,_=study.base.build_design()
        grid={(c["k"],c["profile"],c["n_p"],c["n_q"]) for c in original}
        for gap in study.GAPS:
            selected=[c for c in self.configs if c["gap"]==gap]
            self.assertEqual(len(selected),120)
            self.assertEqual({(c["k"],c["profile"],c["n_p"],c["n_q"]) for c in selected},grid)
            for c in selected:
                self.assertAlmostEqual(c["mi_q"]-c["mi_p"],gap,places=12)
                self.assertAlmostEqual(c["delta"],-gap,places=12)
        self.assertEqual(len({c["configuration_id"] for c in self.configs}),360)

    def test_original_ids_and_populations_are_preserved(self):
        original,populations,arrays=study.base.build_design()
        reused=[c for c in self.configs if c["record_source"]=="original"]
        self.assertEqual({c["configuration_id"] for c in reused},{c["configuration_id"] for c in original})
        for key,pop in populations.items():
            self.assertEqual(pop,self.pops[key])
            for p,q in zip(arrays[key],self.arrays[key],strict=True):np.testing.assert_array_equal(p,q)

    def test_new_populations_preserve_margins_and_targets(self):
        for pop in self.pops.values():
            for side in "pq":
                p=np.array(pop["probability_"+side])
                self.assertTrue((p>0).all())
                np.testing.assert_allclose(p.sum(0),pop["margin_"+side],atol=1e-12)
                np.testing.assert_allclose(p.sum(1),pop["margin_"+side],atol=1e-12)
                self.assertAlmostEqual(pop["achieved_mi_"+side],pop["mi_"+side],places=10)

    def test_streams_are_distinct_across_gap_and_population(self):
        selected=[c for c in self.configs if c["k"]==4 and c["profile"]=="uniform" and c["n_p"]==1000]
        seeds={study.base.seed_for(c["configuration_id"],0,side) for c in selected for side in "pq"}
        self.assertEqual(len(seeds),6)

    def test_combined_counts_intervals_and_reused_rates(self):
        if not (study.OUTPUT/"combined_audit.json").exists():self.skipTest("Extension has not finished")
        audit=json.loads((study.OUTPUT/"combined_audit.json").read_text())
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["pairs"],36000000)
        self.assertEqual(audit["new_pairs"],24000000)
        self.assertEqual(audit["reused_pairs"],12000000)
        rates=pd.read_csv(study.OUTPUT/"combined_rates.csv")
        primary=rates[rates.denominator.eq("all")]
        self.assertEqual(len(primary),720)
        for row in primary.itertuples():
            ci=binomtest(row.rejections,row.replicates).proportion_ci(method="wilson")
            self.assertAlmostEqual(row.rejection_low,ci.low,places=12)
            self.assertAlmostEqual(row.rejection_high,ci.high,places=12)
        old=pd.read_csv(study.base.OUTPUT/"rates.csv")
        reused=rates[np.isclose(rates.gap,.01)][old.columns].sort_values(["configuration_id","method","denominator"]).reset_index(drop=True)
        old=old.sort_values(["configuration_id","method","denominator"]).reset_index(drop=True)
        pd.testing.assert_frame_equal(old,reused)
        pairs=pd.read_csv(study.OUTPUT/"combined_paired.csv")
        pairs=pairs[pairs.denominator.eq("all")]
        self.assertEqual(len(pairs),360)
        self.assertTrue(pairs.only_expanded.eq(0).all())
        np.testing.assert_array_equal(pairs.only_wald+pairs.only_expanded+pairs.both_reject+pairs.neither_reject,100000)

    def test_all_gaps_are_included_in_current_figures(self):
        path=study.base.ROOT.parent/"Thesis Writeup/Welch MI/figures_rewrite/mi_gap_power_evidence.json"
        if not path.exists():self.skipTest("Figures have not been generated")
        evidence=json.loads(path.read_text())
        configs={c["configuration_id"]:c for c in self.configs}
        all_ids=[]
        for data in evidence["figures"].values():
            ids=data["configurations"]
            self.assertEqual(len(ids),120)
            self.assertEqual(set(data["gaps"]),set(study.GAPS))
            self.assertEqual({configs[key]["gap"] for key in ids},set(study.GAPS))
            all_ids.extend(ids)
        self.assertEqual(len(all_ids),360)
        self.assertEqual(set(all_ids),set(configs))

    def test_new_numerical_claims_match_combined_evidence(self):
        thesis=study.base.ROOT.parent/"Thesis Writeup/Welch MI"
        if not (study.OUTPUT/"combined_audit.json").exists():self.skipTest("Extension is absent")
        text=(thesis/"chapters_rewrite/06_results.tex").read_text()
        rates=pd.read_csv(study.OUTPUT/"combined_rates.csv")
        primary=rates[rates.denominator.eq("all")]
        for profile,k,n,gap in [("uniform",4,2500,.005),("uniform",4,2500,.02),
                                ("same_skew",16,50000,.005),("different_skew",16,1000,.005),
                                ("different_skew",16,1000,.02)]:
            row,=primary[primary.profile.eq(profile)&primary.k.eq(k)&primary.n_p.eq(n)&
                np.isclose(primary.gap,gap)&primary.method.eq("expanded_welch")].to_dict("records")
            self.assertIn(f'{100*row["rejection_rate"]:.2f}\\%',text)
        at_max=primary[primary.n_p.eq(50000)]
        small=at_max[np.isclose(at_max.gap,.005)].rejection_rate
        for rate in [small.min(),small.max()]:self.assertIn(f'{100*rate:.2f}\\%',text)
        self.assertGreater(at_max[~np.isclose(at_max.gap,.005)].rejection_rate.min(),.999)
        paired=pd.read_csv(study.OUTPUT/"combined_paired.csv")
        self.assertLess(paired[paired.denominator.eq("all")&paired.n_p.eq(10000)].difference.max()*100,.32)


if __name__=="__main__":unittest.main()
