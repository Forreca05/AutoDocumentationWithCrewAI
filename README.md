# 🧠 AutoDocumentationWithCrewAI

Documentação automática de código utilizando a framework [CrewAI](https://github.com/joaomdmoura/crewAI).

Este projeto organiza **agentes colaborativos** para analisar e documentar código Python de forma autônoma. Ele combina ferramentas de leitura de arquivos, análise semântica e geração de texto, criando uma pipeline de documentação estruturada e escalável.

---

## 🚀 Funcionalidades

* 📄 Leitura de arquivos fonte (ex.: `.py`)
* 🧠 Análise da estrutura e lógica do código
* ✍️ Geração automática de documentação em linguagem natural
* 🤖 Execução encadeada de agentes (Leitor → Analista → Documentador → Formatter)
* 🔄 Integração com GitHub via **webhook** para automação em *push* ou *pull request*
* 🌐 Exposição local com **ngrok** para receber webhooks externamente

---

## 🛠️ Requisitos

* Python **3.11+**
* [CrewAI](https://github.com/joaomdmoura/crewAI)
* Ambiente virtual recomendado (**venv**)
* [ngrok](https://ngrok.com/) para testes locais de webhook (opcional)

---

## 🧠 Modelos de Linguagem

O projeto utiliza modelos locais através do [LM Studio](https://lmstudio.ai/).  
Isso permite processar e gerar documentação **offline**, garantindo:

* Maior controle sobre execução
* Privacidade dos dados
* Independência de API externa (não é necessária API key)

---

## ⚙️ Instalação e uso

### 1. Criar e ativar o ambiente virtual

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/macOS
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o servidor de webhook (Flask)

```bash
py webhook_server.py
```

O servidor ficará disponível em `http://localhost:5000/webhook`.

### 4. Expor localmente com ngrok

```bash
ngrok http 5000
```

* Copie a URL pública (ex.: `https://abcd1234.ngrok.io`)  
* Configure-a como **Webhook** no GitHub (`https://abcd1234.ngrok.io/webhook`)

### 5. Configurar Webhook no GitHub

1. Vá em **Settings → Webhooks** no repositório  
2. Clique em **Add webhook**  
3. Cole a URL do ngrok com `/webhook`  
4. Escolha `application/json`  
5. Selecione os eventos desejados (ex.: *push*)  
6. Salve

### 6. O que acontece quando o webhook dispara?

* GitHub envia um POST → servidor Flask  
* O servidor extrai o repositório e dispara `main.py` em *background*  
* A pipeline roda: leitura de código → análise → documentação → formatação

### 7. Execução manual (sem webhook)

```bash
py main.py
```

Modos suportados:

1. **Arquivo único (raw link GitHub)**  
   * Informe a URL *raw* de um arquivo  
   * O sistema gera documentação técnica para esse arquivo

2. **Repositório completo (clone)**  
   * Informe a URL do repositório, ex.: `https://github.com/usuario/repositorio`  
   * Escolha a *branch*  
   * O sistema clona, processa os arquivos e gera documentação do projeto completo

---

## 📁 Estrutura do Projeto

* `main.py` — Script principal de documentação  
* `webhook_server.py` — Servidor Flask para integração com GitHub  
* `src/crew.py` — Inicializa e orquestra os agentes do CrewAI  
* `src/custom_tools/` — Ferramentas customizadas (clonagem, download, parsing)  
* `src/config/` — Arquivos YAML com configs de agentes e tarefas  

---

## ❗ Limitações conhecidas

Como o projeto depende de modelos locais via LM Studio, o desempenho varia conforme hardware e contexto. Algumas limitações:

* 🔁 **Instabilidade** — pipeline pode alternar entre execuções corretas e falhas  
* 📄 **Documentação incorreta ou inventada** — outputs para arquivos inexistentes ou ignorando ferramentas  
* 🧠 **Alucinações** — aumentam com complexidade e limite de tokens  
* ❌ **Ignorar instruções de tools** — por ex., não seguir listas de arquivos fornecidas  
* ✍️ **Documentação inline inconsistente** — dificuldade em gerar docstrings confiáveis  
* 💥 **Crashes em modelos grandes** — consumo elevado de memória/contexto  
* ⏳ **Tempo de execução elevado** — especialmente durante a execução da DocumentationCrew  
* 📂 **Limitação de leitura de arquivos** — FileReadTool lê um arquivo por vez e requer caminho exato; para contornar, os arquivos eram concatenados num único arquivo identificado. Funciona para repositórios pequenos, mas grandes podem falhar ou consumir muita memória

---

## 🔮 Possíveis Implementações Futuras

1️⃣ **Suporte a repositórios maiores**  
* Processamento em chunks de arquivos ou pacotes de diretórios  
* Uso de arquivo índice para iterar sobre caminhos e ler arquivos separadamente  
* MultiFileReadTool para leitura estruturada de múltiplos arquivos

2️⃣ **Modelos mais avançados**  
* Integração com modelos maiores ou mais recentes  
* Resumos intermediários para gerenciar limites de tokens em repositórios extensos

3️⃣ **Documentação inline e completa**  
* Geração de docstrings faltantes  
* Atualização de docstrings existentes para refletir alterações do código

4️⃣ **Maior autonomia dos agentes**  
* Agentes menos dependentes de tools específicas  
* Encadeamento dinâmico com feedback entre agentes para corrigir inconsistências

5️⃣ **Processamento incremental e resumido**  
* Processar arquivos em etapas  
* Combinar resumos intermediários para reduzir consumo de memória e melhorar robustez

---

## 📌 Nota

Este trabalho foi desenvolvido no âmbito do **Estágio de Verão — Summer Opportunities 2025**, realizado na **Consulteer** durante os meses de **julho e agosto**.  

Além do código, este repositório inclui também um arquivo PDF com a minha **review detalhada da ferramenta utilizada** (CrewAI).