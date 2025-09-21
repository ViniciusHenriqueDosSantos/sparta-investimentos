import subprocess
import sys

def run_command(command, description):
    print(f"{description}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("""
  python run.py start     - Inicia o servidor
  python run.py build     - Instala dependências, inicializa banco e inicia
  python run.py install   - Instala apenas as dependências
  python run.py init      - Inicializa apenas o banco de dados
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        run_command("uvicorn main:app --host 0.0.0.0 --port 8000 --reload", 
                   "Iniciando servidor da API Sparta")
    
    elif command == "build":
        print("Instalando dependências...")
        run_command("pip install -r requirements.txt", "Instalando dependências")
        print("Inicializando banco de dados...")
        run_command("python init_database.py", "Inicializando banco de dados")
        print("Iniciando servidor...")
        run_command("uvicorn main:app --host 0.0.0.0 --port 8000 --reload", 
                   "Iniciando servidor da API Sparta")
    
    elif command == "install":
        run_command("pip install -r requirements.txt", "Instalando dependências")
    
    elif command == "init":
        run_command("python init_database.py", "Inicializando banco de dados")
        
    else:
        print(f"Comando desconhecido: {command}")

if __name__ == "__main__":
    main()
