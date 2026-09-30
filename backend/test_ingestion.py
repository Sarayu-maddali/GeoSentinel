import numpy as np
import unittest

from app.services.ingestion_service import IngestionError, ingest_directory, ingest_raster, preprocess_array


class IngestionTests(unittest.TestCase):
    def test_preprocess_array_is_channels_first_and_normalized(self):
        source = np.array([[[-2.0, 0.0], [2.0, np.nan]]], dtype=np.float32)

        processed = preprocess_array(source, target_size=(4, 4))

        self.assertEqual(processed.shape, (1, 4, 4))
        self.assertEqual(processed.dtype, np.float32)
        self.assertGreaterEqual(float(processed.min()), 0.0)
        self.assertLessEqual(float(processed.max()), 1.0)
        self.assertTrue(np.isfinite(processed).all())

    def test_ingest_directory_does_not_create_outputs_for_empty_raw_directory(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            records = ingest_directory(raw_dir, root / "processed")

            self.assertEqual(records, [])
            self.assertTrue((root / "processed").exists())

    def test_ingest_rejects_unknown_extensions(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "notes.txt"
            source.write_text("not an image", encoding="utf-8")

            with self.assertRaisesRegex(IngestionError, "unsupported raster extension"):
                ingest_raster(source, Path(directory) / "processed")


if __name__ == "__main__":
    unittest.main()
