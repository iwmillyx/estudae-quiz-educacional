# ------------------------------------------------------------
# Aqui ficam:
#  - seleção de CATEGORIA (ENEM ou MILITAR)
#  - listagem do ranking somando TODAS as matérias da categoria
# Observações:
#  - os dados vêm do módulo 'dados' (carregar_dados, ranking_geral)
#  - quando migrar para banco, basta trocar o import (ex.: dados_db)
# ------------------------------------------------------------

import tkinter as tk
from tkinter import font, filedialog
from dados.dados import carregar_dados, ranking_geral

# =============== Cores principais (tema do grupo) ===============
COR_VERDE = "#005227"  # verde do cabeçalho
COR_FUNDO = "#ffffff"  # fundo geral branco
COR_TEXTO = "#0f172a"  # texto escuro (quase preto)

# =============== Criação da janela principal ===============
janela = tk.Tk()
janela.title("Ranking Geral — ENEM/MILITAR")
janela.geometry("500x500")
janela.configure(bg=COR_FUNDO)  # fundo branco geral

# Fonte padrão
fonte_padrao = font.Font(family="Segoe UI", size=10)
janela.option_add("*Font", fonte_padrao)

# =============== Cabeçalho verde ===========================
frame_header = tk.Frame(janela, bg=COR_VERDE, height=80)
frame_header.pack(fill="x")

label_titulo = tk.Label(
    frame_header,
    text="🏆  Ranking Geral",
    bg=COR_VERDE,
    fg="white",
    font=("Segoe UI", 16, "bold")
)
label_titulo.pack(pady=20)

# =============== Carrega dados =============================
dados = carregar_dados()

# Variável da categoria (ENEM/MILITAR)
categoria_var = tk.StringVar(value="ENEM")

# sempre que trocar ENEM/MILITAR, atualiza a lista automaticamente
categoria_var.trace_add("write", lambda *_: atualizar_lista())

# =============== Área de seleção ===========================
frame_controles = tk.Frame(janela, bg=COR_FUNDO)
frame_controles.pack(pady=10)

label_instrucao = tk.Label(
    frame_controles,
    text="Escolha a categoria:",
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
label_instrucao.pack(pady=5)

# menu dropdown
opcoes_categoria = list(dados.keys())
menu_categoria = tk.OptionMenu(frame_controles, categoria_var, *opcoes_categoria)
menu_categoria.config(bg="#f1f5f9", fg=COR_TEXTO, activebackground="#d1fae5", bd=0)
menu_categoria.pack(pady=5)

# =============== Lista (ranking) ============================
frame_lista = tk.Frame(janela, bg=COR_FUNDO)
frame_lista.pack(pady=10)

listbox = tk.Listbox(
    frame_lista,
    width=50,
    height=15,
    bg="#f8fafc",
    fg=COR_TEXTO,
    font=("Consolas", 11),
    selectbackground="#b7e4c7",
    selectforeground="black",
    bd=0,
    highlightthickness=1,
    highlightbackground="#d1d5db"
)
listbox.pack()

# =============== Funções ============================
def atualizar_lista():
    """Atualiza o ranking da categoria selecionada."""
    cat = categoria_var.get()
    lista = ranking_geral(dados, cat)
    listbox.delete(0, tk.END)

    ultimo_pontos = None
    ultimo_rank = 0
    for i, (aluno, pontos) in enumerate(lista, start=1):
        pos = ultimo_rank if pontos == ultimo_pontos else i
        ultimo_pontos = pontos
        ultimo_rank = pos

        # medalhas pros top 3
        medalha = ""
        if pos == 1:
            medalha = "🥇"
        elif pos == 2:
            medalha = "🥈"
        elif pos == 3:
            medalha = "🥉"

        listbox.insert(tk.END, f"{pos}) {medalha} {aluno} - {pontos}")
        # muda cor dos top 3
        cor = "#FFB032" if pos == 1 else "#A9A9A9" if pos == 2 else "#B87333" if pos == 3 else COR_TEXTO
        listbox.itemconfig(tk.END, fg=cor)

    janela.title(f"Ranking Geral — {cat}")

def exportar_txt():
    """Exporta o ranking atual pra um arquivo .txt"""
    cat = categoria_var.get()
    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile=f"ranking_{cat}.txt",
        filetypes=[("Arquivo de texto", "*.txt")]
    )
    if not caminho:
        return

    linhas = [listbox.get(i) for i in range(listbox.size())]
    with open(caminho, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

# chama uma vez pra preencher
atualizar_lista()

# mantém janela aberta
janela.mainloop()
