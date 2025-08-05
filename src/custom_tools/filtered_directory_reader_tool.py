import os
import time
from pydantic import Field
from crewai.tools import BaseTool

class FilteredDirectoryReaderTool(BaseTool):
    name: str = Field("FilteredDirectoryReaderTool", init=False)
    description: str = Field(
        "Lista ficheiros de código e escreve list_of_files.txt no diretório atual.",
        init=False
    )

    def _run(self, directory: str) -> str:
        if not os.path.isdir(directory):
            return f"❌ Diretório '{directory}' não encontrado."

        code_files = []
        ignored_dirs = {".git", "__pycache__", ".github", ".vscode", "node_modules"}
        allowed_extensions = {
            ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rb", ".rs"
        }

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in allowed_extensions:
                    full_path = os.path.join(root, file)
                    code_files.append(full_path)

        if not code_files:
            return "⚠️ Nenhum ficheiro de código relevante encontrado."

        # Caminho fora do repositório clonado
        output_file = os.path.join(os.getcwd(), "list_of_files.txt")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(code_files))
        except Exception as e:
            return f"❌ Erro ao escrever list_of_files.txt: {str(e)}"

        # ✅ Esperar até o sistema garantir que o ficheiro foi criado
        timeout = 5  # segundos
        for _ in range(timeout * 10):
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                break
            time.sleep(0.1)
        else:
            return "❌ Ficheiro não ficou disponível após escrita (timeout)."

        return f"✅ {len(code_files)} ficheiros listados em '{output_file}'."
