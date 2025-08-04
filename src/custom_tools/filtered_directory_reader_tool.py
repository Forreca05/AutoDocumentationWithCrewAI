import os
from pydantic import Field
from crewai.tools import BaseTool

class FilteredDirectoryReaderTool(BaseTool):
    name: str = Field("FilteredDirectoryReaderTool", init=False)
    description: str = Field(
        "Lista apenas ficheiros de código relevantes, ignorando .git, __pycache__, etc.",
        init=False
    )

    def _run(self, directory: str) -> str:
        code_files = []
        ignored_dirs = {".git", "__pycache__", ".github", ".vscode", "node_modules"}
        allowed_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rb", ".rs"}

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in allowed_extensions:
                    full_path = os.path.join(root, file)
                    code_files.append(full_path)

        return "\n".join(code_files)
