# ------------------------------------------------------------
# Aqui ficam:
#  - seleção de CATEGORIA (ENEM ou MILITAR)
#  - seleção de MATÉRIA (carregada conforme a categoria)
#  - listagem do ranking SOMENTE daquela matéria
# Observações:
#  - os dados vêm do módulo 'dados' (carregar_dados, ranking_materia)
#  - quando migrar para banco, basta trocar o import (ex.: dados_db)
# ------------------------------------------------------------

import tkinter as tk
from tkinter import font
from dados.banco_dadosUsuarios import carregar_ranking_materias

# ===== TEMA MOBILE DO ESTUDAE =====
COR_VERDE = "#005227"     # fundo geral
COR_BG = "#005227"        # fundo de trás
COR_CARD = "#f7fdf9"      # card clarinho
COR_ACCENT = "#68ddbd"    # verde claro
COR_TEXT = "#08321a"      # texto escuro

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

    # Card claro envolvendo “Categoria” + dropdown
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

    # ================= LISTBOX =================
    list_frame = tk.Frame(scrollable, bg=COR_BG)
    list_frame.pack(fill="both", expand=True)

    listbox = tk.Listbox(
        list_frame, width=40, height=12,
        bg=COR_CARD, fg=COR_TEXT,
        font=("Consolas", 11),
        bd=0,
        highlightthickness=1,
        highlightbackground="#e0e7e9",
        activestyle="none"
    )
    listbox.pack(pady=4, padx=2, fill="both", expand=True)

    # ================= FUNÇÕES =================
    def preencher_materias():
        cat = categoria_var.get()
        materias = []

        try:
            materias = dados[cat]["materias"]
        except:
            # fallback dependendo da estrutura recebida
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

        listbox.delete(0, tk.END)

        if not mat:
            return

        lista = []
        container_data = dados.get(cat, {})

        if isinstance(container_data, dict) and mat in container_data:
            lista = container_data.get(mat, [])

        ultimo_pontos = None
        ultimo_rank = 0

        for i, (aluno, pontos) in enumerate(lista, start=1):
            pos = ultimo_rank if pontos == ultimo_pontos else i
            ultimo_pontos = pontos
            ultimo_rank = pos

            medalha = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else ""
            cor = "#FFB032" if pos == 1 else "#A9A9A9" if pos == 2 else "#B87333" if pos == 3 else COR_TEXT

            listbox.insert(tk.END, f"{pos}) {medalha} {aluno} - {pontos}")
            listbox.itemconfig(tk.END, fg=cor)

        root.title(f"Ranking — {cat} / {mat}")

    categoria_var.trace_add("write", lambda *_: (preencher_materias(), atualizar_lista()))
    materia_var.trace_add("write", lambda *_: atualizar_lista())

    # ================= BOTÃO VOLTAR (igual ao ranking geral) =================
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
