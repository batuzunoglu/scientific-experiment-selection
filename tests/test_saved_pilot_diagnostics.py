"""Private diagnostic helpers tested with fabricated predictions and unfitted stubs."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from scripts import inspect_measured_pilot_artifacts as d


class SavedDiagnosticsTests(unittest.TestCase):
    def test_predictions_are_existing_only_complete_and_binary(self):
        run={'arm':'A','policy':'random','seed':7,'curve':[
            {'acquired_conditions':k,'evaluation_predictions':[[0,1,0]]*6} for k in range(13)]}
        got=d.condition_accuracies(run)
        self.assertEqual(len(got),6);self.assertEqual(len(got[0]),13)
        run['curve'][0].pop('evaluation_predictions')
        with self.assertRaises(ValueError):d.condition_accuracies(run)
        run['curve'][0]['evaluation_predictions']=[[0,1,3]]*6
        with self.assertRaises(ValueError):d.condition_accuracies(run)

    def test_public_or_existing_output_forbidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError):d.private_output(root/'public',root/'private')
            private=root/'private';private.mkdir()
            out=d.private_output(private/'new',private)
            self.assertEqual(out.stat().st_mode & 0o777,0o700)
            with self.assertRaises(FileExistsError):d.private_output(out,private)

    def test_cli_pickle_class_alias_loads_without_fitting_or_predicting(self):
        import io,pickle
        from unittest.mock import patch
        from scientific_experiment_selection.measured_pilot import MeasuredLogisticAdapter
        cls=MeasuredLogisticAdapter
        model=cls('B')  # Unfitted fabricated state, no ML dependency access.
        with patch.object(cls,'__module__','__main__'),patch('__main__.MeasuredLogisticAdapter',cls,create=True):
            payload=pickle.dumps(model)
        with patch.object(cls,'fit',side_effect=AssertionError('fit forbidden')),patch.object(cls,'predict',side_effect=AssertionError('predict forbidden')):
            loaded=d.TrustedPilotUnpickler(io.BytesIO(payload)).load()
        self.assertIs(type(loaded),cls);self.assertEqual(loaded.arm,'B')
