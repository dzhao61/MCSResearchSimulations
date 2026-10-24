"""Independent upper-null sensitivity extension; leaves the base study immutable."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import numpy as np
import pandas as pd
import redesign_study as study

OUTPUT = study.OUTPUT / 'calibration_sensitivity'


def design(base=study.OUTPUT):
    base = Path(base)
    configs = pd.read_csv(base/'configurations.csv').set_index('configuration_id')
    focus = pd.read_csv(base/'focus.csv')
    lower = json.loads((base/'focus_nulls.json').read_text())
    cases, arrays = [], {}
    for row in focus[focus.standardised_difference.isin([2., 4.])].sort_values(['focus','standardised_difference']).itertuples():
        alt = configs.loc[row.configuration_id].to_dict()
        target = float(alt['mi_q'])
        spec = dict(k=int(alt['k']), profile=alt['profile'], construction='copying',
                    mi_p=target, mi_q=target, n_p=int(alt['n_p']), n_q=int(alt['n_q']))
        # A new namespace makes every fitting/evaluation stream independent of the base study.
        key = 'upper_' + study.digest(spec)[:16]
        pair_id = 'upper_pair_' + study.digest(spec)[:16]
        p, q = [study.construct_copying(study.margin(spec['k'], rho), target).probability
                for rho in study.PROFILES[spec['profile']]]
        arrays[pair_id] = (p, q)
        cases.append(dict(configuration_id=key, pair_id=pair_id, reference_id=key,
                          alternative_id=row.configuration_id, lower_id=lower[row.focus],
                          focus=row.focus, effect=float(row.standardised_difference),
                          delta=0., true_delta=study.population_moments(p)['mi']-study.population_moments(q)['mi'],
                          replicates=study.REPLICATES, **spec))
    assert len(cases) == 6 and len({c['configuration_id'] for c in cases}) == 6
    return cases, arrays


def fingerprint():
    return study.digest({'base_kernel': study.fingerprint(), 'extension': study.sha(Path(__file__))})


def prepare(output=OUTPUT, base=study.OUTPUT, count=study.REPLICATES):
    output, base = Path(output), Path(base)
    output.mkdir(parents=True, exist_ok=True)
    cases, arrays = design(base)
    protocol = dict(seed=study.SEED, source=fingerprint(), replicates=count,
                    fitting_settings=6, evaluation_settings=6, new_pairs=12*count,
                    alpha=study.ALPHA, effects=[2.,4.],
                    null='Both MI values equal the larger MI of the fixed alternative; margins and sample sizes unchanged',
                    independent_streams='Unique upper configuration keys and separate fit/evaluation phases',
                    base_inputs={n: study.sha(base/n) for n in ('protocol.json','configurations.csv','focus.csv','focus_nulls.json','references.json')})
    path = output/'protocol.json'
    if path.exists() and json.loads(path.read_text()) != protocol:
        raise RuntimeError('Sensitivity protocol changed; use a new output directory')
    study.atomic_json(path, protocol)
    pd.DataFrame(cases).to_csv(output/'configurations.csv', index=False)
    with (output/'populations.npz').open('wb') as f:
        np.savez_compressed(f, **{key+'_'+side: a for key,pair in arrays.items() for side,a in zip('pq',pair)})
    return cases, arrays


def audit(output=OUTPUT, base=study.OUTPUT):
    output = Path(output)
    protocol = json.loads((output/'protocol.json').read_text())
    cases, arrays = design(base)
    assert protocol['source'] == fingerprint()
    for name, digest in protocol['base_inputs'].items():
        assert study.sha(Path(base)/name) == digest
    for c in cases:
        for phase in ('fit','evaluation'):
            identity=json.loads((output/phase/c['configuration_id']/'identity.json').read_text())
            assert identity['source'] == protocol['source'] and identity['config'] == c
            assert identity['count'] == protocol['replicates']
    refs=json.loads((output/'references.json').read_text())
    study.audit(output, cases, arrays, refs)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['preflight','pilot','all','audit'])
    parser.add_argument('--base',type=Path,default=study.OUTPUT)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.mode=='audit':
        audit(args.output,args.base); return
    output=args.output/'pilot' if args.mode=='pilot' else args.output
    count=200 if args.mode=='pilot' else study.REPLICATES
    cases,arrays=prepare(output,args.base,count)
    if args.mode=='preflight': return
    for phase in ('fit','evaluation'):
        tasks=[(str(output),phase,c,*arrays[c['pair_id']],count,fingerprint()) for c in cases]
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            rows=[]
            for f in as_completed([pool.submit(study.run_task,t) for t in tasks]):
                rows.append(f.result()); print(f'{phase}: {len(rows)}/6',flush=True)
        pd.DataFrame(rows).to_csv(output/(phase+'_execution.csv'),index=False)
    study.fit_references(output,cases)
    audit(output,args.base)


if __name__=='__main__': main()
