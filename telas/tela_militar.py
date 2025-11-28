import tkinter as tk
from tkinter import ttk
from dados.banco_dadosUsuarios import obter_xp_materias_quiz, obter_niveis_completados_materia


def montar_militar(root, usuario=None, nome=None, on_voltar=None, on_fazer_quiz=None):
    """Monta a tela de Concurso Militar dentro da janela principal"""

    # Obter XP real do usuário no quiz Militar (id_quiz=2)
    xp_por_materia = obter_xp_materias_quiz(usuario[0], id_quiz=2) if usuario else {}

    # Obter níveis realmente completados por matéria
    niveis_completados = obter_niveis_completados_materia(usuario[0], id_quiz=2) if usuario else {}

    # Limpa a tela
    for w in root.winfo_children():
        w.destroy()

    root.title("Militar")
    root.config(bg="#005227")

    # ============ MAPEAMENTO CORRETO DAS MATÉRIAS COM SUFIXOS ============
    materias_por_concurso = {
        "Exército": [
            "Português (Exército)", 
            "Matemática (Exército)", 
            "História (Exército)", 
            "Geografia (Exército)", 
            "Inglês (Exército)", 
            "Física (Exército)", 
            "Química (Exército)"
        ],
        "Marinha": [
            "Português (Marinha)", 
            "Matemática (Marinha)", 
            "Física (Marinha)", 
            "Química (Marinha)", 
            "Inglês (Marinha)"
        ],
        "Aeronáutica": [
            "Português (Aeronáutica)", 
            "Matemática (Aeronáutica)", 
            "Inglês (Aeronáutica)", 
            "Física (Aeronáutica)"
        ]
    }

    # Dados das matérias (TODAS COM NOME COMPLETO DO BANCO)
    todas_materias = {
        # EXÉRCITO
        "Matemática (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Matemática (Exército)", 0), 
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Matemática (Exército)", [])
        },
        "Português (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Português (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Português (Exército)", [])
        },
        "Física (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Física (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Física (Exército)", [])
        },
        "Química (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Química (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Química (Exército)", [])
        },
        "História (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("História (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("História (Exército)", [])
        },
        "Geografia (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Geografia (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Geografia (Exército)", [])
        },
        "Inglês (Exército)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Inglês (Exército)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Inglês (Exército)", [])
        },
        
        # MARINHA
        "Português (Marinha)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Português (Marinha)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Português (Marinha)", [])
        },
        "Matemática (Marinha)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Matemática (Marinha)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Matemática (Marinha)", [])
        },
        "Física (Marinha)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Física (Marinha)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Física (Marinha)", [])
        },
        "Química (Marinha)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Química (Marinha)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Química (Marinha)", [])
        },
        "Inglês (Marinha)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Inglês (Marinha)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Inglês (Marinha)", [])
        },
        
        # AERONÁUTICA
        "Português (Aeronáutica)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Português (Aeronáutica)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Português (Aeronáutica)", [])
        },
        "Matemática (Aeronáutica)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Matemática (Aeronáutica)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Matemática (Aeronáutica)", [])
        },
        "Inglês (Aeronáutica)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Inglês (Aeronáutica)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Inglês (Aeronáutica)", [])
        },
        "Física (Aeronáutica)": {
            "max": 3, 
            "current": 0, 
            "xp": xp_por_materia.get("Física (Aeronáutica)", 0),
            "xp_necessario": {1:0, 2:100, 3:250},
            "niveis_feitos": niveis_completados.get("Física (Aeronáutica)", [])
        },
    }

    tela_atual = {"nome": "categorias", "concurso": None}
    materia_selecionada = {"nome": None}

    # Atualiza o nível atual baseado no XP do usuário
    for mat, data in todas_materias.items():
        xp = data["xp"]
        current_level = 0
        for nivel, xp_req in sorted(data["xp_necessario"].items()):
            if xp >= xp_req:
               current_level = nivel
        data["current"] = current_level

    # ==================== FUNÇÕES ====================
   
    def limpar_conteudo():
        for w in main_frame.winfo_children():
            w.destroy()

    def mostrar_categorias():
        limpar_conteudo()
        
        # Desvincular eventos de scroll
        root.unbind_all("<MouseWheel>")
        
        tela_atual["nome"] = "categorias"
        tela_atual["concurso"] = None
       
        header = tk.Frame(main_frame, bg="#005227", height=50)
        header.pack(fill="x", pady=(10, 0))
       
        tk.Button(
            header,
            text="← Voltar",
            font=("Segoe UI", 11, "bold"),
            bg="#03bb85",
            fg="black",
            activebackground="#02a677",
            activeforeground="white",
            relief="flat",
            command=on_voltar if on_voltar else lambda: print("Voltar para home")
        ).pack(side="left", padx=15, pady=10)
       
        tk.Label(
            main_frame,
            text="Concurso Militar",
            font=("Segoe UI Semibold", 20),
            bg="#005227",
            fg="white"
        ).pack(pady=(20, 30))
       
        btn_frame = tk.Frame(main_frame, bg="#005227")
        btn_frame.pack(expand=True)
       
        concursos = [
            ("Exército", "🪖"),
            ("Marinha", "⚓"),
            ("Aeronáutica", "✈️")
        ]
        
        for txt, emoji in concursos:
            tk.Button(
                btn_frame,
                text=f"{emoji} {txt}",
                font=("Segoe UI", 13, "bold"),
                bg="#03bb85",
                fg="#0a0a0a",
                width=20,
                height=2,
                relief="flat",
                activebackground="#02a677",
                activeforeground="white",
                command=lambda c=txt: mostrar_materias(c)
            ).pack(pady=12)

    def extrair_nome_display(nome_completo):
        """Remove o sufixo para exibição: 'Português (Exército)' -> 'Português'"""
        return nome_completo.split(" (")[0]

    def mostrar_materias(concurso):
        limpar_conteudo()
        
        # Desvincular eventos anteriores
        root.unbind_all("<MouseWheel>")
        
        tela_atual["nome"] = "materias"
        tela_atual["concurso"] = concurso
       
        # Matérias do concurso (já com sufixo completo)
        materias_concurso = materias_por_concurso.get(concurso, [])
       
        header = tk.Frame(main_frame, bg="#005227", height=50)
        header.pack(fill="x", pady=(10, 0))
       
        tk.Button(
            header,
            text="← Voltar",
            font=("Segoe UI", 11, "bold"),
            bg="#03bb85",
            fg="black",
            activebackground="#02a677",
            activeforeground="white",
            relief="flat",
            command=mostrar_categorias
        ).pack(side="left", padx=15, pady=10)
       
        canvas = tk.Canvas(main_frame, bg="#005227", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#005227")
       
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
       
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=375)
        canvas.configure(yscrollcommand=scrollbar.set)
       
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
       
        tk.Label(
            scrollable_frame,
            text=f"Matérias - {concurso}",
            font=("Helvetica", 16, "bold"),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(15, 10))
       
        # Exibir botões com nome LIMPO mas guardar nome COMPLETO
        for nome_completo in materias_concurso:
            nome_display = extrair_nome_display(nome_completo)
            
            tk.Button(
                scrollable_frame,
                text=nome_display,
                font=("Segoe UI", 12),
                bg="#03bb85",
                fg="black",
                activebackground="#02a677",
                activeforeground="white",
                relief="flat",
                command=lambda n=nome_completo: mostrar_detalhe_materia(n, canvas, scrollable_frame)
            ).pack(fill="x", padx=20, pady=5)
       
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        root.unbind_all("<MouseWheel>")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def mostrar_detalhe_materia(nome_materia, canvas_pai, frame_pai):
        """Mostra os detalhes e níveis COM SISTEMA DE DESBLOQUEIO"""
        tela_atual["nome"] = "detalhe"
        materia_selecionada["nome"] = nome_materia
       
        for w in frame_pai.winfo_children():
            w.destroy()
       
        data = todas_materias[nome_materia]
        max_lvl = data["max"]
        current = data.get("current", 0)
        xp_materia = data.get("xp", 0)
        xp_necessario = data.get("xp_necessario", {1: 0, 2: 100, 3: 250})
        niveis_feitos = data.get("niveis_feitos", [])
        
        # Nome para exibição (sem sufixo)
        nome_display = extrair_nome_display(nome_materia)
       
        # Título
        tk.Label(
            frame_pai,
            text=nome_display,
            font=("Segoe UI Semibold", 18),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(0, 5))
       
        # XP
        tk.Label(
            frame_pai,
            text=f"XP: {xp_materia}",
            font=("Segoe UI", 12, "bold"),
            bg="#005227",
            fg="#68ddbd"
        ).pack(anchor="w", padx=20, pady=(0, 10))
       
        # Barra de progresso baseada em níveis completados
        niveis_completos = len(niveis_feitos)
        pct = int(100 * niveis_completos / max_lvl) if max_lvl > 0 else 0
       
        progress_frame = tk.Frame(frame_pai, bg="#005227")
        progress_frame.pack(fill="x", padx=20, pady=(5, 15))
       
        progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=pct
        )
        progress.pack(fill="x")
       
        style = ttk.Style()
        style.configure("TProgressbar", thickness=15, troughcolor="white", background="#68ddbd")
    
        tk.Label(
            frame_pai,
            text=f"Progresso: {pct}% ({niveis_completos} de {max_lvl} níveis completados)",
            font=("Segoe UI", 10),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(5, 20))
       
        # Título níveis
        tk.Label(
            frame_pai,
            text="Níveis Disponíveis",
            font=("Segoe UI Semibold", 14),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(10, 10))
       
        # Container níveis
        levels_container = tk.Frame(frame_pai, bg="#005227")
        levels_container.pack(fill="both", padx=20, pady=(0, 20))
       
        for nivel in range(1, max_lvl + 1):
            xp_requerido = xp_necessario.get(nivel, 0)
            esta_desbloqueado = xp_materia >= xp_requerido
            nivel_completado = nivel in niveis_feitos
           
            # Card
            nivel_card = tk.Frame(levels_container, bg="#68ddbd", relief="raised", bd=2)
            nivel_card.pack(fill="x", pady=8)
           
            card_content = tk.Frame(nivel_card, bg="#68ddbd")
            card_content.pack(fill="x", padx=15, pady=12)
           
            # Header
            header_frame = tk.Frame(card_content, bg="#68ddbd")
            header_frame.pack(fill="x", pady=(0, 8))
           
            tk.Label(
                header_frame,
                text=f"Nível {nivel}",
                font=("Segoe UI", 13, "bold"),
                bg="#68ddbd",
                fg="#005227"
            ).pack(side="left")
           
            if nivel_completado:
                tk.Label(
                    header_frame,
                    text="✓ Completado",
                    font=("Segoe UI", 10, "bold"),
                    bg="#68ddbd",
                    fg="#00aa00"
                ).pack(side="right")
            elif not esta_desbloqueado:
                tk.Label(
                    header_frame,
                    text="🔒 Bloqueado",
                    font=("Segoe UI", 10, "bold"),
                    bg="#68ddbd",
                    fg="#cc0000"
                ).pack(side="right")
           
            # XP info se bloqueado
            if not esta_desbloqueado:
                tk.Label(
                    card_content,
                    text=f"Requer {xp_requerido} XP para desbloquear",
                    font=("Segoe UI", 9),
                    bg="#68ddbd",
                    fg="#005227"
                ).pack(anchor="w", pady=(0, 8))
               
                xp_progress_frame = tk.Frame(card_content, bg="#68ddbd")
                xp_progress_frame.pack(fill="x", pady=(0, 8))
               
                xp_pct = min(100, int(100 * xp_materia / xp_requerido)) if xp_requerido > 0 else 100
               
                xp_canvas = tk.Canvas(xp_progress_frame, width=250, height=15, bg="#005227", highlightthickness=0)
                xp_canvas.pack()
               
                largura_preenchida = int(250 * (xp_pct / 100))
                xp_canvas.create_rectangle(0, 0, largura_preenchida, 15, fill="#00ff88", outline="")
               
                tk.Label(
                    card_content,
                    text=f"{xp_materia} / {xp_requerido} XP",
                    font=("Segoe UI", 8),
                    bg="#68ddbd",
                    fg="#005227"
                ).pack(anchor="w")
           
            # Botão
            if esta_desbloqueado:
                texto_botao = "✓ Refazer Quiz" if nivel_completado else "📝 Fazer Quiz"
               
                def criar_comando(m, n):
                    return lambda: on_fazer_quiz(m, n) if on_fazer_quiz else print(f"Quiz: {m} - Nível {n}")
               
                tk.Button(
                    card_content,
                    text=texto_botao,
                    font=("Segoe UI", 11, "bold"),
                    bg="#005227",
                    fg="#68ddbd",
                    activebackground="#003d1f",
                    activeforeground="#68ddbd",
                    relief="flat",
                    width=20,
                    command=criar_comando(nome_materia, nivel)
                ).pack(pady=(8, 0))
            else:
                tk.Button(
                    card_content,
                    text="🔒 Bloqueado",
                    font=("Segoe UI", 11, "bold"),
                    bg="#666666",
                    fg="#cccccc",
                    relief="flat",
                    width=20,
                    state="disabled"
                ).pack(pady=(8, 0))
       
        canvas_pai.update_idletasks()
        canvas_pai.configure(scrollregion=canvas_pai.bbox("all"))

    # Layout principal
    main_frame = tk.Frame(root, bg="#005227")
    main_frame.pack(fill="both", expand=True)
   
    mostrar_categorias()


# Teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("375x812")
    root.resizable(False, False)
   
    usuario_teste = (1, "Usuario Teste")
   
    def voltar_teste():
        print("Voltando...")
        root.destroy()
   
    def on_fazer_quiz(materia, nivel):
        nivel_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
        nivel_nome = nivel_map.get(nivel, "Fácil")
        
        print(f"🎮 Iniciando Quiz: {materia} - {nivel_nome}")
        
        from telas.tela_quiz import TelaQuiz
        
        def voltar_ao_militar():
            montar_militar(root, usuario=usuario_teste, on_voltar=voltar_teste, on_fazer_quiz=on_fazer_quiz)
        
        def ao_finalizar(resultado):
            print(f"✅ Quiz finalizado! XP ganho: {resultado['xp_ganho']}")
            voltar_ao_militar()
        
        TelaQuiz(
            root=root,
            usuario=usuario_teste[0],
            modo="militar",
            materia=materia,  # Passa o nome COMPLETO com sufixo
            nivel=nivel_nome,
            on_voltar=voltar_ao_militar,
            on_finalizar=ao_finalizar
        )
   
    montar_militar(root, usuario=usuario_teste, on_voltar=voltar_teste, on_fazer_quiz=on_fazer_quiz)
    root.mainloop()