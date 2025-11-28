# arquivo: telas/ranking_por_materia.py
import tkinter as tk
from tkinter import font
from dados.banco_dadosUsuarios import carregar_ranking_materias

# ===== TEMA MOBILE DO ESTUDAE =====
COR_VERDE = "#005227"
COR_BG = "#005227"
COR_CARD = "#f7fdf9"
COR_ACCENT = "#68ddbd"
COR_TEXT = "#08321a"

def mostrar_ranking_por_materia(root, dados=None, on_back=None):

    # ================= AJUSTES DA JANELA =================
    try:
        root.geometry("375x700")
    except:
        pass

    for w in root.winfo_children():
        w.destroy()

    root.configure(bg=COR_BG)

    if dados is None:
        dados = carregar_ranking_materias()

    fonte_titulo = font.Font(family="Segoe UI", size=18, weight="bold")
    fonte_normal = font.Font(family="Segoe UI", size=11)

    # ================= HEADER =================
    header = tk.Frame(root, bg=COR_VERDE, height=72)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="📘 Ranking por Matéria",
        bg=COR_VERDE,
        fg="white",
        font=fonte_titulo
    ).pack(pady=12)

    # ================= ÁREA COM SCROLL =================
    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=COR_BG)

    scrollable.bind("<Configure>", lambda e:
        canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable, anchor="nw", width=355)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(12, 10))
    scrollbar.pack(side="right", fill="y")

    # ==== Scroll com segurança ====
    def _on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            pass

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # ================= FILTROS (Categoria + Matéria) =================
    frame_ctrl = tk.Frame(scrollable, bg=COR_BG)
    frame_ctrl.pack(fill="x", pady=(6, 12))

    center_ctrl = tk.Frame(frame_ctrl, bg=COR_BG)
    center_ctrl.pack(anchor="center")

    ctrl_card = tk.Frame(center_ctrl, bg="#eaf8f1", padx=10, pady=8)
    ctrl_card.pack()

    # ---- Categoria ----
    tk.Label(ctrl_card, text="Categoria", bg="#eaf8f1", fg=COR_VERDE, font=fonte_normal)\
        .grid(row=0, column=0, padx=(0, 12), sticky="w")

    categoria_var = tk.StringVar(value="ENEM")
    opcoes = list(dados.keys()) if isinstance(dados, dict) else ["ENEM", "MILITAR"]

    menu_cat = tk.OptionMenu(ctrl_card, categoria_var, *opcoes)
    menu_cat.config(
        width=12, bg=COR_ACCENT, fg=COR_VERDE,
        bd=0, relief="flat", highlightthickness=0
    )
    menu_cat.grid(row=0, column=1, sticky="e")

    # ---- Matéria ----
    tk.Label(ctrl_card, text="Matéria", bg="#eaf8f1", fg=COR_VERDE, font=fonte_normal)\
        .grid(row=1, column=0, padx=(0, 12), sticky="w")

    materia_var = tk.StringVar(value="")

    menu_mat = tk.OptionMenu(ctrl_card, materia_var, "")
    menu_mat.config(
        width=12, bg=COR_ACCENT, fg=COR_VERDE,
        bd=0, relief="flat", highlightthickness=0
    )
    menu_mat.grid(row=1, column=1, sticky="e")

    # ================= CONTAINER DO RANKING - TODOS OS USUÁRIOS =================
    list_frame = tk.Frame(scrollable, bg=COR_BG)
    list_frame.pack(fill="both", expand=True, pady=10)

    ranking_container = tk.Frame(list_frame, bg=COR_CARD, bd=1, relief="solid")
    ranking_container.pack(fill="both", expand=True, padx=2)

    # ================= FUNÇÕES =================
    def preencher_materias():
        cat = categoria_var.get()
        materias = []

        try:
            materias = dados[cat]["materias"]
        except:
            entry = dados.get(cat, {})
            if isinstance(entry, dict):
                materias = list(entry.keys())

        menu = menu_mat["menu"]
        menu.delete(0, "end")

        if materias:
            materia_var.set(materias[0])
            for m in materias:
                menu.add_command(label=m, command=lambda v=m: materia_var.set(v))
        else:
            materia_var.set("")

    def atualizar_lista():
        cat = categoria_var.get()
        mat = materia_var.get()

        # Limpa container
        for widget in ranking_container.winfo_children():
            widget.destroy()

        if not mat:
            return

        lista = []
        container_data = dados.get(cat, {})

        if isinstance(container_data, dict) and mat in container_data:
            lista = container_data.get(mat, [])

        # MOSTRA TODOS OS USUÁRIOS (removida a limitação de TOP 10)
        ultimo_pontos = None
        ultimo_rank = 0

        for i, (aluno, pontos) in enumerate(lista, start=1):
            pos = ultimo_rank if pontos == ultimo_pontos else i
            ultimo_pontos = pontos
            ultimo_rank = pos

            # Cores e medalhas para TOP 3
            if pos == 1:
                medalha = "🥇"
                cor_bg = "#FFF9E6"
                cor_texto = "#FFB032"
                peso = "bold"
            elif pos == 2:
                medalha = "🥈"
                cor_bg = "#F5F5F5"
                cor_texto = "#A9A9A9"
                peso = "bold"
            elif pos == 3:
                medalha = "🥉"
                cor_bg = "#FFF4E6"
                cor_texto = "#B87333"
                peso = "bold"
            else:
                medalha = ""
                cor_bg = COR_CARD
                cor_texto = COR_TEXT
                peso = "normal"

            # Frame de cada item
            item_frame = tk.Frame(ranking_container, bg=cor_bg, height=40)
            item_frame.pack(fill="x", padx=8, pady=4)
            item_frame.pack_propagate(False)

            # Posição
            tk.Label(
                item_frame,
                text=f"{pos})",
                bg=cor_bg,
                fg=cor_texto,
                font=font.Font(family="Segoe UI", size=12, weight=peso),
                width=3,
                anchor="w"
            ).pack(side="left", padx=(5, 0))

            # Medalha (se tiver)
            if medalha:
                tk.Label(
                    item_frame,
                    text=medalha,
                    bg=cor_bg,
                    font=font.Font(size=14)
                ).pack(side="left", padx=2)

            # Nome do aluno
            tk.Label(
                item_frame,
                text=aluno,
                bg=cor_bg,
                fg=cor_texto,
                font=font.Font(family="Segoe UI", size=11, weight=peso),
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=5)

            # Pontos
            tk.Label(
                item_frame,
                text=f"{pontos} XP",
                bg=cor_bg,
                fg=cor_texto,
                font=font.Font(family="Segoe UI", size=11, weight=peso),
                anchor="e"
            ).pack(side="right", padx=5)

        root.title(f"Ranking — {cat} / {mat}")

    categoria_var.trace_add("write", lambda *_: (preencher_materias(), atualizar_lista()))
    materia_var.trace_add("write", lambda *_: atualizar_lista())

    # ================= BOTÃO VOLTAR =================
    btn_frame = tk.Frame(scrollable, bg=COR_BG)
    btn_frame.pack(fill="x", pady=(15, 25))

    def voltar():
        if callable(on_back):
            on_back()
        else:
            for w in root.winfo_children():
                w.destroy()

    btn_back = tk.Button(
        btn_frame,
        text="← Voltar",
        bg="#d32f2f",
        fg="white",
        width=20,
        height=2,
        relief="flat",
        cursor="hand2",
        command=voltar
    )
    btn_back.pack()

    # inicialização
    preencher_materias()
    atualizar_lista()

    return