from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from .custom_tools.github_downloader_tool import GitHubDownloaderTool

# LLM local (ex: LM Studio com llama-3)
my_llm = LLM(
    model="lm_studio/google/gemma-3n-e4b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

@CrewBase
class CodeDocumentationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def github_file_downloader(self) -> Agent:
        return Agent(
            config=self.agents_config["github_file_downloader"],
            tools=[GitHubDownloaderTool()],
            llm=my_llm,
            verbose=True,
        )
    
    @agent
    def code_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["code_reader"],
            tools=[FileReadTool()],
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
        return Task(
            config=self.tasks_config["download_github_file_task"],
        )

    @task
    def read_code_task(self) -> Task:
        return Task(config=self.tasks_config["read_code_task"])

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
        """Cria a equipe que realiza a documentação de código."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
