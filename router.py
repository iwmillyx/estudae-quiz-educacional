# ------------------------------------------------------------
# Router de Telas (Tkinter) do EstudAe
# Aqui ficam:
#  - as funções que trocam de tela dentro da mesma janela
#  - chamadas para: Splash, Login e Home
# Observações:
#  - cada tela fica em um arquivo separado (ex.: telas/splash.py)
# ------------------------------------------------------------

import tkinter as tk

from telas.tela_inicio import montar_logo
from telas.tela_login import App as TelaLogin
from telas.home import montar_home
from telas.tela_enem import montar_enem
from telas.tela_militar import montar_militar

class Router:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.usuario_logado = None   # username
        self.nome_logado = None      # nome completo

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()

    # 1) Logo
    def ir_para_splash(self):
        montar_logo(self.root, ao_clicar=self.ir_para_login)

    # 2) Login/Cadastro (a TelaLogin chama de volta on_login quando der certo)
    def ir_para_login(self):
        self.limpar()
        # passe o callback de sucesso:
        TelaLogin(self.root, on_login=self._login_ok)

    def _login_ok(self, usuario: str, nome: str):
        self.usuario_logado = usuario
        self.nome_logado = nome
        self.ir_para_home()

    # 3) Home
    def ir_para_home(self):
        self.limpar()
        montar_home(
            self.root,
            usuario=self.usuario_logado,
            nome=self.nome_logado,
            on_enem=self.ir_para_enem,
            on_militar=self.ir_para_militar,
        )

    # 4) ENEM (tela da sua amiga)
    def ir_para_enem(self):
        self.limpar()
        montar_enem(self.root, usuario=self.usuario_logado, nome=self.nome_logado)

    # 5) MILITAR
    def ir_para_militar(self):   # <- NOVA FUNÇÃO
        self.limpar()
        montar_militar(
            self.root,
            usuario=self.usuario_logado,
            nome=self.nome_logado,
            on_voltar=self.ir_para_home,
        )
