from crewai.tools import BaseTool
from pydantic import Field
import subprocess
import os

class GitHubRepoClonerTool(BaseTool):
    name: str = Field(default="GitHub Repo Cloner", init=False)
    description: str = Field(
        default="Clona um repositório GitHub inteiro para um diretório local.",
        init=False
    )

    def _run(self, repo_url: str, clone_dir: str = "repositorio_clonado") -> str:
        try:
            if os.path.exists(clone_dir):
                return f"A pasta '{clone_dir}' já existe. Apague-a antes de clonar novamente."

            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
            return f"✅ Repositório clonado com sucesso em '{clone_dir}'."
        except subprocess.CalledProcessError as e:
            return f"❌ Erro ao clonar repositório: {str(e)}"
