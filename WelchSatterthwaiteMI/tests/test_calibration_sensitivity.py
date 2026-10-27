"""Checks for independent populations, strict calibration and paired uncertainty."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import unittest
from scipy.stats import norm,t
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
import calibration_sensitivity as sensitivity
import report_calibration_sensitivity as report
import redesign_report
import redesign_study as study


class CalibrationSensitivityTests(unittest.TestCase):
    def test_grid_tolerance_boundary_and_overshooting_the_target(self):
        rows=[]
        for i,(wald,expanded) in enumerate([(100,70),(60,45),(60,36),(40,30),(60,43),(60,37)]):
            for method,rejected in [('wald',wald),('expanded',expanded)]:
                rows.append(dict(configuration_id=str(i),method=method,denominator='all',
                                 count=1000,rejected=rejected,rate=rejected/1000))
        grid,summary=redesign_report.calibration_grid(pd.DataFrame(rows),{str(i) for i in range(6)})
        self.assertEqual(grid.classification.tolist(),['toward','toward','away','away','within','within'])
        self.assertEqual((summary['toward'],summary['away'],summary['within']),(2,2,2))
        self.assertEqual(summary['away_wald_below'],1)

    def test_nominal_upper_summary_uses_uncalibrated_reference_distributions(self):
        path=sensitivity.OUTPUT/'nominal_upper_rates.csv'
        if not path.exists(): self.skipTest('Nominal upper-null report not present')
        summary=pd.read_csv(path).set_index(['configuration_id','method'])
        self.assertEqual(len(summary),18)
        for c in sensitivity.design()[0]:
            key=c['configuration_id'];r=study.load_records(sensitivity.OUTPUT,'evaluation',key)
            a=r['influence_variance_p']/c['n_p'];b=r['influence_variance_q']/c['n_q']
            df=(a+b)**2/(a*a/c['n_p']+b*b/c['n_q'])
            pvalues={'wald':2*norm.sf(abs(r['statistic'])),
                     'size':2*t.sf(abs(r['statistic']),df),
                     'expanded':2*t.sf(abs(r['statistic']),r['expanded_welch_degrees_of_freedom'])}
            for m,p in pvalues.items():
                valid=r['expanded_valid'] if m=='expanded' else r['base_valid']
                expected=int((valid & (p<=.05)).sum())
                self.assertEqual(summary.loc[(key,m),'rejected'],expected)
                self.assertEqual(summary.loc[(key,m),'count'],100000)

    def test_reported_power_matches_independent_decision_api(self):
        import json
        cases,_=sensitivity.design()
        power_path=sensitivity.OUTPUT/'power.csv'
        if not power_path.exists(): self.skipTest('Sensitivity run not present')
        powers=pd.read_csv(power_path).set_index(['configuration_id','calibration','quantity'])
        configs=pd.read_csv(study.OUTPUT/'configurations.csv').set_index('configuration_id').to_dict('index')
        lower=json.loads((study.OUTPUT/'references.json').read_text())
        upper=json.loads((sensitivity.OUTPUT/'references.json').read_text())
        for c in cases:
            records=study.load_records(study.OUTPUT,'evaluation',c['alternative_id'])
            for location,ref in [('lower',lower[c['lower_id']]),('upper',upper[c['configuration_id']])]:
                _,yes=study.decisions(records,configs[c['alternative_id']],ref,calibrated=True)
                for m in study.METHODS:
                    self.assertAlmostEqual(yes[m].mean(),powers.loc[(c['configuration_id'],location,m),'estimate'],places=14)
                self.assertAlmostEqual((yes['expanded'].astype(float)-yes['wald']).mean(),
                                       powers.loc[(c['configuration_id'],location,'expanded_minus_wald'),'estimate'],places=14)

    def test_upper_design_preserves_alternative_margins_and_sampling(self):
        cases,arrays=sensitivity.design()
        base=pd.read_csv(study.OUTPUT/'configurations.csv').set_index('configuration_id')
        assert {(c['focus'],c['effect']) for c in cases}=={(s,e) for s in 'ABC' for e in (2.,4.)}
        for c in cases:
            alt=base.loc[c['alternative_id']]
            assert c['mi_p']==c['mi_q']==alt.mi_q
            assert (c['n_p'],c['n_q'],c['profile'])==(alt.n_p,alt.n_q,alt.profile)
            assert c['configuration_id'] not in base.index
            for p,rho in zip(arrays[c['pair_id']],study.PROFILES[c['profile']]):
                np.testing.assert_allclose(p.sum(0),study.margin(c['k'],rho),atol=1e-12)
                np.testing.assert_allclose(p.sum(1),study.margin(c['k'],rho),atol=1e-12)
                assert abs(study.population_moments(p)['mi']-alt.mi_q)<1e-11
            assert study.seed_for('fit',c['configuration_id'],0,'p')!=study.seed_for('evaluation',c['configuration_id'],0,'p')


    def test_strict_ties_and_invalid_outputs(self):
        data=dict(absolute=np.r_[np.arange(18),np.inf,-np.inf],
                  size=np.r_[np.zeros(3),np.ones(17)],expanded=np.r_[np.zeros(3),np.ones(17)])
        yes=report.reject(data,report.cutoffs(data))
        assert yes[:,0].sum()==1
        assert yes[:,1].sum()==yes[:,2].sum()==0  # boundary ties all excluded
        assert not yes[-1].any()
        np.testing.assert_array_equal(yes[:,0],yes[:,3])


    def test_joint_resampling_preserves_identical_and_opposite_contrasts(self):
        a=np.array([True,False]*50)
        decision=np.column_stack([a,~a,a,a,~a,a,~a,~a])
        rng=np.random.default_rng(9)
        for _ in range(30):
            x=report.resample_joint(decision,rng)
            assert x[0]==x[2]==x[3]==x[5]
            assert x[1]==x[4]==x[6]==x[7]
            assert x[0]+x[1]==1


    def test_conditional_df_means_are_not_plotted_as_unconditional(self):
        data=pd.DataFrame(dict(df_mean=[5.,5.,5.],nu_mom=[10.,10.,10.],df_valid_count=[100,99,0],count=[100]*3))
        out=redesign_report.mean_df_over_moment_target(data)
        assert out[0]==.5 and np.isnan(out[1:]).all()


if __name__=="__main__": unittest.main()
