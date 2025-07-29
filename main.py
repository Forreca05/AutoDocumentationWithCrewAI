from src.crew import CodeDocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

url = "https://raw.githubusercontent.com/Forreca05/Jaba-is-You/master/src/main/java/com/t10g06/baba/controller/game/ArenaController.java"
output_path = extract_output_path(url)

if __name__ == "__main__":
    inputs = {"url": url,
              "output_path": output_path}
    print(f"🪵 DEBUG: output_path = {output_path}")
    CodeDocumentationCrew().crew().kickoff(inputs=inputs)
