# ------------------------------------------------------------
# Aqui ficam:
#  - o ponto de entrada da aplicação (Tkinter)
#  - a criação da janela principal e do Router
#  - a primeira tela exibida (Splash)
# Fluxo:
#  1) Splash (logo + botão)
#  2) Login (cadastro)
#  3) Home
# ------------------------------------------------------------

import tkinter as tk
from router import Router
from pathlib import Path

if __name__ == "__main__":
    db_path = Path("dados") / "estudae.db"

    if not db_path.exists():
        print("🔨 Banco de dados não encontrado. Inicializando...")
        try:
            from dados.database import inicializar_banco, popular_dados_iniciais
            inicializar_banco()
            popular_dados_iniciais()
            print("✅ Banco criado com sucesso!\n")

            # Pergunta se quer popular perguntas
            resposta = input("\n📥 Deseja importar perguntas da API? (recomendado) [S/n]: ")
            if resposta.lower() != 'n':
                print("\n⏳ Importando perguntas... (pode demorar um pouco)")
                try:
                    from dados.popular_perguntas import criar_niveis_e_popular
                    criar_niveis_e_popular()
                    print("✅ Perguntas importadas com sucesso!\n")
                except Exception as e:
                    print(f"⚠️ Erro ao importar perguntas: {e}")
                    print("Você pode importar depois executando: python dados/popular_perguntas.py\n")

        except Exception as e:
            print(f"❌ Erro ao criar banco: {e}")
            print("Execute manualmente: python dados/database.py")
            exit(1)
    
    root = tk.Tk()
    
    root.title("EstudAe")
    root.geometry("375x700")  # Simula mobile
    root.resizable(False, False)
    
    app = Router(root)
    app.ir_para_login()
    root.mainloop()