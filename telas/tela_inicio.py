# ------------------------------------------------------------
# Aqui ficam:
#  - o logo/imagem principal (redimensionado com Pillow)
#  - o botão "Vamos começar" (branco com texto preto)
#  - o subtítulo em negrito preto
# Observações:
#  - imagem esperada: img/logoEstudae.png (na raiz do projeto)
#  - se a imagem não existir, é mostrado um quadrado de placeholder
# ------------------------------------------------------------

import tkinter as tk
import os
from PIL import Image, ImageTk


def montar_logo(root: tk.Tk, ao_clicar):
    """
    Mostra a tela de abertura (logo) do EstudAe.
    Parâmetros:
      - root: janela principal (Tk)
      - ao_clicar: função chamada ao clicar em "Vamos começar"
    """
    # limpa a janela
    for w in root.winfo_children():
        w.destroy()

    COR_FUNDO = "#07442E"  # cor de fundo nova
    COR_DETALHE = "#68ddbd"  # verde claro pra contrastar

    root.configure(bg=COR_FUNDO)
    root.title("EstudAe")

    frame = tk.Frame(root, bg=COR_FUNDO)
    frame.pack(expand=True, fill="both")

    # ===== tenta carregar o logo =====
    proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_logo = os.path.join(proj_root, "img", "logoSemFundo2.png")

    img = None
    if os.path.exists(caminho_logo):
        try:
            pil_img = Image.open(caminho_logo).resize((200, 200))
            img = ImageTk.PhotoImage(pil_img)

            logo_lbl = tk.Label(frame, image=img, bg=COR_FUNDO)
            logo_lbl.pack(pady=(40, 8))
            logo_lbl.image = img
            frame._img = img
        except Exception:
            img = None

    if not img:
        # placeholder se não tiver imagem
        ph = tk.Frame(frame, width=220, height=220, bg=COR_DETALHE)
        ph.pack_propagate(False)
        ph.pack(pady=(40, 8))
        tk.Label(ph, text="EstudAe", bg=COR_DETALHE, fg="#0f172a",
                 font=("Cooper Black", 36)).pack(expand=True)

    # ===== subtítulo sem sombra =====
    tk.Label(
        frame,
        text="Pronto pra começar sua jornada?",
        bg=COR_FUNDO,
        fg="black",
        font=("Cooper Black", 14, "bold")
    ).pack(pady=(5, 40))

    # ===== botão branco com texto preto =====
    btn = tk.Button(
        frame,
        text="Vamos começar",
        bg="#ffffff", fg="black",
        activebackground="#e5e5e5", activeforeground="black",
        font=("Arial", 16, "bold"),
        relief="raised", width=18, height=2,
        command=ao_clicar
    )
    btn.pack(pady=10)

    # dica
    tk.Label(frame, text="(ou pressione Enter)", bg=COR_FUNDO, fg=COR_DETALHE, font=("Arial", 10)).pack(pady=(6, 24))

    # Enter também inicia
    root.bind("<Return>", lambda e: ao_clicar())

# ===== Execução isolada (teste rápido) ===== 
if __name__ == "__main__": 
    def teste_callback(): 
        print("Botão 'Vamos começar' clicado!") 
            
    root = tk.Tk() 
    root.geometry("420x640")        
    montar_logo(root, ao_clicar=teste_callback) 
    root.mainloop()