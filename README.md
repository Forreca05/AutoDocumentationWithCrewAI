# 🧠 AutoDocumentationWithCrewAI

Documentação automática de código utilizando a framework [CrewAI](https://github.com/joaomdmoura/crewAI).

Este projeto organiza agentes colaborativos para analisar e documentar código Python de forma autônoma, utilizando ferramentas como leitura de arquivos, análise semântica e geração de texto.

---

## 🚀 Funcionalidades

- 📄 Leitura de arquivos fonte (ex: `.py`)
- 🧠 Análise da estrutura do código
- ✍️ Geração automática de documentação
- 🤖 Execução em cadeia de agentes (Leitor → Analista → Documentador)

---

## 🛠️ Requisitos

- Python 3.11+
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- Ambiente virtual recomendado (venv)

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

### 3. Execute o projeto

```bash
py main.py
```

