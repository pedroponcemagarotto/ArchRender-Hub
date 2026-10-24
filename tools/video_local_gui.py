#!/usr/bin/env python3
"""GUI Windows/Linux/macOS for the offline ArchRender Hub MP4 generator."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

HERE = Path(__file__).resolve().parent
VIDEO_SCRIPT = HERE / "video_local.py"


class VideoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ArchRender Hub | Videos gratuitos no PC")
        self.geometry("780x620")
        self.minsize(660, 560)
        self.files: list[str] = []

        wrapper = ttk.Frame(self, padding=18)
        wrapper.pack(fill="both", expand=True)
        ttk.Label(wrapper, text="Criar video de apresentacao", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(
            wrapper,
            text="100% local: usa as imagens originais aprovadas e FFmpeg. "
                 "Nao gera objetos ou paredes novos.",
            wraplength=700,
        ).pack(anchor="w", pady=(6, 14))

        ttk.Label(wrapper, text="1. Escolha as imagens na ordem desejada").pack(anchor="w")
        list_frame = ttk.Frame(wrapper)
        list_frame.pack(fill="both", expand=True, pady=(5, 8))
        self.listbox = tk.Listbox(list_frame, height=9, selectmode="browse")
        self.listbox.pack(side="left", fill="both", expand=True)
        buttons = ttk.Frame(list_frame)
        buttons.pack(side="left", fill="y", padx=(10, 0))
        for title, action in (
            ("Adicionar", self.add),
            ("Remover", self.remove),
            ("Subir", lambda: self.move(-1)),
            ("Descer", lambda: self.move(1)),
        ):
            ttk.Button(buttons, text=title, command=action).pack(fill="x", pady=3)

        options = ttk.LabelFrame(wrapper, text="2. Configuracao", padding=10)
        options.pack(fill="x", pady=8)
        self.resolution = tk.StringVar(value="720p")
        self.seconds = tk.StringVar(value="4")
        self.transition = tk.StringVar(value="dissolve")
        self.motion = tk.StringVar(value="auto")
        self.audio = tk.StringVar()
        self.ffmpeg = tk.StringVar()

        self._combo(options, 0, "Resolucao", self.resolution, ("720p", "1080p", "vertical"))
        self._combo(options, 1, "Segundos/cena", self.seconds, ("3", "4", "5", "6", "8"))
        self._combo(options, 2, "Transicao", self.transition, ("dissolve", "cut"))
        self._combo(
            options, 3, "Movimento", self.motion,
            ("auto", "zoom-in", "zoom-out", "pan-left", "pan-right", "still")
        )

        ttk.Label(options, text="Musica opcional").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Entry(options, textvariable=self.audio).grid(row=4, column=1, sticky="ew", padx=8)
        ttk.Button(options, text="Escolher...", command=self.pick_audio).grid(row=4, column=2)
        ttk.Label(options, text="FFmpeg.exe (se nao estiver no PATH)").grid(
            row=5, column=0, sticky="w", pady=5
        )
        ttk.Entry(options, textvariable=self.ffmpeg).grid(row=5, column=1, sticky="ew", padx=8)
        ttk.Button(options, text="Localizar...", command=self.pick_ffmpeg).grid(row=5, column=2)
        options.columnconfigure(1, weight=1)

        self.action = ttk.Button(wrapper, text="3. Gerar video MP4", command=self.make_video)
        self.action.pack(fill="x", pady=(9, 6), ipady=5)
        self.message = tk.StringVar(value="Escolha imagens JPG ou PNG para comecar.")
        ttk.Label(wrapper, textvariable=self.message, wraplength=710).pack(anchor="w")
        ttk.Label(
            wrapper,
            text="Observacao: zoom e pan sao movimentos 2D, nao passeio 3D real. "
                 "Para trilhas, use apenas audio de uso autorizado.",
            foreground="#555555", wraplength=700,
        ).pack(anchor="w", pady=(8, 0))

    def _combo(self, parent: ttk.Frame, row: int, label: str, variable: tk.StringVar,
               options: tuple[str, ...]) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(
            parent, textvariable=variable, values=options, state="readonly", width=17
        ).grid(row=row, column=1, sticky="w", padx=8)

    def refresh(self, select: int | None = None) -> None:
        self.listbox.delete(0, tk.END)
        for i, name in enumerate(self.files):
            self.listbox.insert(tk.END, f"{i+1:02d}. {Path(name).name}")
        if select is not None and 0 <= select < len(self.files):
            self.listbox.selection_set(select)
            self.listbox.see(select)

    def add(self) -> None:
        chosen = filedialog.askopenfilenames(
            title="Escolha as imagens aprovadas",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp *.bmp")],
        )
        for filename in chosen:
            if filename not in self.files:
                self.files.append(filename)
        self.refresh(len(self.files) - 1 if self.files else None)

    def selected(self) -> int | None:
        items = self.listbox.curselection()
        return int(items[0]) if items else None

    def remove(self) -> None:
        index = self.selected()
        if index is not None:
            del self.files[index]
            self.refresh(min(index, len(self.files) - 1))

    def move(self, delta: int) -> None:
        index = self.selected()
        if index is None:
            return
        target = index + delta
        if 0 <= target < len(self.files):
            self.files[index], self.files[target] = self.files[target], self.files[index]
            self.refresh(target)

    def pick_audio(self) -> None:
        filename = filedialog.askopenfilename(
            title="Musica local com direitos de uso",
            filetypes=[("Audio", "*.mp3 *.wav *.m4a *.ogg *.flac")],
        )
        if filename:
            self.audio.set(filename)

    def pick_ffmpeg(self) -> None:
        filename = filedialog.askopenfilename(
            title="Localizar o programa FFmpeg",
            filetypes=[("Executavel FFmpeg", "ffmpeg.exe"), ("Todos os arquivos", "*.*")],
        )
        if filename:
            self.ffmpeg.set(filename)

    def make_video(self) -> None:
        if not self.files:
            messagebox.showwarning("Faltam imagens", "Adicione pelo menos uma imagem.")
            return
        save = filedialog.asksaveasfilename(
            title="Onde salvar o video?",
            defaultextension=".mp4",
            initialfile="ArchRender_apresentacao.mp4",
            filetypes=[("Video MP4", "*.mp4")],
        )
        if not save:
            return
        if Path(save).exists():
            messagebox.showerror("Arquivo ja existe", "Escolha outro nome de arquivo para nao sobrescrever.")
            return
        cmd = [
            sys.executable, str(VIDEO_SCRIPT), "--output", save,
            "--size", self.resolution.get(),
            "--seconds", self.seconds.get(),
            "--transition", self.transition.get(),
            "--motion", self.motion.get(),
        ]
        if self.ffmpeg.get().strip():
            cmd += ["--ffmpeg", self.ffmpeg.get().strip()]
        if self.audio.get().strip():
            cmd += ["--audio", self.audio.get().strip()]
        cmd += self.files

        self.action.configure(state="disabled")
        self.message.set("Gerando no PC. O programa continuara aberto ate concluir.")

        def worker() -> None:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.after(0, lambda: self.complete(result, save))

        threading.Thread(target=worker, daemon=True).start()

    def complete(self, result: subprocess.CompletedProcess[str], save: str) -> None:
        self.action.configure(state="normal")
        if result.returncode == 0:
            self.message.set("Video criado: " + save)
            messagebox.showinfo("Video pronto", "Arquivo MP4 salvo com sucesso:\n" + save)
        else:
            details = (result.stderr or result.stdout or "Falha desconhecida").strip()
            self.message.set("O video nao foi criado. Confira FFmpeg, imagens e espaco no disco.")
            messagebox.showerror("Falha ao gerar", details[-2600:])


if __name__ == "__main__":
    VideoApp().mainloop()
