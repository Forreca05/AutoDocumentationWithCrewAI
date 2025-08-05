from crewai.tools import BaseTool
from pydantic import Field
import os

class LoadFileListTool(BaseTool):
    name: str = Field("Load Valid File Paths", init=False)
    description: str = Field("Lê list_of_files.txt e retorna uma lista de caminhos de ficheiro normalizados.", init=False)

    def _run(self, list_file_path: str) -> str:
        try:
            with open(list_file_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            cleaned = [line.replace('\\', '/').strip() for line in lines if os.path.isfile(line.strip())]
            return "\n".join(cleaned)
        except Exception as e:
            return f"Erro ao carregar lista: {str(e)}"
