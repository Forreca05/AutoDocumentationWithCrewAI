# 🧠 AutoDocumentationWithCrewAI

Documentação automática de código utilizando a framework [CrewAI](https://github.com/joaomdmoura/crewAI).

Este projeto organiza agentes colaborativos para analisar e documentar código Python de forma autônoma, utilizando ferramentas como leitura de arquivos, análise semântica e geração de texto.

---

## 🚀 Funcionalidades

- 📄 Leitura de arquivos fonte (ex: `.py`)
- 🧠 Análise da estrutura do código
- ✍️ Geração automática de documentação
- 🤖 Execução em cadeia de agentes (Leitor → Analista → Documentador)
- 🔄 Integração com GitHub via webhook para automação em push ou pull request
- 🌐 Exposição local com ngrok para receber webhooks externamente

---

## 🛠️ Requisitos

- Python 3.11+
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- Ambiente virtual recomendado (venv)
- [ngrok](https://ngrok.com/) para expor localmente a API de webhook (opcional, para testes locais)

---

## 🧠 Modelos de Linguagem

Este projeto utiliza um modelo de linguagem local através do [LM Studio](https://lmstudio.ai/). Isso permite processamento e geração de texto de forma offline, garantindo maior controle e privacidade durante a análise e documentação automática do código e evita a necessidade de ter uma API key.

---

## ⚙️ Instalação e uso

### 1. Crie e ative o ambiente virtual:

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\activate  # Para Windows
# ou
source .venv/bin/activate  # Para Linux/macOS
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação de webhook (Flask)

Este servidor escuta eventos do GitHub para iniciar a geração automática da documentação quando um push ocorre.

```bash
py webhook_server.py
```

O servidor vai rodar localmente na porta 5000 (http://localhost:5000/webhook).

### 4. Exponha localmente com ngrok (para receber webhooks do GitHub)

Se quiser testar localmente, você pode usar o ngrok para criar um túnel HTTP:

```bash
ngrok http 5000
```

- Copie a URL pública gerada pelo ngrok, algo como https://abcd1234.ngrok.io

- Configure essa URL como webhook no repositório GitHub, adicionando /webhook no final (ex: https://abcd1234.ngrok.io/webhook)

### 5. Configure o webhook no GitHub

- Vá em **Settings** → **Webhooks** no seu repositório GitHub
- Clique em **Add webhook**
- Cole a URL do ngrok com `/webhook`
- Escolha o conteúdo do tipo `application/json`
- Selecione os eventos que quer ouvir, por exemplo, **push**
- Salve o webhook

### 6. O que acontece quando o webhook é acionado?

Quando um push é detectado, o webhook envia uma requisição POST para seu servidor Flask. Ele:

- Extrai a URL do repositório do payload
- Inicia em background a geração automática da documentação chamando `main.py` com parâmetros
- Retorna uma resposta de confirmação

### Como rodar o projeto manualmente

Se quiser rodar sem webhook, pode executar diretamente o script principal:

```bash
py main.py
```

Ao usar essa opção, você poderá escolher entre **duas formas de execução**:

1. **Usar o link *raw* de um arquivo no GitHub**  
   Basta fornecer a URL direta (*raw*) de um arquivo hospedado no GitHub.  
   O sistema irá processar o conteúdo desse arquivo e gerar a documentação técnica para ele.

2. **Clonar um repositório completo**  
   Basta passar o link principal do repositório no GitHub, por exemplo:  
   `https://github.com/usuario/repositorio`  
   Em seguida, indicar a *branch* que deseja utilizar.  
   O sistema irá clonar essa branch, processar todos os arquivos e gerar a documentação técnica do projeto completo.

## 📁 Estrutura do projeto

- `main.py` — Script principal para geração da documentação.
- `webhook_server.py` — Servidor Flask para receber eventos do GitHub.
- `src/custom_tools/` — Ferramentas personalizadas para clonagem, download e leitura de código.
- `src/config/` — Arquivos YAML com configurações dos agentes e tarefas.


 ## ❗ Limitações conhecidas

Como este projeto utiliza um modelo de linguagem local via LM Studio, o que implica depender muito do hardware da máquina,algumas limitações foram observadas durante o uso:

- 🔁 **Comportamento instável:** Às vezes os agentes funcionam corretamente, outras vezes não. Há bastante oscilação na performance.

- 📄 **Documentação incorreta ou inventada:** O modelo pode gerar documentação para ficheiros que não existem ou ignorar o output real das tools, acrescentando itens fictícios.

- 🧠 **Alucinações frequentes:** Devido à complexidade lógica e ao número de agentes, o modelo tende a alucinar com frequência, especialmente quando o número de tokens fica próximo do limite.

- ❌ **Não segue corretamente as instruções das tools:** Por exemplo, mesmo quando um ficheiro `.txt` indica quais ficheiros devem ser documentados, o modelo ignora e inventa outros.

- ✍️ **Falta de documentação inline:** Mesmo com tentativas de forçar documentação inline nos métodos/funções, os resultados são inconsistentes ou inexistentes.

- 💥 **Crashes inesperados:** Modelos maiores tendem a gerar mais falhas de execução locais, principalmente por gestão de memória ou limite de contexto.

 
 
