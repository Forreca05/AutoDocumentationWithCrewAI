import os
from crewai.tools import BaseTool
from pydantic import Field

class ExportCodeToFileTool(BaseTool):
    name: str = Field("ExportCodeToFileTool", init=False)
    description: str = Field(
        "Lê os ficheiros listados no ficheiro list_of_files.txt, retorna seu conteúdo e salva tudo em {final_result}.",
        init=False
    )

    def _run(self, final_result: str, list_file_path: str = "list_of_files.txt") -> str:
        if not os.path.isfile(list_file_path):
            return f"❌ {list_file_path} não encontrado."

        try:
            with open(list_file_path, "r", encoding="utf-8") as f:
                file_paths = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return f"❌ Erro ao ler {list_file_path}: {e}"

        if not file_paths:
            return f"⚠️ {list_file_path} está vazio."

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

        final_content = "\n\n".join(all_contents)

        try:
            with open(final_result, "w", encoding="utf-8") as final_file:
                final_file.write(final_content)
        except Exception as e:
            return f"❌ Erro ao salvar {final_result}: {e}"

        return f"✅ Conteúdo combinado salvo com sucesso em {final_result}"
