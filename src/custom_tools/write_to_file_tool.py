import os
from pydantic import Field
from crewai.tools import BaseTool

class WriteToFileTool(BaseTool):
    name: str = Field("Write to file", init=False)
    description: str = Field("Escreve conteúdo num ficheiro local, substituindo o conteúdo anterior.", init=False)

    def _run(self, file_path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Conteúdo escrito com sucesso em: {file_path}"
        except Exception as e:
            return f"Erro ao escrever o ficheiro {file_path}: {str(e)}"
