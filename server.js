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
