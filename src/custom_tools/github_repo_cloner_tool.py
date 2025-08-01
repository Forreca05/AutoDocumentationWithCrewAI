import subprocess
import os
import shutil
import stat
from crewai.tools import BaseTool
from pydantic import Field

class GitHubRepoClonerTool(BaseTool):
    name: str = Field("GitHub Repository Cloner", init=False)
    description: str = Field(
        "Clona um repositório GitHub para um diretório local. Apaga o diretório se já existir.",
        init=False
    )

    def _on_rm_error(self, func, path, exc_info):
        # Tenta remover permissão de só leitura e apaga de novo
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def _run(self, repo_url: str, clone_dir: str) -> str:
        try:
            if os.path.exists(clone_dir):
                shutil.rmtree(clone_dir, onerror=self._on_rm_error)

            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
            return f"✅ Repositório clonado com sucesso em '{clone_dir}'."

        except subprocess.CalledProcessError as e:
            return f"❌ Erro ao executar comando Git: {str(e)}"
        except Exception as e:
            return f"⚠️ Erro inesperado: {str(e)}"
