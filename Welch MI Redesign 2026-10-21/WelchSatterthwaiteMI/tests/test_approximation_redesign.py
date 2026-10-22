"""Statistical and evidence-integrity checks for the independent redesign."""
import sys
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
from scipy.stats import t, binomtest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'experiments'))
import redesign_study as study


class RedesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.configs, cls.displays, cls.pairs, cls.arrays, _, cls.focus = study.build_design()

    def test_scope_and_null_matching(self):
        self.assertEqual(len(self.configs), 342)
        self.assertEqual(sum(c['mi_p']==c['mi_q'] for c in self.configs),186)
        self.assertEqual(sum(d['study']=='association' for d in self.displays),63)
        by_id={c['configuration_id']:c for c in self.configs}
        for c in self.configs:
            n=by_id[c['reference_id']]
            for key in ('mi_p','k','profile','construction','n_p','n_q'):
                self.assertEqual(c[key],n[key])
            self.assertEqual(n['mi_p'],n['mi_q'])
        fake={k:{'null_sd':.01} for k in self.focus.values()}
        expanded,_,_,_,rows,_=study.build_design(fake)
        self.assertEqual(len(rows),27)
        self.assertEqual({r['standardised_difference'] for r in rows},set(study.EFFECTS))
        for row in rows:
            c=next(c for c in expanded if c['configuration_id']==row['configuration_id'])
            self.assertEqual(c['reference_id'],self.focus[row['focus']])

    def test_sample_size_comparator_is_n_not_n_minus_one(self):
        c=next(c for c in self.configs if c['n_p']==20 and c['k']==4 and c['profile']=='uniform')
        r=study.sample(c,*self.arrays[c['pair_id']],'test',0,50)
        values,df=study.method_values(r,c,10.)
        a=r['influence_variance_p']/c['n_p']; b=r['influence_variance_q']/c['n_q']
        expected=(a+b)**2/(a*a/c['n_p']+b*b/c['n_q'])
        np.testing.assert_allclose(df,expected)
        np.testing.assert_allclose(values['size'][0],2*t.sf(abs(r['statistic']),expected))
        self.assertTrue(np.any(abs(df-expected*19/20)>.1))

    def test_zero_variance_values_are_in_moments(self):
        x=np.array([0.,0.,1.,2.,3.])
        m=study.moment_summary(x)
        self.assertEqual(m['count'],5)
        self.assertEqual(m['zero_count'],2)
        self.assertAlmostEqual(m['mean'],1.2)
        self.assertAlmostEqual(m['nu_mom'],2*x.mean()**2/np.var(x,ddof=1))
        cp=np.array([[3,0],[0,3]])
        components,*_=study.independent_values(cp,cp,10.)
        self.assertEqual(components[0][1],0.)
        self.assertTrue(np.isnan(components[0][3]))

    def test_fixed_reference_calibration_and_ties(self):
        c=next(c for c in self.configs if c['configuration_id']==self.focus['A'])
        r=study.sample(c,*self.arrays[c['pair_id']],'cal-test',0,2000)
        ref={'nu_ref':3.7,'calibration':study.calibrate(r,c,3.7)}
        _,dec=study.decisions(r,c,ref,calibrated=True)
        np.testing.assert_array_equal(dec['wald'],dec['reference'])
        for method in study.METHODS:
            self.assertLessEqual(int(dec[method].sum()),100)
        tied=np.array([.01]*20+[.5]*80)
        cut=study.calibration_threshold(tied,np.ones(100,bool))
        self.assertLessEqual(int((tied<cut).sum()),5)

    def test_stream_independence_and_batch_invariance(self):
        c=self.configs[0]; p,q=self.arrays[c['pair_id']]
        a=study.sample(c,p,q,'fit',0,50,batch=7)
        b=study.sample(c,p,q,'fit',0,50,batch=50)
        d=study.sample(c,p,q,'evaluation',0,50)
        for key in a:
            np.testing.assert_equal(a[key],b[key])
        self.assertFalse(np.array_equal(a['plugin_mi_p'],d['plugin_mi_p']))
        self.assertNotEqual(study.seed_for('pilot_fit','x',0,'p'),study.seed_for('fit','x',0,'p'))

    def test_corruption_is_detected_and_checkpoint_is_immutable(self):
        c=self.configs[0]; p,q=self.arrays[c['pair_id']]
        with tempfile.TemporaryDirectory() as tmp:
            task=(tmp,'evaluation',c,p,q,20,study.fingerprint())
            study.run_task(task)
            r=study.load_records(tmp,'evaluation',c['configuration_id'])
            self.assertEqual(len(r['statistic']),20)
            with self.assertRaises(RuntimeError):
                study.run_task((*task[:-2],21,task[-1]))
            path=Path(tmp)/'evaluation'/c['configuration_id']/'chunk_000.npz'
            path.write_bytes(path.read_bytes()+b'corrupt')
            with self.assertRaises(AssertionError):
                study.load_records(tmp,'evaluation',c['configuration_id'])

    def test_deliverable_rate_intervals_match_independent_binomial_calculation(self):
        output=study.OUTPUT
        figures=study.ROOT.parent/'Thesis Writeup/Welch MI/figures_rewrite'
        if not (figures/'focused_redesign_cases_rates.tex').exists():
            self.skipTest('Delivered manuscript source is separate.')
        text=(figures/'focused_redesign_cases_rates.tex').read_text()
        rates=pd.read_csv(output/'rates.csv')
        rates=rates[rates.denominator.eq('all')].set_index(['configuration_id','method'])
        keys=list(self.focus.values())
        keys += [c['configuration_id'] for c in self.configs if c['k']==16 and c['profile'] in ('same_skew','different_skew')
                 and c['n_p']==c['n_q'] and c['n_p'] in (1000,10000) and c['mi_p']==c['mi_q']==.02 and c['construction']=='copying']
        self.assertEqual(len(keys),7)
        for key in keys:
            for method in study.METHODS:
                row=rates.loc[(key,method)]
                interval=binomtest(int(row.rejected),int(row['count'])).proportion_ci(method='wilson')
                self.assertIn(f'{row.rate:.4f} [{interval.low:.4f}, {interval.high:.4f}]',text)

    def test_deliverable_power_contrasts_preserve_pairing_and_percentage_units(self):
        figures=study.ROOT.parent/'Thesis Writeup/Welch MI/figures_rewrite'
        if not (figures/'focused_redesign_power_contrasts.tex').exists():
            self.skipTest('Delivered manuscript source is separate.')
        text=(figures/'focused_redesign_power_contrasts.tex').read_text()
        focus=pd.read_csv(study.OUTPUT/'focus.csv')
        paired=pd.read_csv(study.OUTPUT/'paired.csv')
        paired=paired[paired.denominator.eq('all')].set_index(['configuration_id','comparator'])
        for row in focus[focus.standardised_difference.eq(2)].itertuples():
            for other in ('wald','size'):
                p=paired.loc[(row.configuration_id,other)]
                difference=(p.only_expanded-p.only_comparator)/p['count']
                variance=((p.only_expanded+p.only_comparator)/p['count']-difference**2)/(p['count']-1)
                lo=difference-1.96*np.sqrt(variance);hi=difference+1.96*np.sqrt(variance)
                self.assertIn(f'{100*difference:+.3f} & [{100*lo:+.3f}, {100*hi:+.3f}]',text)


if __name__=='__main__': unittest.main()
