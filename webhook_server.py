from flask import Flask, request, jsonify
import threading
import subprocess
import sys

app = Flask(__name__)

def run_doc_generation_with_args(method, url, branch=None):
    args = [sys.executable, "main.py", method, url]
    if branch:
        args.append(branch)
    subprocess.Popen(args)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')

    try:
        if event == "push":
            repo_url = data['repository']['clone_url']
            ref = data.get('ref', '')
            branch = ref.split('/')[-1] if ref else 'main'
            print(f"📥 Push recebido: {repo_url} @ {branch}")
            threading.Thread(target=run_doc_generation_with_args, args=("clone_repo", repo_url, branch)).start()

        elif event == "pull_request":
            action = data.get('action')
            if action == "closed":
                print("Pull Request fechada — nenhuma ação será tomada.")
                return "✅ Pull request fechada — ignorado", 200

            # Para outras ações como "opened", "synchronize", "reopened" etc:
            repo_url = data['pull_request']['head']['repo']['clone_url']
            branch = data['pull_request']['head']['ref']
            print(f"📥 Pull Request recebido: {repo_url} @ {branch}")
            threading.Thread(target=run_doc_generation_with_args, args=("clone_repo", repo_url, branch)).start()

        else:
            return jsonify({'status': 'ignored', 'message': 'Evento não suportado'}), 200

        return jsonify({'status': 'success', 'message': 'Documentação iniciada'}), 200

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)
