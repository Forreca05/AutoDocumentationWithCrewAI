from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

import os
from dotenv import load_dotenv

# Tools personalizadas
from crewai_tools import FileReadTool, DirectoryReadTool
from .custom_tools.github_downloader_tool import GitHubDownloaderTool
from .custom_tools.github_repo_cloner_tool import GitHubRepoClonerTool
from .custom_tools.filtered_directory_reader_tool import FilteredDirectoryReaderTool
from .custom_tools.export_code_to_file_tool import ExportCodeToFileTool
from .custom_tools.cleaner_tool import CleanerTool

# Configuração do modelo de linguagem com LM Studio
#download_llm = LLM(
#    model="lm_studio/google/gemma-3n-e4b",
#    base_url="http://127.0.0.1:1234/v1",
#    api_key="not-needed"
#)

#document_llm = LLM(
#    model="lm_studio/google_gemma-3n-e4b-it",
#    base_url="http://127.0.0.1:1234/v1",
#    api_key="not-needed"
#)

# Configuração do modelo de linguagem com Open API Key

# Carregar variáveis do .env
load_dotenv()

download_llm = LLM(
    model="gpt-4.1-mini", 
    api_key=os.getenv("OPENAI_API_KEY")
)

document_llm = LLM(
    model="gpt-4.1-mini", 
    api_key=os.getenv("OPENAI_API_KEY")
)


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
            llm=download_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def repo_cloner(self):
        return Agent(
            config=self.agents_config["repo_cloner"],
            tools=[GitHubRepoClonerTool()],
            llm=download_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def file_lister(self):
        return Agent(
            config=self.agents_config["file_lister"],
            tools=[FilteredDirectoryReaderTool()],
            llm=download_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def code_exporter(self):
        return Agent(
            config=self.agents_config["code_exporter"],
            tools=[ExportCodeToFileTool()],
            llm=download_llm,
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def cleaner(self):
        return Agent(
            config=self.agents_config["cleaner"],
            tools=[CleanerTool()],
            llm=download_llm,
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
    def code_exporter_task(self):
        return Task(config=self.tasks_config["code_exporter_task"])
    
    @task
    def cleaner_task(self):
        return Task(config=self.tasks_config["cleaner_task"])

    @crew
    def crew(self):
        if self.method == "raw_link":
            agents = [
                self.github_file_downloader(),
            ]
            tasks = [
                self.download_github_file_task(),
            ]
        elif self.method == "clone_repo":
            agents = [
                self.repo_cloner(),
                self.file_lister(),
                self.code_exporter(),
                self.cleaner()
            ]
            tasks = [
                self.clone_repo_task(),
                self.list_files_task(),
                self.code_exporter_task(),
                self.cleaner_task()
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

    def __init__(self, method: str):
        self.method = method  # "raw_link" ou "clone_repo"

    @agent
    def raw_code_reader(self, output_path=None):
        file_path = output_path
        code_reader_tool_dynamic = FileReadTool(file_path=file_path)
        return Agent(
            config=self.agents_config["raw_code_reader"],
            tools=[code_reader_tool_dynamic],
            llm=document_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def code_reader(self, final_text=None):
        file_path = final_text
        code_reader_tool = FileReadTool(file_path=file_path)
        return Agent(
            config=self.agents_config["code_reader"],
            tools=[code_reader_tool],
            llm=document_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def code_insight_agent(self):
        key = "raw_code_insight_agent" if self.method == "raw_link" else "code_insight_agent"
        return Agent(
            config=self.agents_config[key],
            llm=document_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def doc_writer(self):
        key = "raw_doc_writer" if self.method == "raw_link" else "doc_writer"
        return Agent(
            config=self.agents_config[key],
            llm=document_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def markdown_formatter(self):
        key = "raw_markdown_formatter" if self.method == "raw_link" else "markdown_formatter"
        return Agent(
            config=self.agents_config[key],
            llm=document_llm,
            verbose=True,
            allow_delegation=False
        )
    
    @task
    def read_code_task_raw_link(self):
        return Task(config=self.tasks_config["read_code_task_raw_link"])
    
    @task
    def read_code_task(self):
        return Task(config=self.tasks_config["read_code_task"])

    @task
    def extract_insights_task(self):
        key = "extract_insights_task_raw_link" if self.method == "raw_link" else "extract_insights_task"
        return Task(config=self.tasks_config[key])

    @task
    def generate_doc_task(self):
        key = "generate_doc_task_raw_link" if self.method == "raw_link" else "generate_doc_task"
        return Task(config=self.tasks_config[key])

    @task
    def markdown_format_task(self):
        key = "markdown_format_task_raw_link" if self.method == "raw_link" else "markdown_format_task"
        return Task(
            config=self.tasks_config[key],
            output_file="documentacao_final.md"
        )

    @crew
    def crew(self):
        if self.method == "raw_link":
            agents = [
                self.raw_code_reader(),
                self.code_insight_agent(),
                self.doc_writer(),
                self.markdown_formatter()
            ]

            tasks = [
                self.read_code_task_raw_link(),
                self.extract_insights_task(),
                self.generate_doc_task(),
                self.markdown_format_task()
            ]
        elif self.method == "clone_repo":
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
