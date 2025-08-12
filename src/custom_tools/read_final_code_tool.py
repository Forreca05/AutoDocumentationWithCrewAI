from typing import Optional, Union
from crewai_tools import FileReadTool
from pydantic import Field

class SafeReadFileTool(FileReadTool):
    name: str = Field("Safe Read File Tool", init=False)
    description: str = Field(
        "Lê um ficheiro, convertendo o parâmetro line_count de str para int quando necessário.",
        init=False
    )

    def _normalize_args(self, line_count: Optional[Union[str, int]]) -> Optional[int]:
        if isinstance(line_count, str):
            if line_count.strip().lower() in ("", "none", "null"):
                return None
            try:
                return int(line_count)
            except Exception:
                raise ValueError(f"⚠ line_count inválido: {line_count}")
        return line_count

    def _run(self, file_path: str, start_line: Optional[int] = None, line_count: Optional[Union[int, str]] = None) -> str:
        try:
            line_count = self._normalize_args(line_count)
        except ValueError as e:
            return str(e)

        # Normalizar start_line caso queira (opcional)
        if isinstance(start_line, str):
            if start_line.strip().lower() in ("", "none", "null"):
                start_line = None
            else:
                try:
                    start_line = int(start_line)
                except Exception:
                    return f"⚠ start_line inválido: {start_line}"

        return super()._run(file_path=file_path, start_line=start_line, line_count=line_count)
