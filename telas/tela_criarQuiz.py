import tkinter as tk
from tkinter import messagebox, ttk  # Adicionei ttk para combobox


def montar_criador_quiz(root, usuario_xp=0, usuario_nivel=1, on_voltar=None, on_salvar=None):
    """
    Tela para criar quiz personalizado
    
    SISTEMA DE DESBLOQUEIO:
    - Precisa ter 500 XP OU ser nível 5+ para criar quiz
    """
    
    # Limpa a tela
    for w in root.winfo_children():
        w.destroy()
    
    root.title("EstudAe - Criar Quiz")
    root.config(bg="#005227")
    
    # VERIFICA REQUISITOS
    XP_MINIMO = 500
    NIVEL_MINIMO = 5
    
    pode_criar = usuario_xp >= XP_MINIMO or usuario_nivel >= NIVEL_MINIMO
    
    # ==================== TELA BLOQUEADA ====================
    if not pode_criar:
        frame_bloqueado = tk.Frame(root, bg="#005227")
        frame_bloqueado.pack(expand=True, fill="both", padx=30, pady=50)
        
        tk.Label(
            frame_bloqueado,
            text="🔒",
            font=("Arial", 80),
            bg="#005227",
            fg="#68ddbd"
        ).pack(pady=(0, 20))
        
        tk.Label(
            frame_bloqueado,
            text="Recurso Bloqueado",
            font=("Segoe UI", 20, "bold"),
            bg="#005227",
            fg="white"
        ).pack(pady=(0, 15))
        
        tk.Label(
            frame_bloqueado,
            text="Para criar seus próprios quizzes,\nvocê precisa alcançar:",
            font=("Segoe UI", 12),
            bg="#005227",
            fg="white",
            justify="center"
        ).pack(pady=(0, 20))
        
        req_card = tk.Frame(frame_bloqueado, bg="#68ddbd", relief="raised", bd=3)
        req_card.pack(fill="x", pady=10)
        
        req_content = tk.Frame(req_card, bg="#68ddbd")
        req_content.pack(padx=20, pady=20)
        
        # Requisito 1: XP
        req1_frame = tk.Frame(req_content, bg="#68ddbd")
        req1_frame.pack(fill="x", pady=8)
        
        xp_ok = usuario_xp >= XP_MINIMO
        xp_icon = "✓" if xp_ok else "✗"
        xp_color = "#00aa00" if xp_ok else "#cc0000"
        
        tk.Label(
            req1_frame,
            text=f"{xp_icon} {XP_MINIMO} XP",
            font=("Segoe UI", 13, "bold"),
            bg="#68ddbd",
            fg=xp_color,
            anchor="w"
        ).pack(side="left")
        
        tk.Label(
            req1_frame,
            text=f"Você tem: {usuario_xp} XP",
            font=("Segoe UI", 11),
            bg="#68ddbd",
            fg="#005227",
            anchor="e"
        ).pack(side="right")
        
        tk.Label(
            req_content,
            text="OU",
            font=("Segoe UI", 12, "bold"),
            bg="#68ddbd",
            fg="#005227"
        ).pack(pady=5)
        
        # Requisito 2: Nível
        req2_frame = tk.Frame(req_content, bg="#68ddbd")
        req2_frame.pack(fill="x", pady=8)
        
        nivel_ok = usuario_nivel >= NIVEL_MINIMO
        nivel_icon = "✓" if nivel_ok else "✗"
        nivel_color = "#00aa00" if nivel_ok else "#cc0000"
        
        tk.Label(
            req2_frame,
            text=f"{nivel_icon} Nível {NIVEL_MINIMO}",
            font=("Segoe UI", 13, "bold"),
            bg="#68ddbd",
            fg=nivel_color,
            anchor="w"
        ).pack(side="left")
        
        tk.Label(
            req2_frame,
            text=f"Você está no: Nível {usuario_nivel}",
            font=("Segoe UI", 11),
            bg="#68ddbd",
            fg="#005227",
            anchor="e"
        ).pack(side="right")
        
        falta_xp = max(0, XP_MINIMO - usuario_xp)
        falta_nivel = max(0, NIVEL_MINIMO - usuario_nivel)
        
        if falta_xp < falta_nivel * 100:
            msg = f"Continue estudando!\nFaltam {falta_xp} XP para desbloquear."
        else:
            msg = f"Continue estudando!\nFaltam {falta_nivel} níveis para desbloquear."
        
        tk.Label(
            frame_bloqueado,
            text=msg,
            font=("Segoe UI", 11),
            bg="#005227",
            fg="#68ddbd",
            justify="center"
        ).pack(pady=(20, 0))
        
        tk.Button(
            frame_bloqueado,
            text="← Voltar",
            font=("Segoe UI", 12, "bold"),
            bg="#03bb85",
            fg="black",
            activebackground="#02a677",
            activeforeground="white",
            relief="flat",
            width=20,
            command=on_voltar if on_voltar else lambda: print("Voltar")
        ).pack(pady=20)
        
        return
    
    # ==================== DADOS DAS MATÉRIAS ====================
    materias_enem = {
        "Ciências da Natureza": ["Física", "Química", "Biologia"],
        "Ciências Humanas": ["História", "Geografia", "Filosofia", "Sociologia"],
        "Linguagens e Códigos": ["Português", "Literatura", "Inglês", "Espanhol", "Artes"],
        "Matemática": ["Matemática"]
    }
    
    materias_militar = [
        "Matemática", "Física", "Química", "Português", 
        "Inglês", "História", "Geografia", "Redação"
    ]
    
    # ==================== TELA DE CRIAÇÃO ====================
    
    # Estado do quiz sendo criado
    quiz_data = {
        "titulo": tk.StringVar(),
        "categoria": tk.StringVar(),
        "area": tk.StringVar(),  # Para ENEM
        "materia": tk.StringVar(),
        "nivel": tk.StringVar(value="1"),
        "perguntas": []
    }
    
    # Canvas com scroll
    canvas = tk.Canvas(root, bg="#005227", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#005227")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frames dinâmicos que aparecem/desaparecem
    area_frame_ref = {"frame": None}
    materia_frame_ref = {"frame": None}
    
    def limpar_frames_dinamicos():
        """Remove frames dinâmicos anteriores"""
        if area_frame_ref["frame"]:
            area_frame_ref["frame"].destroy()
            area_frame_ref["frame"] = None
        if materia_frame_ref["frame"]:
            materia_frame_ref["frame"].destroy()
            materia_frame_ref["frame"] = None
    
    def criar_radiobutton_customizado(parent, text, variable, value, bg_color="#005227"):
        """Cria radiobutton maior com bolinha preta"""
        frame = tk.Frame(parent, bg=bg_color)
        frame.pack(anchor="w", pady=3)
        
        rb = tk.Radiobutton(
            frame,
            text=text,
            variable=variable,
            value=value,
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 11),
            selectcolor="black",
            activebackground=bg_color,
            activeforeground="white",
            indicatoron=1,
            borderwidth=2,
            relief="flat"
        )
        rb.pack(side="left", padx=5)
        
        return rb
    
    def criar_combobox(parent, values, textvariable):
        """Cria um combobox estilizado"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Custom.TCombobox',
            fieldbackground='white',
            background='#68ddbd',
            foreground='black',
            arrowcolor='#005227',
            borderwidth=1
        )
        
        combo = ttk.Combobox(
            parent,
            textvariable=textvariable,
            values=values,
            state='readonly',
            font=("Segoe UI", 10),
            style='Custom.TCombobox',
            width=35
        )
        return combo
    
    def atualizar_campos_categoria(*args):
        """Atualiza campos quando categoria muda"""
        limpar_frames_dinamicos()
        
        quiz_data["area"].set("")
        quiz_data["materia"].set("")
        
        categoria = quiz_data["categoria"].get()
        
        if categoria == "ENEM":
            # Cria frame de área logo após cat_frame
            area_frame_ref["frame"] = tk.Frame(form_frame, bg="#005227")
            area_frame_ref["frame"].pack(fill="x", pady=(0, 10))
            
            tk.Label(
                area_frame_ref["frame"],
                text="Área do Conhecimento:",
                font=("Segoe UI", 11, "bold"),
                bg="#005227",
                fg="white"
            ).pack(anchor="w", pady=(0, 5))
            
            areas = list(materias_enem.keys())
            combo_area = criar_combobox(area_frame_ref["frame"], areas, quiz_data["area"])
            combo_area.pack(fill="x")
            
        elif categoria == "MILITAR":
            # Cria frame de matéria logo após cat_frame
            materia_frame_ref["frame"] = tk.Frame(form_frame, bg="#005227")
            materia_frame_ref["frame"].pack(fill="x", pady=(0, 10))
            
            tk.Label(
                materia_frame_ref["frame"],
                text="Matéria:",
                font=("Segoe UI", 11, "bold"),
                bg="#005227",
                fg="white"
            ).pack(anchor="w", pady=(0, 5))
            
            combo_materia = criar_combobox(materia_frame_ref["frame"], materias_militar, quiz_data["materia"])
            combo_materia.pack(fill="x")
    
    def atualizar_materias_enem(*args):
        """Atualiza matérias quando área do ENEM é selecionada"""
        # Remove frame de matéria anterior se existir
        if materia_frame_ref["frame"]:
            materia_frame_ref["frame"].destroy()
            materia_frame_ref["frame"] = None
        
        area = quiz_data["area"].get()
        
        if area and area in materias_enem:
            # Cria frame de matérias dentro do form_frame
            materia_frame_ref["frame"] = tk.Frame(form_frame, bg="#005227")
            materia_frame_ref["frame"].pack(fill="x", pady=(0, 10))
            
            tk.Label(
                materia_frame_ref["frame"],
                text="Matéria:",
                font=("Segoe UI", 11, "bold"),
                bg="#005227",
                fg="white"
            ).pack(anchor="w", pady=(0, 5))
            
            combo_materia = criar_combobox(materia_frame_ref["frame"], materias_enem[area], quiz_data["materia"])
            combo_materia.pack(fill="x")
    
    # Vincula mudanças
    quiz_data["categoria"].trace_add("write", atualizar_campos_categoria)
    quiz_data["area"].trace_add("write", atualizar_materias_enem)
    
    def adicionar_pergunta():
        """Abre janela para adicionar pergunta"""
        popup = tk.Toplevel(root)
        popup.title("Adicionar Pergunta")
        popup.geometry("400x650")
        popup.config(bg="#005227")
        popup.transient(root)
        popup.grab_set()
        
        pergunta_text = tk.StringVar()
        alt_a = tk.StringVar()
        alt_b = tk.StringVar()
        alt_c = tk.StringVar()
        alt_d = tk.StringVar()
        correta = tk.IntVar(value=0)
        
        tk.Label(
            popup,
            text="Nova Pergunta",
            font=("Segoe UI", 16, "bold"),
            bg="#005227",
            fg="white"
        ).pack(pady=15)
        
        # Pergunta
        tk.Label(popup, text="Pergunta:", font=("Segoe UI", 11, "bold"), bg="#005227", fg="white").pack(anchor="w", padx=20)
        
        pergunta_entry = tk.Text(popup, font=("Segoe UI", 11), width=40, height=3, wrap="word")
        pergunta_entry.pack(padx=20, pady=(0, 10))
        
        # Alternativas com radiobuttons maiores
        tk.Label(popup, text="Alternativas:", font=("Segoe UI", 11, "bold"), bg="#005227", fg="white").pack(anchor="w", padx=20, pady=(5, 5))
        tk.Label(popup, text="(Marque a alternativa correta)", font=("Segoe UI", 9), bg="#005227", fg="#68ddbd").pack(anchor="w", padx=20)
        
        for i, (letra, var) in enumerate([("A", alt_a), ("B", alt_b), ("C", alt_c), ("D", alt_d)]):
            frame_alt = tk.Frame(popup, bg="#005227")
            frame_alt.pack(fill="x", padx=20, pady=5)
            
            tk.Label(frame_alt, text=f"{letra})", font=("Segoe UI", 10, "bold"), bg="#005227", fg="white", width=2).pack(side="left")
            
            rb = tk.Radiobutton(
                frame_alt,
                text="",
                variable=correta,
                value=i,
                bg="#005227",
                fg="white",
                selectcolor="black",
                activebackground="#005227",
                indicatoron=1
            )
            rb.pack(side="left", padx=5)
            
            tk.Entry(frame_alt, textvariable=var, font=("Segoe UI", 10), width=30).pack(side="left")
        
        def salvar_pergunta():
            pergunta = pergunta_entry.get("1.0", "end-1c").strip()
            
            if not pergunta or not all([alt_a.get(), alt_b.get(), alt_c.get(), alt_d.get()]):
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            
            quiz_data["perguntas"].append({
                "pergunta": pergunta,
                "alternativas": [alt_a.get(), alt_b.get(), alt_c.get(), alt_d.get()],
                "correta": correta.get()
            })
            
            atualizar_lista_perguntas()
            popup.destroy()
        
        tk.Button(
            popup,
            text="✓ Adicionar Pergunta",
            font=("Segoe UI", 11, "bold"),
            bg="#68ddbd",
            fg="#005227",
            relief="flat",
            width=25,
            command=salvar_pergunta
        ).pack(pady=20)
    
    def atualizar_lista_perguntas():
        """Atualiza a lista de perguntas"""
        for w in lista_perguntas_frame.winfo_children():
            w.destroy()
        
        if not quiz_data["perguntas"]:
            tk.Label(
                lista_perguntas_frame,
                text="Nenhuma pergunta adicionada ainda",
                font=("Segoe UI", 10),
                bg="#005227",
                fg="#68ddbd"
            ).pack(pady=10)
        else:
            for i, p in enumerate(quiz_data["perguntas"]):
                pergunta_item = tk.Frame(lista_perguntas_frame, bg="#68ddbd", relief="raised", bd=2)
                pergunta_item.pack(fill="x", pady=3)
                
                texto_pergunta = p['pergunta'][:50] + ("..." if len(p['pergunta']) > 50 else "")
                
                tk.Label(
                    pergunta_item,
                    text=f"{i+1}. {texto_pergunta}",
                    font=("Segoe UI", 10),
                    bg="#68ddbd",
                    fg="#005227",
                    anchor="w"
                ).pack(side="left", padx=10, pady=8)
                
                tk.Button(
                    pergunta_item,
                    text="✗",
                    font=("Arial", 12, "bold"),
                    bg="#ff6b6b",
                    fg="white",
                    relief="flat",
                    width=3,
                    command=lambda idx=i: remover_pergunta(idx)
                ).pack(side="right", padx=5)
        
        contador_label.config(text=f"Perguntas: {len(quiz_data['perguntas'])}/10")
    
    def remover_pergunta(idx):
        quiz_data["perguntas"].pop(idx)
        atualizar_lista_perguntas()
    
    def salvar_quiz():
        if not quiz_data["titulo"].get():
            messagebox.showwarning("Atenção", "Digite um título para o quiz!")
            return
        
        if not quiz_data["categoria"].get():
            messagebox.showwarning("Atenção", "Escolha uma categoria!")
            return
        
        if not quiz_data["materia"].get():
            messagebox.showwarning("Atenção", "Escolha uma matéria!")
            return
        
        if len(quiz_data["perguntas"]) < 5:
            messagebox.showwarning("Atenção", "Adicione pelo menos 5 perguntas!")
            return
        
        resultado = {
            "titulo": quiz_data["titulo"].get(),
            "categoria": quiz_data["categoria"].get(),
            "area": quiz_data["area"].get() if quiz_data["categoria"].get() == "ENEM" else None,
            "materia": quiz_data["materia"].get(),
            "nivel": int(quiz_data["nivel"].get()),
            "perguntas": quiz_data["perguntas"],
            "autor_xp": usuario_xp,
            "autor_nivel": usuario_nivel
        }
        
        if on_salvar:
            on_salvar(resultado)
        else:
            messagebox.showinfo("Sucesso", f"Quiz '{resultado['titulo']}' salvo com sucesso!")
            if on_voltar:
                on_voltar()
    
    # Header
    tk.Button(
        scrollable_frame,
        text="← Voltar",
        font=("Segoe UI", 11, "bold"),
        bg="#03bb85",
        fg="black",
        relief="flat",
        command=on_voltar if on_voltar else lambda: print("Voltar")
    ).pack(anchor="w", padx=20, pady=(15, 10))
    
    tk.Label(
        scrollable_frame,
        text="✏️ Criar Quiz Personalizado",
        font=("Segoe UI", 18, "bold"),
        bg="#005227",
        fg="white"
    ).pack(pady=(0, 15))
    
    # Formulário
    form_frame = tk.Frame(scrollable_frame, bg="#005227")
    form_frame.pack(fill="x", padx=20)
    
    # Título
    tk.Label(form_frame, text="Título do Quiz:", font=("Segoe UI", 11, "bold"), bg="#005227", fg="white").pack(anchor="w")
    tk.Entry(form_frame, textvariable=quiz_data["titulo"], font=("Segoe UI", 11), width=40).pack(fill="x", pady=(0, 10))
    
    # Categoria
    tk.Label(form_frame, text="Categoria:", font=("Segoe UI", 11, "bold"), bg="#005227", fg="white").pack(anchor="w", pady=(0, 5))
    cat_frame = tk.Frame(form_frame, bg="#005227")
    cat_frame.pack(fill="x", pady=(0, 10))
    
    criar_radiobutton_customizado(cat_frame, "🧠 ENEM", quiz_data["categoria"], "ENEM")
    criar_radiobutton_customizado(cat_frame, "🏅 Militar", quiz_data["categoria"], "MILITAR")
    
    # Nível - vem DEPOIS dos campos dinâmicos
    nivel_label = tk.Label(scrollable_frame, text="Nível de Dificuldade:", font=("Segoe UI", 11, "bold"), bg="#005227", fg="white")
    nivel_label.pack(anchor="w", padx=20, pady=(15, 5))
    nivel_frame = tk.Frame(scrollable_frame, bg="#005227")
    nivel_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    criar_radiobutton_customizado(nivel_frame, "⭐ Fácil", quiz_data["nivel"], "1")
    criar_radiobutton_customizado(nivel_frame, "⭐⭐ Médio", quiz_data["nivel"], "2")
    criar_radiobutton_customizado(nivel_frame, "⭐⭐⭐ Difícil", quiz_data["nivel"], "3")
    
    # Lista de perguntas
    tk.Label(scrollable_frame, text="Perguntas do Quiz:", font=("Segoe UI", 12, "bold"), bg="#005227", fg="white").pack(anchor="w", padx=20, pady=(15, 5))
    
    contador_label = tk.Label(scrollable_frame, text="Perguntas: 0/10", font=("Segoe UI", 10), bg="#005227", fg="#68ddbd")
    contador_label.pack(anchor="w", padx=20)
    
    lista_perguntas_frame = tk.Frame(scrollable_frame, bg="#005227", height=200)
    lista_perguntas_frame.pack(fill="both", padx=20, pady=10)
    
    atualizar_lista_perguntas()
    
    # Botões
    tk.Button(
        scrollable_frame,
        text="+ Adicionar Pergunta",
        font=("Segoe UI", 11, "bold"),
        bg="#68ddbd",
        fg="#005227",
        relief="flat",
        width=30,
        command=adicionar_pergunta
    ).pack(pady=10)
    
    tk.Button(
        scrollable_frame,
        text="💾 Salvar Quiz",
        font=("Segoe UI", 12, "bold"),
        bg="#00ff88",
        fg="#005227",
        relief="flat",
        width=30,
        height=2,
        command=salvar_quiz
    ).pack(pady=(10, 30))
    
    # Empacota canvas
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)


# Teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("375x700")  # Ajustado para 375x700
    root.resizable(False, False)
    
    def salvar_teste(quiz):
        print("=" * 50)
        print("Quiz salvo com sucesso!")
        print(f"Título: {quiz['titulo']}")
        print(f"Categoria: {quiz['categoria']}")
        if quiz.get('area'):
            print(f"Área: {quiz['area']}")
        print(f"Matéria: {quiz['materia']}")
        print(f"Nível: {quiz['nivel']}")
        print(f"Total de perguntas: {len(quiz['perguntas'])}")
        print("=" * 50)
    
    # Teste com usuário que PODE criar (500+ XP)
    montar_criador_quiz(root, usuario_xp=600, usuario_nivel=3, on_salvar=salvar_teste)
    
    # Teste com usuário BLOQUEADO (descomentar para testar)
    # montar_criador_quiz(root, usuario_xp=200, usuario_nivel=2, on_salvar=salvar_teste)
    
    root.mainloop()
