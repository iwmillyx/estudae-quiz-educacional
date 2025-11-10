# ------------------------------------------------------------
# Aqui ficam:
#  - o título e a identidade visual (verde do grupo)
#  - os botões principais para iniciar a jornada (ENEM / Militar)
# Observações:
#  - por enquanto, os botões só dão print (placeholder)
#  - depois você pode abrir novas janelas/telas com as funcionalidades
# ------------------------------------------------------------

# ------------------------------------------------------------
# Tela Home do EstudAe
# ------------------------------------------------------------
import tkinter as tk

def montar_home(root, usuario=None, nome=None, on_enem=None, on_militar=None):
    """Monta a tela inicial dentro da janela principal"""
    # limpa o que já existir
    for w in root.winfo_children():
        w.destroy()

    root.title("EstudAe")
    root.geometry("400x600")
    root.config(bg="#005227")

    # título
    titulo = tk.Label(
        root,
        text="EstudAe",
        font=("Cooper Black", 60),
        bg="#005227",
        fg="#FFFFFF"
    )
    titulo.pack(pady=30)

    # linha decorativa
    linha = tk.Frame(root, bg="#68ddbd", height=4, width=500)
    linha.pack(pady=(0, 5))

    # subtítulo
    subtitulo = tk.Label(
        root,
        text=f"Olá, {nome or usuario or 'Aluno(a)'}!\nEscolha sua jornada de estudos",
        font=("Cooper Black", 14, "italic"),
        bg="#005227",
        fg="#FFFFFF",
        justify="center"
    )
    subtitulo.pack(pady=(0, 20))

    # área dos botões
    frame_escolhas = tk.Frame(root, bg="#005227")
    frame_escolhas.pack(expand=True, pady=50)

    # botão ENEM
    botao_enem = tk.Button(
        frame_escolhas,
        text="🧠 Enem",
        bg="#68ddbd",
        font=("Arial", 16, "bold"),
        fg="black",
        activebackground="#005227",
        relief="raised",
        width=20,
        height=2,
        command=(on_enem if on_enem else lambda: print("Botão ENEM clicado!"))
    )
    botao_enem.pack(pady=10, fill="x", padx=50)

    # botão Militar
    botao_militar = tk.Button(
        frame_escolhas,
        text="🏅 Concurso Militar",
        bg="#68ddbd",
        font=("Arial", 16, "bold"),
        fg="black",
        activebackground="#005227",
        relief="raised",
        width=20,
        height=2,
        command=(on_militar if on_militar else lambda: print("Botão Militar clicado!"))
    )
    botao_militar.pack(pady=10, fill="x", padx=50)
