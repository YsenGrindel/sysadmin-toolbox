"""Config Drift Lite — desktop GUI or CLI; Python 3.10+ / Tkinter."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from engine import Comparison, compare, html_report

UI = {
    "fr": {
        "title": "Config Drift Lite — Comparateur de configurations",
        "before": "Avant (reference)",
        "after": "Apres (nouveau)",
        "browse": "Parcourir…",
        "compare": "Comparer les configurations",
        "export": "Exporter le rapport HTML",
        "placeholder": "Selectionnez deux dossiers puis cliquez sur Comparer.",
        "select": "Selectionnez un fichier pour afficher les differences.",
        "unchanged": "Fichier identique dans les deux instantanes.",
        "summary": "Modifies: {modified} | Ajoutes: {added} | Supprimes: {removed} | Identiques: {unchanged} | Ignores: {ignored}",
        "error": "Erreur de comparaison",
        "save_error": "Export impossible",
        "saved": "Rapport enregistre.",
        "safety": "Lecture seule et hors ligne. Les rapports peuvent contenir des informations sensibles.",
        "filename": "Fichier",
        "status": "Statut",
    },
    "en": {
        "title": "Config Drift Lite — Configuration comparator",
        "before": "Before (reference)",
        "after": "After (new)",
        "browse": "Browse…",
        "compare": "Compare configurations",
        "export": "Export HTML report",
        "placeholder": "Select two directories and click Compare.",
        "select": "Select a file to view its differences.",
        "unchanged": "This file is identical in both snapshots.",
        "summary": "Modified: {modified} | Added: {added} | Removed: {removed} | Unchanged: {unchanged} | Skipped: {ignored}",
        "error": "Comparison error",
        "save_error": "Export failed",
        "saved": "Report saved.",
        "safety": "Read-only and offline. Reports may contain sensitive information.",
        "filename": "File",
        "status": "Status",
    },
}


def start_gui(lang: str) -> None:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    T = UI[lang]

    class Window(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.title(T["title"])
            self.geometry("1000x700")
            self.minsize(730, 480)
            self.before_var = tk.StringVar()
            self.after_var = tk.StringVar()
            self.status_var = tk.StringVar(value=T["placeholder"])
            self.result: Comparison | None = None
            self.items: dict[str, int] = {}

            wrapper = ttk.Frame(self, padding=16)
            wrapper.pack(fill="both", expand=True)
            ttk.Label(wrapper, text="Config Drift Lite", font=("Segoe UI", 19, "bold")).pack(anchor="w")
            ttk.Label(wrapper, text=T["safety"], wraplength=850).pack(anchor="w", pady=(2, 16))
            for title, variable in [(T["before"], self.before_var), (T["after"], self.after_var)]:
                line = ttk.Frame(wrapper)
                line.pack(fill="x", pady=4)
                ttk.Label(line, text=title, width=24).pack(side="left")
                ttk.Entry(line, textvariable=variable).pack(side="left", fill="x", expand=True, padx=8)
                ttk.Button(line, text=T["browse"], command=lambda v=variable: self.choose(v)).pack(side="left")

            buttons = ttk.Frame(wrapper)
            buttons.pack(fill="x", pady=(12, 10))
            ttk.Button(buttons, text=T["compare"], command=self.do_compare).pack(side="left")
            self.export_button = ttk.Button(buttons, text=T["export"], command=self.export, state="disabled")
            self.export_button.pack(side="left", padx=10)
            ttk.Label(wrapper, textvariable=self.status_var, wraplength=850).pack(anchor="w", pady=(0, 10))

            pane = ttk.Panedwindow(wrapper, orient="vertical")
            pane.pack(fill="both", expand=True)
            top = ttk.Frame(pane)
            bottom = ttk.Frame(pane)
            pane.add(top, weight=2)
            pane.add(bottom, weight=3)
            self.tree = ttk.Treeview(top, columns=("status", "path"), show="headings", selectmode="browse")
            self.tree.heading("status", text=T["status"])
            self.tree.heading("path", text=T["filename"])
            self.tree.column("status", width=120, stretch=False)
            self.tree.column("path", width=680, stretch=True)
            tree_scroll = ttk.Scrollbar(top, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=tree_scroll.set)
            tree_scroll.pack(side="right", fill="y")
            self.tree.pack(fill="both", expand=True)
            self.tree.bind("<<TreeviewSelect>>", self.show_change)
            self.diff = tk.Text(bottom, wrap="none", font=("Consolas", 10), state="disabled")
            yscroll = ttk.Scrollbar(bottom, orient="vertical", command=self.diff.yview)
            xscroll = ttk.Scrollbar(bottom, orient="horizontal", command=self.diff.xview)
            self.diff.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
            yscroll.pack(side="right", fill="y")
            xscroll.pack(side="bottom", fill="x")
            self.diff.pack(fill="both", expand=True)
            self.set_diff(T["select"])

        def choose(self, variable: "tk.StringVar") -> None:
            selected = filedialog.askdirectory(parent=self)
            if selected:
                variable.set(selected)

        def set_diff(self, value: str) -> None:
            self.diff.configure(state="normal")
            self.diff.delete("1.0", "end")
            self.diff.insert("1.0", value)
            self.diff.configure(state="disabled")

        def do_compare(self) -> None:
            try:
                result = compare(self.before_var.get(), self.after_var.get())
            except (OSError, ValueError) as exc:
                messagebox.showerror(T["error"], str(exc), parent=self)
                return
            self.result = result
            self.items = {}
            self.tree.delete(*self.tree.get_children())
            for i, change in enumerate(result.changes):
                item = self.tree.insert("", "end", values=(change.status, change.path))
                self.items[item] = i
            counts = result.counts()
            self.status_var.set(T["summary"].format(**counts, ignored=len(result.skipped)))
            self.set_diff(T["select"])
            self.export_button.configure(state="normal")

        def show_change(self, _event: object) -> None:
            selection = self.tree.selection()
            if selection and self.result is not None:
                change = self.result.changes[self.items[selection[0]]]
                self.set_diff(change.diff() or T["unchanged"])

        def export(self) -> None:
            if self.result is None:
                return
            chosen = filedialog.asksaveasfilename(
                parent=self, title=T["export"], defaultextension=".html",
                filetypes=[("HTML", "*.html")], initialfile="config-drift-report.html",
            )
            if not chosen:
                return
            try:
                Path(chosen).write_text(html_report(self.result), encoding="utf-8")
                messagebox.showinfo(T["export"], T["saved"], parent=self)
            except OSError as exc:
                messagebox.showerror(T["save_error"], str(exc), parent=self)

    Window().mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two local configuration snapshots offline, in GUI or CLI mode."
    )
    parser.add_argument("--before", help="Reference directory (CLI mode)")
    parser.add_argument("--after", help="New directory (CLI mode)")
    parser.add_argument("--report", help="Write local HTML report (CLI mode)")
    parser.add_argument("--lang", choices=("fr", "en"), default="fr", help="GUI language")
    args = parser.parse_args()
    if bool(args.before) != bool(args.after):
        parser.error("--before and --after must be provided together.")
    if args.report and not args.before:
        parser.error("--report requires --before and --after.")
    if not args.before:
        try:
            start_gui(args.lang)
            return 0
        except ImportError as exc:
            print(f"Tkinter not available: {exc}", file=sys.stderr)
            return 2
    try:
        result = compare(args.before, args.after)
        counts = result.counts()
        for status, count in counts.items():
            print(f"{status}: {count}")
        print(f"skipped: {len(result.skipped)}")
        for change in result.changes:
            if change.status != "unchanged":
                print(f"[{change.status}] {change.path}")
        if args.report:
            Path(args.report).write_text(html_report(result), encoding="utf-8")
            print(f"Report saved: {args.report}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
