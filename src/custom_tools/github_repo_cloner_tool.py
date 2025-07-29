import subprocess
import os
import shutil
from crewai.tools import BaseTool
from pydantic import Field

class GitHubDownloaderTool(BaseTool):
    name: str = Field("GitHub Repository Cloner", init=False)
    description: str = Field(
        "Clona um repositório GitHub para um diretório local. Apaga o diretório se já existir.",
        init=False
    )

    def _run(self, repo_url: str, clone_dir: str) -> str:
        try:
            # Se a pasta já existe, apaga-a primeiro
            if os.path.exists(clone_dir):
                shutil.rmtree(clone_dir)  # ⚠️ Apaga a pasta inteira com tudo dentro!

            # Clona o novo repositório
            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
            return f"✅ Repositório clonado com sucesso em '{clone_dir}'."

        except subprocess.CalledProcessError as e:
            return f"❌ Erro ao executar comando Git: {str(e)}"
        except Exception as e:
            return f"⚠️ Erro inesperado: {str(e)}"
