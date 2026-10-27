"""Presentation orientation must preserve values, intervals and inclusion rules."""
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments'))
from report_ratio_tools import (comparison_curves,
    mean_df_over_moment_target, plain_log_tick)


class RatioDisplayTests(unittest.TestCase):
    def test_saved_curves_share_their_scientific_benchmarks(self):
        root=ROOT/'results/approximation_redesign'
        d=pd.read_csv(root/'moments.csv')
        displays=pd.read_csv(root/'displays.csv',keep_default_na=False)
        d=d[d.configuration_id.isin(displays[displays.study.eq('null')].configuration_id)]
        before=d.copy(deep=True)
        mean,_,_,_=comparison_curves(d,'mean')
        variance,low,high,sample=comparison_curves(d,'variance')
        df,_,_,sample_df=comparison_curves(d,'df')
        np.testing.assert_allclose(mean,d['mean']/d.population_v,rtol=1e-12)
        np.testing.assert_allclose(variance,(d.population_tau2/d.n)/d.variance,rtol=1e-12)
        np.testing.assert_allclose(df,d.nu_fo/d.nu_mom,rtol=1e-12)
        np.testing.assert_allclose(df,1/(mean**2*variance),rtol=1e-12)
        complete=d.df_valid_count.eq(d['count'])
        np.testing.assert_allclose(sample_df[complete],(d.df_mean/d.nu_mom)[complete],rtol=1e-12)
        self.assertTrue(np.isnan(sample_df[~complete]).all())
        np.testing.assert_allclose(low,variance-1.96*d.variance_ratio_mcse,rtol=1e-12)
        np.testing.assert_allclose(high,variance+1.96*d.variance_ratio_mcse,rtol=1e-12)
        self.assertTrue(np.all(low>0) and np.all(low<variance) and np.all(variance<high))
        pd.testing.assert_frame_equal(d,before)

    def test_unconditional_mean_over_target_excludes_incomplete_and_invalid_estimates(self):
        d=pd.DataFrame(dict(df_mean=[5.,5.,0.,5.,np.inf,5.],nu_mom=[10.,10.,10.,np.inf,10.,0.],
            df_valid_count=[100,99,100,100,100,100],count=[100]*6))
        r=mean_df_over_moment_target(d)
        self.assertEqual(r[0],.5)
        self.assertTrue(np.isnan(r[1:]).all())

    def test_worked_example_and_width_bound_match_the_plotted_data(self):
        root=ROOT/'results/approximation_redesign'
        d=pd.read_csv(root/'moments.csv')
        displays=pd.read_csv(root/'displays.csv',keep_default_na=False)
        d=d[d.configuration_id.isin(displays[displays.study.eq('null')].configuration_id)
            &d.profile.eq('different_skew')]
        selected=d[d.k.eq(16)&d.side.eq('p')&d.n.eq(1000)]
        self.assertEqual(len(selected),1)
        point,_,_,sample=comparison_curves(selected,'variance')
        self.assertEqual(round(point[0],3),.756)
        self.assertEqual(round(sample[0],2),1.67)
        for kind in ['mean','variance']:
            p,l,h,_=comparison_curves(d,kind)
            self.assertLess(np.nanmax(np.maximum(p-l,h-p)/p),.013)

    def test_power_axis_is_negative_signed_difference_in_null_sd_units(self):
        import json
        r=ROOT/'results/approximation_redesign'
        focus=pd.read_csv(r/'focus.csv')
        configs=pd.read_csv(r/'configurations.csv').set_index('configuration_id')
        refs=json.loads((r/'references.json').read_text())
        nulls=json.loads((r/'focus_nulls.json').read_text())
        for row in focus.itertuples():
            delta=configs.loc[row.configuration_id,'delta']
            self.assertLessEqual(delta,0.)
            self.assertAlmostEqual(-delta/refs[nulls[row.focus]]['null_sd'],
                                   row.standardised_difference,places=8)

    def test_split_rows_keep_their_values_and_common_scales(self):
        import importlib.util
        import matplotlib.pyplot as plt
        path=ROOT.parent/'Thesis Writeup/Welch MI/figures_rewrite/focused_results_displays.py'
        spec=importlib.util.spec_from_file_location('split_result_displays',path)
        plots=importlib.util.module_from_spec(spec);spec.loader.exec_module(plots)
        root=ROOT/'results/approximation_redesign'
        moments=pd.read_csv(root/'moments.csv');displays=pd.read_csv(root/'displays.csv',keep_default_na=False)
        data=moments[moments.configuration_id.isin(displays[displays.study.eq('null')].configuration_id)
            &moments.profile.eq('different_skew')]
        for group,fields in [('moment_predictions',['mean_ratio','variance_ratio','plugin_variance_ratio']),
                             ('component_df',['df_ratio','sample_df'])]:
            fig=plots.approximation_figure(data,group)
            try:
                self.assertEqual(len(fig.axes),2*len(fields))
                for row,field in enumerate(fields):
                    for col,side in enumerate('pq'):
                        ax=fig.axes[row*2+col]
                        for line,k in zip(ax.lines[:4],[2,4,8,16]):
                            subset=data[data.side.eq(side)&data.k.eq(k)].sort_values('n')
                            expected=mean_df_over_moment_target(subset) if field=='sample_df' else subset[field]
                            np.testing.assert_allclose(line.get_ydata(),expected,rtol=1e-12,equal_nan=True)
                        self.assertEqual(len(ax.lines),5)  # four table sizes plus agreement at one
                        self.assertEqual(ax.get_ylim(),fig.axes[row*2].get_ylim())
                rows=range(1,3) if group=='moment_predictions' else range(2)
                limits=[fig.axes[2*r].get_ylim() for r in rows]
                self.assertTrue(all(limit==limits[0] for limit in limits))
            finally:plt.close(fig)

    def test_near_independence_panel_separates_the_mean_from_its_target(self):
        import importlib.util
        import matplotlib.pyplot as plt
        path=ROOT.parent/'Thesis Writeup/Welch MI/figures_rewrite/focused_results_displays.py'
        spec=importlib.util.spec_from_file_location('near_independence_displays',path)
        plots=importlib.util.module_from_spec(spec);spec.loader.exec_module(plots)
        root=ROOT/'results/approximation_redesign';moments=pd.read_csv(root/'moments.csv')
        displays=pd.read_csv(root/'displays.csv',keep_default_na=False)
        data=moments[moments.configuration_id.isin(displays[displays.study.eq('association')].configuration_id)
            &moments.profile.eq('different_skew')&moments.n.eq(1000)]
        for detailed in (False,True):
            fig=plots.near_independence_figure(data,detailed=detailed)
            try:
                for col,side in enumerate('pq'):
                    ax=fig.axes[4+col];d=data[data.side.eq(side)].sort_values('mi')
                    self.assertEqual(len(ax.lines),6 if detailed else 4)
                    np.testing.assert_allclose(ax.lines[0].get_ydata(),d.df_mean,rtol=1e-12)
                    np.testing.assert_allclose(ax.lines[1].get_ydata(),((d.k-1)**2+2*d.n*d.mi)/2,rtol=1e-12)
                    np.testing.assert_allclose(ax.lines[2].get_ydata(),d.nu_mom,rtol=1e-12)
                    np.testing.assert_allclose(ax.lines[3].get_ydata(),d.nu_fo,rtol=1e-12)
                    self.assertEqual(len(ax.collections),1 if detailed else 0)
            finally:plt.close(fig)

    def test_tick_at_agreement_is_plain_one(self):
        self.assertEqual(plain_log_tick(1.),'1')
        self.assertEqual(plain_log_tick(.1),'0.1')
        self.assertEqual(plain_log_tick(10.),'10')


if __name__=='__main__':unittest.main()
