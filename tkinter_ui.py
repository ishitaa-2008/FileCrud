import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import os

# ── Theme constants ───────────────────────────────────────────────────────────
BG        = "#0d0d0d"
BG2       = "#141414"
BG3       = "#1a1a1a"
BORDER    = "#2a2a2a"
FG        = "#f0f0f0"
FG_DIM    = "#888888"
ACCENT    = "#e8ff47"
ACCENT_FG = "#0d0d0d"
RED       = "#ff5c5c"
GREEN     = "#9effa0"
FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_H1   = ("Segoe UI", 13, "bold")


# ── Helper ────────────────────────────────────────────────────────────────────

def list_items() -> list:
    return sorted(Path('').rglob('*'))


# ── Main Application ──────────────────────────────────────────────────────────

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🗂️  File Manager — CRUD")
        self.geometry("900x620")
        self.minsize(760, 520)
        self.configure(bg=BG)
        self.resizable(True, True)

        # Style ttk widgets
        self._apply_style()
        self._build_layout()

    # ── Styling ───────────────────────────────────────────────────────────────
    def _apply_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame",       background=BG)
        style.configure("TLabel",       background=BG,  foreground=FG,       font=FONT_UI)
        style.configure("Dim.TLabel",   background=BG,  foreground=FG_DIM,   font=("Segoe UI", 9))
        style.configure("H1.TLabel",    background=BG,  foreground=FG,       font=FONT_H1)
        style.configure("Accent.TLabel",background=BG,  foreground=ACCENT,   font=FONT_BOLD)

        style.configure("TButton",
            background=ACCENT, foreground=ACCENT_FG,
            font=FONT_BOLD, borderwidth=0, focuscolor=ACCENT,
            padding=(14, 6)
        )
        style.map("TButton",
            background=[("active", "#fff"), ("pressed", "#c8df30")],
            foreground=[("active", ACCENT_FG)]
        )

        style.configure("Danger.TButton",
            background=RED, foreground="#fff",
            font=FONT_BOLD, borderwidth=0, padding=(14, 6)
        )
        style.map("Danger.TButton",
            background=[("active", "#ff8080"), ("pressed", "#cc3333")]
        )

        style.configure("TEntry",
            fieldbackground=BG3, foreground=FG,
            insertcolor=ACCENT, bordercolor=BORDER,
            lightcolor=BORDER, darkcolor=BORDER,
            font=FONT_MONO, padding=6
        )

        style.configure("Sidebar.TFrame", background="#111")
        style.configure("Sidebar.TButton",
            background="#1a1a1a", foreground=FG_DIM,
            font=FONT_UI, borderwidth=0, anchor="w", padding=(12, 8)
        )
        style.map("Sidebar.TButton",
            background=[("active", "#252525"), ("selected", "#1f1f1f")],
            foreground=[("active", FG)]
        )
        style.configure("Active.Sidebar.TButton",
            background="#1f1f1f", foreground=ACCENT,
            font=FONT_BOLD, borderwidth=0, anchor="w", padding=(12, 8)
        )

        style.configure("TScrollbar",
            background=BG3, troughcolor=BG, bordercolor=BG,
            arrowcolor=FG_DIM
        )

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # ── Top bar ────────────────────────────────────────────────────────────
        top = ttk.Frame(self, style="Sidebar.TFrame")
        top.pack(fill="x", side="top")
        ttk.Label(top, text="  🗂️  File Manager",
                  background="#111", foreground=FG,
                  font=("Segoe UI", 12, "bold")).pack(side="left", padx=10, pady=10)
        ttk.Label(top, text=f"  cwd: {Path.cwd()}",
                  background="#111", foreground=FG_DIM,
                  font=("Courier New", 8)).pack(side="right", padx=14, pady=10)

        # ── Body container ─────────────────────────────────────────────────────
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # ── Sidebar ────────────────────────────────────────────────────────────
        self.sidebar = ttk.Frame(body, style="Sidebar.TFrame", width=195)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        sep = tk.Frame(body, bg=BORDER, width=1)
        sep.pack(side="left", fill="y")

        # ── Main panel ─────────────────────────────────────────────────────────
        self.main = ttk.Frame(body)
        self.main.pack(side="left", fill="both", expand=True)

        # Build sidebar buttons
        self.nav_buttons = {}
        ops = [
            ("📄  Create File",   self.show_create_file),
            ("👁️   Read File",    self.show_read_file),
            ("✏️   Update File",  self.show_update_file),
            ("🗑️   Delete File",  self.show_delete_file),
            ("🔤  Rename File",   self.show_rename_file),
            ("📁  Create Folder", self.show_create_folder),
            ("🗑️   Delete Folder",self.show_delete_folder),
            ("📋  List All",      self.show_list_all),
        ]
        ttk.Label(self.sidebar, text="  OPERATIONS",
                  background="#111", foreground=FG_DIM,
                  font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=6, pady=(16, 4))

        for label, cmd in ops:
            btn = ttk.Button(self.sidebar, text=label,
                             style="Sidebar.TButton",
                             command=lambda c=cmd, l=label: self._nav(l, c))
            btn.pack(fill="x", padx=6, pady=1)
            self.nav_buttons[label] = btn

        self._active_nav = None
        # Default view
        self.show_list_all()
        self._nav("📋  List All", self.show_list_all)

    def _nav(self, label, cmd):
        """Highlight active sidebar button and render panel."""
        if self._active_nav and self._active_nav in self.nav_buttons:
            self.nav_buttons[self._active_nav].configure(style="Sidebar.TButton")
        self._active_nav = label
        self.nav_buttons[label].configure(style="Active.Sidebar.TButton")
        cmd()

    # ── Panel helpers ─────────────────────────────────────────────────────────
    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _header(self, text):
        ttk.Label(self.main, text=text, style="H1.TLabel").pack(
            anchor="w", padx=24, pady=(22, 4))
        tk.Frame(self.main, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(0, 14))

    def _label(self, parent, text, dim=False):
        style = "Dim.TLabel" if dim else "TLabel"
        ttk.Label(parent, text=text, style=style).pack(anchor="w", pady=(0, 2))

    def _entry(self, parent, placeholder="") -> ttk.Entry:
        e = ttk.Entry(parent, font=FONT_MONO)
        if placeholder:
            e.insert(0, placeholder)
            e.configure(foreground=FG_DIM)
            def on_focus_in(event, entry=e, ph=placeholder):
                if entry.get() == ph:
                    entry.delete(0, "end")
                    entry.configure(foreground=FG)
            def on_focus_out(event, entry=e, ph=placeholder):
                if not entry.get():
                    entry.insert(0, ph)
                    entry.configure(foreground=FG_DIM)
            e.bind("<FocusIn>",  on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
        e.pack(fill="x", pady=(0, 10))
        return e

    def _text_area(self, parent, height=7) -> scrolledtext.ScrolledText:
        t = scrolledtext.ScrolledText(
            parent, height=height, font=FONT_MONO,
            bg=BG3, fg=FG, insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightbackground=BORDER, highlightthickness=1,
            wrap="word"
        )
        t.pack(fill="both", expand=False, pady=(0, 10))
        return t

    def _msg(self, parent, text, kind="info"):
        colors = {"info": ACCENT, "success": GREEN, "error": RED, "warn": "#ffcc44"}
        color  = colors.get(kind, FG)
        lbl = tk.Label(parent, text=text, bg=BG2, fg=color,
                       font=FONT_MONO, wraplength=520, justify="left",
                       padx=10, pady=6, relief="flat")
        lbl.pack(fill="x", pady=(6, 0))
        return lbl

    def _file_list_box(self, parent):
        """Render scrollable file listing."""
        frame = tk.Frame(parent, bg=BG2, bd=0, highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="both", expand=False, pady=(0, 14))

        canvas = tk.Canvas(frame, bg=BG2, height=160, bd=0, highlightthickness=0)
        sb     = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=BG2)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)

        canvas.pack(side="left",  fill="both", expand=True)
        sb.pack(side="right", fill="y")

        items = list_items()
        if not items:
            tk.Label(inner, text="  📭 No items found.", bg=BG2,
                     fg=FG_DIM, font=FONT_MONO).pack(anchor="w", padx=10, pady=8)
        else:
            for item in items:
                icon = "📁" if item.is_dir() else "📄"
                tk.Label(inner, text=f"  {icon}  {item}", bg=BG2,
                         fg=GREEN, font=FONT_MONO).pack(anchor="w", padx=6, pady=1)

    def _get_entry_val(self, entry: ttk.Entry, placeholder="") -> str:
        val = entry.get().strip()
        return "" if val == placeholder else val

    # ── Views ─────────────────────────────────────────────────────────────────

    def show_create_file(self):
        self._clear_main()
        self._header("📄  Create File")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "File name")
        name_entry = self._entry(pad, "e.g. notes.txt")
        self._label(pad, "Content")
        content_box = self._text_area(pad)
        msg_frame = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_create():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. notes.txt")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a file name.", "warn"); return
            p = Path(name)
            if p.exists():
                self._msg(msg_frame, f"✖  '{name}' already exists.", "error"); return
            try:
                p.write_text(content_box.get("1.0", "end-1c"))
                self._msg(msg_frame, f"✔  '{name}' created successfully!", "success")
            except Exception as e:
                self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Create File", command=on_create).pack(anchor="w", pady=(4, 0))

    def show_read_file(self):
        self._clear_main()
        self._header("👁️  Read File")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "File name")
        name_entry = self._entry(pad, "e.g. notes.txt")
        content_lbl = tk.Label(pad, text="", bg=BG, fg=FG_DIM,
                               font=FONT_MONO, justify="left")
        content_lbl.pack(anchor="w")

        output_box = scrolledtext.ScrolledText(
            pad, height=8, font=FONT_MONO,
            bg=BG2, fg=GREEN, state="disabled",
            relief="flat", bd=0,
            highlightbackground=BORDER, highlightthickness=1
        )
        output_box.pack(fill="both", pady=(4, 8))

        msg_frame = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_read():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. notes.txt")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a file name.", "warn"); return
            p = Path(name)
            if not p.exists():
                self._msg(msg_frame, f"✖  '{name}' not found.", "error"); return
            if p.is_dir():
                self._msg(msg_frame, "⚠ That is a folder, not a file.", "warn"); return
            try:
                data = p.read_text()
                output_box.configure(state="normal")
                output_box.delete("1.0", "end")
                output_box.insert("1.0", data)
                output_box.configure(state="disabled")
                content_lbl.configure(text=f"📄 {name}", fg=ACCENT)
            except Exception as e:
                self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Read File", command=on_read).pack(anchor="w")

    def show_update_file(self):
        self._clear_main()
        self._header("✏️  Update File")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "File name")
        name_entry = self._entry(pad, "e.g. notes.txt")

        mode_var = tk.StringVar(value="Overwrite")
        mode_row = ttk.Frame(pad); mode_row.pack(anchor="w", pady=(0, 8))
        for m in ("Overwrite", "Append"):
            tk.Radiobutton(
                mode_row, text=m, variable=mode_var, value=m,
                bg=BG, fg=FG, selectcolor=BG3,
                activebackground=BG, activeforeground=ACCENT,
                font=FONT_UI
            ).pack(side="left", padx=(0, 16))

        self._label(pad, "New content")
        content_box = self._text_area(pad)
        msg_frame = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_update():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. notes.txt")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a file name.", "warn"); return
            p = Path(name)
            if not p.exists():
                self._msg(msg_frame, f"✖  '{name}' not found.", "error"); return
            content = content_box.get("1.0", "end-1c")
            try:
                if mode_var.get() == "Overwrite":
                    p.write_text(content)
                    self._msg(msg_frame, "✔  File overwritten successfully!", "success")
                else:
                    with open(p, 'a') as f:
                        f.write("\n" + content)
                    self._msg(msg_frame, "✔  Content appended successfully!", "success")
            except Exception as e:
                self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Update File", command=on_update).pack(anchor="w")

    def show_delete_file(self):
        self._clear_main()
        self._header("🗑️  Delete File")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "File name")
        name_entry = self._entry(pad, "e.g. notes.txt")
        self._label(pad, "⚠  This action cannot be undone.", dim=True)
        msg_frame = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_delete():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. notes.txt")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a file name.", "warn"); return
            p = Path(name)
            if not p.exists():
                self._msg(msg_frame, f"✖  '{name}' not found.", "error"); return
            if p.is_dir():
                self._msg(msg_frame, "⚠ That is a folder. Use Delete Folder.", "warn"); return
            if messagebox.askyesno("Confirm Delete", f"Delete '{name}'?"):
                try:
                    os.remove(p)
                    self._msg(msg_frame, f"✔  '{name}' deleted.", "success")
                except Exception as e:
                    self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Delete File", style="Danger.TButton",
                   command=on_delete).pack(anchor="w", pady=(6, 0))

    def show_rename_file(self):
        self._clear_main()
        self._header("🔤  Rename File")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "Current file name")
        name_entry = self._entry(pad, "e.g. old_name.txt")
        self._label(pad, "New file name")
        new_entry  = self._entry(pad, "e.g. new_name.txt")
        msg_frame  = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_rename():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. old_name.txt")
            new  = self._get_entry_val(new_entry,  "e.g. new_name.txt")
            if not name or not new:
                self._msg(msg_frame, "⚠ Please fill in both fields.", "warn"); return
            p = Path(name)
            if not p.exists():
                self._msg(msg_frame, f"✖  '{name}' not found.", "error"); return
            try:
                p.rename(new)
                self._msg(msg_frame, f"✔  Renamed to '{new}'.", "success")
            except Exception as e:
                self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Rename", command=on_rename).pack(anchor="w")

    def show_create_folder(self):
        self._clear_main()
        self._header("📁  Create Folder")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "Folder name")
        name_entry = self._entry(pad, "e.g. my_folder")
        msg_frame  = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_create():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. my_folder")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a folder name.", "warn"); return
            p = Path(name)
            if p.exists():
                self._msg(msg_frame, f"✖  '{name}' already exists.", "error"); return
            try:
                p.mkdir(parents=True)
                self._msg(msg_frame, f"✔  Folder '{name}' created!", "success")
            except Exception as e:
                self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Create Folder", command=on_create).pack(anchor="w")

    def show_delete_folder(self):
        self._clear_main()
        self._header("🗑️  Delete Folder")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        self._label(pad, "Existing files & folders:")
        self._file_list_box(pad)

        self._label(pad, "Folder name")
        name_entry = self._entry(pad, "e.g. my_folder")
        self._label(pad, "⚠  Folder must be empty.", dim=True)
        msg_frame  = ttk.Frame(pad); msg_frame.pack(fill="x")

        def on_delete():
            for w in msg_frame.winfo_children(): w.destroy()
            name = self._get_entry_val(name_entry, "e.g. my_folder")
            if not name:
                self._msg(msg_frame, "⚠ Please enter a folder name.", "warn"); return
            p = Path(name)
            if not p.exists():
                self._msg(msg_frame, f"✖  '{name}' not found.", "error"); return
            if not p.is_dir():
                self._msg(msg_frame, "⚠ That is a file. Use Delete File.", "warn"); return
            if messagebox.askyesno("Confirm Delete", f"Delete folder '{name}'?"):
                try:
                    p.rmdir()
                    self._msg(msg_frame, f"✔  Folder '{name}' deleted.", "success")
                except OSError:
                    self._msg(msg_frame, "✖  Folder is not empty.", "error")
                except Exception as e:
                    self._msg(msg_frame, f"Error: {e}", "error")

        ttk.Button(pad, text="Delete Folder", style="Danger.TButton",
                   command=on_delete).pack(anchor="w", pady=(6, 0))

    def show_list_all(self):
        self._clear_main()
        self._header("📋  All Files & Folders")
        pad = ttk.Frame(self.main); pad.pack(fill="both", padx=24, expand=True)

        items = list_items()
        ttk.Label(pad, text=f"{len(items)} item(s) found",
                  style="Dim.TLabel").pack(anchor="w", pady=(0, 8))

        frame = tk.Frame(pad, bg=BG2, highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame, bg=BG2, bd=0, highlightthickness=0)
        sb     = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=BG2)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        if not items:
            tk.Label(inner, text="  📭 No items.", bg=BG2,
                     fg=FG_DIM, font=FONT_MONO).pack(anchor="w", padx=12, pady=10)
        else:
            for item in items:
                icon  = "📁" if item.is_dir() else "📄"
                color = "#7eb8ff" if item.is_dir() else GREEN
                tk.Label(inner, text=f"  {icon}  {item}", bg=BG2,
                         fg=color, font=FONT_MONO).pack(anchor="w", padx=10, pady=2)

        ttk.Button(pad, text="↺  Refresh",
                   command=self.show_list_all).pack(anchor="w", pady=(10, 0))


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()
