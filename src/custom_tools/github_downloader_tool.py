from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests

class GitHubDownloaderTool(BaseTool):
    name: str = Field("GitHub File Downloader", init=False)
    description: str = Field("Faz download de um ficheiro diretamente de um link RAW do GitHub", init=False)

    def _run(self, url: str, output_path: str = "downloaded_file.py") -> str:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                return f"Ficheiro guardado como: {output_path}"
            else:
                return f"Erro ao fazer download. Status code: {response.status_code}"
        except Exception as e:
            return f"Erro: {str(e)}"
