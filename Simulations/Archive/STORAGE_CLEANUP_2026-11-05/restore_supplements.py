#!/usr/bin/env python3
"""Restore archived supplement contents after verified storage deduplication.

Only an explicitly named output is created. Existing files are never overwritten.
The workspace's canonical result files must retain the manifest's hashes.
"""
import argparse
import base64
import gzip
import hashlib
import json
import shutil
import struct
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CHUNK = 4 * 1024 * 1024


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as src:
        for block in iter(lambda: src.read(CHUNK), b''):
            h.update(block)
    return h.hexdigest()


def strip_zip64(extra):
    result = b''
    while len(extra) >= 4:
        tag, length = struct.unpack('<HH', extra[:4])
        field, extra = extra[:4 + length], extra[4 + length:]
        if tag != 1:
            result += field
    return result + extra


def info_from_record(entry):
    m = entry['metadata']
    info = zipfile.ZipInfo(entry['name'], tuple(m['date_time']))
    for key in ['compress_type', 'create_system', 'create_version', 'extract_version',
                'internal_attr', 'external_attr', 'volume']:
        setattr(info, key, m[key])
    info.comment = base64.b64decode(m['comment_b64'])
    info.extra = strip_zip64(base64.b64decode(m['extra_b64']))
    info.file_size = entry['size']
    return info


def load_manifest():
    with gzip.open(HERE / 'working_draft_manifest.json.gz', 'rt', encoding='utf-8') as src:
        return json.load(src)


def restore_working_draft(output, manifest):
    temporary = output.with_name(output.name + '.restoring')
    if output.exists() or temporary.exists():
        raise FileExistsError('The output or temporary output already exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(HERE / 'unique_entries.zip') as unique, zipfile.ZipFile(temporary, 'w', allowZip64=True) as restored:
            restored.comment = base64.b64decode(manifest['zip_comment_b64'])
            for entry in manifest['entries']:
                info = info_from_record(entry)
                if entry['source'] == 'unique_entries.zip':
                    src = unique.open(entry['name'])
                else:
                    src = (ROOT / entry['source']).open('rb')
                digest = hashlib.sha256()
                size = 0
                with src, restored.open(info, 'w') as dst:
                    for block in iter(lambda: src.read(CHUNK), b''):
                        digest.update(block)
                        size += len(block)
                        dst.write(block)
                if size != entry['size'] or digest.hexdigest() != entry['sha256']:
                    raise ValueError('Source changed or corrupted: ' + entry['name'])
        temporary.rename(output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return output


def verify_members(path, manifest):
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if [e.filename for e in entries] != [e['name'] for e in manifest['entries']]:
            raise ValueError('Archive membership or order differs')
        for record in manifest['entries']:
            digest = hashlib.sha256()
            with archive.open(record['name']) as src:
                for block in iter(lambda: src.read(CHUNK), b''):
                    digest.update(block)
            if digest.hexdigest() != record['sha256']:
                raise ValueError('Member content differs: ' + record['name'])
    return len(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', choices=['working-draft', 'duplicate-copy'])
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.archive == 'working-draft':
        manifest = load_manifest()
        restore_working_draft(output, manifest)
        count = verify_members(output, manifest)
        print(f'Restored and SHA-256 verified all {count:,} original members: {output}')
        print('The ZIP container may have a different checksum after recompression; member contents are identical.')
    else:
        details = json.loads((HERE / 'duplicate_copy.json').read_text())
        source = ROOT / details['retained_copy']
        if file_hash(source) != details['sha256']:
            raise ValueError('Retained copy does not match its verified hash')
        if output.exists():
            raise FileExistsError(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as src, output.open('xb') as dst:
            shutil.copyfileobj(src, dst, CHUNK)
        if file_hash(output) != details['sha256']:
            raise ValueError('Restored copy failed verification')
        print('Restored the byte-identical supplement copy:', output)


if __name__ == '__main__':
    main()
