# ------------------------------------------------------------
# Aqui ficam:
#  - a interface de Login e Cadastro
#  - leitura/gravação de 'usuarios.txt' (formato: usuario;senha;nome;nasc;tel;email;estado)
#  - validações básicas (e-mail, data, senha)
#  - "Esqueci a senha": redefine a senha com e-mail + data de nascimento
#
# Observações:
#  - é uma versão simples para começar rápido (sem banco ainda)
#  - quando migrar para banco (SQLite/Postgres), basta trocar as funções
#    de salvar/carregar mantendo as mesmas assinaturas
# ------------------------------------------------------------
# telas/tela_login.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
from datetime import datetime
from PIL import Image, ImageTk
from utils import calcular_tamanho, calcular_padding, calcular_font_size

ARQUIVO_USUARIOS = "dados/usuarios.txt"

# ------------------------------------------------------------
# LISTA DE ESTADOS
# ------------------------------------------------------------
ESTADOS_BRASIL = [
    "AC - Acre", "AL - Alagoas", "AP - Amapá", "AM - Amazonas",
    "BA - Bahia", "CE - Ceará", "DF - Distrito Federal", "ES - Espírito Santo",
    "GO - Goiás", "MA - Maranhão", "MT - Mato Grosso", "MS - Mato Grosso do Sul",
    "MG - Minas Gerais", "PA - Pará", "PB - Paraíba", "PR - Paraná",
    "PE - Pernambuco", "PI - Piauí", "RJ - Rio de Janeiro", "RN - Rio Grande do Norte",
    "RS - Rio Grande do Sul", "RO - Rondônia", "RR - Roraima", "SC - Santa Catarina",
    "SP - São Paulo", "SE - Sergipe", "TO - Tocantins"
]

# ------------------------------------------------------------
# FUNÇÕES DE ARQUIVO (mantidas)
# ------------------------------------------------------------
def carregar_usuarios():
    usuarios = {}
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) >= 7:
                    user, senha, nome, nasc, tel, email, estado = dados[:7]
                    usuarios[user] = {
                        "senha": senha,
                        "nome": nome,
                        "nasc": nasc,
                        "tel": tel,
                        "email": email,
                        "estado": estado,
                    }
    return usuarios

def salvar_usuario(usuario, senha, nome, nasc, tel, email, estado):
    os.makedirs(os.path.dirname(ARQUIVO_USUARIOS), exist_ok=True)
    with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(f"{usuario};{senha};{nome};{nasc};{tel};{email};{estado}\n")

def salvar_todos(usuarios_dict):
    os.makedirs(os.path.dirname(ARQUIVO_USUARIOS), exist_ok=True)
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        for u, d in usuarios_dict.items():
            f.write(f"{u};{d['senha']};{d['nome']};{d['nasc']};{d['tel']};{d['email']};{d['estado']}\n")

# ------------------------------------------------------------
# VALIDAÇÕES (mantidas)
# ------------------------------------------------------------
def email_valido(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""))

def data_valida(dia: str, mes: str, ano: str) -> bool:
    if dia in ("", "Dia") or mes in ("", "Mês") or ano in ("", "Ano"):
        return False
    try:
        dt = datetime(int(ano), int(mes), int(dia))
        return dt <= datetime.now()
    except ValueError:
        return False

def senha_valida(s: str) -> tuple[bool, str]:
    if len(s or "") < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."
    if not re.search(r"[A-Za-z]", s) or not re.search(r"\d", s):
        return False, "A senha deve conter letras e números."
    return True, ""

# ------------------------------------------------------------
# APLICATIVO
# ------------------------------------------------------------
class App:
    def __init__(self, root, on_login=None):
        self.root = root
        self.on_login = on_login
        
        self.root.title("EstudAe")
        
        # Cores
        self.COR_FUNDO = "#07442E"
        self.COR_CARD = "#ffffff"
        self.COR_CAMPO = "#e3f2fd"
        self.COR_BOTAO = "#00bcd4"
        self.COR_TEXTO_ESCURO = "#333333"
        
        self.root.configure(bg=self.COR_FUNDO)
        self.tela_inicial()

    def limpar_tela(self):
        for w in self.root.winfo_children():
            w.destroy()

    def criar_entry_arredondado(self, parent, var=None, show=None, width=280):
        """Cria Entry com cantos arredondados"""
        container = tk.Frame(parent, bg=parent.cget("bg"))
        
        canvas = tk.Canvas(
            container,
            width=width,
            height=40,
            bg=parent.cget("bg"),
            highlightthickness=0
        )
        canvas.pack()
        
        # Fundo arredondado
        radius = 8
        canvas.create_rectangle(0, 0, width, 40, fill=self.COR_CAMPO, outline="")
        canvas.create_oval(0, 0, radius*2, radius*2, fill=self.COR_CAMPO, outline="")
        canvas.create_oval(width-radius*2, 0, width, radius*2, fill=self.COR_CAMPO, outline="")
        canvas.create_oval(0, 40-radius*2, radius*2, 40, fill=self.COR_CAMPO, outline="")
        canvas.create_oval(width-radius*2, 40-radius*2, width, 40, fill=self.COR_CAMPO, outline="")
        
        entry = tk.Entry(
            container,
            font=("Arial", 11),
            bg=self.COR_CAMPO,
            fg=self.COR_TEXTO_ESCURO,
            relief="flat",
            bd=0,
            textvariable=var,
            show=show if show else ""
        )
        entry.place(x=10, y=10, width=width-20, height=20)
        
        container._entry = entry
        return container

    def carregar_logo(self, parent, tamanho=(120, 120)):
        """Carrega logo - TELA INICIAL"""
        proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # ==== MUDE O NOME DA IMAGEM AQUI PARA A TELA INICIAL ====
        caminho_logo = os.path.join(proj_root, "img", "logoSemFundo2.png")
        
        if os.path.exists(caminho_logo):
            try:
                pil_img = Image.open(caminho_logo).resize(tamanho)
                img = ImageTk.PhotoImage(pil_img)
                logo_lbl = tk.Label(parent, image=img, bg=parent.cget("bg"))
                # ==== MUDE O ESPAÇAMENTO AQUI (pady) ====
                logo_lbl.pack(pady=(0, 10))
                logo_lbl.image = img
                parent._img = img
                return
            except:
                pass
        
        placeholder = tk.Frame(parent, width=tamanho[0], height=tamanho[1], bg="#4bc9a0")
        placeholder.pack(pady=(0, 10))
        placeholder.pack_propagate(False)
        tk.Label(placeholder, text="📚", font=("Arial", 50), bg="#4bc9a0").place(relx=0.5, rely=0.5, anchor="center")

    def carregar_logo_login(self, parent, tamanho=(100, 100)):
        """Carrega logo - TELA DE LOGIN"""
        proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # ==== MUDE O NOME DA IMAGEM AQUI PARA A TELA DE LOGIN ====
        caminho_logo = os.path.join(proj_root, "img", "logoLogin.png")  # <-- COLOQUE O NOME DA SUA IMAGEM AQUI
        
        if os.path.exists(caminho_logo):
            try:
                pil_img = Image.open(caminho_logo).resize(tamanho)
                img = ImageTk.PhotoImage(pil_img)
                logo_lbl = tk.Label(parent, image=img, bg=parent.cget("bg"))
                # ==== MUDE O ESPAÇAMENTO AQUI (pady) ====
                logo_lbl.pack(pady=(0, 10))
                logo_lbl.image = img
                parent._img = img
                return
            except:
                pass
        
        # Placeholder caso a imagem não exista
        placeholder = tk.Frame(parent, width=tamanho[0], height=tamanho[1], bg="#4bc9a0")
        placeholder.pack(pady=(0, 10))
        placeholder.pack_propagate(False)
        tk.Label(placeholder, text="🔐", font=("Arial", 40), bg="#4bc9a0").place(relx=0.5, rely=0.5, anchor="center")

    # -------------------- TELA INICIAL --------------------
    def tela_inicial(self):
        self.limpar_tela()
        
        frame = tk.Frame(self.root, bg=self.COR_FUNDO)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.carregar_logo(frame, tamanho=(140, 140))
        
        tk.Label(
            frame,
            text="Bem-vindo ao EstudAe!",
            font=("Arial", 22, "bold"),
            bg=self.COR_FUNDO,
            fg="#ffffff"
        ).pack(pady=(10, 35))
        
        btn_login = tk.Button(
            frame,
            text="Login",
            font=("Arial", 14),
            bg="#ffffff",
            fg=self.COR_TEXTO_ESCURO,
            width=22,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.tela_login
        )
        btn_login.pack(pady=(0, 15))
        
        label_cadastro = tk.Label(
            frame,
            text="Cadastre-se",
            font=("Arial", 12, "underline"),
            bg=self.COR_FUNDO,
            fg="#a7f3d0",
            cursor="hand2"
        )
        label_cadastro.pack(pady=10)
        label_cadastro.bind("<Button-1>", lambda e: self.tela_cadastro())
        label_cadastro.bind("<Enter>", lambda e: label_cadastro.config(fg="#d1fae5"))
        label_cadastro.bind("<Leave>", lambda e: label_cadastro.config(fg="#a7f3d0"))

    # -------------------- TELA DE LOGIN --------------------
    def tela_login(self):
        self.limpar_tela()
        
        # Container principal
        # ==== MUDE O rely AQUI PARA SUBIR/DESCER TUDO (imagem + card) ====
        # Valores menores = mais pra cima | Valores maiores = mais pra baixo
        container = tk.Frame(self.root, bg=self.COR_FUNDO)
        container.place(relx=0.5, rely=0.45, anchor="center")  # Mudei de 0.5 para 0.45 (mais pra cima)
        
        # ===== LOGO DA TELA DE LOGIN (DIFERENTE DA INICIAL) =====
        # ==== MUDE O TAMANHO DA IMAGEM AQUI: tamanho=(largura, altura) ====
        self.carregar_logo_login(container, tamanho=(150, 150))
        
        # ===== CARD COMEÇA AQUI =====
        card = tk.Frame(container, bg=self.COR_CARD, padx=10, pady=10)
        # ==== MUDE O ESPAÇAMENTO ENTRE LOGO E CARD AQUI: pady=(espaço_cima, espaço_baixo) ====
        card.pack(pady=(15, 0))  # Mudei de 10 para 15  # Espaço entre logo e card
        
        tk.Label(
            card,
            text="Login",
            font=("Arial", 24, "bold"),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO_ESCURO
        ).pack(pady=(10, 25))
        
        # Usuário
        tk.Label(card, text="Usuário:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5)
        usuario_container = self.criar_entry_arredondado(card, width=280)
        usuario_container.pack(pady=(5, 15))
        usuario_entry = usuario_container._entry
        
        # Senha
        tk.Label(card, text="Senha:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5)
        
        frame_senha_container = tk.Frame(card, bg=self.COR_CARD)
        frame_senha_container.pack(pady=(5, 5))
        
        canvas_senha = tk.Canvas(frame_senha_container, width=280, height=40, bg=self.COR_CARD, highlightthickness=0)
        canvas_senha.pack()
        
        radius = 8
        canvas_senha.create_rectangle(0, 0, 280, 40, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(0, 0, radius*2, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(280-radius*2, 0, 280, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(0, 40-radius*2, radius*2, 40, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(280-radius*2, 40-radius*2, 280, 40, fill=self.COR_CAMPO, outline="")
        
        senha_entry = tk.Entry(
            frame_senha_container,
            font=("Arial", 11),
            bg=self.COR_CAMPO,
            fg=self.COR_TEXTO_ESCURO,
            relief="flat",
            bd=0,
            show="*"
        )
        senha_entry.place(x=10, y=10, width=200, height=20)
        
        def toggle_senha():
            if senha_entry.cget("show") == "*":
                senha_entry.config(show="")
                btn_toggle.config(text="Ocultar")
            else:
                senha_entry.config(show="*")
                btn_toggle.config(text="Mostrar")
        
        btn_toggle = tk.Button(
            frame_senha_container,
            text="Mostrar",
            font=("Arial", 9),
            bg=self.COR_CAMPO,
            fg=self.COR_BOTAO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=toggle_senha
        )
        btn_toggle.place(x=220, y=8)
        
        label_esqueci = tk.Label(card, text="Esqueci minha senha", font=("Arial", 9), bg=self.COR_CARD, fg=self.COR_BOTAO, cursor="hand2")
        label_esqueci.pack(pady=(5, 25))
        label_esqueci.bind("<Button-1>", lambda e: self.tela_recuperar_senha())
        
        def logar():
            users = carregar_usuarios()
            u = usuario_entry.get().strip()
            s = senha_entry.get()
            if u in users and users[u]["senha"] == s:
                nome = users[u]['nome']
                messagebox.showinfo("Sucesso", f"Bem-vindo, {nome}!")
                if callable(self.on_login):
                    self.on_login(u, nome)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        
        btn_login = tk.Button(card, text="Entrar", font=("Arial", 14, "bold"), bg=self.COR_BOTAO, fg="#ffffff", width=25, height=2, relief="flat", cursor="hand2", command=logar)
        btn_login.pack(pady=(0, 20))
        
        btn_voltar = tk.Button(card, text="← Voltar", font=("Arial", 10), bg=self.COR_CARD, fg="#999999", relief="flat", bd=0, cursor="hand2", command=self.tela_inicial)
        btn_voltar.pack()
        
        usuario_entry.focus_set()
        self.root.bind("<Return>", lambda e: logar())

    # -------------------- TELA DE CADASTRO --------------------
    def tela_cadastro(self):
        self.limpar_tela()
        
        # Container principal - SEM SCROLL
        container = tk.Frame(self.root, bg=self.COR_FUNDO)
        container.pack(expand=True, fill="both")
        
        # ===== CARD SEM LOGO =====
        card = tk.Frame(container, bg=self.COR_CARD, padx=25, pady=15)
        card.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(card, text="Cadastro", font=("Arial", 22, "bold"), bg=self.COR_CARD, fg=self.COR_TEXTO_ESCURO).pack(pady=(5, 15))

        # Variáveis
        nome_var = tk.StringVar()
        sobrenome_var = tk.StringVar()
        usuario_var = tk.StringVar()
        senha_var = tk.StringVar()
        conf_var = tk.StringVar()
        tel_var = tk.StringVar()
        email_var = tk.StringVar()
        estado_var = tk.StringVar(value="Selecione o estado")

        # NOME E SOBRENOME (lado a lado) - espaçamento reduzido
        frame_nomes = tk.Frame(card, bg=self.COR_CARD)
        frame_nomes.pack(pady=3)
        
        frame_nome = tk.Frame(frame_nomes, bg=self.COR_CARD)
        frame_nome.pack(side="left", padx=3)
        tk.Label(frame_nome, text="Nome", font=("Arial", 10), bg=self.COR_CARD, fg="#666666").pack(anchor="w")
        nome_container = self.criar_entry_arredondado(frame_nome, var=nome_var, width=130)
        nome_container.pack()
        
        frame_sobrenome = tk.Frame(frame_nomes, bg=self.COR_CARD)
        frame_sobrenome.pack(side="left", padx=3)
        tk.Label(frame_sobrenome, text="Sobrenome", font=("Arial", 10), bg=self.COR_CARD, fg="#666666").pack(anchor="w")
        sobrenome_container = self.criar_entry_arredondado(frame_sobrenome, var=sobrenome_var, width=130)
        sobrenome_container.pack()
        
        nome_entry = nome_container._entry
        sobrenome_entry = sobrenome_container._entry

        # USUÁRIO - espaçamento reduzido
        tk.Label(card, text="Usuário:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        usuario_container = self.criar_entry_arredondado(card, var=usuario_var, width=280)
        usuario_container.pack(padx=5)
        usuario_entry = usuario_container._entry

        # SENHA com Mostrar/Ocultar - espaçamento reduzido
        tk.Label(card, text="Senha:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        
        frame_senha = tk.Frame(card, bg=self.COR_CARD)
        frame_senha.pack(padx=5)
        
        canvas_senha = tk.Canvas(frame_senha, width=280, height=40, bg=self.COR_CARD, highlightthickness=0)
        canvas_senha.pack()
        
        radius = 8
        canvas_senha.create_rectangle(0, 0, 280, 40, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(0, 0, radius*2, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(280-radius*2, 0, 280, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(0, 40-radius*2, radius*2, 40, fill=self.COR_CAMPO, outline="")
        canvas_senha.create_oval(280-radius*2, 40-radius*2, 280, 40, fill=self.COR_CAMPO, outline="")
        
        senha_entry = tk.Entry(frame_senha, textvariable=senha_var, show="*", font=("Arial", 11), bg=self.COR_CAMPO, fg=self.COR_TEXTO_ESCURO, relief="flat", bd=0)
        senha_entry.place(x=10, y=10, width=200, height=20)
        
        def toggle_s():
            if senha_entry.cget("show") == "*":
                senha_entry.config(show="")
                btn_s.config(text="Ocultar")
            else:
                senha_entry.config(show="*")
                btn_s.config(text="Mostrar")
        
        btn_s = tk.Button(frame_senha, text="Mostrar", font=("Arial", 9), bg=self.COR_CAMPO, fg=self.COR_BOTAO, relief="flat", bd=0, cursor="hand2", command=toggle_s)
        btn_s.place(x=220, y=8)

        # CONFIRMAR SENHA com Mostrar/Ocultar - espaçamento reduzido
        tk.Label(card, text="Confirmar Senha:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        
        frame_conf = tk.Frame(card, bg=self.COR_CARD)
        frame_conf.pack(padx=5)
        
        canvas_conf = tk.Canvas(frame_conf, width=280, height=40, bg=self.COR_CARD, highlightthickness=0)
        canvas_conf.pack()
        
        canvas_conf.create_rectangle(0, 0, 280, 40, fill=self.COR_CAMPO, outline="")
        canvas_conf.create_oval(0, 0, radius*2, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_conf.create_oval(280-radius*2, 0, 280, radius*2, fill=self.COR_CAMPO, outline="")
        canvas_conf.create_oval(0, 40-radius*2, radius*2, 40, fill=self.COR_CAMPO, outline="")
        canvas_conf.create_oval(280-radius*2, 40-radius*2, 280, 40, fill=self.COR_CAMPO, outline="")
        
        conf_entry = tk.Entry(frame_conf, textvariable=conf_var, show="*", font=("Arial", 11), bg=self.COR_CAMPO, fg=self.COR_TEXTO_ESCURO, relief="flat", bd=0)
        conf_entry.place(x=10, y=10, width=200, height=20)
        
        def toggle_conf():
            if conf_entry.cget("show") == "*":
                conf_entry.config(show="")
                btn_conf.config(text="Ocultar")
            else:
                conf_entry.config(show="*")
                btn_conf.config(text="Mostrar")
        
        btn_conf = tk.Button(frame_conf, text="Mostrar", font=("Arial", 9), bg=self.COR_CAMPO, fg=self.COR_BOTAO, relief="flat", bd=0, cursor="hand2", command=toggle_conf)
        btn_conf.place(x=220, y=8)

        # E-MAIL - espaçamento reduzido
        tk.Label(card, text="E-mail:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        email_container = self.criar_entry_arredondado(card, var=email_var, width=280)
        email_container.pack(padx=5)

        # DATA DE NASCIMENTO - espaçamento reduzido
        tk.Label(card, text="Data de nascimento:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        frame_data = tk.Frame(card, bg=self.COR_CARD)
        frame_data.pack(pady=3)
        
        dias = [str(i).zfill(2) for i in range(1, 32)]
        meses = [str(i).zfill(2) for i in range(1, 13)]
        anos = [str(i) for i in range(1940, datetime.now().year + 1)]
        
        dia_cb = ttk.Combobox(frame_data, values=dias, width=8, state="readonly")
        dia_cb.set("Dia")
        dia_cb.pack(side="left", padx=3)
        
        mes_cb = ttk.Combobox(frame_data, values=meses, width=8, state="readonly")
        mes_cb.set("Mês")
        mes_cb.pack(side="left", padx=3)
        
        ano_cb = ttk.Combobox(frame_data, values=anos, width=10, state="readonly")
        ano_cb.set("Ano")
        ano_cb.pack(side="left", padx=3)

        # ESTADO - espaçamento reduzido
        tk.Label(card, text="Estado:", font=("Arial", 10), bg=self.COR_CARD, fg="#666666", anchor="w").pack(fill="x", padx=5, pady=(8, 2))
        estado_cb = ttk.Combobox(card, values=ESTADOS_BRASIL, state="readonly", textvariable=estado_var)
        estado_cb.pack(fill="x", padx=5, ipady=5)

        # Mensagem de erro
        msg_label = tk.Label(card, text="", font=("Arial", 9), bg=self.COR_CARD, fg="#dc2626", wraplength=280)
        msg_label.pack(pady=8)
        
        def cadastrar():
            msg_label.config(text="")
            nome = nome_var.get().strip()
            sobrenome = sobrenome_var.get().strip()
            nome_completo = f"{nome} {sobrenome}".strip()
            usuario = usuario_var.get().strip()
            senha = senha_var.get()
            conf = conf_var.get()
            email = email_var.get().strip()
            estado = estado_var.get()
            dia, mes, ano = dia_cb.get(), mes_cb.get(), ano_cb.get()

            if not all([nome, sobrenome, usuario, senha, conf, email]) or estado == "Selecione o estado":
                msg_label.config(text="❌ Preencha todos os campos"); return
            if not data_valida(dia, mes, ano):
                msg_label.config(text="❌ Data de nascimento inválida"); return
            data_nasc = f"{dia}/{mes}/{ano}"

            ok, motivo = senha_valida(senha)
            if not ok: msg_label.config(text=f"❌ {motivo}"); return
            if senha != conf: msg_label.config(text="❌ As senhas não coincidem"); return
            if not email_valido(email): msg_label.config(text="❌ E-mail inválido"); return

            users = carregar_usuarios()
            if usuario in users: msg_label.config(text="❌ Usuário já existe"); return
            if any(d["email"] == email for d in users.values()):
                msg_label.config(text="❌ E-mail já cadastrado"); return

            try:
                salvar_usuario(usuario, senha, nome_completo, data_nasc, "", email, estado)  # tel = ""
            except Exception as ex:
                messagebox.showerror("Erro", f"Falha ao salvar: {ex}"); return

            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.tela_login()
        
        # Botão cadastrar - espaçamento reduzido
        btn_cadastrar = tk.Button(card, text="Cadastrar", font=("Arial", 13, "bold"), bg=self.COR_BOTAO, fg="#ffffff", width=25, height=2, relief="flat", cursor="hand2", command=cadastrar)
        btn_cadastrar.pack(pady=(8, 10))
        
        btn_voltar = tk.Button(card, text="← Voltar", font=("Arial", 10), bg=self.COR_CARD, fg="#999999", relief="flat", bd=0, cursor="hand2", command=self.tela_inicial)
        btn_voltar.pack()

        nome_entry.focus_set()
        self.root.bind("<Return>", lambda e: cadastrar())

    def tela_recuperar_senha(self):
        messagebox.showinfo("Info", "Em breve!")

# ------------------------------------------------------------
# TESTE
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from utils import calcular_tamanho, calcular_padding, calcular_font_size
    
    def callback_teste(user, nome):
        print(f"Login: {user} - {nome}")
    
    root = tk.Tk()
    root.geometry("375x812")
    root.resizable(False, False)
    app = App(root, on_login=callback_teste)
    root.mainloop()