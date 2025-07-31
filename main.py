import sys
from src.crew import CodeDocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

def main(method=None, inputs=None):
    if method is None or inputs is None:
        # Modo interativo original (input)
        print("\n📄 Como preferes gerar a documentação do teu código?\n")
        print("  1️⃣  Usar o link RAW direto do GitHub (arquivo único)")
        print("  2️⃣  Clonar um repositório completo\n")

        choice = input("Escolhe uma opção (1 ou 2): ").strip()

        if choice == "1":
            url = input("\n📎 Cola o link RAW do GitHub: ").strip()
            output_path = extract_output_path(url)
            method = "raw_link"
            inputs = {
                "url": url,
                "output_path": output_path
            }
        elif choice == "2":
            repo_url = input("\n📎 Cola o link do repositório GitHub: ").strip()
            method = "clone_repo"
            inputs = {
                "repo_url": repo_url,
                "clone_dir": "requests_repo"
            }
        else:
            print("\n❌ Opção inválida. Usa 1 ou 2.")
            exit(1)

    # Executa a crew
    crew = CodeDocumentationCrew(method=method).crew()
    crew.kickoff(inputs=inputs)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # exemplo: python main.py clone_repo https://github.com/usuario/repositorio.git
        method = sys.argv[1]
        if method == "raw_link":
            inputs = {
                "url": sys.argv[2],
                "output_path": extract_output_path(sys.argv[2])
            }
        elif method == "clone_repo":
            inputs = {
                "repo_url": sys.argv[2],
                "clone_dir": "requests_repo"
            }
        else:
            print("Método inválido.")
            sys.exit(1)
        main(method, inputs)
    else:
        main()
