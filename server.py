from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    data = request.json
    # Beispiel: Eingabe verarbeiten und Antwort generieren
    user_input = data.get('input', '')
    response = f"Du hast gefragt: {user_input}. MCP antwortet: Hallo Welt!"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
