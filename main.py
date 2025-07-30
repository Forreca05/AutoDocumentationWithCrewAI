from src.crew import CodeDocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

if __name__ == "__main__":
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
            "output_path" : output_path
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

    # Cria a crew e executa
    crew = CodeDocumentationCrew(method=method).crew()
    crew.kickoff(inputs=inputs)
