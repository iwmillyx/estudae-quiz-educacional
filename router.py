# ------------------------------------------------------------
# Router de Telas (Tkinter) do EstudAe
# Aqui ficam:
#  - as funções que trocam de tela dentro da mesma janela
#  - chamadas para: Splash, Login e Home
# Observações:
#  - cada tela fica em um arquivo separado (ex.: telas/splash.py)
# ------------------------------------------------------------
import tkinter as tk
from telas.tela_login import App as TelaLogin
from telas.home import montar_home
from telas.tela_enem import montar_enem
from telas.tela_militar import montar_militar

class Router:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.usuario_logado = None
        self.nome_logado = None

    def limpar(self):
        """Limpa todos os widgets da janela"""
        for w in self.root.winfo_children():
            w.destroy()

    def ir_para_login(self):
        """Navega para a tela de login"""
        self.limpar()
        TelaLogin(self.root, on_login=self._login_ok)

    def _login_ok(self, usuario: str, nome: str):
        """Callback chamado após login bem-sucedido"""
        self.usuario_logado = usuario
        self.nome_logado = nome
        self.ir_para_home()

    def ir_para_home(self):
        """Navega para a tela home (escolha: ENEM ou Militar)"""
        if not self.usuario_logado:  # validação
            self.ir_para_login()
            return
            
        self.limpar()
        montar_home(
            self.root,
            usuario=self.usuario_logado,
            nome=self.nome_logado,
            on_enem=self.ir_para_enem,
            on_militar=self.ir_para_militar,
        )

    def ir_para_enem(self):
        """Navega para a tela do ENEM"""
        self.limpar()
        montar_enem(
            self.root, 
            usuario=self.usuario_logado, 
            nome=self.nome_logado,
            on_voltar=self.ir_para_home
        )

    def ir_para_militar(self):
        """Navega para a tela de Concurso Militar"""
        self.limpar()
        montar_militar(
            self.root,
            usuario=self.usuario_logado,
            nome=self.nome_logado,
            on_voltar=self.ir_para_home,
        )