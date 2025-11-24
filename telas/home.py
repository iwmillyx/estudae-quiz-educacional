# ------------------------------------------------------------
# Aqui ficam:
#  - o título e a identidade visual (verde do grupo)
#  - os botões principais para iniciar a jornada (ENEM / Militar)
# Observações:
#  - por enquanto, os botões só dão print (placeholder)
#  - depois você pode abrir novas janelas/telas com as funcionalidades
# ------------------------------------------------------------

# ------------------------------------------------------------
# Tela Home do EstudAe
# ------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

def montar_home(root, usuario=None, nome=None, on_enem=None, on_militar=None, dados_usuario=None):
    """
    Monta a tela inicial com sistema de XP e progressão
    
    dados_usuario = {
        'nome': 'Emily Tavares',
        'xp_total': 1250,
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

    # ==================== HEADER COM BOTÃO DE PERFIL ====================
    header_frame = tk.Frame(root, bg="#005227")
    header_frame.pack(fill="x", pady=(10, 0))
    
    # Botão de perfil MENOR no canto superior direito
    def abrir_perfil():
        """Abre uma janela com informações detalhadas do usuário"""
        janela_perfil = tk.Toplevel(root)
        janela_perfil.title("Perfil do Usuário")
        janela_perfil.geometry("450x600")
        janela_perfil.config(bg="#005227")
        janela_perfil.transient(root)
        janela_perfil.grab_set()
        
        # Container principal (sem scroll inicialmente)
        container_principal = tk.Frame(janela_perfil, bg="#005227")
        container_principal.pack(fill="both", expand=True)
        
        # Variáveis para controlar o scroll
        canvas = None
        scrollbar = None
        scrollable_frame = None
        content_frame = container_principal  # Frame onde o conteúdo será colocado
        
        # Título
        titulo_perfil = tk.Label(
            content_frame,
            text="👤 Perfil",
            font=("Cooper Black", 24),
            bg="#005227",
            fg="#FFFFFF"
        )
        titulo_perfil.pack(pady=20)
        
        # Card com informações principais
        info_card = tk.Frame(content_frame, bg="#68ddbd", relief="raised", bd=3)
        info_card.pack(pady=10, padx=30, fill="x")
        
        content_principal = tk.Frame(info_card, bg="#68ddbd")
        content_principal.pack(pady=20, padx=20, fill="x")
        
        # Informações principais (SEM os rankings)
        labels_principais = [
            ("Nome:", dados_usuario['nome']),
            ("Nível Geral:", f"⭐ {dados_usuario['nivel_geral']}"),
            ("XP Total:", f"{dados_usuario['xp_total']:,}".replace(',', '.')),
            ("Streak:", f"🔥 {dados_usuario['streak_dias']} dias"),
        ]
        
        for titulo, valor in labels_principais:
            frame_linha = tk.Frame(content_principal, bg="#68ddbd")
            frame_linha.pack(fill="x", pady=5)
            
            tk.Label(
                frame_linha,
                text=titulo,
                font=("Arial", 12, "bold"),
                bg="#68ddbd",
                fg="#005227",
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                frame_linha,
                text=valor,
                font=("Arial", 12),
                bg="#68ddbd",
                fg="#005227",
                anchor="e"
            ).pack(side="right")
        
        # ==================== CARD DE RANKINGS ====================
        # Espaçamento
        tk.Frame(content_frame, bg="#005227", height=10).pack()
        
        # Card com rankings
        ranking_card = tk.Frame(content_frame, bg="#68ddbd", relief="raised", bd=3)
        ranking_card.pack(pady=10, padx=30, fill="x")
        
        # Título do card de rankings
        tk.Label(
            ranking_card,
            text="📊 Rankings",
            font=("Arial", 14, "bold"),
            bg="#68ddbd",
            fg="#005227"
        ).pack(pady=(15, 10))
        
        content_rankings = tk.Frame(ranking_card, bg="#68ddbd")
        content_rankings.pack(pady=(0, 20), padx=20, fill="x")
        
        # Todos os rankings
        labels_rankings = [
            ("Geral:", f"🏆 #{dados_usuario['ranking_posicao']}"),
            ("ENEM:", f"🧠 #{dados_usuario['ranking_enem']}"),
            ("Militar:", f"🏅 #{dados_usuario['ranking_militar']}"),
        ]
        
        for titulo, valor in labels_rankings:
            frame_linha = tk.Frame(content_rankings, bg="#68ddbd")
            frame_linha.pack(fill="x", pady=5)
            
            tk.Label(
                frame_linha,
                text=titulo,
                font=("Arial", 12, "bold"),
                bg="#68ddbd",
                fg="#005227",
                anchor="w"
            ).pack(side="left")
            
            tk.Label(
                frame_linha,
                text=valor,
                font=("Arial", 12),
                bg="#68ddbd",
                fg="#005227",
                anchor="e"
            ).pack(side="right")
        
        # Separador (removido - não precisa mais)
        
        # Botão fechar (mais pra cima agora)
        btn_fechar = tk.Button(
            content_frame,
            text="Fechar",
            bg="#68ddbd",
            font=("Arial", 12, "bold"),
            fg="#005227",
            activebackground="#005227",
            activeforeground="#68ddbd",
            relief="flat",
            width=15,
            command=janela_perfil.destroy
        )
        btn_fechar.pack(pady=(30, 20))
    
    # Botão de perfil MENOR
    botao_perfil = tk.Button(
        header_frame,
        text="👤",
        font=("Arial", 14),
        bg="#68ddbd",
        fg="#005227",
        activebackground="#005227",
        activeforeground="#68ddbd",
        relief="raised",
        bd=2,
        width=2,
        height=1,
        command=abrir_perfil
    )
    botao_perfil.pack(side="right", padx=20)
    
    titulo = tk.Label(
        header_frame,
        text="EstudAe",
        font=("Cooper Black", 50),
        bg="#005227",
        fg="#FFFFFF"
    )
    titulo.pack(side="left", padx=20)

    linha = tk.Frame(root, bg="#68ddbd", height=3, width=400)
    linha.pack(pady=(10, 5))

    # ==================== SAUDAÇÃO ====================
    subtitulo = tk.Label(
        root,
        text=f"Olá, {dados_usuario['nome'].split()[0]}!\nEscolha sua jornada de estudos",
        font=("Cooper Black", 14, "italic"),
        bg="#005227",
        fg="#FFFFFF",
        justify="center"
    )
    subtitulo.pack(pady=(0, 20))

    # ==================== SÓ OS CARDS DAS CATEGORIAS ====================
    categorias_frame = tk.Frame(root, bg="#005227")
    categorias_frame.pack(expand=True, pady=20, padx=40, fill="both")

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
        fg="#005227",
        anchor="w"
    )
    enem_titulo.pack(anchor="w")

    enem_xp = tk.Label(
        enem_info,
        text=f"XP: {dados_usuario['xp_enem']} | Progresso: {dados_usuario['progresso_enem']}%",
        font=("Arial", 11),
        bg="#68ddbd",
        fg="#005227",
        anchor="w"
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
        height=1,
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
        fg="#005227",
        anchor="w"
    )
    militar_titulo.pack(anchor="w")

    militar_xp = tk.Label(
        militar_info,
        text=f"XP: {dados_usuario['xp_militar']} | Progresso: {dados_usuario['progresso_militar']}%",
        font=("Arial", 11),
        bg="#68ddbd",
        fg="#005227",
        anchor="w"
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
        height=1,
        command=(on_militar if on_militar else lambda: print("Botão Militar clicado!"))
    )
    botao_militar.pack(pady=(0, 15))


# ==================== EXEMPLO DE USO ====================
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x800")
    
    # Dados de exemplo (sua amiga vai pegar isso do banco de dados)
    dados_exemplo = {
        'nome': 'Emily Tavares',
        'xp_total': 1250,
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