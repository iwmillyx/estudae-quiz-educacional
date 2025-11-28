import tkinter as tk
from telas.tela_login import App as TelaLogin
from telas.home import montar_home
from telas.tela_enem import montar_enem
from telas.tela_militar import montar_militar
from telas.tela_quiz import TelaQuiz
from telas.tela_criarQuiz import montar_criador_quiz
from dados.banco_dadosUsuarios import (
    obter_dados_usuario,
    atualizar_pontuacao,
    obter_id_materia_por_nome,
    salvar_resultado_quiz
)

class Router:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.usuario_logado = None
        self.nome_logado = None
        self.id_usuario = None
        self.usuario_xp = 0
        self.usuario_nivel = 1
        self.materias_progresso = {}  # Armazena o progresso por matéria

    def limpar(self):
        """Limpa todos os widgets da janela"""
        for w in self.root.winfo_children():
            w.destroy()

    def ir_para_login(self):
        """Navega para a tela de login"""
        self.limpar()
        TelaLogin(self.root, on_login=self._login_ok)

    def _login_ok(self, usuario: str, nome: str, id_usuario: int = None):
        """Callback chamado após login bem-sucedido"""
        self.usuario_logado = usuario
        self.nome_logado = nome
        self.id_usuario = id_usuario  # ADICIONE ESTA LINHA
        
        # Carrega dados reais do banco
        if id_usuario:
            dados = obter_dados_usuario(id_usuario)
            self.usuario_xp = dados['xp_total']
            self.usuario_nivel = dados['nivel_geral']
        
        self.ir_para_home()

    def ir_para_home(self):
        """Navega para a tela home (escolha: ENEM ou Militar)"""
        if not self.usuario_logado:
            self.ir_para_login()
            return
            
        # Pega dados do banco se tiver id_usuario
        if self.id_usuario:
            dados_usuario = obter_dados_usuario(self.id_usuario)
        else:
            dados_usuario = {
                'nome': self.nome_logado,
                'xp_total': self.usuario_xp,
                'nivel_geral': self.usuario_nivel,
                'ranking_posicao': 0,
                'ranking_enem': 0,
                'ranking_militar': 0,
                'streak_dias': 0,
                'progresso_geral': 0,
                'xp_enem': 0,
                'progresso_enem': 0,
                'xp_militar': 0,
                'progresso_militar': 0
            }
            
        self.limpar()
        montar_home(
            self.root,
            usuario=self.usuario_logado,
            nome=self.nome_logado,
            on_enem=self.ir_para_enem,
            on_militar=self.ir_para_militar,
            on_criar_quiz=self.ir_para_criar_quiz,
            dados_usuario=dados_usuario
        )
    
    def ir_para_enem(self):
        """Navega para a tela do ENEM"""
        self.limpar()
        montar_enem(
            self.root, 
            usuario=self.id_usuario,
            nome=self.nome_logado,
            on_voltar=self.ir_para_home,
            on_fazer_quiz=self._fazer_quiz_enem
        )

    def ir_para_militar(self):
        """Navega para a tela de Concurso Militar"""
        self.limpar()
        montar_militar(
            self.root,
            usuario=(self.id_usuario, self.nome_logado),
            nome=self.nome_logado,
            on_voltar=self.ir_para_home,
            on_fazer_quiz=self._fazer_quiz_militar
        )
    
    def _fazer_quiz_enem(self, materia: str, nivel: int):
        """
        Inicia um quiz do ENEM para a matéria e nível específicos
        
        Args:
            materia: Nome da matéria (ex: "Física", "Matemática")
            nivel: Nível do quiz (1, 2 ou 3)
        """
        # Converte número do nível para nome
        nivel_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
        nivel_nome = nivel_map.get(nivel, "Fácil")
        
        self.limpar()
        TelaQuiz(
            self.root,
            usuario=self.id_usuario,
            modo="enem",
            materia=materia,
            nivel=nivel_nome,
            on_voltar=self.ir_para_enem,
            on_finalizar=self._quiz_finalizado_enem
        )
    
    def _fazer_quiz_militar(self, materia: str, nivel: int):
        """
        Inicia um quiz Militar para a matéria e nível específicos
        
        Args:
            materia: Nome da matéria
            nivel: Nível do quiz (1, 2 ou 3)
        """
        # Converte número do nível para nome
        nivel_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
        nivel_nome = nivel_map.get(nivel, "Fácil")
        
        self.limpar()
        TelaQuiz(
            self.root,
            usuario=self.id_usuario,
            modo="militar",
            materia=materia,
            nivel=nivel_nome,
            on_voltar=self.ir_para_militar,
            on_finalizar=self._quiz_finalizado_militar
        )
    
    def _quiz_finalizado_enem(self, resultado):
        """
        Callback chamado quando o usuário termina um quiz do ENEM
        
        Args:
            resultado: dict com {xp_ganho, acertos, erros, materia, nivel}
        """
        # SALVA PONTUAÇÃO NO HISTÓRICO DE QUIZZES (banco de dados) 
        if self.id_usuario:
            materia = resultado.get('materia')
            nivel = resultado.get('nivel')
            xp_ganho = resultado.get('xp_ganho', 0)
            acertos = resultado.get('acertos', 0)
            total_questoes = resultado.get('total_questoes', 10)
            
            # Remove sufixo do concurso se houver
            materia_limpa = materia.split(" (")[0]
            
            # Salva no histórico
            try:
                salvar_resultado_quiz(
                    id_usuario=self.id_usuario,
                    id_quiz=1,
                    materia=materia_limpa,
                    nivel=nivel,
                    acertos=acertos,
                    total_questoes=total_questoes,
                    xp_ganho=xp_ganho
                )

                print(f"✅ Quiz salvo no histórico: {materia_limpa} - {nivel}")
            except Exception as e:
                print(f"❌ Erro ao salvar histórico: {e}")

            # Salva pontuação no banco de dados (sistema antigo)
            id_materia = obter_id_materia_por_nome(materia_limpa)
            
            if id_materia:
                try:
                    atualizar_pontuacao(self.id_usuario, id_materia, xp_ganho)
                    print(f"✅ {xp_ganho} XP salvos em {materia_limpa}!")
                except Exception as e:
                    print(f"❌ Erro ao salvar pontuação: {e}")

        # Atualiza XP do usuário local
        self.usuario_xp += resultado.get('xp_ganho', 0)
        
        # Atualiza nível da matéria se passou
        nivel = resultado.get('nivel')
        aproveitamento = resultado.get('aproveitamento', 0)
        
        # Se acertou 70% ou mais, desbloqueia próximo nível
        if aproveitamento >= 70:
            materia = resultado.get('materia')
            chave = f"{materia}_{nivel}"
            self.materias_progresso[chave] = True
        
        # Volta para a tela do ENEM
        self.ir_para_enem()
    
    def _quiz_finalizado_militar(self, resultado):
        """Callback quando termina quiz militar"""

        # Salva pontuação no banco de dados
        if self.id_usuario:
            materia = resultado.get('materia')
            nivel = resultado.get('nivel')
            xp_ganho = resultado.get('xp_ganho', 0)
            acertos = resultado.get('acertos', 0)
            total_questoes = resultado.get('total_questoes', 10)
            
            # Remove sufixo do concurso
            materia_limpa = materia.split(" (")[0]
            
            # Salva no histórico
            try:
                salvar_resultado_quiz(
                    id_usuario=self.id_usuario,
                    id_quiz=2,  # 2 = MILITAR
                    materia=materia_limpa,
                    nivel=nivel,
                    acertos=acertos,
                    total_questoes=total_questoes,
                    xp_ganho=xp_ganho
                )
                print(f"✅ Quiz salvo no histórico: {materia_limpa} - {nivel}")
            except Exception as e:
                print(f"❌ Erro ao salvar histórico: {e}")

            # Salva pontuação no banco de dados (sistema antigo)
            id_materia = obter_id_materia_por_nome(materia)
            
            if id_materia:
                try:
                    atualizar_pontuacao(self.id_usuario, id_materia, xp_ganho)
                    print(f"✅ {xp_ganho} XP salvos em {materia}!")
                except Exception as e:
                    print(f"❌ Erro ao salvar pontuação: {e}")

        # atualiza XP local
        self.usuario_xp += resultado.get('xp_ganho', 0)
        
        nivel = resultado.get('nivel')
        aproveitamento = resultado.get('aproveitamento', 0)
        
        if aproveitamento >= 70:
            materia = resultado.get('materia')
            chave = f"{materia}_{nivel}"
            self.materias_progresso[chave] = True
        
        self.ir_para_militar()
    
    def ir_para_criar_quiz(self):
        """Navega para a tela de criar quiz personalizado"""
        self.limpar()
        montar_criador_quiz(
            self.root,
            usuario_xp=self.usuario_xp,
            usuario_nivel=self.usuario_nivel,
            on_voltar=self.ir_para_home,
            on_salvar=self._salvar_quiz_criado
        )
    
    def _salvar_quiz_criado(self, quiz_data):
        """
        Callback quando o usuário salva um quiz personalizado
        
        Args:
            quiz_data: dict com os dados do quiz criado
        """

        # Salva o quiz no banco de dados
        if self.id_usuario:
            try:
                from dados.banco_dadosUsuarios import criar_quiz_personalizado, adicionar_pergunta_quiz
                
                # Cria o quiz
                criar_quiz_personalizado(
                    self.id_usuario,
                    quiz_data['titulo'],
                    quiz_data.get('descricao', '')
                )
                
                # TODO: Adicionar perguntas ao quiz
                # (você precisará modificar criar_quiz_personalizado para retornar o id)
                
                print(f"💾 Quiz '{quiz_data['titulo']}' salvo com sucesso!")
                
                from tkinter import messagebox
                messagebox.showinfo("Sucesso!", f"Quiz '{quiz_data['titulo']}' criado com sucesso! 🎉")
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Erro", f"Erro ao salvar quiz: {e}")
                print(f"❌ Erro ao salvar quiz: {e}")
        
        # Volta para home
        self.ir_para_home()
