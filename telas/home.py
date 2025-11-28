# ------------------------------------------------------------
# Tela Home do EstudAe
# ------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dados.banco_dadosUsuarios import carregar_dados_ranking, ranking_geral, carregar_ranking_materias

def montar_home(root, usuario=None, nome=None, on_enem=None, on_militar=None, on_criar_quiz=None, on_ranking=None, dados_usuario=None):
    """
    Monta a tela inicial com sistema de XP e progressão
    """
    # Limpa a tela
    for w in root.winfo_children():
        w.destroy()

    root.title("EstudAe")
    root.config(bg="#005227")

    # Dados padrão caso não sejam fornecidos
    if dados_usuario is None:
        dados_usuario = {
            'nome': nome or usuario or 'Aluno(a)',
            'xp_total': 0,
            'nivel_geral': 1,
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

    # ==================== CONTAINER PRINCIPAL ====================
    main_container = tk.Frame(root, bg="#005227")
    main_container.pack(fill="both", expand=True)

    # ==================== RODAPÉ FIXO (AGORA FUNCIONA!) ====================
    footer_frame = tk.Frame(main_container, bg="#68ddbd", height=65)
    footer_frame.pack(side="bottom", fill="x")
    footer_frame.pack_propagate(False)

    footer_content = tk.Frame(footer_frame, bg="#68ddbd")
    footer_content.pack(expand=True, fill="both")

    # ===== ALTERADO: mostrar_menu_rankings agora abre janelas reutilizáveis =====
    def mostrar_menu_rankings():
        # Limpa e mostra menu simples com botões que carregam as telas no mesmo root
        for widget in root.winfo_children():
            widget.destroy()

        menu_container = tk.Frame(root, bg="#005227")
        menu_container.pack(expand=True, fill="both")

        center_frame = tk.Frame(menu_container, bg="#005227")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center_frame,
            text="🏆 Rankings",
            font=("Cooper Black", 28),
            bg="#005227",
            fg="#FFFFFF"
        ).pack(pady=(0, 10))

        tk.Label(
            center_frame,
            text="Escolha o tipo de ranking:",
            font=("Arial", 13),
            bg="#005227",
            fg="#FFFFFF"
        ).pack(pady=(0, 20))

        # importar localmente para evitar dependências circulares
        def abrir_geral():
            from telas.ranking_geral import mostrar_ranking_geral
            mostrar_ranking_geral(root, dados=None, on_back=lambda: montar_home(root, dados_usuario=dados_usuario,
                                                                                on_enem=on_enem, on_militar=on_militar,
                                                                                on_criar_quiz=on_criar_quiz, on_ranking=on_ranking))

        def abrir_por_materia():
            from telas.ranking_materia import mostrar_ranking_por_materia
            mostrar_ranking_por_materia(root, dados=None, on_back=lambda: montar_home(root, dados_usuario=dados_usuario,
                                                                                    on_enem=on_enem, on_militar=on_militar,
                                                                                    on_criar_quiz=on_criar_quiz, on_ranking=on_ranking))

        tk.Button(center_frame, text="📊 Ranking Geral", font=("Arial", 13, "bold"),
                bg="#68ddbd", fg="#005227", width=22, height=2, command=abrir_geral).pack(pady=10)

        tk.Button(center_frame, text="📖 Ranking por Matéria", font=("Arial", 13, "bold"),
                bg="#68ddbd", fg="#005227", width=22, height=2, command=abrir_por_materia).pack(pady=10)

        tk.Button(menu_container, text="← Voltar", font=("Arial", 12, "bold"),
                bg="#d32f2f", fg="#FFFFFF", width=15,
                command=lambda: montar_home(root, dados_usuario=dados_usuario,
                                            on_enem=on_enem, on_militar=on_militar,
                                            on_criar_quiz=on_criar_quiz, on_ranking=on_ranking)).pack(side="bottom", pady=24)

    botao_rankings = tk.Button(
        footer_content,
        text="🏆 Ver Rankings",
        font=("Arial", 12, "bold"),
        bg="#005227",
        fg="#68ddbd",
        activebackground="#003d1f",
        activeforeground="#68ddbd",
        relief="flat",
        cursor="hand2",
        command=mostrar_menu_rankings
    )
    botao_rankings.pack(expand=True, fill="both", padx=40, pady=10)

    # ==================== CANVAS COM SCROLL (AGORA ACIMA DO RODAPÉ) ====================
    canvas = tk.Canvas(main_container, bg="#005227", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#005227")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=375)
    canvas.configure(yscrollcommand=scrollbar.set)

    # CANVAS NÃO EXPANDE PARA CIMA DO RODAPÉ
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mouse scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # ==================== HEADER COM BOTÃO DE PERFIL ====================
    header_frame = tk.Frame(scrollable_frame, bg="#005227")
    header_frame.pack(fill="x", pady=(15, 0))
    
    titulo_container = tk.Frame(header_frame, bg="#005227")
    titulo_container.pack(expand=True)
    
    titulo = tk.Label(
        titulo_container,
        text="EstudAe",
        font=("Cooper Black", 40),
        bg="#005227",
        fg="#FFFFFF"
    )
    titulo.pack()

    # Botão de perfil
    def abrir_perfil():
        janela_perfil = tk.Toplevel(root)
        janela_perfil.title("Perfil do Usuário")
        janela_perfil.geometry("450x600")
        janela_perfil.config(bg="#005227")
        janela_perfil.transient(root)
        janela_perfil.grab_set()
        
        container_principal = tk.Frame(janela_perfil, bg="#005227")
        container_principal.pack(fill="both", expand=True)
        
        tk.Label(
            container_principal,
            text="👤 Perfil",
            font=("Cooper Black", 24),
            bg="#005227",
            fg="#FFFFFF"
        ).pack(pady=20)

        info_card = tk.Frame(container_principal, bg="#68ddbd", relief="raised", bd=3)
        info_card.pack(pady=10, padx=30, fill="x")

        content_principal = tk.Frame(info_card, bg="#68ddbd")
        content_principal.pack(pady=20, padx=20, fill="x")

        labels_principais = [
            ("Nome:", dados_usuario['nome']),
            ("Nível Geral:", f"⭐ {dados_usuario['nivel_geral']}"),
            ("XP Total:", f"{dados_usuario['xp_total']:,}".replace(',', '.')),
            ("Streak:", f"🔥 {dados_usuario['streak_dias']} dias"),
        ]

        for titulo_label, valor in labels_principais:
            frame_linha = tk.Frame(content_principal, bg="#68ddbd")
            frame_linha.pack(fill="x", pady=5)
            
            tk.Label(
                frame_linha,
                text=titulo_label,
                font=("Arial", 12, "bold"),
                bg="#68ddbd",
                fg="#005227"
            ).pack(side="left")
            
            tk.Label(
                frame_linha,
                text=valor,
                font=("Arial", 12),
                bg="#68ddbd",
                fg="#005227"
            ).pack(side="right")

        tk.Button(
            container_principal,
            text="Fechar",
            bg="#68ddbd",
            font=("Arial", 12, "bold"),
            fg="#005227",
            activebackground="#005227",
            activeforeground="#68ddbd",
            relief="flat",
            width=15,
            command=janela_perfil.destroy
        ).pack(pady=(30, 20))

    botao_perfil = tk.Button(
        scrollable_frame,
        text="👤",
        font=("Arial", 16),
        bg="#68ddbd",
        fg="#005227",
        activebackground="#005227",
        activeforeground="#68ddbd",
        relief="solid",
        bd=1,
        width=3,
        height=1,
        command=abrir_perfil
    )
    botao_perfil.place(x=310, y=27)

    linha = tk.Frame(scrollable_frame, bg="#68ddbd", height=3)
    linha.pack(fill="x", padx=20, pady=(10, 5))

    # ==================== SAUDAÇÃO ====================
    subtitulo = tk.Label(
        scrollable_frame,
        text=f"Olá, {dados_usuario['nome'].split()[0]}!\nEscolha sua jornada de estudos",
        font=("Cooper Black", 14, "italic"),
        bg="#005227",
        fg="#FFFFFF",
        justify="center"
    )
    subtitulo.pack(pady=(5, 10))

    # ==================== CARDS DAS CATEGORIAS ====================
    categorias_frame = tk.Frame(scrollable_frame, bg="#005227")
    categorias_frame.pack(pady=(10, 5), padx=30, fill="x")

    # Card ENEM
    card_enem = tk.Frame(categorias_frame, bg="#68ddbd", relief="raised", bd=3)
    card_enem.pack(pady=10, fill="x")

    enem_info = tk.Frame(card_enem, bg="#68ddbd")
    enem_info.pack(pady=15, padx=20, fill="x")

    enem_titulo = tk.Label(
        enem_info,
        text="🧠 Enem",
        font=("Arial", 18, "bold"),
        bg="#68ddbd",
        fg="#005227"
    )
    enem_titulo.pack(anchor="w")

    enem_xp = tk.Label(
        enem_info,
        text=f"XP: {dados_usuario['xp_enem']} | Progresso: {dados_usuario['progresso_enem']}%",
        font=("Arial", 11),
        bg="#68ddbd",
        fg="#005227"
    )
    enem_xp.pack(anchor="w", pady=(5, 10))

    botao_enem = tk.Button(
        card_enem,
        text="Continuar Estudos →",
        bg="#005227",
        font=("Arial", 12, "bold"),
        fg="#68ddbd",
        activebackground="#003d1f",
        activeforeground="#68ddbd",
        relief="flat",
        width=25,
        command=(on_enem if on_enem else lambda: print("Botão ENEM clicado!"))
    )
    botao_enem.pack(pady=(0, 15))

    # Card Militar
    card_militar = tk.Frame(categorias_frame, bg="#68ddbd", relief="raised", bd=3)
    card_militar.pack(pady=10, fill="x")

    militar_info = tk.Frame(card_militar, bg="#68ddbd")
    militar_info.pack(pady=15, padx=20, fill="x")

    militar_titulo = tk.Label(
        militar_info,
        text="🏅 Concurso Militar",
        font=("Arial", 18, "bold"),
        bg="#68ddbd",
        fg="#005227"
    )
    militar_titulo.pack(anchor="w")

    militar_xp = tk.Label(
        militar_info,
        text=f"XP: {dados_usuario['xp_militar']} | Progresso: {dados_usuario['progresso_militar']}%",
        font=("Arial", 11),
        bg="#68ddbd",
        fg="#005227"
    )
    militar_xp.pack(anchor="w", pady=(5, 10))

    botao_militar = tk.Button(
        card_militar,
        text="Continuar Estudos →",
        bg="#005227",
        font=("Arial", 12, "bold"),
        fg="#68ddbd",
        activebackground="#003d1f",
        activeforeground="#68ddbd",
        relief="flat",
        width=25,
        command=(on_militar if on_militar else lambda: print("Botão Militar clicado!"))
    )
    botao_militar.pack(pady=(0, 15))

    # Card Criar Quiz
    card_criar = tk.Frame(categorias_frame, bg="#ffa726", relief="raised", bd=3)
    card_criar.pack(pady=10, fill="x")

    criar_info = tk.Frame(card_criar, bg="#ffa726")
    criar_info.pack(pady=15, padx=20, fill="x")

    criar_titulo = tk.Label(
        criar_info,
        text="✏️ Criar Meu Quiz",
        font=("Arial", 18, "bold"),
        bg="#ffa726",
        fg="#005227"
    )
    criar_titulo.pack(anchor="w")

    criar_desc = tk.Label(
        criar_info,
        text="Crie seus próprios quizzes personalizados",
        font=("Arial", 11),
        bg="#ffa726",
        fg="#005227"
    )
    criar_desc.pack(anchor="w", pady=(5, 10))

    botao_criar = tk.Button(
        card_criar,
        text="Criar Quiz →",
        bg="#005227",
        font=("Arial", 12, "bold"),
        fg="#ffa726",
        activebackground="#003d1f",
        activeforeground="#ffa726",
        relief="flat",
        width=25,
        command=(on_criar_quiz if on_criar_quiz else lambda: print("Botão Criar Quiz clicado!"))
    )
    botao_criar.pack(pady=(0, 15))

    # Espaço final para o scroll não colar no rodapé
    tk.Frame(scrollable_frame, bg="#005227", height=80).pack()


# ==================== EXEMPLO DE USO ====================
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("375x700")
    root.resizable(False, False)
    
    dados_exemplo = {
        'nome': 'Emily Tavares',
        'xp_total': 580,
        'nivel_geral': 15,
        'ranking_posicao': 47,
        'ranking_enem': 20,
        'ranking_militar': 35,
        'streak_dias': 5,
        'progresso_geral': 67,
        'xp_enem': 580,
        'progresso_enem': 45,
        'xp_militar': 670,
        'progresso_militar': 55
    }
    
    montar_home(root, dados_usuario=dados_exemplo)
    root.mainloop()