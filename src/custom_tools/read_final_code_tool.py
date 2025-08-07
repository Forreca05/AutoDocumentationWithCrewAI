import os
from crewai.tools import BaseTool
from pydantic import Field

class ReadFinalCodeTool(BaseTool):
    name: str = Field("ReadFinalCodeTool", init=False)
    description: str = Field(
        "Lê o conteúdo completo do ficheiro especificado em final_result.",
        init=False
    )

    def _run(self, file_path: str) -> str:
        if not os.path.isfile(file_path):
            return f"❌ Ficheiro '{file_path}' não encontrado."

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
            return f"📄 Conteúdo do ficheiro '{file_path}':\n\n{content}"
        except Exception as e:
            return f"❌ Erro ao ler o ficheiro '{file_path}': {e}"
