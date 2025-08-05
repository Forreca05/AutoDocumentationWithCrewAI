import os

from crewai.tools import BaseTool
from pydantic import Field

class ReadFileTool(BaseTool):
    name: str = Field("ReadFileTool", init=False)
    description: str = Field(
        "Lê os ficheiros listados no ficheiro list_of_files.txt e retorna seu conteúdo para análise.",
        init=False
    )

    def _run(self, list_file_path: str = "list_of_files.txt") -> str:
        if not os.path.isfile(list_file_path):
            return f"❌ list_of_files.txt não encontrado no caminho: {list_file_path}"

        with open(list_file_path, "r", encoding="utf-8") as f:
            file_paths = [line.strip() for line in f if line.strip()]

        if not file_paths:
            return "⚠️ list_of_files.txt está vazio."

        all_contents = []
        for path in file_paths:
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                        all_contents.append(f"--- FILE: {path} ---\n{content}")
                except Exception as e:
                    all_contents.append(f"--- FILE: {path} ---\n⚠️ Erro ao ler o ficheiro: {e}")
            else:
                all_contents.append(f"--- FILE: {path} ---\n⚠️ Caminho inválido ou ficheiro não encontrado.")

        return "\n\n".join(all_contents)
