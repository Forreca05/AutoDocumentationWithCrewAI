from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, DirectoryReadTool
from .custom_tools.github_repo_cloner_tool import GitHubRepoClonerTool
from .custom_tools.github_downloader_tool import GitHubDownloaderTool

my_llm = LLM(
    model="lm_studio/google/gemma-3n-e4b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

@CrewBase
class CodeDocumentationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, method: str):
        self.method = method  # "raw_link" ou "clone_repo"

    @agent
    def github_file_downloader(self) -> Agent:
        return Agent(
            config=self.agents_config["github_file_downloader"],
            tools=[GitHubDownloaderTool()],
            llm=my_llm,
            verbose=True,
        )

    @agent
    def repo_cloner(self) -> Agent:
        return Agent(
            config=self.agents_config["repo_cloner"],
            tools=[GitHubRepoClonerTool()],
            llm=my_llm,
            verbose=True,
        )

    @agent
    def file_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["file_reader"],
            tools=[FileReadTool()],
            llm=my_llm,
            verbose=True,
        )
    
    @agent
    def directory_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["directory_reader"],
            tools=[DirectoryReadTool(directory="./requests_repo")],
            llm=my_llm,
            verbose=True,
        )

    @agent
    def code_insight_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["code_insight_agent"],
            llm=my_llm,
            verbose=True,
        )

    @agent
    def doc_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["doc_writer"],
            llm=my_llm,
            verbose=True,
        )

    @agent
    def markdown_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config["markdown_formatter"],
            llm=my_llm,
            verbose=True,
        )
    
    @task
    def download_github_file_task(self) -> Task:
        return Task(config=self.tasks_config["download_github_file_task"])

    @task
    def clone_repo_task(self) -> Task:
        return Task(config=self.tasks_config["clone_repo_task"])

    @task
    def read_file_task(self) -> Task:
        return Task(config=self.tasks_config["read_file_task"])
    
    @task
    def read_directory_task(self) -> Task:
        return Task(config=self.tasks_config["read_directory_task"])
    
    @task
    def extract_insights_task(self) -> Task:
        return Task(config=self.tasks_config["extract_insights_task"])

    @task
    def generate_doc_task(self) -> Task:
        return Task(config=self.tasks_config["generate_doc_task"])

    @task
    def markdown_format_task(self) -> Task:
        return Task(
            config=self.tasks_config["markdown_format_task"],
            output_file="documentacao_final.md"
        )

    @crew
    def crew(self) -> Crew:
        if self.method == "raw_link":
            agents = [
                self.github_file_downloader(),
                self.file_reader(),
                self.code_insight_agent(),
                self.doc_writer(),
                self.markdown_formatter()
            ]
            tasks = [
                self.download_github_file_task(),
                self.read_file_task(),
                self.extract_insights_task(),
                self.generate_doc_task(),
                self.markdown_format_task()
            ]
        elif self.method == "clone_repo":
            agents = [
                self.repo_cloner(),
                self.directory_reader(),
                self.code_insight_agent(),
                self.doc_writer(),
                self.markdown_formatter()
            ]
            tasks = [
                self.clone_repo_task(),
                self.read_directory_task(),
                self.extract_insights_task(),
                self.generate_doc_task(),
                self.markdown_format_task()
            ]
        else:
            raise ValueError("Método inválido. Usa 'raw_link' ou 'clone_repo'.")

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
