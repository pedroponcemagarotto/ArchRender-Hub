"""Offline tests of the optional geometry-preserving photometric workflow."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from PIL import Image
    import refino_fotometrico as tool
except (ImportError, SystemExit):
    Image = None
    tool = None


@unittest.skipUnless(Image is not None and tool is not None, "Pillow opcional ausente")
class PhotometricTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="archrender_color_")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.original = self.root / "original.png"
        base = Image.new("RGB", (16, 12), (105, 125, 142))
        for y in range(5, 11):
            for x in range(8, 14):
                base.putpixel((x, y), (26, 35, 50))
        base.save(self.original)
        self.original_hash = hashlib.sha256(self.original.read_bytes()).hexdigest()

    def test_01_retains_dimensions_and_source_bytes(self):
        target = self.root / "result.png"
        metadata = tool.render(self.original, target, "interior")
        self.assertEqual((16, 12), (metadata["width"], metadata["height"]))
        self.assertFalse(metadata["geometry_edited"])
        self.assertFalse(metadata["new_objects_generated"])
        self.assertEqual(self.original_hash,
                         hashlib.sha256(self.original.read_bytes()).hexdigest())
        with Image.open(target) as result:
            self.assertEqual((16, 12), result.size)
            self.assertEqual("PNG", result.format)
            self.assertNotEqual(result.convert("RGB").getpixel((8, 6)), (26, 35, 50))

    def test_02_blocks_input_overwrite_and_existing_result(self):
        with self.assertRaisesRegex(ValueError, "sobrescreva"):
            tool.render(self.original, self.original)
        target = self.root / "result.png"
        tool.render(self.original, target)
        with self.assertRaises(FileExistsError):
            tool.render(self.original, target)

    def test_03_rejects_bad_preset_and_output_format(self):
        with self.assertRaisesRegex(ValueError, "Preset"):
            tool.render(self.original, self.root / "good.png", "unknown")
        with self.assertRaisesRegex(ValueError, "PNG ou JPEG"):
            tool.render(self.original, self.root / "out.tiff")

    def test_04_presets_produce_different_photometric_results(self):
        a = self.root / "a.png"
        b = self.root / "b.png"
        tool.render(self.original, a, "interior")
        tool.render(self.original, b, "lavanderia")
        self.assertNotEqual(hashlib.sha256(a.read_bytes()).digest(),
                            hashlib.sha256(b.read_bytes()).digest())
        with Image.open(a) as img:
            self.assertEqual(img.size, (16, 12))
        with Image.open(b) as img:
            self.assertEqual(img.size, (16, 12))


if __name__ == "__main__":
    unittest.main(verbosity=2)
