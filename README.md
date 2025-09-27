# MCP4All

## Projektbeschreibung

Dieses Projekt demonstriert einen einfachen MCP-Server (Model Context Protocol) in Python. Ziel ist es, die Funktionsweise von MCP zu verstehen und erste Automatisierungen zu realisieren.

## Installation

1. Python 3 installieren (falls nicht vorhanden)
2. Benötigte Pakete installieren:
   ```bash
   pip install flask
   ```

## Beispielcode

Der MCP-Server ist in `server.py` implementiert:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
	data = request.json
	user_input = data.get('input', '')
	response = f"Du hast gefragt: {user_input}. MCP antwortet: Hallo Welt!"
	return jsonify({'response': response})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
```

## Nutzung

Starte den Server:
```bash
python server.py
```

Sende eine Anfrage (z. B. mit `curl`):
```bash
curl -X POST http://localhost:5000/mcp -H "Content-Type: application/json" -d '{"input": "Was ist MCP?"}'
```

Antwort:
```json
{"response": "Du hast gefragt: Was ist MCP?. MCP antwortet: Hallo Welt!"}
```

## Lizenz
Siehe LICENSE.
Test
