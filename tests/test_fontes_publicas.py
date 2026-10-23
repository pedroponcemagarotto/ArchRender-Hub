"""Public source catalog contracts: offline, traceable, no implied benchmark."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import metodo_integrado as method  # noqa: E402


class PublicSourceTests(unittest.TestCase):
    def test_01_seven_unique_sources_with_licenses(self):
        items = method.list_public_sources()
        self.assertEqual(7, len(items))
        self.assertEqual(7, len({x["id"] for x in items}))
        self.assertEqual(2, sum(x["type"] == "3d_scene" for x in items))
        self.assertEqual(5, sum(x["type"] == "photo" for x in items))
        self.assertTrue(all(x["source_url"].startswith("https://") for x in items))
        self.assertTrue(all(x["license_url"].startswith("https://") for x in items))

    def test_02_not_downloaded_or_visual_benchmarked(self):
        for item in method.list_public_sources():
            self.assertIs(item["acquired"], False)
            self.assertEqual("nao_executado", item["benchmark_status"])
            self.assertTrue(item["author"])
            self.assertTrue(item["source_url"])

    def test_03_cc_by_requirements_and_cc0_model(self):
        items = {x["id"]: x for x in method.list_public_sources()}
        self.assertEqual("CC0", items["AR-PUB-001"]["license"])
        self.assertEqual("modelo_3d_disponivel", items["AR-PUB-001"]["ground_truth"])
        self.assertEqual("CC BY", items["AR-PUB-002"]["license"])
        self.assertIn("obrigatoria", items["AR-PUB-002"]["attribution"])
        self.assertEqual("apenas_fotografia", items["AR-PUB-005"]["ground_truth"])

    def test_04_cli_filters_are_offline_and_never_claim_generation(self):
        script = ROOT / "tools" / "metodo_integrado.py"
        p = subprocess.run([sys.executable, str(script), "sources", "--category", "lavanderia"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(0, p.returncode, p.stderr)
        self.assertIn("AR-PUB-005", p.stdout)
        self.assertNotIn("AR-PUB-002", p.stdout)
        self.assertIn("Download: nao | Benchmark: nao_executado", p.stdout)
        q = subprocess.run([sys.executable, str(script), "sources", "--json"],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(0, q.returncode, q.stderr)
        self.assertEqual(7, len(json.loads(q.stdout)["assets"]))

    def test_05_duplicate_or_false_download_status_is_refused(self):
        doc = json.loads(method.PUBLIC_SOURCES.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            file = Path(td) / "public.json"
            doc["assets"].append(dict(doc["assets"][0]))
            file.write_text(json.dumps(doc), encoding="utf-8")
            with patch.object(method, "PUBLIC_SOURCES", file):
                with self.assertRaisesRegex(ValueError, "repetidos"):
                    method.list_public_sources()
            doc["assets"].pop()
            doc["assets"][0]["acquired"] = True
            file.write_text(json.dumps(doc), encoding="utf-8")
            with patch.object(method, "PUBLIC_SOURCES", file):
                with self.assertRaisesRegex(ValueError, "sem evidencia de aquisicao"):
                    method.list_public_sources()

            doc["assets"][0]["acquisition_evidence"] = "sha256:verificado-fora-do-github"
            doc["assets"][0]["benchmark_status"] = "executado"
            file.write_text(json.dumps(doc), encoding="utf-8")
            with patch.object(method, "PUBLIC_SOURCES", file):
                with self.assertRaisesRegex(ValueError, "sem evidencia"):
                    method.list_public_sources()

            doc["assets"][0]["benchmark_evidence"] = "AR-PUB-001-R1-RELATORIO"
            file.write_text(json.dumps(doc), encoding="utf-8")
            with patch.object(method, "PUBLIC_SOURCES", file):
                self.assertEqual(7, len(method.list_public_sources()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
