# ------------------------------------------------------------
# Aqui ficam:
#  - a interface de Login e Cadastro
#  - leitura/gravação de 'usuarios.txt' (formato: usuario;senha;nome;nasc;tel;email;estado)
#  - validações básicas (e-mail, telefone, data, senha)
#  - "Esqueci a senha": redefine a senha com e-mail + data de nascimento
#
# Observações:
#  - é uma versão simples para começar rápido (sem banco ainda)
#  - quando migrar para banco (SQLite/Postgres), basta trocar as funções
#    de salvar/carregar mantendo as mesmas assinaturas
# ------------------------------------------------------------

import tkinter as tk                 # componentes base da GUI
from tkinter import ttk, messagebox  # widgets modernos e caixas de diálogo
import os                            # checar se arquivo existe
import re                            # validação simples com regex
from datetime import datetime        # validar data (e evitar futura)

ARQUIVO_USUARIOS = "usuarios.txt"    # arquivo onde guardamos os cadastros

# ------------------------------------------------------------
# LISTA DE ESTADOS (usada no combobox do cadastro)
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
# FUNÇÕES DE ARQUIVO
# ------------------------------------------------------------
def carregar_usuarios():
    """
    Lê usuarios.txt e devolve um dicionário no formato:
    {
      "usuario1": {"senha": "...", "nome": "...", "nasc": "dd/mm/aaaa",
                   "tel": "...", "email": "...", "estado": "..."},
      ...
    }
    Se o arquivo não existir, retorna {}.
    """
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
    """Acrescenta um novo usuário no final do arquivo (7 campos)."""
    with open(ARQUIVO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(f"{usuario};{senha};{nome};{nasc};{tel};{email};{estado}\n")

def salvar_todos(usuarios_dict):
    """Regrava o arquivo inteiro (útil após redefinição de senha)."""
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        for u, d in usuarios_dict.items():
            f.write(f"{u};{d['senha']};{d['nome']};{d['nasc']};{d['tel']};{d['email']};{d['estado']}\n")

# ------------------------------------------------------------
# VALIDAÇÕES BÁSICAS (simples, sem frescura)
# ------------------------------------------------------------
def email_valido(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""))

def telefone_valido(tel: str) -> bool:
    return bool(re.fullmatch(r"[0-9 \-\+\(\)]{8,20}", tel or ""))

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
# APLICATIVO (GUI)
# ------------------------------------------------------------
class App:
    def __init__(self, root, on_login=None):
        self.root = root
        self.on_login = on_login
        self.root.title("Login e Cadastro")
        self.root.geometry("340x300")
        self.root.resizable(False, False)
        self.tela_inicial()

    def limpar_tela(self):
        for w in self.root.winfo_children():
            w.destroy()

    # -------------------- TELA INICIAL --------------------
    def tela_inicial(self):
        self.limpar_tela()
        tk.Label(self.root, text="Bem-vindo!", font=("Arial", 16, "bold")).pack(pady=30)
        ttk.Button(self.root, text="Login", width=18, command=self.tela_login).pack(pady=12)

        link = tk.Label(self.root, text="Cadastre-se", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        link.pack(pady=6)
        link.bind("<Enter>", lambda e: link.config(fg="darkblue"))
        link.bind("<Leave>", lambda e: link.config(fg="blue"))
        link.bind("<Button-1>", lambda e: self.tela_cadastro())

    # -------------------- TELA DE LOGIN --------------------
    def tela_login(self):
        self.limpar_tela()
        tk.Label(self.root, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.root, text="Usuário:").pack(anchor="w", padx=30)
        usuario_entry = ttk.Entry(self.root)
        usuario_entry.pack(fill="x", padx=30)

        tk.Label(self.root, text="Senha:").pack(anchor="w", padx=30, pady=(8, 0))
        frame_senha = tk.Frame(self.root)
        frame_senha.pack(fill="x", padx=30)
        senha_entry = ttk.Entry(frame_senha, show="*")
        senha_entry.pack(side="left", fill="x", expand=True)

        def toggle():
            senha_entry.config(show="" if senha_entry.cget("show") == "*" else "*")
            btn_toggle.config(text="Ocultar" if senha_entry.cget("show") == "" else "Mostrar")
        btn_toggle = ttk.Button(frame_senha, text="Mostrar", width=10, command=toggle)
        btn_toggle.pack(side="left", padx=6)

        def logar():
            users = carregar_usuarios()
            u = usuario_entry.get().strip()
            s = senha_entry.get()
            if u in users and users[u]["senha"] == s:
                nome = users[u]['nome']
                messagebox.showinfo("Sucesso", f"Bem-vindo, {nome}!")
                # CHAVE: avisa o router que deu certo
                if callable(self.on_login):
                    self.on_login(u, nome)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

        def esqueci():
            janela = tk.Toplevel(self.root)
            janela.title("Recuperar Senha")
            janela.geometry("320x230")
            janela.resizable(False, False)

            tk.Label(janela, text="Recuperar Senha", font=("Arial", 12, "bold")).pack(pady=8)
            tk.Label(janela, text="E-mail cadastrado:").pack(anchor="w", padx=20)
            email_e = ttk.Entry(janela); email_e.pack(fill="x", padx=20, pady=2)
            tk.Label(janela, text="Data de nascimento (dd/mm/aaaa):").pack(anchor="w", padx=20)
            nasc_e = ttk.Entry(janela); nasc_e.pack(fill="x", padx=20, pady=2)
            tk.Label(janela, text="Nova senha:").pack(anchor="w", padx=20)
            nova_e = ttk.Entry(janela, show="*"); nova_e.pack(fill="x", padx=20, pady=2)
            tk.Label(janela, text="Confirmar nova senha:").pack(anchor="w", padx=20)
            conf_e = ttk.Entry(janela, show="*"); conf_e.pack(fill="x", padx=20, pady=2)

            msg = tk.StringVar(value="")
            tk.Label(janela, textvariable=msg, fg="red", wraplength=280, justify="left").pack(anchor="w", padx=20, pady=4)

            def redefinir():
                email = email_e.get().strip()
                nasc = nasc_e.get().strip()
                nova = nova_e.get()
                conf = conf_e.get()
                if not email or not nasc or not nova or not conf:
                    msg.set("Preencha todos os campos."); return
                if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", nasc):
                    msg.set("Use o formato dd/mm/aaaa na data."); return
                ok, motivo = senha_valida(nova)
                if not ok: msg.set(motivo); return
                if nova != conf: msg.set("As senhas não coincidem."); return

                users = carregar_usuarios()
                alvo = None
                for user, d in users.items():
                    if d["email"] == email:
                        alvo = user; break
                if not alvo: msg.set("E-mail não encontrado."); return
                if users[alvo]["nasc"] != nasc: msg.set("Data de nascimento não confere."); return

                users[alvo]["senha"] = nova
                salvar_todos(users)
                messagebox.showinfo("Sucesso", "Senha redefinida!")
                janela.destroy()

            ttk.Button(janela, text="Redefinir", command=redefinir).pack(pady=8)
            ttk.Button(janela, text="Fechar", command=janela.destroy).pack()
            email_e.focus_set()
            janela.bind("<Return>", lambda e: redefinir())

        ttk.Button(self.root, text="Entrar", command=logar).pack(pady=12)

        link = tk.Label(self.root, text="Esqueci minha senha", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        link.pack(pady=4)
        link.bind("<Enter>", lambda e: link.config(fg="darkblue"))
        link.bind("<Leave>", lambda e: link.config(fg="blue"))
        link.bind("<Button-1>", lambda e: esqueci())

        ttk.Button(self.root, text="Voltar", command=self.tela_inicial).pack(pady=10)

        usuario_entry.focus_set()
        self.root.bind("<Return>", lambda e: logar())

    # -------------------- TELA DE CADASTRO --------------------
    def tela_cadastro(self):
        cadastro = tk.Toplevel(self.root)
        cadastro.title("Cadastro de Usuário")
        cadastro.geometry("420x560")
        cadastro.resizable(False, False)

        tk.Label(cadastro, text="Cadastro de Usuário", font=("Arial", 14, "bold")).pack(pady=10)

        usuario_var = tk.StringVar()
        senha_var   = tk.StringVar()
        conf_var    = tk.StringVar()
        nome_var    = tk.StringVar()
        tel_var     = tk.StringVar()
        email_var   = tk.StringVar()
        estado_var  = tk.StringVar(value="Selecione o estado")

        def rotulo(txt): tk.Label(cadastro, text=txt).pack(anchor="w", padx=20)
        def entrada(var, show=None):
            e = ttk.Entry(cadastro, textvariable=var, show=show)
            e.pack(fill="x", padx=20, pady=2); return e

        rotulo("Usuário:"); usuario_e = entrada(usuario_var)

        frame_s = tk.Frame(cadastro); frame_s.pack(fill="x", padx=20, pady=2)
        tk.Label(frame_s, text="Senha:").pack(anchor="w")
        senha_e = ttk.Entry(frame_s, textvariable=senha_var, show="*")
        senha_e.pack(side="left", fill="x", expand=True)
        def toggle_s():
            senha_e.config(show="" if senha_e.cget("show") == "*" else "*")
            btn_s.config(text="Ocultar" if senha_e.cget("show") == "" else "Mostrar")
        btn_s = ttk.Button(frame_s, text="Mostrar", width=10, command=toggle_s); btn_s.pack(side="left", padx=6)

        rotulo("Confirmar Senha:"); conf_e = entrada(conf_var, show="*")
        rotulo("Nome completo:");   nome_e = entrada(nome_var)
        rotulo("Telefone:");        tel_e  = entrada(tel_var)
        rotulo("E-mail:");          email_e= entrada(email_var)

        tk.Label(cadastro, text="Data de nascimento:").pack(anchor="w", padx=20)
        frame_data = tk.Frame(cadastro); frame_data.pack(pady=2)
        dias = [str(i).zfill(2) for i in range(1, 32)]
        meses = [str(i).zfill(2) for i in range(1, 13)]
        ano_atual = datetime.now().year
        anos = [str(i) for i in range(1940, ano_atual + 1)]
        dia_cb = ttk.Combobox(frame_data, values=dias, width=5, state="readonly")
        mes_cb = ttk.Combobox(frame_data, values=meses, width=5, state="readonly")
        ano_cb = ttk.Combobox(frame_data, values=anos, width=7, state="readonly")
        dia_cb.set("Dia"); mes_cb.set("Mês"); ano_cb.set("Ano")
        dia_cb.pack(side="left", padx=3); mes_cb.pack(side="left", padx=3); ano_cb.pack(side="left", padx=3)

        tk.Label(cadastro, text="Estado:").pack(anchor="w", padx=20)
        estado_cb = ttk.Combobox(cadastro, values=ESTADOS_BRASIL, state="readonly", textvariable=estado_var)
        estado_cb.pack(fill="x", padx=20, pady=2)

        msg = tk.StringVar(value="")
        tk.Label(cadastro, textvariable=msg, fg="red", justify="left", wraplength=360).pack(padx=20, pady=4, anchor="w")

        def cadastrar():
            msg.set("")
            usuario = usuario_var.get().strip()
            senha   = senha_var.get()
            conf    = conf_var.get()
            nome    = nome_var.get().strip()
            tel     = tel_var.get().strip()
            email   = email_var.get().strip()
            estado  = estado_var.get()
            dia, mes, ano = dia_cb.get(), mes_cb.get(), ano_cb.get()

            if not all([usuario, senha, conf, nome, tel, email]) or estado == "Selecione o estado":
                msg.set("Preencha todos os campos."); return
            if not data_valida(dia, mes, ano):
                msg.set("Data de nascimento inválida."); return
            data_nasc = f"{dia}/{mes}/{ano}"

            ok, motivo = senha_valida(senha)
            if not ok: msg.set(motivo); return
            if senha != conf: msg.set("As senhas não coincidem."); return
            if not email_valido(email): msg.set("E-mail inválido."); return
            if not telefone_valido(tel): msg.set("Telefone inválido (use dígitos e + - ( ) )."); return

            users = carregar_usuarios()
            if usuario in users: msg.set("Usuário já existe."); return
            if any(d["email"] == email for d in users.values()): msg.set("Este e-mail já está cadastrado."); return

            try:
                salvar_usuario(usuario, senha, nome, data_nasc, tel, email, estado)
            except Exception as ex:
                messagebox.showerror("Erro", f"Falha ao salvar: {ex}"); return

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            cadastro.destroy()

        frame_b = tk.Frame(cadastro); frame_b.pack(pady=12)
        ttk.Button(frame_b, text="Cadastrar", command=cadastrar, width=16).pack(side="left", padx=6)
        ttk.Button(frame_b, text="Fechar", command=cadastro.destroy, width=12).pack(side="left", padx=6)

        usuario_e.focus_set()
        cadastro.bind("<Return>", lambda e: cadastrar())

# ------------------------------------------------------------
# EXECUÇÃO
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
