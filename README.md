
# MCP4All

## Projektbeschreibung

Dieses Projekt demonstriert einen MCP-Server (Model Context Protocol) in Node.js. Ziel ist es, GitHub-Projekte automatisiert als Blog-Posts zu dokumentieren.

## Installation

1. Node.js installieren (falls nicht vorhanden)
2. Abhängigkeiten installieren:
	 ```bash
	 npm install
	 ```

## Beispielcode

Der MCP-Server ist in `server.js` implementiert:

```javascript
const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
	const { repo, token, blog_path = './blog_content' } = req.body;
	if (!repo || !token) {
		return res.status(400).json({ error: 'repo und token sind erforderlich.' });
	}
	try {
		const url = `https://api.github.com/repos/${repo}/readme`;
		const response = await axios.get(url, {
			headers: {
				Authorization: `token ${token}`,
				'User-Agent': 'MCP-Server-Node'
			}
		});
		const content = Buffer.from(response.data.content, 'base64').toString('utf-8');
		fs.mkdirSync(blog_path, { recursive: true });
		const filename = path.join(blog_path, `${repo.replace('/', '_')}.md`);
		fs.writeFileSync(filename, content, 'utf-8');
		res.json({ success: true, file: filename });
	} catch (err) {
		res.status(500).json({ error: err.message });
	}
});

app.get('/', (req, res) => {
	res.send('MCP4All Node.js Server läuft!');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
	console.log(`Server läuft auf Port ${PORT}`);
});
```

## Nutzung

Starte den Server:
```bash
npm start
```

Sende eine Anfrage (z. B. mit `curl`):
```bash
curl -X POST http://localhost:5000/mcp \
	-H "Content-Type: application/json" \
	-d '{"repo":"username/repo","token":"<dein_github_token>"}'
```

Antwort:
```json
{"success": true, "file": "blog_content/username_repo.md"}
```

## Lizenz
Siehe LICENSE.

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
