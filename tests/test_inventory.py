"""Synthetic bytes only; no laboratory fixtures or measurements."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'source'
        self.source.mkdir()

    def run_cli(self, *extra, output='report'):
        return subprocess.run(
            [sys.executable, '-m', 'scientific_experiment_selection.inventory',
             '--source', f'lab={self.source}', '--output', str(self.base / output),
             '--data-kind', 'synthetic', *extra], capture_output=True, text=True)

    def test_hash_sizes_duplicates_unknowns_and_no_source_changes(self):
        for name in ['Exp3_A.CSV', 'Exp03_copy.csv', 'Exp4_Exp5.csv', 'notes.txt']:
            (self.source / name).write_bytes(b'abc')
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.base / 'report/manifest.json').read_text())
        self.assertEqual(manifest['summary']['file_count'], 4)
        self.assertEqual(manifest['summary']['total_bytes'], 12)
        self.assertEqual(manifest['summary']['unknown_experiment_count'], 2)
        self.assertEqual(manifest['summary']['missing_expected_experiments'],
                         ['Exp4', 'Exp5', 'Exp6', 'Exp7', 'Exp8'])
        self.assertEqual(len(manifest['summary']['duplicate_checksums']), 1)
        rows = {r['relative_path']: r for r in manifest['files']}
        self.assertEqual(rows['Exp3_A.CSV']['extension'], '.CSV')
        self.assertEqual(rows['Exp3_A.CSV']['sha256'],
                         'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(rows['Exp3_A.CSV']['experiment'], 'Exp3')
        self.assertEqual(rows['Exp3_A.CSV']['batch'], 'UNKNOWN')
        self.assertEqual(rows['Exp4_Exp5.csv']['experiment'], 'UNKNOWN')
        self.assertEqual(rows['notes.txt']['ingestion_status'], 'inventoried_not_imported')
        self.assertTrue((self.base / 'report/summary.md').is_file())
        self.assertEqual(sorted(p.name for p in self.source.iterdir()), sorted(rows))
        for p in self.source.iterdir():
            self.assertEqual(p.read_bytes(), b'abc')

    def test_deterministic_output_and_nested_unicode_paths(self):
        nested = self.source / 'Exp7' / 'plate α'
        nested.mkdir(parents=True)
        (nested / 'well 1.dat').write_bytes(b'\x00\xff')
        (self.source / '.hidden').write_bytes(b'')
        for output in ['one', 'two']:
            result = self.run_cli(output=output)
            self.assertEqual(result.returncode, 0, result.stderr)
        for filename in ['manifest.json', 'summary.md']:
            self.assertEqual((self.base / 'one' / filename).read_bytes(),
                             (self.base / 'two' / filename).read_bytes())
        manifest = json.loads((self.base / 'one/manifest.json').read_text())
        self.assertEqual(manifest['summary']['file_count'], 2)
        self.assertEqual(manifest['files'][1]['relative_path'], 'Exp7/plate α/well 1.dat')
        self.assertEqual(manifest['files'][1]['experiment'], 'Exp7')
        self.assertEqual(manifest['files'][1]['plate'], 'UNKNOWN')

    def test_symlinks_are_listed_but_not_followed(self):
        external = self.base / 'outside'
        external.mkdir()
        (external / 'secret').write_bytes(b'outside')
        (self.source / 'link').symlink_to(external, target_is_directory=True)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.base / 'report/manifest.json').read_text())
        self.assertEqual(manifest['summary']['file_count'], 0)
        self.assertEqual(manifest['excluded'], [{'source_id': 'lab', 'relative_path': 'link',
                                               'reason': 'symlink_not_followed'}])

    def test_refuses_output_in_source_and_existing_output(self):
        original = self.source / 'raw.txt'
        original.write_bytes(b'preserve')
        self.assertNotEqual(self.run_cli(output='source/report').returncode, 0)
        self.assertFalse((self.source / 'report').exists())
        self.assertEqual(self.run_cli().returncode, 0)
        before = (self.base / 'report/manifest.json').read_bytes()
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertEqual((self.base / 'report/manifest.json').read_bytes(), before)
        self.assertEqual(original.read_bytes(), b'preserve')

    def test_missing_and_overlapping_sources_fail_without_report(self):
        for extra in [('--source', f'other={self.base / "missing"}'),
                      ('--source', f'other={self.source}')]:
            result = self.run_cli(*extra)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('inventory:', result.stderr)
            self.assertFalse((self.base / 'report').exists())

    def test_multiple_sources_preserve_identity_and_cross_source_duplicates(self):
        other = self.base / 'other'
        other.mkdir()
        (other / 'Exp8.csv').write_bytes(b'abc')
        (self.source / 'Exp8.csv').write_bytes(b'abc')
        result = self.run_cli('--source', f'other={other}')
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.base / 'report/manifest.json').read_text())
        self.assertEqual([r['source_id'] for r in manifest['files']], ['lab', 'other'])
        self.assertEqual(manifest['summary']['file_count'], 2)


if __name__ == '__main__':
    unittest.main()
