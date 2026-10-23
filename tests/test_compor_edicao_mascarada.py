"""ArchRender R5 regression tests: pixel-exact protection with source masks."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import compor_edicao_mascarada as module


class TestMaskR5(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.original = self.root / "original.png"
        self.edited = self.root / "candidate.png"
        self.mask = self.root / "mask.png"
        self.output = self.root / "result.png"
        self.lock = self.root / "protected.png"
        self.src = Image.new("RGB", (100, 80), (90, 120, 170))
        d = ImageDraw.Draw(self.src)
        d.rectangle((15, 20, 80, 60), fill=(30, 80, 90))
        self.src.save(self.original)
        dst = Image.new("RGB", (100, 80), (240, 25, 25))
        dst.save(self.edited)
        mask = Image.new("L", (100, 80), 0)
        ImageDraw.Draw(mask).rectangle((25, 30, 60, 45), fill=255)
        mask.save(self.mask)
        self.original_hash = hashlib.sha256(self.original.read_bytes()).hexdigest()

    def test_01_exactly_preserves_pixels_outside_mask(self):
        result = module.compose(self.original, self.edited, self.mask, self.output, feather=0)
        self.assertEqual(0, result["locked_pixel_changes"])
        self.assertFalse(result["architectural_approval"])
        with Image.open(self.output) as f:
            self.assertEqual((100, 80), f.size)
            self.assertEqual(f.getpixel((0, 0))[:3], self.src.getpixel((0, 0)))
            self.assertEqual(f.getpixel((30, 32))[:3], (240, 25, 25))
            self.assertEqual(f.getpixel((85, 70))[:3], self.src.getpixel((85, 70)))
        self.assertEqual(hashlib.sha256(self.original.read_bytes()).hexdigest(), self.original_hash)

    def test_02_feather_never_bleeds_into_locked_pixel(self):
        result = module.compose(self.original, self.edited, self.mask, self.output, feather=6)
        with Image.open(self.output) as f:
            self.assertEqual(f.getpixel((24, 35))[:3], self.src.getpixel((24, 35)))
            self.assertEqual(f.getpixel((61, 35))[:3], self.src.getpixel((61, 35)))
            self.assertNotEqual(f.getpixel((25, 35))[:3], self.src.getpixel((25, 35)))
        self.assertEqual(result["outside_edit_mask_pixel_changes"], 0)

    def test_03_hard_protected_mask_overrides_edit_mask(self):
        protected = Image.new("L", (100, 80), 0)
        ImageDraw.Draw(protected).rectangle((40, 30, 45, 45), fill=10)
        protected.save(self.lock)
        result = module.compose(self.original, self.edited, self.mask, self.output, self.lock)
        self.assertLess(result["editable_fraction_after_protection"], result["editable_fraction_before_protection"])
        with Image.open(self.output) as f:
            self.assertEqual(f.getpixel((42, 33))[:3], self.src.getpixel((42, 33)))
            self.assertNotEqual(f.getpixel((33, 33))[:3], self.src.getpixel((33, 33)))

    def test_04_reject_full_or_empty_mask(self):
        Image.new("L", (100, 80), 255).save(self.mask)
        with self.assertRaisesRegex(ValueError, "excede"):
            module.compose(self.original, self.edited, self.mask, self.output)
        Image.new("L", (100, 80), 0).save(self.mask)
        with self.assertRaisesRegex(ValueError, "vazia"):
            module.compose(self.original, self.edited, self.mask, self.output)

    def test_05_never_resize_silently(self):
        Image.new("RGB", (50, 40), (90, 90, 90)).save(self.edited)
        with self.assertRaisesRegex(ValueError, "mesmo tamanho"):
            module.compose(self.original, self.edited, self.mask, self.output)

    def test_06_reject_existing_output_and_overwrite(self):
        with self.assertRaisesRegex(ValueError, "sobrescrever"):
            module.compose(self.original, self.edited, self.mask, self.original)
        self.output.write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            module.compose(self.original, self.edited, self.mask, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing")

    def test_07_protect_100_percent_of_edit_region(self):
        src_mask = Image.open(self.mask)
        src_mask.save(self.lock)
        with self.assertRaisesRegex(ValueError, "Nenhum pixel"):
            module.compose(self.original, self.edited, self.mask, self.output, self.lock)

    def test_08_source_cannot_be_candidate_output(self):
        with self.assertRaisesRegex(ValueError, "sobrescrever"):
            module.compose(self.original, self.edited, self.mask, self.edited)

    def test_09_invalid_color_mask_is_blocked(self):
        Image.new("RGB", (100, 80), (255, 255, 255)).save(self.mask)
        with self.assertRaisesRegex(ValueError, "tons de cinza"):
            module.compose(self.original, self.edited, self.mask, self.output)

    def test_10_alpha_channel_premultiplication_safe(self):
        # Transparent areas remain transparent; no silent geometry crop.
        rgba = self.src.convert("RGBA")
        rgba.putpixel((0, 0), (100, 50, 50, 0))
        rgba.save(self.original)
        result = module.compose(self.original, self.edited, self.mask, self.output)
        with Image.open(self.output) as f:
            self.assertEqual(f.convert("RGBA").getpixel((0, 0)), (100, 50, 50, 0))
        self.assertEqual(result["locked_pixel_changes"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
