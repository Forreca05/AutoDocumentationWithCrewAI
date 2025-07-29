from src.crew import CodeDocumentationCrew
from urllib.parse import urlparse

def extract_output_path(url):
    path = urlparse(url).path
    return "downloads" + path[path.rfind("/"):]

url = "https://github.com/Forreca05/Codeforces"
clone_dir = "requests_repo"

if __name__ == "__main__":
    inputs = {"repo_url": url,
              "clone_dir": clone_dir}
    CodeDocumentationCrew().crew().kickoff(inputs=inputs)