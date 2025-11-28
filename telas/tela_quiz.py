import tkinter as tk
from tkinter import messagebox
import time
import random
import sys
import os

# Adiciona o diretório pai ao path para importar dados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dados.banco_dadosUsuarios import obter_perguntas_por_nivel, conectar


class TelaQuiz:
    def __init__(self, root, usuario, modo="enem", materia=None, nivel=None, on_voltar=None, on_finalizar=None):
        self.root = root
        self.usuario = usuario
        self.modo = modo
        self.materia_filtro = materia
        self.nivel_filtro = nivel
        self.on_voltar = on_voltar
        self.on_finalizar = on_finalizar

        self.timer_id = None
        self.destruido = False

        # Cores
        self.COR_FUNDO = "#07442E"
        self.COR_CARD = "#ffffff"
        self.COR_CERTA = "#4caf50"
        self.COR_ERRADA = "#f44336"
        self.COR_BOTAO = "#00bcd4"
        self.COR_CAMPO = "#e3f2fd"

        # ===== BUSCA PERGUNTAS DO BANCO DE DADOS =====
        self.questoes = self.carregar_perguntas_do_banco()

        # ===== VALIDAÇÃO FINAL =====
        if len(self.questoes) == 0:
            messagebox.showerror(
                "Sem Questões",
                "Não há questões disponíveis!\n\nExecute 'python popular_perguntas.py' para importar questões da API."
            )
            if callable(on_voltar):
                on_voltar()
            return

        # ===== EMBARALHA E LIMITA =====
        random.shuffle(self.questoes)
        num_questoes = min(10, len(self.questoes))
        self.questoes = self.questoes[:num_questoes]

        # ===== DEBUG =====
        print("\nQUIZ INICIADO:")
        print(f"   Modo: {modo.upper()}")
        print(f"   Matéria: {materia or 'Todas'}")
        print(f"   Nível: {nivel or 'Todos'}")
        print(f"   Questões encontradas: {len(self.questoes)}")

        if num_questoes < 10:
            print(f"   ATENÇÃO: Apenas {num_questoes} questões encontradas!")

        if num_questoes < 5:
            messagebox.showwarning(
                "Poucas Questões",
                f"Este quiz tem apenas {num_questoes} questão(ões)!"
            )

        self.questao_atual = 0
        self.acertos = 0
        self.erros = 0
        self.streak = 0
        self.max_streak = 0
        self.xp_total = 0
        self.tempo_inicio = None
        self.tempo_limite = 30
        self.timer_ativo = True
        self.respondeu = False

        self.montar_tela()
        self.mostrar_questao()
        self.iniciar_timer()

    def salvar_progresso_no_banco(self):
        """Salva o progresso do quiz no banco de dados"""
        try:
            from dados.banco_dadosUsuarios import atualizar_pontuacao, obter_id_materia_por_nome, salvar_progresso_nivel
            
            # Atualizar pontuação na matéria
            if self.materia_filtro:
                id_materia = obter_id_materia_por_nome(self.materia_filtro)
                if id_materia:
                    atualizar_pontuacao(self.usuario, id_materia, self.xp_total)
            
            # Salvar progresso do nível
            if self.materia_filtro and self.nivel_filtro:
                salvar_progresso_nivel(
                    self.usuario, 
                    self.materia_filtro, 
                    self.nivel_filtro,
                    self.xp_total, 
                    self.acertos, 
                    self.erros
                )
            
            return True
        except Exception as e:
            print(f"Erro ao salvar progresso: {e}")
            return False

    # --------------------------------------------------------
    # BANCO DE DADOS
    # --------------------------------------------------------
    def carregar_perguntas_do_banco(self):
        questoes = []
        print("\n[DEBUG] carregar_perguntas_do_banco() chamado")
        print(f"[DEBUG] Modo: {self.modo}")
        print(f"[DEBUG] Matéria filtro: {self.materia_filtro}")
        print(f"[DEBUG] Nível filtro: {self.nivel_filtro}")
        
        conn = conectar()

        try:
            cursor = conn.cursor()

            query = """
                SELECT 
                    p.id_pergunta, p.enunciado,
                    p.alternativa_a, p.alternativa_b, p.alternativa_c, p.alternativa_d,
                    p.alternativa_correta,
                    n.nome AS nivel,
                    m.nome AS materia
                FROM pergunta p
                JOIN nivel n ON p.id_nivel = n.id_nivel
                JOIN materia m ON n.id_materia = m.id_materia
                JOIN categoria c ON m.id_categoria = c.id_categoria
                WHERE c.id_quiz = ?
            """

            id_quiz = 1 if self.modo == "enem" else 2
            params = [id_quiz]

            if self.materia_filtro:
                query += " AND m.nome = ?"
                params.append(self.materia_filtro)

            if self.nivel_filtro:
                query += " AND n.nome = ?"
                params.append(self.nivel_filtro)

            print(f"[DEBUG] Query: {query}")
            print(f"[DEBUG] Params: {params}")

            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            print(f"[DEBUG] Perguntas encontradas: {len(resultados)}")

            for row in resultados:
                questoes.append({
                    "id": row[0],
                    "enunciado": row[1],
                    "alternativas": [
                        {"letra": "A", "texto": row[2]},
                        {"letra": "B", "texto": row[3]},
                        {"letra": "C", "texto": row[4]},
                        {"letra": "D", "texto": row[5]}
                    ],
                    "resposta_correta": row[6],
                    "nivel": row[7],
                    "materia": row[8],
                    "xp": self.calcular_xp_por_nivel(row[7]),
                    "explicacao": "Confira a resposta correta acima!"
                })

            conn.close()

        except Exception as e:
            print(f"[ERRO] Erro ao carregar perguntas: {e}")
            import traceback
            traceback.print_exc()
            conn.close()

        return questoes
    
    def calcular_xp_por_nivel(self, nivel):
        xp_map = {"Fácil": 10, "Médio": 15, "Difícil": 25}
        return xp_map.get(nivel, 10)

    # --------------------------------------------------------
    # LIMPEZA
    # --------------------------------------------------------
    def limpar_tela(self):
        self.destruido = True
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

        for w in self.root.winfo_children():
            try:
                w.destroy()
            except:
                pass

    def destruir(self):
        self.destruido = True
        self.timer_ativo = False

        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

        self.limpar_tela()

    # --------------------------------------------------------
    # TELA
    # --------------------------------------------------------
    def confirmar_saida(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?\nSeu progresso será perdido."):
            self.voltar()

    def montar_tela(self):
        # não chame limpar_tela aqui
        for w in self.root.winfo_children():
            w.destroy()

        self.main_frame = tk.Frame(self.root, bg=self.COR_FUNDO)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header = tk.Frame(self.main_frame, bg=self.COR_FUNDO)
        header.pack(fill="x", pady=10)

        left_header = tk.Frame(header, bg=self.COR_FUNDO)
        left_header.pack(side="left")

        self.label_questao = tk.Label(left_header, text="Questão 1/10",
                                      font=("Arial", 11, "bold"),
                                      bg=self.COR_FUNDO, fg="white")
        self.label_questao.pack(side="left")

        self.label_streak = tk.Label(left_header, text="🔥 0",
                                     font=("Arial", 11, "bold"),
                                     bg=self.COR_FUNDO, fg="#ffa726")
        self.label_streak.pack(side="left", padx=15)

        right_header = tk.Frame(header, bg=self.COR_FUNDO)
        right_header.pack(side="right")

        self.label_timer = tk.Label(right_header, text="30s",
                                    font=("Arial", 11, "bold"),
                                    bg=self.COR_FUNDO, fg="white")
        self.label_timer.pack(side="left", padx=10)

        self.btn_sair = tk.Button(right_header, text="✕",
                                  font=("Arial", 14, "bold"),
                                  bg="#f44336", fg="white",
                                  relief="flat", width=3,
                                  command=self.confirmar_saida)
        self.btn_sair.pack(side="left")

        self.card_questao = tk.Frame(self.main_frame, bg=self.COR_CARD)
        self.card_questao.pack(fill="both", expand=True, pady=10)

        self.label_materia = tk.Label(self.card_questao, text="",
                                      font=("Arial", 10),
                                      bg=self.COR_CARD, fg="#666")
        self.label_materia.pack(pady=5)

        self.label_enunciado = tk.Label(self.card_questao, text="",
                                        font=("Arial", 13),
                                        bg=self.COR_CARD, fg="#333",
                                        wraplength=340, justify="left")
        self.label_enunciado.pack(padx=10, pady=15)

        self.frame_alternativas = tk.Frame(self.card_questao, bg=self.COR_CARD)
        self.frame_alternativas.pack(fill="both", expand=True, padx=15, pady=10)

        # ===== ADICIONADO: placeholder do card de feedback =====
        self.feedback_frame = tk.Frame(self.main_frame, bg=self.COR_FUNDO)
        self.feedback_frame.pack(fill="x", pady=(0, 10))

        self.btn_proxima = tk.Button(self.main_frame, text="Próxima →",
                                     font=("Arial", 12, "bold"),
                                     bg=self.COR_BOTAO, fg="white",
                                     relief="flat",
                                     command=self.proxima_questao)

    # --------------------------------------------------------
    # QUESTÃO
    # --------------------------------------------------------
    def mostrar_questao(self):
        if self.questao_atual >= len(self.questoes):
            self.mostrar_resultado()
            return

        self.respondeu = False
        self.timer_ativo = True

        # ===== ADICIONADO: limpar card de feedback =====
        for w in self.feedback_frame.winfo_children():
            w.destroy()

        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

        self.tempo_inicio = time.time()

        questao = self.questoes[self.questao_atual]

        self.label_questao.config(text=f"Questão {self.questao_atual+1}/{len(self.questoes)}")
        self.label_streak.config(text=f"🔥 {self.streak}")
        self.label_timer.config(text=f"{self.tempo_limite}s", fg="white")

        self.label_materia.config(text=f"Matéria: {questao['materia']}")
        self.label_enunciado.config(text=questao["enunciado"])

        for w in self.frame_alternativas.winfo_children():
            w.destroy()

        self.botoes_alternativas = []
        for alt in questao["alternativas"]:
            btn = tk.Button(
                self.frame_alternativas,
                text=f"{alt['letra']}) {alt['texto']}",
                font=("Arial", 10),
                bg=self.COR_CAMPO,
                anchor="w",
                wraplength=320,  # ADICIONE ESTA LINHA
                justify="left",  # ADICIONE ESTA LINHA
                relief="flat",
                command=lambda l=alt['letra']: self.verificar_resposta(l)
            )
            btn.pack(fill="x", pady=4, padx=5)
            self.botoes_alternativas.append((btn, alt["letra"]))

        self.btn_proxima.pack_forget()
        self.atualizar_timer()

    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------
    def atualizar_timer(self):
        if self.destruido or self.respondeu or not self.timer_ativo:
            return

        tempo_decorrido = int(time.time() - self.tempo_inicio)
        tempo_restante = max(0, self.tempo_limite - tempo_decorrido)

        self.label_timer.config(text=f"{tempo_restante}s")

        if tempo_restante <= 0:
            self.tempo_esgotado()
            return

        self.timer_id = self.root.after(1000, self.atualizar_timer)

    def tempo_esgotado(self):
        if self.respondeu or not self.timer_ativo:
            return

        self.timer_ativo = False
        self.respondeu = True

        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass

        self.erros += 1
        self.streak = 0
        self.label_streak.config(text="🔥 0")

        questao = self.questoes[self.questao_atual]
        for btn, letra in self.botoes_alternativas:
            btn.config(state="disabled")
            if letra == questao["resposta_correta"]:
                btn.config(bg=self.COR_CERTA, fg="white", font=("Arial", 11, "bold"))

        # ===== ALTERADO: usar card =====
        self.mostrar_feedback(
            "⏱ Tempo Esgotado",
            f"O tempo acabou!\nCorreta: {questao['resposta_correta']}\n\nExplicação:\n{questao['explicacao']}",
            "#ff9800"
        )

        self.btn_proxima.pack(fill="x", pady=10)

    # ===============================================================
    # ===== ADICIONADO: FUNÇÃO PARA MOSTRAR FEEDBACK NO CARD =====
    # ===============================================================
    def mostrar_feedback(self, titulo, mensagem, cor):
        # Limpa qualquer feedback antigo
        for w in self.feedback_frame.winfo_children():
            w.destroy()

        card = tk.Frame(self.feedback_frame, bg=cor, padx=10, pady=10)
        card.pack(fill="x", padx=10)

        lbl_titulo = tk.Label(card, text=titulo, font=("Arial", 12, "bold"),
                            bg=cor, fg="white")
        lbl_titulo.pack(anchor="w")

        lbl_msg = tk.Label(card, text=mensagem, font=("Arial", 10),
                        bg=cor, fg="white", justify="left", wraplength=330)
        lbl_msg.pack(anchor="w", pady=(5, 0))

    # --------------------------------------------------------
    # RESPOSTA
    # --------------------------------------------------------
    def verificar_resposta(self, letra_escolhida):
        if self.respondeu:
            return

        self.timer_ativo = False
        self.respondeu = True

        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass

        questao = self.questoes[self.questao_atual]
        correta = questao["resposta_correta"]

        for btn, letra in self.botoes_alternativas:
            btn.config(state="disabled")
            if letra == correta:
                btn.config(bg=self.COR_CERTA, fg="white", font=("Arial", 11, "bold"))
            elif letra == letra_escolhida:
                btn.config(bg=self.COR_ERRADA, fg="white")

        acertou = letra_escolhida == correta
        if acertou:
            self.acertos += 1
            self.streak += 1
            self.xp_total += questao["xp"]

            # ===== ALTERADO: usar card ao invés de messagebox =====
            self.mostrar_feedback(
                "✔ Resposta Correta!",
                f"Você acertou!\n+{questao['xp']} XP",
                self.COR_CERTA
            )
        else:
            self.erros += 1
            self.streak = 0

            # ===== ALTERADO: usar card ao invés de messagebox =====
            self.mostrar_feedback(
                "✘ Resposta Incorreta",
                f"Você errou.\nCorreta: {correta}",
                self.COR_ERRADA
            )


        self.label_streak.config(text=f"🔥 {self.streak}")
        self.btn_proxima.pack(fill="x", pady=10)

    # --------------------------------------------------------
    # NAVEGAÇÃO
    # --------------------------------------------------------
    def proxima_questao(self):
        # precisa resetar isso antes de iniciar nova questão
        self.respondeu = False
        self.timer_ativo = True

        # cancelar timer anterior
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except:
                pass
            self.timer_id = None

        # avançar e mostrar
        self.questao_atual += 1
        # mostra nova questão (que vai iniciar o timer)
        self.mostrar_questao()


    def iniciar_timer(self):
        self.atualizar_timer()

    # --------------------------------------------------------
    # FINALIZAÇÃO
    # --------------------------------------------------------
    def mostrar_resultado(self):
        """Mostra tela de resultado bonita integrada no quiz"""
        # Salvar no banco
        sucesso = self.salvar_progresso_no_banco()
        
        # Limpar tela
        for w in self.main_frame.winfo_children():
            w.destroy()
        
        # Calcular estatísticas
        total = len(self.questoes)
        porcentagem = int((self.acertos / total) * 100) if total > 0 else 0
        
        # Determinar mensagem e cor baseado no desempenho
        if porcentagem >= 80:
            mensagem = "🎉 Excelente!"
            emoji = "🏆"
            cor_principal = "#4caf50"
        elif porcentagem >= 60:
            mensagem = "👏 Muito Bom!"
            emoji = "⭐"
            cor_principal = "#2196f3"
        elif porcentagem >= 40:
            mensagem = "📚 Continue Estudando!"
            emoji = "💪"
            cor_principal = "#ff9800"
        else:
            mensagem = "📖 Não Desista!"
            emoji = "🎯"
            cor_principal = "#f44336"
        
        # Container principal SEM scroll
        resultado_frame = tk.Frame(self.main_frame, bg=self.COR_FUNDO)
        resultado_frame.pack(fill="both", expand=True)
        
        # Emoji
        tk.Label(
            resultado_frame,
            text=emoji,
            font=("Arial", 50),  # Reduzido de 70
            bg=self.COR_FUNDO
        ).pack(pady=(10, 5))
        
        # Título
        tk.Label(
            resultado_frame,
            text=mensagem,
            font=("Arial", 18, "bold"),  # Reduzido de 22
            bg=self.COR_FUNDO,
            fg="white"
        ).pack(pady=(0, 10))
        
        # Card com estatísticas
        stats_card = tk.Frame(resultado_frame, bg="white", relief="raised", bd=2)
        stats_card.pack(fill="x", padx=15, pady=5)
        
        stats_content = tk.Frame(stats_card, bg="white")
        stats_content.pack(fill="x", padx=15, pady=15)
        
        # Porcentagem grande
        tk.Label(
            stats_content,
            text=f"{porcentagem}%",
            font=("Arial", 40, "bold"),  # Reduzido de 48
            bg="white",
            fg=cor_principal
        ).pack(pady=(0, 3))
        
        tk.Label(
            stats_content,
            text="Aproveitamento",
            font=("Arial", 11),
            bg="white",
            fg="#666"
        ).pack(pady=(0, 10))
        
        # Linha divisória
        tk.Frame(stats_content, bg="#e0e0e0", height=1).pack(fill="x", pady=8)
        
        # Grid de estatísticas
        grid_frame = tk.Frame(stats_content, bg="white")
        grid_frame.pack(fill="x", pady=8)
        
        # Acertos
        acertos_frame = tk.Frame(grid_frame, bg="white")
        acertos_frame.pack(side="left", expand=True)
        
        tk.Label(
            acertos_frame,
            text="✅",
            font=("Arial", 24),
            bg="white"
        ).pack()
        
        tk.Label(
            acertos_frame,
            text=f"{self.acertos}",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#4caf50"
        ).pack()
        
        tk.Label(
            acertos_frame,
            text="Acertos",
            font=("Arial", 9),
            bg="white",
            fg="#666"
        ).pack()
        
        # Erros
        erros_frame = tk.Frame(grid_frame, bg="white")
        erros_frame.pack(side="left", expand=True)
        
        tk.Label(
            erros_frame,
            text="❌",
            font=("Arial", 24),
            bg="white"
        ).pack()
        
        tk.Label(
            erros_frame,
            text=f"{self.erros}",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#f44336"
        ).pack()
        
        tk.Label(
            erros_frame,
            text="Erros",
            font=("Arial", 9),
            bg="white",
            fg="#666"
        ).pack()
        
        # XP
        xp_frame = tk.Frame(grid_frame, bg="white")
        xp_frame.pack(side="left", expand=True)
        
        tk.Label(
            xp_frame,
            text="💎",
            font=("Arial", 24),
            bg="white"
        ).pack()
        
        tk.Label(
            xp_frame,
            text=f"{self.xp_total}",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#ffa726"
        ).pack()
        
        tk.Label(
            xp_frame,
            text="XP Ganho",
            font=("Arial", 9),
            bg="white",
            fg="#666"
        ).pack()
        
        # Linha divisória
        tk.Frame(stats_content, bg="#e0e0e0", height=1).pack(fill="x", pady=8)
        
        # Detalhes (mais compactos)
        detalhes_frame = tk.Frame(stats_content, bg="white")
        detalhes_frame.pack(fill="x", pady=5)
        
        tk.Label(
            detalhes_frame,
            text=f"📝 Total: {total} questões",
            font=("Arial", 10),
            bg="white",
            fg="#333",
            anchor="w"
        ).pack(fill="x", pady=1)
        
        if self.materia_filtro:
            tk.Label(
                detalhes_frame,
                text=f"📚 Matéria: {self.materia_filtro}",
                font=("Arial", 10),
                bg="white",
                fg="#333",
                anchor="w"
            ).pack(fill="x", pady=1)
        
        if self.nivel_filtro:
            tk.Label(
                detalhes_frame,
                text=f"⚡ Nível: {self.nivel_filtro}",
                font=("Arial", 10),
                bg="white",
                fg="#333",
                anchor="w"
            ).pack(fill="x", pady=1)
        
        # Mensagem de desbloqueio (mais compacta)
        if porcentagem >= 70:
            desbloqueio_frame = tk.Frame(resultado_frame, bg="#4caf50", relief="raised", bd=2)
            desbloqueio_frame.pack(fill="x", padx=15, pady=8)
            
            tk.Label(
                desbloqueio_frame,
                text="🔓 Próximo nível desbloqueado!",
                font=("Arial", 12, "bold"),
                bg="#4caf50",
                fg="white"
            ).pack(pady=10)
        
        # Botões (fixos na parte inferior)
        botoes_frame = tk.Frame(resultado_frame, bg=self.COR_FUNDO)
        botoes_frame.pack(side="bottom", fill="x", padx=15, pady=15)
        
        tk.Button(
            botoes_frame,
            text="🔄 Refazer",
            font=("Arial", 11, "bold"),
            bg="#2196f3",
            fg="white",
            relief="flat",
            height=2,
            command=self.refazer_quiz
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(
            botoes_frame,
            text="✓ Continuar",
            font=("Arial", 11, "bold"),
            bg="#4caf50",
            fg="white",
            relief="flat",
            height=2,
            command=self.finalizar_e_voltar
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def finalizar_e_voltar(self):
        self.destruir()
        if self.on_finalizar:
            total = len(self.questoes)
            porcentagem = (self.acertos / total) * 100 if total > 0 else 0
            resultado = {
                "xp_ganho": self.xp_total,
                "acertos": self.acertos,
                "erros": self.erros,
                "materia": self.materia_filtro,
                "nivel": self.nivel_filtro,
                "aproveitamento": porcentagem
            }
            self.on_finalizar(resultado)
        else:
            if callable(self.on_voltar):
                self.on_voltar()

    def refazer_quiz(self):
        self.destruir()
        TelaQuiz(
            self.root,
            self.usuario,
            self.modo,
            self.materia_filtro,
            self.nivel_filtro,
            self.on_voltar,
            self.on_finalizar
        )

    def voltar(self):
        self.destruir()
        if callable(self.on_voltar):
            self.on_voltar()


# --------------------------------------------------------
# TESTE STANDALONE
# --------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("375x700")
    root.resizable(False, False)
    root.title("EstudAe - Quiz")
    root.configure(bg="#07442E")

    TelaQuiz(root, "usuario_teste", modo="enem")
    root.mainloop()
