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
from dados.dados import carregar_dados, ranking_materia

# Cores
COR_VERDE = "#005227"
COR_FUNDO = "#ffffff"
COR_TEXTO = "#0f172a"

# Janela
janela = tk.Tk()
janela.title("Ranking por Matéria — ENEM/MILITAR")
janela.geometry("500x550")
janela.configure(bg=COR_FUNDO)

# Fonte padrão
fonte_padrao = font.Font(family="Segoe UI", size=10)
janela.option_add("*Font", fonte_padrao)

# Cabeçalho
frame_header = tk.Frame(janela, bg=COR_VERDE, height=70)
frame_header.pack(fill="x")
tk.Label(frame_header, text="📘  Ranking por Matéria",
         bg=COR_VERDE, fg="white", font=("Segoe UI", 15, "bold")).pack(pady=18)

# Dados
dados = carregar_dados()

# Filtros
frame_controles = tk.Frame(janela, bg=COR_FUNDO)
frame_controles.pack(pady=10)

tk.Label(frame_controles, text="Categoria:", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=5, pady=5, sticky="w")
categoria_var = tk.StringVar(value="ENEM")
opcoes_categoria = list(dados.keys())
menu_categoria = tk.OptionMenu(frame_controles, categoria_var, *opcoes_categoria)
menu_categoria.config(bg="#f1f5f9", fg=COR_TEXTO, activebackground="#d1fae5", bd=0)
menu_categoria.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_controles, text="Matéria:", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=1, column=0, padx=5, pady=5, sticky="w")
materia_var = tk.StringVar(value="")
menu_materia = tk.OptionMenu(frame_controles, materia_var, "")
menu_materia.config(bg="#f1f5f9", fg=COR_TEXTO, activebackground="#d1fae5", bd=0)
menu_materia.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Listbox
listbox = tk.Listbox(
    janela, width=55, height=18, bg="#f8fafc", fg=COR_TEXTO,
    font=("Consolas", 11), selectbackground="#b7e4c7", selectforeground="black",
    bd=0, highlightthickness=1, highlightbackground="#d1d5db"
)
listbox.pack(pady=10)

def preencher_materias():
    """Atualiza as opções de matérias conforme a categoria."""
    cat = categoria_var.get()
    materias = dados[cat]["materias"]
    menu = menu_materia["menu"]
    menu.delete(0, "end")
    if materias:
        materia_var.set(materias[0])
        for m in materias:
            menu.add_command(label=m, command=lambda v=m: materia_var.set(v))
    else:
        materia_var.set("")

def atualizar_lista():
    """Mostra o ranking da matéria selecionada."""
    cat = categoria_var.get()
    mat = materia_var.get()
    if not (cat and mat):
        return
    lista = ranking_materia(dados, cat, mat)
    listbox.delete(0, tk.END)

    ultimo_pontos = None
    ultimo_rank = 0
    for i, (aluno, pontos) in enumerate(lista, start=1):
        pos = ultimo_rank if pontos == ultimo_pontos else i
        ultimo_pontos = pontos
        ultimo_rank = pos

        medalha = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else ""
        cor = "#FFB032" if pos == 1 else "#A9A9A9" if pos == 2 else "#B87333" if pos == 3 else COR_TEXTO

        listbox.insert(tk.END, f"{pos}) {medalha} {aluno} - {pontos}")
        listbox.itemconfig(tk.END, fg=cor)

    janela.title(f"Ranking — {cat} / {mat}  (participantes: {len(lista)})")

def on_categoria_change(*_):
    preencher_materias()
    atualizar_lista()

def on_materia_change(*_):
    atualizar_lista()

# Atualiza automaticamente
categoria_var.trace_add("write", on_categoria_change)
materia_var.trace_add("write", on_materia_change)

# Inicializa
preencher_materias()
atualizar_lista()

janela.mainloop()
