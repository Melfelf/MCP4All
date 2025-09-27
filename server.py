
from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    data = request.json
    action = data.get('action')
    if action == 'import_github_readme':
        repo = data.get('repo')
        token = data.get('token')
        blog_path = data.get('blog_path', './blog_content')
        result = import_github_readme(repo, token, blog_path)
        return jsonify(result)
    # Standardantwort
    user_input = data.get('input', '')
    response = f"Du hast gefragt: {user_input}. MCP antwortet: Hallo Welt!"
    return jsonify({'response': response})

def import_github_readme(repo, token, blog_path):
    url = f"https://api.github.com/repos/{repo}/readme"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "MCP-Server"
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return {"error": f"GitHub API Fehler: {r.status_code}"}
    content = r.json().get('content', '')
    readme_md = base64.b64decode(content).decode('utf-8')
    os.makedirs(blog_path, exist_ok=True)
    filename = os.path.join(blog_path, f"{repo.replace('/', '_')}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(readme_md)
    return {"success": True, "file": filename}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
