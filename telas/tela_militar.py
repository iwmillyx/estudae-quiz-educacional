# telas/tela_militar.py
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class NivelView(tk.Frame):
    """
    Versão em Frame da sua tela Militar (antes era Tk).
    Pode ser encaixada dentro do root do projeto (Router).
    """
    def __init__(self, master, subjects, on_voltar=None):
        super().__init__(master, bg="#005227")
        self.subjects = subjects
        self.on_voltar = on_voltar

        # Fontes
        self.title_font = tkfont.Font(family="Segoe UI Semibold", size=22)
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.button_font = tkfont.Font(family="Verdana", size=10)
        self.level_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        # Tema ttk
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#005227")
        style.configure("TLabel", background="#005227", foreground="#f5f5f5")
        style.configure("TButton", font=self.button_font, padding=6)
        style.map(
            "TButton",
            background=[("active", "#EDF3F3"), ("!active", "#03bb85")],
            foreground=[("active", "#0c0c0c"), ("!active", "#050404")],
        )

        # Layout base deste Frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Barra superior (Voltar opcional)
        topbar = tk.Frame(self, bg="#00421F", height=48)
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        if self.on_voltar:
            tk.Button(
                topbar, text="⬅️ Voltar", font=("Segoe UI", 10, "bold"),
                bg="#03bb85", fg="#0a0a0a", relief="flat",
                activebackground="#02a677", activeforeground="white",
                command=self.on_voltar
            ).pack(side="left", padx=10, pady=6)

        # Área principal
        self.main = ttk.Frame(self)
        self.main.grid(row=1, column=0, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Páginas internas
        self.pages = {}
        self._create_military_page()
        self._create_subject_page()
        self._create_ranking_page()
        self._create_user_page()

        # Rodapé
        self._create_footer()

        # Começa na tela militar
        self._show_page("militar")

    # ====================== TELAS ==========================
    def _create_military_page(self):
        page = ttk.Frame(self.main)
        self.pages["militar"] = page
        page.grid(row=0, column=0, sticky="nsew")

        lbl_title = ttk.Label(page, text="Concurso Militar", font=("Segoe UI Semibold", 20))
        lbl_title.pack(pady=(30, 20))

        btn_frame = ttk.Frame(page)
        btn_frame.pack(expand=True)

        def go_subjects():
            self._show_page("materias")

        for i, (txt, emoji) in enumerate([("Exército", "🪖"), ("Marinha", "⚓"), ("Aeronáutica", "✈️")]):
            b = tk.Button(
                btn_frame, text=f"{emoji} {txt}", font=("Segoe UI", 14, "bold"),
                bg="#03bb85", fg="#0a0a0a", width=20, height=2, relief="flat",
                activebackground="#02a677", activeforeground="white",
                command=go_subjects
            )
            b.grid(row=i, column=0, padx=20, pady=10)

    def _create_subject_page(self):
        page = ttk.Frame(self.main)
        self.pages["materias"] = page
        page.grid(row=0, column=0, sticky="nsew")

        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=2)

        # Lista de matérias
        left = ttk.Frame(page, padding=(12, 12))
        left.grid(row=0, column=0, sticky="nsew")

        ttk.Label(left, text="Matérias - Militar", font=("Helvetica", 16, "bold")).pack(anchor="nw", pady=(0, 10))

        self.subject_buttons = {}
        for name in self.subjects:
            btn = ttk.Button(left, text=name, command=lambda n=name: self._select_subject(n))
            btn.pack(fill="x", pady=6)
            self.subject_buttons[name] = btn

        # Detalhes da matéria
        right = ttk.Frame(page, padding=(20, 20))
        right.grid(row=0, column=1, sticky="nsew")

        self.lbl_title = ttk.Label(right, text="", font=("Segoe UI Semibold", 18))
        self.lbl_title.grid(row=0, column=0, sticky="w")

        self.progress = ttk.Progressbar(
            right, orient="horizontal", mode="determinate", maximum=100, style="TProgressbar"
        )
        self.progress.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        style = ttk.Style()
        style.configure("TProgressbar", thickness=18, troughcolor="white", background="#68ddbd")

        self.levels_frame = ttk.Frame(right)
        self.levels_frame.grid(row=2, column=0, sticky="n", pady=(6, 0))

        self.info_label = ttk.Label(right, text="", font=self.button_font)
        self.info_label.grid(row=3, column=0, sticky="w", pady=(14, 0))

        first = next(iter(self.subjects))
        self._select_subject(first)

    def _create_ranking_page(self):
        page = ttk.Frame(self.main)
        self.pages["ranking"] = page
        page.grid(row=0, column=0, sticky="nsew")

        ttk.Label(page, text="🌍 Ranking Global", font=("Segoe UI Semibold", 18)).pack(pady=20)

        columns = ("Posição", "Nome", "Pontos")
        tree = ttk.Treeview(page, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        tree.pack(padx=20, pady=10, fill="x")

        data = [(1, "Amanda", 980), (2, "João", 920), (3, "Maria", 870), (4, "Carlos", 850), (5, "Ana", 820)]
        for row in data:
            tree.insert("", "end", values=row)

    def _create_user_page(self):
        page = ttk.Frame(self.main)
        self.pages["usuario"] = page
        page.grid(row=0, column=0, sticky="nsew")

        ttk.Label(page, text="👤 Perfil do Usuário", font=("Segoe UI Semibold", 18)).pack(pady=20)

        ttk.Label(
            page,
            text="Nome: Amanda\nProgresso total: 67%\nNível geral: Intermediário\n\nContinue estudando! 💪",
            font=self.button_font,
            justify="center",
        ).pack(pady=20)

    # ---------------------- Rodapé --------------------------
    def _create_footer(self):
        self.footer = tk.Frame(self, bg="#00421F", height=60)
        self.footer.grid(row=2, column=0, sticky="ew")
        self.footer.grid_propagate(False)
        self.footer.columnconfigure((0, 1, 2), weight=1, uniform="b")

        self.footer_buttons = {}

        def mk_btn(col, key, text, target):
            btn = tk.Button(
                self.footer, text=text, font=("Segoe UI", 10, "bold"),
                bg="#03bb85", fg="#070606", relief="flat",
                activebackground="#02a677", activeforeground="white",
                command=lambda: self._show_page(target)
            )
            btn.grid(row=0, column=col, sticky="nsew", padx=10, pady=6)
            self.footer_buttons[key] = btn

        mk_btn(0, "militar", "📖\nMilitar", "militar")
        mk_btn(1, "ranking", "🌍\nRanking", "ranking")
        mk_btn(2, "usuario", "👤\nUsuário", "usuario")

    # ====================== FUNÇÕES ==========================
    def _show_page(self, page_name):
        for _, frame in self.pages.items():
            frame.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        for name, btn in self.footer_buttons.items():
            btn.configure(bg="#02a677" if name == page_name else "#03bb85")

    def _select_subject(self, name):
        data = self.subjects[name]
        max_lvl = data["max"]
        current = data.get("current", 0)

        self.lbl_title.config(text=f"{name}")
        pct = int(100 * current / max_lvl) if max_lvl else 0
        self.progress["value"] = pct
        self.info_label.config(text=f"Nível atual: {current} / {max_lvl} ({pct}%)")

        for w in self.levels_frame.winfo_children():
            w.destroy()

        cols = 6
        for i in range(1, max_lvl + 1):
            is_completed = i <= current
            txt = f"Nível {i}"
            color = "#a4fff7" if is_completed else "#18926E"
            fg = "#080808" if is_completed else "#010101"

            b = tk.Button(
                self.levels_frame,
                text=txt, font=self.level_font,
                bg=color, fg=fg,
                activebackground="#005227", activeforeground="#070707",
                width=12, relief="flat", borderwidth=0,
                command=lambda lvl=i: self._toggle_level(lvl)
            )
            b.grid(row=(i - 1) // cols, column=(i - 1) % cols, padx=8, pady=8)
            b.configure(highlightthickness=1, highlightbackground="#038554")

    def _toggle_level(self, lvl):
        data = self.subjects[self.lbl_title.cget("text")]
        max_lvl = data["max"]
        current = data.get("current", 0)
        new_current = lvl - 1 if lvl <= current else lvl
        data["current"] = max(0, min(new_current, max_lvl))
        self._select_subject(self.lbl_title.cget("text"))

# --------- Função que o Router vai chamar ---------
def montar_militar(root, usuario=None, nome=None, on_voltar=None):
    """
    Monta a tela Militar dentro do root já criado pelo projeto.
    """
    # (limpa o root — o router normalmente já faz isso)
    for w in root.winfo_children():
        w.destroy()

    # materias de exemplo; troque pelas reais quando tiver o módulo de dados
    materias = {
        "Matemática": {"max": 3, "current": 2},
        "Português": {"max": 3, "current": 3},
        "Física": {"max": 3, "current": 1},
        "Química": {"max": 3, "current": 0},
        "História": {"max": 3, "current": 2},
        "Geografia": {"max": 3, "current": 2},
        "Inglês": {"max": 3, "current": 1},
    }

    root.title("Estudae - Militar")
    root.geometry("850x580")
    view = NivelView(root, subjects=materias, on_voltar=on_voltar)
    view.pack(fill="both", expand=True)

# ---------- Modo standalone (continua funcionando) ----------
if __name__ == "__main__":
    materias = {
        "Matemática": {"max": 3, "current": 2},
        "Português": {"max": 3, "current": 3},
        "Física": {"max": 3, "current": 1},
        "Química": {"max": 3, "current": 0},
        "História": {"max": 3, "current": 2},
        "Geografia": {"max": 3, "current": 2},
        "Inglês": {"max": 3, "current": 1},
    }
    root = tk.Tk()
    root.title("Estudae - Militar (standalone)")
    root.geometry("850x580")
    NivelView(root, materias).pack(fill="both", expand=True)
    root.mainloop()
