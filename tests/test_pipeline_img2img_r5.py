"""R5 integration tests: exact pixels, provenance, QA and private reports."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import pipeline_img2img_r5 as hub


class TestImagePipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="archrender_integration_")
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {"ARCHRENDER_DATA_DIR": str(self.data / "private")})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.src = self.data / "original.png"
        self.dst = self.data / "candidate.png"
        self.mask = self.data / "mask.png"
        self.out = self.data / "result.png"
        im = Image.new("RGB", (100, 80), (120, 140, 170))
        ImageDraw.Draw(im).rectangle((14, 11, 90, 71), outline=(15, 20, 35), width=3)
        ImageDraw.Draw(im).line((17, 36, 90, 36), fill=(13, 20, 30), width=3)
        im.save(self.src)
        im2 = Image.new("RGB", (100, 80), (190, 95, 35))
        im2.save(self.dst)
        m = Image.new("L", (100, 80), 0)
        ImageDraw.Draw(m).rectangle((22, 12, 63, 35), fill=255)
        m.save(self.mask)

    def _run(self, **extra):
        options={"original":self.src,"candidate":self.dst,"mask":self.mask,
                 "output":self.out,"reference_id":"ref-test-001",
                 "preserve":["janela original"],"changes":["somente luz"],
                 "anchors":["janela:0.1,0.1,0.9,0.6"],"mode":"local_color",
                 "generator":"test-only/photo-controls","visual":True}
        options.update(extra)
        return hub.execute(**options)

    def test_01_integrated_run_preserves_pixels_and_private_report(self):
        result = self._run()
        self.assertEqual(result["pixels_changed_outside_mask"],0)
        self.assertTrue(Path(result["private_report"]).is_file())
        self.assertTrue(Path(result["output_private"]).is_file())
        self.assertTrue(self.out.with_name("result_qa.png").is_file())
        self.assertFalse(result["client_approved"])
        content=json.loads(Path(result["private_report"]).read_text(encoding="utf8"))
        self.assertEqual(content["generation"]["binding_status"],"nao_comprovado")
        self.assertTrue(content["qa_diagnostic"]["human_review_required"])
        self.assertEqual(content["qa"]["decision"],"aguarda_revisao_humana")
        self.assertFalse(content["qa"]["client_approved"])

    def test_02_missing_ai_edit_provenance_never_marked_approved(self):
        result = self._run(mode="image_edit", generator="fixture", source_inspected=False)
        self.assertEqual(result["generator_attachment_binding"],"nao_comprovado")
        self.assertFalse(result["benchmark_completed"])

    def test_03_declared_evidence_does_not_bypass_manual_qa(self):
        result = self._run(mode="image_edit",generator="fixture",
                           binding_evidence="manual review of upload test log",
                           source_inspected=True)
        self.assertEqual(result["generator_attachment_binding"],"declarado_e_revisado_manualmente")
        self.assertFalse(result["client_approved"])
        self.assertFalse(result["benchmark_completed"])
        content=json.loads(Path(result["private_report"]).read_text())
        self.assertTrue(content["generation"]["source_bound"])
        self.assertFalse(content["qa"]["client_approved"])

    def test_04_bad_region_preflight_rejects_before_output(self):
        with self.assertRaises(ValueError):
            self._run(anchors=["badAnchor:1,0,0,1"])
        self.assertFalse(self.out.exists())

    def test_05_output_preexistence_protected(self):
        self.out.write_bytes(b"previous")
        with self.assertRaises(FileExistsError):
            self._run()
        self.assertEqual(self.out.read_bytes(),b"previous")

    def test_06_non_image_edit_cannot_fake_evidence(self):
        with self.assertRaisesRegex(ValueError,"so se aplica"):
            self._run(binding_evidence="pretend source was used")
        self.assertFalse(self.out.exists())

    def test_07_run_cli_returns_success_without_client_approval(self):
        code=hub.cli(["--original",str(self.src),"--candidate",str(self.dst),
                      "--mask",str(self.mask),"--output",str(self.out),
                      "--reference-id","ref-test-007","--candidate-mode","unknown",
                      "--no-visual"])
        self.assertEqual(code,0)
        self.assertFalse(self.out.with_name("result_qa.png").exists())

    def test_08_existing_visual_blocks_run_before_output_creation(self):
        file = self.out.with_name("result_qa.png")
        file.write_bytes(b"previous diagnostic")
        with self.assertRaisesRegex(FileExistsError, "diagnostica"):
            self._run()
        self.assertFalse(self.out.exists())
        self.assertEqual(file.read_bytes(), b"previous diagnostic")



if __name__ == "__main__":
    unittest.main(verbosity=2)
