from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# Tools personalizadas
from crewai_tools import FileReadTool, DirectoryReadTool
from .custom_tools.github_downloader_tool import GitHubDownloaderTool
from .custom_tools.github_repo_cloner_tool import GitHubRepoClonerTool
from .custom_tools.filtered_directory_reader_tool import FilteredDirectoryReaderTool
from .custom_tools.read_file_tool import ReadFileTool
from .custom_tools.read_final_code_tool import ReadFinalCodeTool

# Configuração do modelo de linguagem
my_llm = LLM(
    model="lm_studio/google/gemma-3n-e4b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

code_reader_tool = FileReadTool(file_path="final.py", line_count=None, encoding="utf-8")

# ----------------------------------------------------------
# CREW 1: Download e agregação de conteúdo
# ----------------------------------------------------------
@CrewBase
class DownloadAndExtractCrew:
    agents_config = "config/agents_download.yaml"
    tasks_config = "config/tasks_download.yaml"

    def __init__(self, method: str):
        self.method = method  # "raw_link" ou "clone_repo"

    @agent
    def github_file_downloader(self):
        return Agent(
            config=self.agents_config["github_file_downloader"],
            tools=[GitHubDownloaderTool()],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def repo_cloner(self):
        return Agent(
            config=self.agents_config["repo_cloner"],
            tools=[GitHubRepoClonerTool()],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def file_lister(self):
        return Agent(
            config=self.agents_config["file_lister"],
            tools=[FilteredDirectoryReaderTool()],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def file_content_reader(self):
        return Agent(
            config=self.agents_config["file_content_reader"],
            tools=[ReadFileTool()],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def download_github_file_task(self):
        return Task(config=self.tasks_config["download_github_file_task"])

    @task
    def clone_repo_task(self):
        return Task(config=self.tasks_config["clone_repo_task"])

    @task
    def list_files_task(self):
        return Task(config=self.tasks_config["list_files_task"])

    @task
    def read_file_contents_task(self):
        return Task(config=self.tasks_config["read_file_contents_task"])

    @crew
    def crew(self):
        if self.method == "raw_link":
            agents = [
                self.github_file_downloader(),
                self.file_content_reader()
            ]
            tasks = [
                self.download_github_file_task(),
                self.read_file_contents_task()
            ]
        elif self.method == "clone_repo":
            agents = [
                self.repo_cloner(),
                self.file_lister(),
                self.file_content_reader()
            ]
            tasks = [
                self.clone_repo_task(),
                self.list_files_task(),
                self.read_file_contents_task()
            ]
        else:
            raise ValueError("Método inválido. Use 'raw_link' ou 'clone_repo'.")

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

# ----------------------------------------------------------
# CREW 2: Leitura de código e geração de documentação
# ----------------------------------------------------------
@CrewBase
class DocumentationCrew:
    agents_config = "config/agents_document.yaml"
    tasks_config = "config/tasks_document.yaml"

    @agent
    def code_reader(self):
        return Agent(
            config=self.agents_config["code_reader"],
            tools=[code_reader_tool],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def code_insight_agent(self):
        return Agent(
            config=self.agents_config["code_insight_agent"],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def doc_writer(self):
        return Agent(
            config=self.agents_config["doc_writer"],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def markdown_formatter(self):
        return Agent(
            config=self.agents_config["markdown_formatter"],
            llm=my_llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def read_code_task(self):
        return Task(config=self.tasks_config["read_code_task"])

    @task
    def extract_insights_task(self):
        return Task(config=self.tasks_config["extract_insights_task"])

    @task
    def generate_doc_task(self):
        return Task(config=self.tasks_config["generate_doc_task"])

    @task
    def markdown_format_task(self):
        return Task(
            config=self.tasks_config["markdown_format_task"],
            output_file="documentacao_final.md"
        )

    @crew
    def crew(self):
        agents = [
            self.code_reader(),
            self.code_insight_agent(),
            self.doc_writer(),
            self.markdown_formatter()
        ]

        tasks = [
            self.read_code_task(),
            self.extract_insights_task(),
            self.generate_doc_task(),
            self.markdown_format_task()
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
