#!/usr/bin/env python3
"""ArchRender Hub: free offline MP4 from approved still images.

Requires Python 3.9+ and an FFmpeg executable with libx264 in PATH (or --ffmpeg).
No Python packages, generative AI, account, telemetry, or remote API.
All image operations are affine crop/pan/zoom; no unseen geometry is invented.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Optional

RESOLUTIONS = {
    "preview": (640, 360),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "vertical": (1080, 1920),
}
SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
SUPPORTED_AUDIO = {".mp3", ".m4a", ".wav", ".ogg", ".flac"}
MOTIONS = ("auto", "zoom-in", "zoom-out", "pan-left", "pan-right", "still")


def find_ffmpeg(explicit: Optional[str]) -> str:
    """Allow user-selected ffmpeg.exe; never download or execute a shell string."""
    if explicit:
        candidate = Path(explicit).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())
        found = shutil.which(explicit)
        if found:
            return found
        raise ValueError("FFmpeg informado nao existe: " + explicit)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise ValueError(
        "FFmpeg nao encontrado. Instale a versao gratuita de "
        "https://ffmpeg.org/download.html e adicione ffmpeg ao PATH, "
        "ou informe --ffmpeg C:\\caminho\\ffmpeg.exe"
    )


def validate_args(args: argparse.Namespace) -> None:
    if not 1 <= len(args.images) <= 20:
        raise ValueError("Escolha entre 1 e 20 imagens por video.")
    for image in args.images:
        if not image.is_file() or image.suffix.lower() not in SUPPORTED_IMAGES:
            raise ValueError("Imagem ausente ou formato nao permitido: " + str(image))
    if args.output.suffix.lower() != ".mp4":
        raise ValueError("O arquivo final deve ter a extensao .mp4")
    if args.output.exists():
        raise ValueError("O video final ja existe. Escolha outro nome para evitar sobrescrita.")
    if any(x.resolve() == args.output.resolve() for x in args.images):
        raise ValueError("Nao use a imagem de entrada como destino.")
    if not 2.0 <= args.seconds <= 12.0:
        raise ValueError("Duracao por imagem deve ser de 2 a 12 segundos.")
    if not 12 <= args.fps <= 30:
        raise ValueError("FPS deve estar entre 12 e 30.")
    if not 0.0 <= args.fade <= 1.5:
        raise ValueError("Transicao deve durar de 0 a 1,5 segundo.")
    if args.transition == "dissolve" and len(args.images) > 1:
        if args.fade <= 0 or args.fade >= args.seconds / 2:
            raise ValueError("Transicao dissolve deve ser maior que zero e menor que metade da cena.")
    if args.audio is not None:
        if not args.audio.is_file() or args.audio.suffix.lower() not in SUPPORTED_AUDIO:
            raise ValueError("Arquivo de audio ausente ou formato nao permitido.")
    if args.quality < 17 or args.quality > 30:
        raise ValueError("Qualidade CRF deve estar entre 17 e 30.")


def motion_filter(motion: str, width: int, height: int, fps: int, frames: int) -> str:
    """Build spatially modest camera movement without hallucinating room structure."""
    n = max(1, frames - 1)
    if motion == "zoom-in":
        zoom = f"1+0.07*on/{n}"
        x = "iw/2-iw/zoom/2"
        y = "ih/2-ih/zoom/2"
    elif motion == "zoom-out":
        zoom = f"1.07-0.07*on/{n}"
        x = "iw/2-iw/zoom/2"
        y = "ih/2-ih/zoom/2"
    elif motion == "pan-left":
        zoom = "1.07"
        x = f"(iw-iw/zoom)*(1-on/{n})"
        y = "ih/2-ih/zoom/2"
    elif motion == "pan-right":
        zoom = "1.07"
        x = f"(iw-iw/zoom)*on/{n}"
        y = "ih/2-ih/zoom/2"
    elif motion == "still":
        zoom = "1"
        x = "0"
        y = "0"
    else:
        raise ValueError("Movimento invalido: " + motion)

    # Letterboxing preserves all source edges; no hardcoded 16:9 crop.
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x16191e,"
        "setsar=1,"
        f"zoompan=z='{zoom}':x='{x}':y='{y}':"
        f"d=1:s={width}x{height}:fps={fps},"
        "format=yuv420p"
    )


def assemble_filter(count: int, seconds: float, fade: float, transition: str) -> tuple[str, str]:
    """Return FFmpeg filtergraph and output label for a sequence of clips."""
    if count < 2:
        raise ValueError("assemble_filter requires 2 or more clips.")
    # Each shot was rendered at precisely the same FPS, dimensions and timebase.
    # Applying additional setpts/fps/settb filters here can erase the constant
    # framerate metadata and make FFmpeg's xfade reject otherwise valid clips.
    if transition == "cut":
        chain = "".join(f"[{i}:v]" for i in range(count))
        return chain + f"concat=n={count}:v=1:a=0[vout]", "[vout]"

    parts: list[str] = []
    previous = "[0:v]"
    for i in range(1, count):
        name = f"[x{i}]"
        offset = i * (seconds - fade)
        parts.append(
            f"{previous}[{i}:v]xfade=transition=fade:"
            f"duration={fade:.3f}:offset={offset:.3f}{name}"
        )
        previous = name
    return ";".join(parts), previous


def run_ffmpeg(args: list[str]) -> None:
    completed = subprocess.run(args, capture_output=True, text=True, check=False)
    if completed.returncode:
        err = (completed.stderr or completed.stdout or "Erro desconhecido do FFmpeg").strip()
        raise RuntimeError("FFmpeg falhou: " + err[-4000:])


def render(args: argparse.Namespace) -> Path:
    validate_args(args)
    ffmpeg = find_ffmpeg(args.ffmpeg)
    width, height = RESOLUTIONS[args.size]
    frames = round(args.seconds * args.fps)
    image_seconds = frames / args.fps
    total_seconds = len(args.images) * image_seconds
    if args.transition == "dissolve" and len(args.images) > 1:
        total_seconds -= (len(args.images) - 1) * args.fade

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="archrender_video_") as work:
        root = Path(work)
        shots: list[Path] = []
        for index, image in enumerate(args.images):
            motion = args.motion
            if motion == "auto":
                motion = ("zoom-in", "pan-right", "zoom-out", "pan-left")[index % 4]
            shot = root / f"shot_{index:03d}.mp4"
            print(f"Preparando plano {index+1}/{len(args.images)}: {image.name} ({motion})", flush=True)
            cmd = [
                ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
                "-loop", "1", "-framerate", str(args.fps), "-i", str(image),
                "-vf", motion_filter(motion, width, height, args.fps, frames),
                "-frames:v", str(frames),
                "-r", str(args.fps), "-an",
                "-c:v", "libx264", "-preset", "veryfast",
                "-crf", str(args.quality), "-pix_fmt", "yuv420p",
                "-threads", "2", str(shot),
            ]
            run_ffmpeg(cmd)
            shots.append(shot)

        # Keep a one-shot project as a simple copy when no soundtrack is supplied.
        if len(shots) == 1 and args.audio is None:
            shutil.copy2(shots[0], args.output)
        else:
            cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
            for shot in shots:
                cmd += ["-i", str(shot)]
            if args.audio is not None:
                cmd += ["-stream_loop", "-1", "-i", str(args.audio)]
            if len(shots) == 1:
                video_map = "0:v:0"
            else:
                graph, video_map = assemble_filter(
                    len(shots), image_seconds, args.fade, args.transition
                )
                cmd += ["-filter_complex", graph]
            cmd += ["-map", video_map]
            if args.audio is not None:
                audio_index = len(shots)
                cmd += ["-map", f"{audio_index}:a:0", "-c:a", "aac", "-b:a", "160k"]
            else:
                cmd += ["-an"]
            cmd += [
                "-c:v", "libx264", "-preset", "veryfast", "-crf",
                str(args.quality), "-pix_fmt", "yuv420p",
                "-threads", "2", "-t", f"{total_seconds:.3f}",
                "-movflags", "+faststart", str(args.output),
            ]
            run_ffmpeg(cmd)
    print(f"MP4 gerado: {args.output} | {total_seconds:.1f} s | {width}x{height}", flush=True)
    return args.output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ArchRender Hub: video arquitetonico offline gratuito (FFmpeg)."
    )
    parser.add_argument("images", nargs="+", type=Path, help="Imagens aprovadas na ordem das cenas.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Destino .mp4")
    parser.add_argument("--seconds", type=float, default=4.0, help="Segundos por imagem (2 a 12).")
    parser.add_argument("--size", choices=RESOLUTIONS, default="720p")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--motion", choices=MOTIONS, default="auto")
    parser.add_argument("--transition", choices=("dissolve", "cut"), default="dissolve")
    parser.add_argument("--fade", type=float, default=0.5, help="Duracao do dissolve.")
    parser.add_argument("--audio", type=Path, help="Musica local com direitos de uso.")
    parser.add_argument("--quality", type=int, default=21, help="CRF H.264: 17 a 30; menor = melhor.")
    parser.add_argument("--ffmpeg", type=str, help="Caminho opcional para ffmpeg.exe.")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        render(args)
        return 0
    except (ValueError, RuntimeError, OSError) as error:
        print("ERRO: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
