"""Read-only file inventory. No spectrum parsing, copying, or scientific inference."""

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat

from scientific_experiment_selection import __version__


def experiment_from_path(relative_path):
    """Conservative token evidence, including directories within the selected root."""
    matches = sorted({int(n) for n in re.findall(
        r'(?<![A-Za-z0-9])Exp0*(\d+)(?![A-Za-z0-9])', relative_path, re.IGNORECASE)})
    if len(matches) == 1 and matches[0] in range(3, 9):
        return f'Exp{matches[0]}'
    return 'UNKNOWN'


def hash_file(path):
    before = path.stat(follow_symlinks=False)
    # Refuse a final-component symlink even if it changed after traversal.
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise ValueError(f'Not a regular file: {path}')
        digest = hashlib.sha256()
        size = 0
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
            size += len(block)
        after = os.fstat(stream.fileno())
    final = path.stat(follow_symlinks=False)
    signatures = {(s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
                  for s in (before, opened, after, final)}
    if len(signatures) != 1 or size != before.st_size:
        raise ValueError(f'File changed during inventory: {path}')
    return size, digest.hexdigest()


def inventory(sources, data_kind, backup_status):
    files, excluded = [], []

    def walk(source_id, root, directory):
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda e: e.name)
        for entry in ordered:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if entry.is_symlink():
                reason = 'symlink_not_followed'
            elif entry.is_dir(follow_symlinks=False):
                walk(source_id, root, path)
                continue
            elif entry.is_file(follow_symlinks=False):
                size, checksum = hash_file(path)
                experiment = experiment_from_path(relative)
                files.append(dict(source_id=source_id, relative_path=relative,
                                  size_bytes=size, sha256=checksum, extension=path.suffix,
                                  experiment=experiment, batch='UNKNOWN', plate='UNKNOWN',
                                  mapping_evidence=relative if experiment != 'UNKNOWN' else None,
                                  mapping_status='unverified_filename_evidence',
                                  ingestion_status='inventoried_not_imported'))
                continue
            else:
                reason = 'non_regular_file_not_read'
            excluded.append(dict(source_id=source_id, relative_path=relative, reason=reason))

    for source_id, root in sorted(sources.items()):
        walk(source_id, root, root)
    files.sort(key=lambda r: (r['source_id'], r['relative_path']))
    excluded.sort(key=lambda r: (r['source_id'], r['relative_path']))
    by_hash = defaultdict(list)
    counts = defaultdict(int)
    for row in files:
        by_hash[row['sha256']].append(dict(source_id=row['source_id'],
                                         relative_path=row['relative_path']))
        counts[row['experiment']] += 1
    return dict(schema_version=1, tool_version=__version__,
                python_version=platform.python_version(), data_kind=data_kind,
                backup_status=backup_status,
                sources=[dict(source_id=k, absolute_path=str(v)) for k, v in sorted(sources.items())],
                files=files, excluded=excluded,
                summary=dict(file_count=len(files), total_bytes=sum(r['size_bytes'] for r in files),
                             counts_by_experiment=dict(sorted(counts.items())),
                             unknown_experiment_count=counts['UNKNOWN'],
                             unknown_batch_count=len(files), unknown_plate_count=len(files),
                             missing_expected_experiments=[f'Exp{i}' for i in range(3, 9)
                                                           if not counts[f'Exp{i}']],
                             expected_batches_status='UNKNOWN: no authoritative batch roster supplied',
                             duplicate_checksums=[dict(sha256=k, files=v) for k, v in sorted(by_hash.items())
                                                  if len(v) > 1]))


def summary_markdown(report):
    summary = report['summary']
    lines = ['# Dataset inventory — review required', '',
             f"Data kind (operator declaration): {report['data_kind']}",
             f"Backup status (operator declaration): {report['backup_status']}", '',
             f"Regular files: {summary['file_count']}; total bytes: {summary['total_bytes']}",
             f"Duplicate checksum groups: {len(summary['duplicate_checksums'])}",
             f"Unknown experiment mappings: {summary['unknown_experiment_count']}",
             f"Expected experiments without unambiguous filename evidence: {', '.join(summary['missing_expected_experiments']) or 'none'}",
             f"Expected batches: {summary['expected_batches_status']}", '',
             'All batch/plate identities require metadata review. Filename evidence is unverified.',
             'No spectra parsed, samples excluded on QC grounds, files copied, or splits assigned.',
             'All regular files inside the supplied roots are listed; unrelated files require manual review.',
             'Missing filename evidence does not prove an experiment is physically absent.', '',
             '## Files', '', 'Paths below use JSON escaping to preserve unusual filenames.', '']
    for row in report['files']:
        label = json.dumps([row['source_id'], row['relative_path']], ensure_ascii=True)
        lines.append(f"- {label}: {row['size_bytes']} bytes; {row['experiment']}; SHA-256 {row['sha256']}")
    lines.extend(['', '## Duplicate checksum groups', ''])
    lines.extend('- ' + json.dumps(group, ensure_ascii=True, sort_keys=True)
                 for group in summary['duplicate_checksums'])
    lines.extend(['', '## Excluded filesystem entries (not read)', ''])
    lines.extend('- ' + json.dumps(row, ensure_ascii=True, sort_keys=True) for row in report['excluded'])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(prog='inventory', description=__doc__)
    parser.add_argument('--source', action='append', required=True, metavar='ID=DIRECTORY')
    parser.add_argument('--output', type=Path, required=True, help='New directory outside all sources')
    parser.add_argument('--data-kind', choices=['synthetic', 'researcher-provided'], required=True)
    parser.add_argument('--backup-status', choices=['unconfirmed', 'confirmed-by-researcher'], default='unconfirmed')
    args = parser.parse_args()
    try:
        sources = {}
        for source in args.source:
            source_id, separator, location = source.partition('=')
            if not separator or not location or not re.fullmatch(r'[A-Za-z0-9_-]+', source_id):
                raise ValueError('Sources must use ID=DIRECTORY with a simple unique ID')
            root = Path(location).expanduser().resolve(strict=True)
            if not root.is_dir() or source_id in sources:
                raise ValueError('Source must be a directory with a unique ID')
            if any(root.is_relative_to(old) or old.is_relative_to(root) for old in sources.values()):
                raise ValueError('Source directories must not overlap')
            sources[source_id] = root
        output = args.output.expanduser().resolve()
        if output.exists() or args.output.is_symlink():
            raise ValueError('Output directory must not already exist')
        if any(output.is_relative_to(root) or root.is_relative_to(output) for root in sources.values()):
            raise ValueError('Output and source directories must not overlap')
        report = inventory(sources, args.data_kind, args.backup_status)
        output.mkdir(parents=True, exist_ok=False)
        (output / 'manifest.json').write_text(json.dumps(report, indent=2, sort_keys=True,
                                                       ensure_ascii=True) + '\n', encoding='utf-8')
        (output / 'summary.md').write_text(summary_markdown(report), encoding='utf-8')
    except (OSError, ValueError) as error:
        parser.exit(2, f'inventory: {error}\n')
    print(f"Inventoried {report['summary']['file_count']} files; review {output / 'summary.md'}")


if __name__ == '__main__':
    main()
