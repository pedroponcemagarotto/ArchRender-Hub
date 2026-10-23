"""ArchRender R4 geometry-risk diagnostic (does not approve architecture)."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import qa_geometria as tool


class TestQAR4(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.a = self.root / "a.png"
        self.b = self.root / "b.png"
        self.baseline = np.full((160, 240, 3), 175, dtype=np.uint8)
        cv2.rectangle(self.baseline, (25, 24), (215, 132), (30, 30, 30), 3)
        cv2.line(self.baseline, (30, 75), (212, 75), (16, 16, 16), 3)
        cv2.rectangle(self.baseline, (62, 82), (115, 121), (60, 60, 60), 3)
        cv2.imwrite(str(self.a), self.baseline)

    def set_result(self, img):
        cv2.imwrite(str(self.b), img)

    def test_01_identical_not_certified(self):
        self.set_result(self.baseline)
        x, _ = tool.diagnose(self.a, self.b, [tool.parse_anchor("wall:0.05,0.05,0.95,0.95")])
        self.assertEqual("identica_sem_alteracao", x["decision"])
        self.assertEqual(1.0, x["global"]["recall"])
        self.assertFalse(x["architectural_approval"])

    def test_02_mild_exposure_change_keeps_edges(self):
        img = cv2.convertScaleAbs(self.baseline, alpha=1.03, beta=7)
        self.set_result(img)
        x, _ = tool.diagnose(self.a, self.b)
        self.assertEqual("conferencia_manual_necessaria", x["decision"])
        self.assertGreaterEqual(x["global"]["recall"], 0.90)
        self.assertFalse(x["architectural_approval"])

    def test_03_wall_removed_warns(self):
        img = self.baseline.copy()
        cv2.line(img, (30, 75), (212, 75), (175, 175, 175), 10)
        self.set_result(img)
        x, _ = tool.diagnose(self.a, self.b,
                             [tool.parse_anchor("wall:0.1,0.4,0.9,0.55")])
        self.assertEqual("alerta_de_deriva_visual", x["decision"])
        self.assertLess(x["anchors"][0]["recall"], 0.7)

    def test_04_mismatched_size_no_misleading_score(self):
        self.set_result(cv2.resize(self.baseline, (120, 80)))
        x, _ = tool.diagnose(self.a, self.b)
        self.assertEqual("resolucoes_incompativeis", x["decision"])
        self.assertIsNone(x["global"])
        y, _ = tool.diagnose(self.a, self.b, allow_resize=True)
        self.assertEqual("revisao_por_redimensionamento", y["decision"])
        self.assertTrue(y["resized_for_diagnostics"])
        self.assertFalse(y["architectural_approval"])

    def test_05_reject_invalid_anchors(self):
        for bad in ("a:0.4,0.2,0.1,0.7", "a:0,0,1", "bad space:0,0,1,1", "a:0,0,0.01,1"):
            with self.assertRaises(ValueError):
                tool.parse_anchor(bad)
        good = tool.parse_anchor("window:0.2,0.3,0.8,0.9")
        self.assertEqual(good["id"], "window")

    def test_06_source_unchanged_and_visual_report(self):
        img = cv2.convertScaleAbs(self.baseline, alpha=1.02, beta=8)
        self.set_result(img)
        digest = hashlib.sha256(self.a.read_bytes()).hexdigest()
        x, frame = tool.diagnose(self.a, self.b,
                                 [tool.parse_anchor("window:0.1,0.1,0.9,0.9")])
        picture = self.root / "visual.png"
        tool.write_visual(x, frame, picture)
        self.assertTrue(picture.is_file())
        self.assertEqual(hashlib.sha256(self.a.read_bytes()).hexdigest(), digest)
        with self.assertRaises(FileExistsError):
            tool.write_visual(x, frame, picture)
        self.assertFalse(x["architectural_approval"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
