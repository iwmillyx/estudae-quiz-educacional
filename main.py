# ------------------------------------------------------------
# Aqui ficam:
#  - o ponto de entrada da aplicação (Tkinter)
#  - a criação da janela principal e do Router
#  - a primeira tela exibida (Splash)
# Fluxo:
#  1) Splash (logo + botão)
#  2) Login (cadastro)
#  3) Home
# ------------------------------------------------------------

import tkinter as tk
from router import Router

if __name__ == "__main__":
    root = tk.Tk()
    app = Router(root)
    app.ir_para_splash()
    root.mainloop()
