import sys
from src.crew import CodeDocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

def main(method=None, inputs=None):
    if method is None or inputs is None:
        # Modo interativo original
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
            branch = (input("🌿 Nome da branch (default: main): ") or "").strip() or "main"
            method = "clone_repo"
            inputs = {
                "repo_url": repo_url,
                "clone_dir": "requests_repo",
                "branch": branch
            }
        else:
            print("\n❌ Opção inválida. Usa 1 ou 2.")
            exit(1)

    crew = CodeDocumentationCrew(method=method).crew()
    crew.kickoff(inputs=inputs)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        method = sys.argv[1]
        if method == "raw_link":
            url = sys.argv[2]
            inputs = {
                "url": url,
                "output_path": extract_output_path(url)
            }
        elif method == "clone_repo":
            repo_url = sys.argv[2]
            branch = sys.argv[3] if len(sys.argv) > 3 else "main"
            inputs = {
                "repo_url": repo_url,
                "clone_dir": "requests_repo",
                "branch": branch
            }
        else:
            print("Método inválido. Usa 'raw_link' ou 'clone_repo'.")
            sys.exit(1)
        main(method, inputs)
    else:
        main()
