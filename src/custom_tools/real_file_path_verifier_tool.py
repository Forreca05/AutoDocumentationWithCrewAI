import os
from pydantic import Field
from crewai.tools import BaseTool

class RealFilePathVerifierTool(BaseTool):
    name: str = Field("Real File Path Verifier", init=False)
    description: str = Field("Verifica caminhos de ficheiros e remove os inválidos de uma lista num ficheiro de texto.", init=False)

    def _run(self, filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                file_paths = [line.strip() for line in f]

            valid_paths = [p for p in file_paths if os.path.exists(p)]

            with open(filepath, 'w', encoding='utf-8') as f:
                for p in valid_paths:
                    f.write(p + '\n')

            return f"Lista validada com sucesso. {len(valid_paths)} caminhos mantidos em {filepath}."
        except Exception as e:
            return f"Erro ao validar os caminhos: {str(e)}"
