import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class NivelApp(tk.Tk):
    def __init__(self, subjects_by_area):
        super().__init__()
        self.title("Estudae - ENEM")
        self.geometry("850x580")
        self.configure(bg="#005227")
        self.minsize(700, 450)
        self.subjects_by_area = subjects_by_area
        self.current_area = None
        self.subjects = {}

        # Fontes
        self.title_font = tkfont.Font(family="Segoe UI Semibold", size=22)
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.button_font = tkfont.Font(family="Verdana", size=10)
        self.level_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        # Tema ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#005227")
        style.configure("TLabel", background="#005227", foreground="#f5f5f5")
        style.configure("TButton", font=self.button_font, padding=6)
        style.map("TButton",
                  background=[("active", "#EDF3F3"), ("!active", "#03bb85")],
                  foreground=[("active", "#0c0c0c"), ("!active", "#050404")])

        # Área principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Páginas
        self.pages = {}
        self.create_area_page()
        self.create_subject_page()
        self.create_ranking_page()
        self.create_user_page()

        # Rodapé
        self.create_footer()

        # Começa direto na tela de áreas
        self.show_page("areas")

    # ====================== TELAS ==========================

    def create_area_page(self):
        """Tela com botões das áreas"""
        page = ttk.Frame(self.main_frame)
        self.pages["areas"] = page
        page.grid(row=0, column=0, sticky="nsew")

        lbl = ttk.Label(page, text="ENEM - Áreas do Conhecimento", font=self.title_font)
        lbl.pack(pady=30)

        areas_frame = ttk.Frame(page)
        areas_frame.pack(pady=20)

        for area in self.subjects_by_area:
            btn = ttk.Button(
                areas_frame,
                text=area,
                command=lambda a=area: self.open_area(a)
            )
            btn.pack(pady=8, ipadx=10, ipady=5, fill="x")

    def create_subject_page(self):
        page = ttk.Frame(self.main_frame)
        self.pages["materias"] = page
        page.grid(row=0, column=0, sticky="nsew")

        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=2)

        # Lista de matérias
        left = ttk.Frame(page, padding=(12, 12))
        left.grid(row=0, column=0, sticky="nsew")

        self.lbl_area = ttk.Label(left, text="", font=("Helvetica", 16, "bold"))
        self.lbl_area.pack(anchor="nw", pady=(0, 10))

        self.subject_buttons = {}
        self.subject_list_frame = ttk.Frame(left)
        self.subject_list_frame.pack(fill="both", expand=True)

        # Detalhes da matéria
        right = ttk.Frame(page, padding=(20, 20))
        right.grid(row=0, column=1, sticky="nsew")

        self.lbl_title = ttk.Label(right, text="", font=("Segoe UI Semibold", 18))
        self.lbl_title.grid(row=0, column=0, sticky="w")

        # Barra de progresso
        self.progress = ttk.Progressbar(
            right, orient="horizontal", mode="determinate", maximum=100,
            style="TProgressbar"
        )
        self.progress.grid(row=1, column=0, sticky="ew", pady=(10, 20))
        style = ttk.Style()
        style.configure("TProgressbar", thickness=18, troughcolor="white", background="#68ddbd")

        # Frame de níveis
        self.levels_frame = ttk.Frame(right)
        self.levels_frame.grid(row=2, column=0, sticky="n", pady=(6, 0))

        # Texto de informação
        self.info_label = ttk.Label(right, text="", font=self.button_font)
        self.info_label.grid(row=3, column=0, sticky="w", pady=(14, 0))

    def create_ranking_page(self):
        page = ttk.Frame(self.main_frame)
        self.pages["ranking"] = page
        page.grid(row=0, column=0, sticky="nsew")

        lbl = ttk.Label(page, text="🌍 Ranking Global", font=("Segoe UI Semibold", 18))
        lbl.pack(pady=20)

        columns = ("Posição", "Nome", "Pontos")
        tree = ttk.Treeview(page, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        tree.pack(padx=20, pady=10, fill="x")

        data = [
            (1, "Amanda", 980),
            (2, "João", 920),
            (3, "Maria", 870),
            (4, "Carlos", 850),
            (5, "Ana", 820),
        ]
        for row in data:
            tree.insert("", "end", values=row)

    def create_user_page(self):
        page = ttk.Frame(self.main_frame)
        self.pages["usuario"] = page
        page.grid(row=0, column=0, sticky="nsew")

        lbl = ttk.Label(page, text="👤 Perfil do Usuário", font=("Segoe UI Semibold", 18))
        lbl.pack(pady=20)

        info = ttk.Label(
            page,
            text="Nome: Amanda\nProgresso total: 67%\nNível geral: Intermediário\n\nContinue estudando! 💪",
            font=self.button_font,
            justify="center"
        )
        info.pack(pady=20)

    # ====================== RODAPÉ ==========================

    def create_footer(self):
        self.footer = tk.Frame(self, bg="#00421F", height=60)
        self.footer.grid(row=1, column=0, sticky="ew")
        self.footer.grid_propagate(False)
        self.footer.columnconfigure((0, 1, 2), weight=1, uniform="b")

        self.footer_buttons = {}

        btn_areas = tk.Button(
            self.footer, text="📘\nÁreas", font=("Segoe UI", 10, "bold"),
            bg="#03bb85", fg="#070707", relief="flat",
            activebackground="#02a677", activeforeground="white",
            command=lambda: self.show_page("areas")
        )
        btn_areas.grid(row=0, column=0, sticky="nsew", padx=10, pady=6)
        self.footer_buttons["areas"] = btn_areas

        btn_ranking = tk.Button(
            self.footer, text="🌍\nRanking", font=("Segoe UI", 10, "bold"),
            bg="#03bb85", fg="#060606", relief="flat",
            activebackground="#02a677", activeforeground="white",
            command=lambda: self.show_page("ranking")
        )
        btn_ranking.grid(row=0, column=1, sticky="nsew", padx=10, pady=6)
        self.footer_buttons["ranking"] = btn_ranking

        btn_user = tk.Button(
            self.footer, text="👤\nUsuário", font=("Segoe UI", 10, "bold"),
            bg="#03bb85", fg="#0c0c0c", relief="flat",
            activebackground="#02a677", activeforeground="white",
            command=lambda: self.show_page("usuario")
        )
        btn_user.grid(row=0, column=2, sticky="nsew", padx=10, pady=6)
        self.footer_buttons["usuario"] = btn_user

    # ====================== FUNÇÕES ==========================

    def show_page(self, page_name):
        for name, frame in self.pages.items():
            frame.grid_forget()

        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

        if self.footer_buttons:
            for name, btn in self.footer_buttons.items():
                btn.configure(bg="#02a677" if name == page_name else "#03bb85")

    def open_area(self, area_name):
        """Abre as matérias da área escolhida"""
        self.current_area = area_name
        self.subjects = self.subjects_by_area[area_name]
        self.lbl_area.config(text=f"{area_name}")
        for w in self.subject_list_frame.winfo_children():
            w.destroy()

        for name in self.subjects:
            btn = ttk.Button(
                self.subject_list_frame,
                text=name,
                command=lambda n=name: self.select_subject(n)
            )
            btn.pack(fill="x", pady=6)

        # Mostra página de matérias
        self.show_page("materias")

        # Seleciona primeira matéria automaticamente
        first = next(iter(self.subjects))
        self.select_subject(first)

    def select_subject(self, name):
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
                text=txt,
                font=self.level_font,
                bg=color,
                fg=fg,
                activebackground="#005227",
                activeforeground="#070707",
                width=12,
                relief="flat",
                borderwidth=0,
                command=lambda lvl=i: self.toggle_level(lvl)
            )
            b.grid(row=(i - 1) // cols, column=(i - 1) % cols, padx=8, pady=8)
            b.configure(highlightthickness=1, highlightbackground="#038554")

    def toggle_level(self, lvl):
        data = self.subjects[self.lbl_title.cget("text")]
        max_lvl = data["max"]
        current = data.get("current", 0)

        if lvl <= current:
            new_current = lvl - 1
        else:
            new_current = lvl

        data["current"] = max(0, min(new_current, max_lvl))
        self.select_subject(self.lbl_title.cget("text"))

# ------------------------------------------------------------
# Função usada pelo Router para abrir o ENEM dentro da janela principal
# ------------------------------------------------------------
def montar_enem(root, usuario=None, nome=None):
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font as tkfont

    # limpa a janela atual
    for w in root.winfo_children():
        w.destroy()

    # usa os mesmos dados do seu __main__ (pode trocar para vir do banco)
    materias_enem = {
        "Ciências da Natureza": {
            "Física": {"max": 3, "current": 1},
            "Química": {"max": 3, "current": 2},
            "Biologia": {"max": 3, "current": 2},
        },
        "Ciências Humanas": {
            "História": {"max": 3, "current": 3},
            "Geografia": {"max": 3, "current": 2},
            "Filosofia": {"max": 3, "current": 1},
            "Sociologia": {"max": 3, "current": 1},
        },
        "Linguagens e Códigos": {
            "Português": {"max": 3, "current": 2},
            "Literatura": {"max": 3, "current": 1},
            "Inglês": {"max": 3, "current": 2},
            "Espanhol": {"max": 3, "current": 1},
            "Artes": {"max": 3, "current": 3},
        },
        "Matemática": {
            "Matemática": {"max": 3, "current": 2},
        }
    }

    # janela base (mesma estética)
    root.title("Estudae - ENEM")
    root.geometry("850x580")
    root.configure(bg="#005227")

    title_font = tkfont.Font(family="Segoe UI Semibold", size=22)
    button_font = tkfont.Font(family="Verdana", size=10)
    level_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")

    # container principal
    container = tk.Frame(root, bg="#005227")
    container.pack(fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    # topo
    topo = tk.Frame(container, bg="#005227")
    topo.grid(row=0, column=0, sticky="ew")
    tk.Label(topo, text=f"🧠 ENEM  —  {nome or usuario or 'Aluno(a)'}",
             bg="#005227", fg="#f5f5f5", font=title_font).pack(pady=14)

    # miolo dividido em duas colunas
    miolo = tk.Frame(container, bg="#005227")
    miolo.grid(row=1, column=0, sticky="nsew", padx=14, pady=10)
    miolo.grid_columnconfigure(0, weight=1)
    miolo.grid_columnconfigure(1, weight=2)
    miolo.grid_rowconfigure(0, weight=1)

    # ===== Coluna esquerda: áreas & matérias =====
    left = tk.Frame(miolo, bg="#005227")
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    tk.Label(left, text="Áreas do Conhecimento", bg="#005227",
             fg="#f5f5f5", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(0, 8))

    areas_frame = tk.Frame(left, bg="#005227")
    areas_frame.pack(fill="x", pady=(0, 8))

    # subframe com lista de matérias da área selecionada
    tk.Label(left, text="Matérias", bg="#005227",
             fg="#f5f5f5", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(10, 6))
    materias_frame = tk.Frame(left, bg="#005227")
    materias_frame.pack(fill="both", expand=True)

    # ===== Coluna direita: detalhes & níveis =====
    right = tk.Frame(miolo, bg="#ffffff")
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_rowconfigure(3, weight=1)  # empurrar níveis pra cima

    titulo_materia = tk.Label(right, text="", bg="#ffffff",
                              fg="#0f172a", font=("Segoe UI Semibold", 18))
    titulo_materia.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

    # barra de progresso
    prog_style = ttk.Style()
    try:
        prog_style.theme_use("clam")
    except tk.TclError:
        pass
    prog_style.configure("EnemProgress.Horizontal.TProgressbar", thickness=18,
                         troughcolor="#ffffff", background="#68ddbd")
    progresso = ttk.Progressbar(right, orient="horizontal", mode="determinate",
                                maximum=100, style="EnemProgress.Horizontal.TProgressbar")
    progresso.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))

    # níveis
    levels_frame = tk.Frame(right, bg="#ffffff")
    levels_frame.grid(row=2, column=0, sticky="n", padx=16)

    info_label = tk.Label(right, text="", bg="#ffffff", fg="#0f172a",
                          font=("Verdana", 10))
    info_label.grid(row=3, column=0, sticky="sw", padx=16, pady=12)

    # --- estado e helpers ---
    state = {"area": None, "subjects": {}, "current_subject": None}

    def render_materias(area):
        state["area"] = area
        state["subjects"] = materias_enem[area]
        # limpa lista
        for w in materias_frame.winfo_children():
            w.destroy()
        # cria botões de matéria
        for nome_mat in state["subjects"]:
            tk.Button(
                materias_frame, text=nome_mat,
                font=("Segoe UI", 10), bg="#03bb85", fg="#0a0a0a",
                activebackground="#02a677", activeforeground="white",
                relief="flat", padx=8, pady=6,
                command=lambda n=nome_mat: select_subject(n)
            ).pack(fill="x", pady=4)

    def select_subject(nome_mat):
        state["current_subject"] = nome_mat
        data = state["subjects"][nome_mat]
        max_lvl = data["max"]
        current = data.get("current", 0)

        titulo_materia.config(text=nome_mat)
        pct = int(100 * current / max_lvl) if max_lvl else 0
        progresso["value"] = pct
        info_label.config(text=f"Nível atual: {current} / {max_lvl} ({pct}%)")

        # render níveis
        for w in levels_frame.winfo_children():
            w.destroy()

        cols = 6
        for i in range(1, max_lvl + 1):
            is_done = i <= current
            txt = f"Nível {i}"
            bg = "#a4fff7" if is_done else "#18926E"
            fg = "#080808" if is_done else "#010101"
            b = tk.Button(
                levels_frame, text=txt, font=level_font,
                bg=bg, fg=fg, activebackground="#005227",
                activeforeground="#070707", width=12, relief="flat", borderwidth=0,
                command=lambda lvl=i: toggle_level(lvl)
            )
            b.grid(row=(i - 1) // cols, column=(i - 1) % cols, padx=8, pady=8)
            b.configure(highlightthickness=1, highlightbackground="#038554")

    def toggle_level(lvl):
        nome_mat = state["current_subject"]
        if not nome_mat:
            return
        data = state["subjects"][nome_mat]
        max_lvl = data["max"]
        current = data.get("current", 0)
        new_current = (lvl - 1) if lvl <= current else lvl
        data["current"] = max(0, min(new_current, max_lvl))
        select_subject(nome_mat)

    # render botões das áreas
    for area in materias_enem:
        tk.Button(
            areas_frame, text=area,
            font=("Segoe UI", 10, "bold"),
            bg="#68ddbd", fg="#0a0a0a",
            activebackground="#02a677", activeforeground="white",
            relief="flat", padx=8, pady=6,
            command=lambda a=area: (render_materias(a), select_subject(next(iter(materias_enem[a]))))
        ).pack(fill="x", pady=4)

    # seleciona automaticamente a primeira área/matéria
    first_area = next(iter(materias_enem))
    render_materias(first_area)
    select_subject(next(iter(materias_enem[first_area])))



if __name__ == "__main__":
    materias_enem = {
        "Ciências da Natureza": {
            "Física": {"max": 3, "current": 1},
            "Química": {"max": 3, "current": 2},
            "Biologia": {"max": 3, "current": 2},
        },
        "Ciências Humanas": {
            "História": {"max": 3, "current": 3},
            "Geografia": {"max": 3, "current": 2},
            "Filosofia": {"max": 3, "current": 1},
            "Sociologia": {"max": 3, "current": 1},
        },
        "Linguagens e Códigos": {
            "Português": {"max": 3, "current": 2},
            "Literatura": {"max": 3, "current": 1},
            "Inglês": {"max": 3, "current": 2},
            "Espanhol": {"max": 3, "current": 1},
            "Artes": {"max": 3, "current": 3},
        },
        "Matemática": {
            "Matemática": {"max": 3, "current": 2},
        }
    }

    app = NivelApp(materias_enem)
    app.mainloop()