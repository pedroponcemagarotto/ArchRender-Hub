"""Tests for the offline no-API architectural MP4 workflow."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import video_local as vl  # noqa: E402


def make_png(path: Path, color: tuple[int, int, int]) -> None:
    """Use only the stdlib to create tiny valid RGB PNG test fixtures."""
    width, height = 96, 54
    pixels = b"".join(b"\x00" + bytes(color) * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(pixels))
        + chunk(b"IEND", b"")
    )


class OfflineVideoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="archrender_vidtest_")
        self.root = Path(self.tmp.name)
        self.img1 = self.root / "sala.png"
        self.img2 = self.root / "lavanderia.png"
        make_png(self.img1, (175, 175, 168))
        make_png(self.img2, (210, 221, 239))
        self.output = self.root / "apresentacao.mp4"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def args(self) -> object:
        return vl.build_parser().parse_args([
            "-o", str(self.output), "--size", "preview",
            "--seconds", "2", "--fps", "12",
            str(self.img1), str(self.img2),
        ])

    def test_01_script_and_gui_python_syntax(self) -> None:
        for name in ("video_local.py", "video_local_gui.py"):
            ast.parse((TOOLS / name).read_text(encoding="utf-8"))

    def test_02_check_input_and_non_overwrite(self) -> None:
        args = self.args()
        vl.validate_args(args)
        self.output.write_bytes(b"already exists")
        with self.assertRaisesRegex(ValueError, "ja existe"):
            vl.validate_args(args)

    def test_03_unauthorized_extension(self) -> None:
        args = self.args()
        args.images[0] = self.root / "not_an_image.pdf"
        with self.assertRaisesRegex(ValueError, "Imagem ausente"):
            vl.validate_args(args)

    def test_04_motion_filter_and_transition_offsets(self) -> None:
        for motion in vl.MOTIONS[1:]:
            text = vl.motion_filter(motion, 640, 360, 12, 24)
            self.assertIn("zoompan=", text)
            self.assertIn("s=640x360:fps=12", text)
        graph, label = vl.assemble_filter(3, 2.0, 0.5, "dissolve")
        self.assertIn("offset=1.500", graph)
        self.assertIn("offset=3.000", graph)
        self.assertEqual("[x2]", label)
        graph, label = vl.assemble_filter(2, 2.0, 0.5, "cut")
        self.assertIn("concat=n=2", graph)
        self.assertEqual("[vout]", label)

    def test_05_missing_ffmpeg_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "nao existe"):
            vl.find_ffmpeg(str(self.root / "nao_existe_ffmpeg.exe"))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "FFmpeg and ffprobe not installed")
    def test_06_end_to_end_preview_mp4_and_metadata(self) -> None:
        completed = subprocess.run(
            [
                sys.executable, str(TOOLS / "video_local.py"),
                "--output", str(self.output), "--size", "preview",
                "--seconds", "2", "--fps", "12",
                "--motion", "auto", "--transition", "dissolve",
                str(self.img1), str(self.img2),
            ],
            capture_output=True, text=True, timeout=90, check=False
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(self.output.is_file())
        meta = subprocess.check_output([
            shutil.which("ffprobe"), "-v", "error",
            "-show_entries", "stream=codec_name,width,height,avg_frame_rate",
            "-show_entries", "format=duration",
            "-of", "json", str(self.output),
        ], text=True, timeout=15)
        data = json.loads(meta)
        video = next(x for x in data["streams"] if x["codec_name"] == "h264")
        self.assertEqual((video["width"], video["height"]), (640, 360))
        self.assertEqual(video["avg_frame_rate"], "12/1")
        self.assertAlmostEqual(float(data["format"]["duration"]), 3.5, delta=0.2)

    def test_07_reject_existing_output_in_cli(self) -> None:
        self.output.write_bytes(b"original must be preserved")
        old = self.output.read_bytes()
        self.assertEqual(
            2, vl.main(["-o", str(self.output), str(self.img1)])
        )
        self.assertEqual(self.output.read_bytes(), old)


if __name__ == "__main__":
    unittest.main(verbosity=2)
