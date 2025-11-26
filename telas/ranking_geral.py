# ------------------------------------------------------------
# Aqui ficam:
#  - seleção de CATEGORIA (ENEM ou MILITAR)
#  - listagem do ranking somando TODAS as matérias da categoria
# Observações:
#  - os dados vêm do banco de dados (carregar_dados_ranking, ranking_geral)
# ------------------------------------------------------------

# arquivo: telas/ranking_geral.py
import tkinter as tk
from tkinter import font
from dados.banco_dadosUsuarios import carregar_dados_ranking, ranking_geral

# Tema mobile-friendly
COR_VERDE = "#005227"
COR_BG = "#005227"
COR_CARD = "#f7fdf9"
COR_ACCENT = "#68ddbd"
COR_TEXT = "#08321a"

def mostrar_ranking_geral(root, dados=None, on_back=None):

    # Ajusta janela
    try:
        root.geometry("375x700")
    except:
        pass

    root.configure(bg=COR_VERDE)

    # Limpa tela
    for w in root.winfo_children():
        w.destroy()

    # Carrega dados caso não venham de fora
    if dados is None:
        dados = carregar_dados_ranking()

    fonte_titulo = font.Font(family="Segoe UI", size=18, weight="bold")
    fonte_normal = font.Font(family="Segoe UI", size=11)

    # ================= HEADER =================
    header = tk.Frame(root, bg=COR_VERDE, height=72)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="🏆 Ranking Geral",
        bg=COR_VERDE,
        fg="white",
        font=fonte_titulo
    ).pack(pady=12)

    # ================= SCROLL AREA =================
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

    # Mousewheel seguro
    def _on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            pass

    def _bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bind_mousewheel)
    canvas.bind("<Leave>", _unbind_mousewheel)

    # ================= CONTROLES (categoria) =================
    frame_ctrl = tk.Frame(scrollable, bg=COR_BG)
    frame_ctrl.pack(fill="x", pady=(6, 12))

    center_ctrl = tk.Frame(frame_ctrl, bg=COR_BG)
    center_ctrl.pack(anchor="center")

    ctrl_card = tk.Frame(center_ctrl, bg="#eaf8f1", padx=10, pady=8)
    ctrl_card.pack()

    tk.Label(
        ctrl_card, text="Categoria",
        bg="#eaf8f1", fg=COR_VERDE, font=fonte_normal
    ).grid(row=0, column=0, sticky="w", padx=(0, 12))

    categoria_var = tk.StringVar(value="ENEM")
    opcoes = list(dados.keys()) if isinstance(dados, dict) else ["ENEM", "MILITAR"]

    menu = tk.OptionMenu(ctrl_card, categoria_var, *opcoes)
    menu.config(
        width=12, bg=COR_ACCENT, fg=COR_VERDE,
        bd=0, relief="flat", highlightthickness=0
    )
    menu.grid(row=0, column=1, sticky="e")

    # ================= LISTA (ranking) =================
    list_frame = tk.Frame(scrollable, bg=COR_BG)
    list_frame.pack(fill="both", expand=True)

    listbox = tk.Listbox(
        list_frame,
        width=40,
        height=12,
        bg=COR_CARD,
        fg=COR_TEXT,
        font=("Consolas", 11),
        bd=0,
        highlightthickness=1,
        highlightbackground="#e0e7e9",
        activestyle="none"
    )
    listbox.pack(pady=4, padx=2, fill="both", expand=True)

    # ================= FUNÇÃO DE ATUALIZAR =================
    def atualizar_lista():
        cat = categoria_var.get()
        lista = ranking_geral(dados, cat)

        listbox.delete(0, tk.END)

        ultimo_pontos = None
        ultimo_rank = 0

        for i, (aluno, pontos) in enumerate(lista, start=1):

            pos = ultimo_rank if pontos == ultimo_pontos else i
            ultimo_pontos = pontos
            ultimo_rank = pos

            medalha = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else ""

            linha = f"{pos}) {medalha} {aluno} - {pontos}"
            listbox.insert(tk.END, linha)

            cor = "#FFB032" if pos == 1 else "#A9A9A9" if pos == 2 else "#B87333" if pos == 3 else COR_TEXT
            listbox.itemconfig(tk.END, fg=cor)

    categoria_var.trace_add("write", lambda *_: atualizar_lista())
    atualizar_lista()

    # ================= BOTÃO VOLTAR (correto) =================
    btn_frame = tk.Frame(scrollable, bg=COR_BG)
    btn_frame.pack(fill="x", pady=(10, 20))

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
    btn_back.pack(pady=10)


    # automatic update on category change
    categoria_var.trace_add("write", lambda *_: atualizar_lista())

    atualizar_lista()
    return