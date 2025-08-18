import os
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
from src.crew import DownloadAndExtractCrew, DocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

def get_repo_name(repo_url: str) -> str:
    path = urlparse(repo_url).path
    parts = path.strip("/").split("/")
    
    if len(parts) >= 2:
        repo_name = parts[1] 
    else:
        repo_name = os.path.basename(path)

    return repo_name.replace(".git", "")

def normalize_github_url(repo_url: str) -> str:
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) >= 2:
        normalized_path = "/".join(path_parts[:2]) + ".git"
        return f"{parsed.scheme}://{parsed.netloc}/{normalized_path}"
    return repo_url

def main(method=None, inputs=None):
    if method is None or inputs is None:
        print("\n📄 Como preferes gerar a documentação do teu código?\n")
        print("  1️⃣  Usar o link RAW direto do GitHub (arquivo único)")
        print("  2️⃣  Clonar um repositório completo\n")

        choice = input("Escolhe uma opção (1 ou 2): ").strip()

        if choice == "1":
            url = input("\n📎 Cola o link RAW do GitHub: ").strip()
            method = "raw_link"
            inputs = {
                "url": url,
                "output_path": extract_output_path(url),
            }
        elif choice == "2":
            repo_url = input("\n📎 Cola o link do repositório GitHub: ").strip()
            branch = (input("🌿 Nome da branch (default: main): ") or "").strip() or "main"
            method = "clone_repo"
            inputs = {
                "repo_url": normalize_github_url(repo_url),
                "clone_dir": get_repo_name(repo_url),
                "branch": branch,
                "output_file": "list_of_files.txt",
                "list_file_path": "list_of_files.txt",
                "final_result": "final.py",
                "final_text" : "code_output.txt"
            }
        else:
            print("\n❌ Opção inválida. Usa 1 ou 2.")
            exit(1)

    # 1️⃣ Primeira etapa: download/clonagem + concatenação de ficheiros
    pre_crew = DownloadAndExtractCrew(method=method).crew()
    pre_crew.kickoff(inputs=inputs)

    # 2️⃣ Segunda etapa: leitura e documentação
    doc_crew = DocumentationCrew(method=method).crew()
    doc_crew.kickoff(inputs=inputs)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        method = sys.argv[1]
        if method == "clone_repo":
            repo_url = sys.argv[2]
            branch = sys.argv[3] if len(sys.argv) > 3 else "main"
            inputs = {
                "repo_url": normalize_github_url(repo_url),
                "clone_dir": get_repo_name(repo_url),
                "branch": branch,
                "output_file": "list_of_files.txt",
                "list_file_path": "list_of_files.txt",
                "final_result": "final.py",
                "final_text" : "code_output.txt"
            }
        else:
            print("Método inválido. Usa 'raw_link' ou 'clone_repo'.")
            sys.exit(1)
        main(method, inputs)
    else:
        main()
