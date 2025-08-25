# 🧠 AutoDocumentationWithCrewAI

Automatic code documentation using the [CrewAI](https://github.com/joaomdmoura/crewAI) framework.

This project organizes **collaborative agents** to autonomously analyze and document Python code. It combines tools for file reading, semantic analysis, and text generation, creating a structured and scalable documentation pipeline.

---

## 🚀 Features

* 📄 Reads source files (e.g., `.py`)
* 🧠 Analyzes code structure and logic
* ✍️ Automatically generates natural language documentation
* 🤖 Chained execution of agents (Reader → Analyst → Documenter → Formatter)
* 🔄 GitHub integration via **webhook** for automation on *push* or *pull request*
* 🌐 Local exposure with **ngrok** to receive external webhooks

---

## 🛠️ Requirements

* Python **3.11+**
* [CrewAI](https://github.com/joaomdmoura/crewAI)
* Virtual environment recommended (**venv**)
* [ngrok](https://ngrok.com/) for local webhook testing (optional)

---

## 🧠 Language Models

The project uses local models through [LM Studio](https://lmstudio.ai/).  
This allows processing and documentation generation **offline**, ensuring:

* Greater execution control
* Data privacy
* Independence from external APIs (no API key required)

---

## ⚙️ Installation and Usage

### 1. Create and activate the virtual environment

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/macOS
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the webhook server (Flask)

```bash
py webhook_server.py
```

The server will be available at `http://localhost:5000/webhook`.

### 4. Expose locally with ngrok

```bash
ngrok http 5000
```

* Copy the public URL (e.g., `https://abcd1234.ngrok.io`)  
* Configure it as **Webhook** in GitHub (`https://abcd1234.ngrok.io/webhook`)

### 5. Configure Webhook in GitHub

1. Go to **Settings → Webhooks** in the repository  
2. Click **Add webhook**  
3. Paste the ngrok URL with `/webhook`  
4. Choose `application/json`  
5. Select desired events (e.g., *push*)  
6. Save

### 6. What happens when the webhook is triggered?

* GitHub sends a POST → Flask server  
* The server extracts the repository and triggers `main.py` in the background  
* The pipeline runs: code reading → analysis → documentation → formatting

### 7. Manual execution (without webhook)

```bash
py main.py
```

Supported modes:

1. **Single file (raw GitHub link)**  
   * Provide the *raw* URL of a file  
   * The system generates technical documentation for that file

2. **Complete repository (clone)**  
   * Provide the repository URL, e.g., `https://github.com/user/repository`  
   * Choose the branch  
   * The system clones, processes files, and generates documentation for the entire project

---

## 📁 Project Structure

* `main.py` — Main documentation script  
* `webhook_server.py` — Flask server for GitHub integration  
* `src/crew.py` — Initializes and orchestrates CrewAI agents  
* `src/custom_tools/` — Custom tools (cloning, downloading, parsing)  
* `src/config/` — YAML configuration files for agents and tasks  

---

## ❗ Known Limitations

Since the project depends on local models via LM Studio, performance varies according to hardware and context. Some limitations include:

* 🔁 **Instability** — pipeline may alternate between correct runs and failures  
* 📄 **Incorrect or fabricated documentation** — outputs for non-existent files or ignoring tools  
* 🧠 **Hallucinations** — increase with complexity and token limits  
* ❌ **Ignoring tool instructions** — e.g., not following provided file lists  
* ✍️ **Inconsistent inline documentation** — difficulty generating reliable docstrings  
* 💥 **Crashes with large models** — high memory/context consumption  
* ⏳ **Long execution time** — especially during DocumentationCrew execution  
* 📂 **File reading limitation** — FileReadTool reads one file at a time and requires exact path; workaround was concatenating files into a single file. Works for small repos, but large ones may fail or consume too much memory

---

## 🔮 Possible Future Implementations

1️⃣ **Support for larger repositories**  
* Processing in chunks of files or directory packages  
* Use of index file to iterate over paths and read files separately  
* MultiFileReadTool for structured multi-file reading

2️⃣ **More advanced models**  
* Integration with larger or more recent models  
* Intermediate summaries to handle token limits in large repositories

3️⃣ **Inline and complete documentation**  
* Generation of missing docstrings  
* Updating existing docstrings to reflect code changes

4️⃣ **Greater agent autonomy**  
* Less dependence on specific tools  
* Dynamic chaining with feedback between agents to fix inconsistencies

5️⃣ **Incremental and summarized processing**  
* Process files in stages  
* Combine intermediate summaries to reduce memory usage and improve robustness

---

## 🔑 Experience with OpenAI API

At the end of the internship, I was able to integrate the project with the **OpenAI API**, using a personal key.  
The difference between running the system only with local models (LM Studio) and with the API was **huge**:

* 🚀 **Speed** — while local models took minutes (sometimes froze or failed), the OpenAI version executed in about **30 seconds**.  
* 📄 **Documentation quality** — outputs no longer had errors, omissions, or hallucinations; the generated document was **coherent and faithful to the code**.  
* 🔁 **Reliability** — each execution produced stable results, unlike the typical inconsistency of the local environment.  

This change made it clear that using an external API like OpenAI’s was not just an incremental improvement:  
it was a **leap in quality and efficiency** that completely transformed the project experience.

---

## 📌 Note

This work was developed within the scope of the **Summer Internship — Summer Opportunities 2025**, carried out at **Consulteer** during the months of **July and August**.  

In addition to the code, this repository also includes a PDF file with my **detailed review of the tool used** (CrewAI).
