from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# Imports de ferramentas personalizadas usadas pelos agentes
from crewai_tools import FileReadTool
from .custom_tools.github_downloader_tool import GitHubDownloaderTool
from .custom_tools.github_repo_cloner_tool import GitHubRepoClonerTool
from .custom_tools.filtered_directory_reader_tool import FilteredDirectoryReaderTool
from .custom_tools.real_file_path_verifier_tool import RealFilePathVerifierTool
from .custom_tools.list_file_loader_tool import LoadFileListTool
from .custom_tools.read_file_tool import ReadFileTool
from .custom_tools.write_to_file_tool import WriteToFileTool

# Configuração do modelo de linguagem (LLM) que será usado pelos agentes
my_llm = LLM(
    model="lm_studio/google/gemma-3n-e4b",
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

@CrewBase
class CodeDocumentationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, method: str):
        self.method = method  # Pode ser "raw_link" para baixar arquivo ou "clone_repo" para clonar repositório

    # Definição dos agentes - cada um com ferramentas e configuração específicas

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
    def file_lister(self) -> Agent:
        return Agent(
            config=self.agents_config["file_lister"],
            tools=[FilteredDirectoryReaderTool(directory="./requests_repo")],
            llm=my_llm,
            verbose=True,
        )

    #@agent
    #def real_file_verifier(self) -> Agent:
     #   return Agent(
      #      config=self.agents_config["real_file_verifier"],
       #     tools=[RealFilePathVerifierTool()],
        #    llm=my_llm,
         #   verbose=True,
        #)

    @agent
    def file_content_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["file_content_reader"],
            tools=[ReadFileTool()],
            llm=my_llm,
            verbose=True,
        )

    """ 
    Comentado por enquanto para testar o pipeline sem atualização inline de documentação.
    Isso pode ajudar a verificar se o processo geral funciona sem a parte de modificação de código,
    o que é útil para depuração ou para usar apenas análise e geração de documentação externa.
    """
    # @agent
    # def inline_doc_updater(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["inline_doc_updater"],
    #         tools=[WriteToFileTool()],
    #         llm=my_llm,
    #         verbose=True,
    #     )

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

    # Definição das tarefas relacionadas aos agentes acima

    @task
    def download_github_file_task(self) -> Task:
        return Task(config=self.tasks_config["download_github_file_task"])

    @task
    def clone_repo_task(self) -> Task:
        return Task(config=self.tasks_config["clone_repo_task"])

    @task
    def list_files_task(self) -> Task:
        return Task(config=self.tasks_config["list_files_task"])

    #@task
    #def verify_files_exist_task(self) -> Task:
     #   return Task(config=self.tasks_config["verify_files_exist_task"])

    @task
    def read_file_contents_task(self) -> Task:
        return Task(config=self.tasks_config["read_file_contents_task"])

    """
    Também comentado para testar fluxo sem alterar arquivos,
    para ver se a análise e documentação funcionam sozinhas, sem reescrever o código.
    """
    # @task
    # def update_inline_docs_task(self) -> Task:
    #     return Task(config=self.tasks_config["update_inline_docs_task"])

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

    # Define a crew (pipeline de execução) baseado no método escolhido
    @crew
    def crew(self) -> Crew:
        if self.method == "raw_link":
            agents = [
                self.github_file_downloader(),
                self.file_content_reader(),
                # Inline doc updater está comentado aqui também, para testar fluxo sem editar arquivos
                # self.inline_doc_updater(),
                self.code_insight_agent(),
                self.doc_writer(),
                self.markdown_formatter()
            ]
            tasks = [
                self.download_github_file_task(),
                self.read_file_contents_task(),
                # self.update_inline_docs_task(),
                self.extract_insights_task(),
                self.generate_doc_task(),
                self.markdown_format_task()
            ]
        elif self.method == "clone_repo":
            agents = [
                self.repo_cloner(),
                self.file_lister(),
                #self.real_file_verifier(),
                self.file_content_reader(),
                # Inline doc updater ativado aqui está comentado para testes
                # self.inline_doc_updater(),
                self.code_insight_agent(),
                self.doc_writer(),
                self.markdown_formatter()
            ]
            tasks = [
                self.clone_repo_task(),
                self.list_files_task(),
                #self.verify_files_exist_task(),
                self.read_file_contents_task(),
                # self.update_inline_docs_task(),
                self.extract_insights_task(),
                self.generate_doc_task(),
                self.markdown_format_task()
            ]
        else:
            raise ValueError("Método inválido. Use 'raw_link' ou 'clone_repo'.")

        # Retorna o pipeline de execução sequencial com agentes e tarefas configuradas
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
