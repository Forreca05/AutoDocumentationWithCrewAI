# Gerenciador de Tarefas

## Visão Geral
Este documento descreve a estrutura e o funcionamento do gerenciador de tarefas. Ele detalha as classes `Task` e `TaskManager`, seus atributos, métodos e como eles interagem para gerenciar uma lista de tarefas.

## Classe Task
A classe `Task` representa uma única tarefa.

### Atributos
- `id` (str): Identificador único da tarefa (gerado usando UUID).
- `title` (str): O título da tarefa.
- `priority` (str): A prioridade da tarefa (baixa, média, alta).
- `completed` (bool): Indica se a tarefa foi concluída.
- `created_at` (datetime): Data e hora de criação da tarefa.
- `completed_at` (Optional[datetime]): Data e hora de conclusão da tarefa (se aplicável).

### Métodos
- `__init__(self, title: str, priority: str = "mÃ©dia")`: Inicializa uma nova instância da classe Task.
- `mark_complete(self)`: Marca a tarefa como concluída.
- `__repr__(self)`: Retorna uma representação string da tarefa.

## Classe TaskManager
A classe `TaskManager` gerencia uma lista de tarefas.

### Atributos
- `VALID_PRIORITIES` (List[str]): Uma lista de prioridades válidas ("baixa", "média", "alta").
- `tasks` (List[Task]): Uma lista de objetos Task.

### Métodos
- `__init__(self)`: Inicializa uma nova instância da classe TaskManager com uma lista vazia de tarefas.
- `add_task(self, title: str, priority: str = "mÃ©dia")`: Adiciona uma nova tarefa à lista.
- `get_pending_tasks(self, sorted_by_priority: bool = True)`: Retorna uma lista de tarefas pendentes (não concluídas), que pode ser ordenada por prioridade.
- `complete_task(self, task_id: str)`: Marca uma tarefa como concluída pelo seu ID.
- `get_completed_tasks(self)`: Retorna uma lista de tarefas concluídas.
- `list_all_tasks(self)`: Retorna uma lista de todas as tarefas.
- `__repr__(self)`: Retorna uma representação string da classe TaskManager.

## Exemplo de Uso
O bloco `if __name__ == "__main__":` demonstra como usar a classe `TaskManager`. Ele cria um gerenciador de tarefas, adiciona algumas tarefas, imprime as tarefas pendentes, as tarefas concluídas e todas as tarefas.

## Formatação Markdown
A documentação foi formatada usando Markdown para facilitar a leitura e a publicação em repositórios, wikis ou sites. Os cabeçalhos, listas e blocos de código foram utilizados para organizar o conteúdo de forma clara e concisa.
