# telas/tela_inicio.py
import tkinter as tk
import os
from PIL import Image, ImageTk
from utils import calcular_tamanho, calcular_padding, calcular_font_size

def montar_logo(root: tk.Tk, ao_clicar):
    """
    Mostra a tela de abertura (logo) do EstudAe - RESPONSIVA
    Parâmetros:
    - root: janela principal (Tk)
    - ao_clicar: função chamada ao clicar em "Vamos começar"
    """
    # Limpa a janela
    for w in root.winfo_children():
        w.destroy()

    # Cores
    COR_FUNDO = "#07442E"
    COR_DETALHE = "#68ddbd"

    root.configure(bg=COR_FUNDO)
    root.title("EstudAe")

    # Frame principal centralizado
    frame = tk.Frame(root, bg=COR_FUNDO)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # CENTRALIZA TUDO

    # ===== LOGO (responsivo) =====
    proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_logo = os.path.join(proj_root, "img", "logoSemFundo2.png")

    # Tamanho do logo baseado na tela
    largura_logo = int(root.winfo_width() * 0.53) or 200  # 53% da largura
    altura_logo = largura_logo  # mantém proporção quadrada

    img = None
    if os.path.exists(caminho_logo):
        try:
            pil_img = Image.open(caminho_logo).resize((largura_logo, altura_logo))
            img = ImageTk.PhotoImage(pil_img)

            logo_lbl = tk.Label(frame, image=img, bg=COR_FUNDO)
            logo_lbl.pack(pady=calcular_padding(root, 0.05))
            logo_lbl.image = img
            frame._img = img
        except Exception:
            img = None

    if not img:
        # Placeholder se não tiver imagem (também responsivo)
        ph = tk.Frame(frame, width=largura_logo, height=altura_logo, bg=COR_DETALHE)
        ph.pack_propagate(False)
        ph.pack(pady=calcular_padding(root, 0.05))
        
        font_size_ph = calcular_font_size(root, base_size=36)
        tk.Label(
            ph, 
            text="EstudAe", 
            bg=COR_DETALHE, 
            fg="#0f172a",
            font=("Cooper Black", font_size_ph)
        ).pack(expand=True)

    # ===== SUBTÍTULO (responsivo) =====
    font_size_subtitulo = calcular_font_size(root, base_size=14)
    tk.Label(
        frame,
        text="Pronto pra começar sua jornada?",
        bg=COR_FUNDO,
        fg="black",
        font=("Cooper Black", font_size_subtitulo, "bold")
    ).pack(pady=calcular_padding(root, 0.03))

    # ===== BOTÃO (responsivo e centralizado) =====
    btn_largura, btn_altura = calcular_tamanho(root, largura_percent=0.7, altura_percent=0.08)
    font_size_btn = calcular_font_size(root, base_size=16)
    
    btn = tk.Button(
        frame,
        text="Vamos começar",
        bg="#ffffff", 
        fg="black",
        activebackground="#e5e5e5", 
        activeforeground="black",
        font=("Arial", font_size_btn, "bold"),
        relief="raised",
        cursor="hand2",
        command=ao_clicar
    )
    # Configura tamanho do botão
    btn.config(width=int(btn_largura/10), height=int(btn_altura/20))
    btn.pack(pady=calcular_padding(root, 0.02))

    # ===== DICA (responsiva) =====
    font_size_dica = calcular_font_size(root, base_size=10)
    tk.Label(
        frame, 
        text="(ou pressione Enter)", 
        bg=COR_FUNDO, 
        fg=COR_DETALHE, 
        font=("Arial", font_size_dica)
    ).pack(pady=calcular_padding(root, 0.01))

    # Enter também inicia
    root.bind("<Return>", lambda e: ao_clicar())


# ===== Teste isolado =====
if __name__ == "__main__":
    # Importa utils apenas para teste
    import sys
    sys.path.append('..')
    from utils import calcular_tamanho, calcular_padding, calcular_font_size
    
    def teste_callback():
        print("Botão 'Vamos começar' clicado!")

    root = tk.Tk()
    
    # TESTE EM DIFERENTES TAMANHOS:
    root.geometry("375x812")  # iPhone 13
    # root.geometry("430x932")  # iPhone Pro Max
    # root.geometry("360x800")  # Android
    
    root.resizable(False, False)
    montar_logo(root, ao_clicar=teste_callback)
    root.mainloop()