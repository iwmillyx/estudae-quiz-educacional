import tkinter as tk
from tkinter import ttk
from dados.banco_dadosUsuarios import obter_dados_usuario, obter_xp_materias_quiz, obter_niveis_completados_materia

def montar_enem(root, usuario=None, nome=None, on_voltar=None, on_fazer_quiz=None):
    """Monta a tela do ENEM dentro da janela principal"""
   
    # Limpa a tela
    for w in root.winfo_children():
        w.destroy()

    root.title("ENEM")
    root.config(bg="#005227")

    # Dados das matérias por área (ATUALIZADO COM XP)
    materias_enem = {
        "Ciências da Natureza": {
            "Física": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Química": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Biologia": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
        },
        "Ciências Humanas": {
            "História": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Geografia": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Filosofia": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Sociologia": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
        },
        "Linguagens e Códigos": {
            "Português": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Literatura": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Inglês": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Espanhol": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
            "Artes": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
        },
        "Matemática": {
            "Matemática": {"max": 3, "current": 0, "xp": 0, "xp_necessario": {1: 0, 2: 100, 3: 250}, "niveis_feitos": []},
        }
    }

    # Atualiza XP real do usuário
    if usuario:  # 'usuario' é id_usuario
       dados_usuario = obter_dados_usuario(usuario)
       xp_por_materia = obter_xp_materias_quiz(usuario, id_quiz=1)  # ENEM = 1
       niveis_completados = obter_niveis_completados_materia(usuario, id_quiz=1)  # NOVO

       for area, materias in materias_enem.items():
           for materia_nome, dados in materias.items():
               xp_usuario = xp_por_materia.get(materia_nome, 0)
               dados['xp'] = xp_usuario
               dados['niveis_feitos'] = niveis_completados.get(materia_nome, [])  # NOVO

            # Determina o nível atual
               current = 0
               for nivel, xp_req in sorted(dados['xp_necessario'].items()):
                   if xp_usuario >= xp_req:
                      current = nivel
               current = min(current, dados['max'])  # não ultrapassa o nível máximo
               dados['current'] = current

            # Progresso baseado em NÍVEIS COMPLETADOS
               niveis_completos = len(dados['niveis_feitos'])
               pct = int(100 * niveis_completos / dados['max']) if dados['max'] > 0 else 0
               dados['pct'] = pct

    # Variáveis de controle
    tela_atual = {"nome": "areas"}
    area_selecionada = {"nome": None, "materias": {}}
    materia_selecionada = {"nome": None}

    # ==================== FUNÇÕES ====================
   
    def limpar_conteudo():
        """Limpa apenas o conteúdo, mantendo o frame principal"""
        for w in main_frame.winfo_children():
            w.destroy()

    def mostrar_areas():
        """Mostra a tela de áreas do conhecimento"""
        limpar_conteudo()
        
        # Desvincular eventos de scroll
        root.unbind_all("<MouseWheel>")
        
        tela_atual["nome"] = "areas"
       
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
            text="Áreas do Conhecimento",
            font=("Segoe UI Semibold", 18),
            bg="#005227",
            fg="white"
        ).pack(pady=(20, 30))
       
        areas_frame = tk.Frame(main_frame, bg="#005227")
        areas_frame.pack(expand=True, padx=30)
       
        for area in materias_enem.keys():
            tk.Button(
                areas_frame,
                text=area,
                font=("Segoe UI", 12, "bold"),
                bg="#03bb85",
                fg="black",
                activebackground="#02a677",
                activeforeground="white",
                relief="flat",
                width=25,
                height=2,
                command=lambda a=area: mostrar_materias(a)
            ).pack(pady=8)

    def mostrar_materias(area_nome):
        """Mostra a lista de matérias de uma área"""
        limpar_conteudo()
        
        # Desvincular eventos anteriores
        root.unbind_all("<MouseWheel>")
        
        tela_atual["nome"] = "materias"
        area_selecionada["nome"] = area_nome
        area_selecionada["materias"] = materias_enem[area_nome]
       
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
            command=mostrar_areas
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
            text=f"{area_nome}",
            font=("Helvetica", 16, "bold"),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(15, 10))
       
        for materia_nome in area_selecionada["materias"].keys():
            tk.Button(
                scrollable_frame,
                text=materia_nome,
                font=("Segoe UI", 12),
                bg="#03bb85",
                fg="black",
                activebackground="#02a677",
                activeforeground="white",
                relief="flat",
                command=lambda m=materia_nome: mostrar_detalhe_materia(m, canvas, scrollable_frame)
            ).pack(fill="x", padx=20, pady=5)
       
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        root.unbind_all("<MouseWheel>")  # Remove bindings anteriores
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def mostrar_detalhe_materia(materia_nome, canvas_pai, frame_pai):
        """Mostra os detalhes e níveis de uma matéria COM SISTEMA DE DESBLOQUEIO"""
        tela_atual["nome"] = "detalhe"
        materia_selecionada["nome"] = materia_nome
       
        for w in frame_pai.winfo_children():
            w.destroy()
       
        data = area_selecionada["materias"][materia_nome]
        max_lvl = data["max"]
        current = data.get("current", 0)
        xp_materia = data.get("xp", 0)
        xp_necessario = data.get("xp_necessario", {1: 0, 2: 100, 3: 250})
        niveis_feitos = data.get("niveis_feitos", [])  # NOVO: lista de níveis completados
       
        # Título da matéria
        tk.Label(
            frame_pai,
            text=materia_nome,
            font=("Segoe UI Semibold", 18),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))
       
        # XP da matéria
        tk.Label(
            frame_pai,
            text=f"XP: {xp_materia}",
            font=("Segoe UI", 12, "bold"),
            bg="#005227",
            fg="#68ddbd"
        ).pack(anchor="w", padx=20, pady=(0, 10))
       
        # Barra de progresso baseada em níveis completados
        pct = data.get('pct', 0)
        niveis_completos = len(niveis_feitos)
       
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
       
        # Texto mostra níveis COMPLETADOS
        tk.Label(
            frame_pai,
            text=f"Progresso: {pct}% ({niveis_completos} de {max_lvl} níveis completados)",
            font=("Segoe UI", 10),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(5, 20))
       
        # Título dos níveis
        tk.Label(
            frame_pai,
            text="Níveis Disponíveis",
            font=("Segoe UI Semibold", 14),
            bg="#005227",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(10, 10))
       
        # Container dos níveis
        levels_container = tk.Frame(frame_pai, bg="#005227")
        levels_container.pack(fill="both", padx=20, pady=(0, 20))
       
        for nivel in range(1, max_lvl + 1):
            xp_requerido = xp_necessario.get(nivel, 0)
            esta_desbloqueado = xp_materia >= xp_requerido
            nivel_completado = nivel in niveis_feitos
           
            # Card do nível
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
           
            # Info de XP se bloqueado
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
           
            # Texto mostra níveis COMPLETADOS
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
                    command=criar_comando(materia_nome, nivel)
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
   
    mostrar_areas()


# Teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("375x812")
    root.resizable(False, False)
   
    usuario_teste = 1  # ← ADICIONE ESTA LINHA
   
    def voltar_teste():
        print("Voltando...")
        root.destroy()
   
    def quiz_teste(materia, nivel):
        print(f"🎮 Quiz: {materia} - Nível {nivel}")
    
    def on_fazer_quiz(materia, nivel):
        # Converte número do nível para nome
        nivel_map = {1: "Fácil", 2: "Médio", 3: "Difícil"}
        nivel_nome = nivel_map.get(nivel, "Fácil")
        
        print(f"🎮 Iniciando Quiz: {materia} - {nivel_nome}")
        
        # Importa aqui para evitar import circular
        from telas.tela_quiz import TelaQuiz
        
        def voltar_ao_enem():
            montar_enem(root, usuario=usuario_teste, on_voltar=voltar_teste, on_fazer_quiz=on_fazer_quiz)
        
        def ao_finalizar(resultado):
            print(f"✅ Quiz finalizado! XP ganho: {resultado['xp_ganho']}")
            voltar_ao_enem()
        
        TelaQuiz(
            root=root,
            usuario=usuario_teste,
            modo="enem",
            materia=materia,
            nivel=nivel_nome,  # ← AQUI! Passa o NOME, não o número!
            on_voltar=voltar_ao_enem,
            on_finalizar=ao_finalizar
        )
   
    montar_enem(root, usuario=usuario_teste, on_voltar=voltar_teste, on_fazer_quiz=on_fazer_quiz)
    root.mainloop()