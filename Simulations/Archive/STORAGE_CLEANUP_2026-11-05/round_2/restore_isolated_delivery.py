#!/usr/bin/env python3
"""Restore the old delivery-test copy from retained canonical files and unique entries."""
from pathlib import Path
import argparse,gzip,hashlib,json,os,shutil,zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.parent
CHUNK=4*1024*1024

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as src:
        for block in iter(lambda:src.read(CHUNK),b''):h.update(block)
    return h.hexdigest()

def manifest():
    with gzip.open(HERE/'isolated_delivery_manifest.json.gz','rt') as src:return json.load(src)

def restore(output, data):
    if output.exists():raise FileExistsError(output)
    output.mkdir(parents=True)
    with zipfile.ZipFile(HERE/'isolated_delivery_unique.zip') as unique:
        for entry in data['files']:
            path=output/entry['path'];path.parent.mkdir(parents=True,exist_ok=True)
            src=unique.open(entry['path']) if entry['source']=='unique' else (ROOT/entry['source']).open('rb')
            h=hashlib.sha256();size=0
            with src,path.open('xb') as dst:
                for block in iter(lambda:src.read(CHUNK),b''):
                    dst.write(block);h.update(block);size+=len(block)
            if size!=entry['size'] or h.hexdigest()!=entry['sha256']:
                raise ValueError('Changed recovery source: '+entry['path'])
            path.chmod(entry['mode']);os.utime(path,ns=(entry['mtime_ns'],entry['mtime_ns']))
    for entry in data['symlinks']:
        path=output/entry['path'];path.parent.mkdir(parents=True,exist_ok=True);path.symlink_to(entry['target'])
    for entry in sorted(data['directories'],key=lambda x:len(Path(x['path']).parts),reverse=True):
        path=output/entry['path'];path.mkdir(parents=True,exist_ok=True)
        path.chmod(entry['mode']);os.utime(path,ns=(entry['mtime_ns'],entry['mtime_ns']))
    return output

def verify(output, data):
    for entry in data['files']:
        path=output/entry['path']
        if not path.is_file() or path.stat().st_size!=entry['size'] or digest(path)!=entry['sha256']:
            raise ValueError('Restoration failed verification: '+entry['path'])
    for entry in data['symlinks']:
        path=output/entry['path']
        if not path.is_symlink() or os.readlink(path)!=entry['target']:raise ValueError(path)
    return len(data['files'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();data=manifest();output=args.output.resolve()
    restore(output,data);print('Restored and SHA-256 verified',verify(output,data),'files in',output)
