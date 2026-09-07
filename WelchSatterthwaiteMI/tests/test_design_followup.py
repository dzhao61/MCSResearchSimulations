"""Verify the experimental contrasts, not just the output formatting."""
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from run_design_followup import build, PROTOCOL, SOURCE


class FollowupDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks,cls.manifest,cls.populations=build(json.loads(PROTOCOL.read_text()))

    def test_all_predeclared_cells_and_unique_seeds(self):
        self.assertEqual(self.manifest.groupby('experiment').size().to_dict(),{
            'heterogeneous_margins':36,'baseline_sensitivity':108,
            'allocation_reversal':360,'convergence':24})
        self.assertTrue(self.manifest.simulation_seed.is_unique)

    def test_baseline_change_preserves_margins_and_scale(self):
        groups={}
        for task in self.tasks:
            r=task['configuration']
            if r['experiment']!='baseline_sensitivity':continue
            key=(r['shape'],r['skewness']);a=task['probability_p'];b=task['probability_q']
            values=np.concatenate([a.sum(0),a.sum(1),b.sum(0),b.sum(1),[r['shared_reachable_mi']]])
            if key in groups:np.testing.assert_allclose(values,groups[key],atol=1e-9)
            groups[key]=values

    def test_reversal_keeps_populations_and_reverses_only_samples(self):
        original=pd.read_csv(SOURCE/'population_definitions.csv')
        cells=pd.read_csv(SOURCE/'cell_results.csv')
        cells=cells[(cells.experiment=='robustness_imbalance')&(cells.method=='normal_wald')&(cells.nominal_alpha==.05)]
        for task in self.tasks:
            r=task['configuration']
            if r['experiment']!='allocation_reversal':continue
            match=cells[(cells['shape']==r['shape'])&(cells.skewness==r['skewness'])&
                        (cells.relative_effect==r['relative_effect'])&(cells.n_p==r['n_q'])&(cells.n_q==r['n_p'])]
            self.assertEqual(len(match),1)
            p=original[original.population_id==match.iloc[0].population_id].iloc[0]
            for side in ('p','q'):
                np.testing.assert_array_equal(task['probability_'+side],json.loads(p['probability_'+side+'_json']))

    def test_heterogeneous_margins_cannot_be_relabelled_into_each_other(self):
        for task in self.tasks:
            if task['configuration']['experiment']!='heterogeneous_margins':continue
            p,q=task['probability_p'],task['probability_q']
            self.assertFalse(np.allclose(np.sort(p.sum(1)),np.sort(q.sum(1))))
            np.testing.assert_allclose(p.sum(1),np.full(p.shape[0],1/p.shape[0]),atol=1e-9)
            self.assertAlmostEqual(q.sum(1).max(),.7,places=8)


if __name__=='__main__':
    unittest.main()
