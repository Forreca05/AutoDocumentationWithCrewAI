from flask import Flask, request, jsonify
import threading
import subprocess
import sys  # <-- IMPORTANTE para capturar o Python ativo

app = Flask(__name__)

def run_doc_generation_with_args(method, url):
    # Usa o mesmo interpretador Python que está rodando este script
    subprocess.Popen([sys.executable, "main.py", method, url])

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        repo_url = data['repository']['clone_url']
        print(f"Recebido push para repositório: {repo_url}")
    except Exception as e:
        print(f"Erro ao extrair URL do payload: {e}")
        return jsonify({'status': 'error', 'message': 'Payload inválido'}), 400

    # Inicia a geração de documentação em background com o repo_url
    threading.Thread(target=run_doc_generation_with_args, args=("raw_link", "https://raw.githubusercontent.com/Forreca05/Autonomous-Documentation/refs/heads/main/task_manager.py")).start()

    return jsonify({'status': 'success', 'message': 'Geração de documentação iniciada'}), 200

if __name__ == "__main__":
    app.run(port=5000)
