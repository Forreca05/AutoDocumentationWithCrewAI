import os
import re
import regex
from crewai.tools import BaseTool
from pydantic import Field
from typing import ClassVar, Dict, List

class CodeSplitterTool(BaseTool):
    LANG_KEYWORDS: ClassVar[Dict[str, List[str]]] = {
        "py": ["def ", "import ", "class "],
        "cpp": ["#include", "std::", "int main"],
        "js": ["function ", "console.log", "export "],
        "java": ["public class", "void main", "import java"],
        "c": ["#include", "int main", "printf"],
    }

    name: str = Field("Code Splitter Tool", init=False)
    description: str = Field("Une todos os blocos num ficheiro só, limpa emojis e corrige extensão.", init=False)

    def detect_language(self, content: str, fallback="txt") -> str:
        content_lower = content.lower()
        for lang, keywords in self.LANG_KEYWORDS.items():
            if any(kw.lower() in content_lower for kw in keywords):
                return lang
        return fallback

    def clean_text(self, text: str) -> str:
        # Remove apenas emojis
        return regex.sub(r'\p{Emoji_Presentation}', '', text)

    def _run(self, *args, **kwargs) -> str:
        """
        Sempre processa o arquivo 'final.py' no diretório atual.
        Ignora qualquer parâmetro passado pela execução.
        """
        input_file = "final.py"
        output_file = "code_output.txt"

        if not os.path.exists(input_file):
            return f"⚠ Arquivo '{input_file}' não encontrado."

        # Se existir, apaga para evitar conflitos
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex para capturar blocos incluindo linha marcador e conteúdo até próximo marcador ou fim
        pattern = re.compile(r'(?m)^--- FILE: .+ ---$\n?(.*?)(?=^--- FILE: .+ ---$|\Z)', re.DOTALL)
        matches = list(pattern.finditer(content))
        if not matches:
            return "⚠ Nenhum marcador de ficheiro encontrado no input."

        lines = content.splitlines(keepends=True)
        output_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("--- FILE:"):
                output_lines.append(line)
                i += 1
                block_lines = []
                while i < len(lines) and not lines[i].startswith("--- FILE:"):
                    block_lines.append(lines[i])
                    i += 1
                block_text = "".join(block_lines)
                cleaned_block = self.clean_text(block_text)
                output_lines.append(cleaned_block)
                output_lines.append("\n")  # separa blocos
            else:
                output_lines.append(line)
                i += 1

        combined_content = "".join(output_lines)

        with open(output_file, "w", encoding="utf-8") as out:
            out.write(combined_content)

        return f"✅ Feito! Conteúdo unido, emojis removidos, salvo em '{output_file}'."
