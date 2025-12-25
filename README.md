
# MCP4All

Comprehensive example implementations of a Model Context Protocol (MCP) server that transform GitHub repository READMEs into local blog content. The repository ships two lightweight HTTP servers:

- **Node.js (Express) implementation** in `server.js`
- **Python (Flask) implementation** in `server.py`

Both variants expose a `/mcp` endpoint that can be driven by an MCP client (or any HTTP client) to pull a GitHub README, decode it, and write it to a local `blog_content` folder as Markdown.

---

## Table of contents
- [Features](#features)
- [Repository layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the servers](#running-the-servers)
  - [Node.js server](#nodejs-server)
  - [Python server](#python-server)
- [API](#api)
  - [POST /mcp (Node.js)](#post-mcp-nodejs)
  - [POST /mcp (Python)](#post-mcp-python)
- [Examples](#examples)
- [Development notes](#development-notes)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features
- Fetches the README of any public or private GitHub repository via the GitHub REST API.
- Saves the decoded README as a Markdown file into a configurable `blog_content` directory.
- Small, dependency-light servers that can be run with Node.js or Python.
- Simple HTTP contract that can be wired into MCP-aware clients or scripts.

## Repository layout
- `server.js` — Express server that fetches GitHub READMEs and writes them locally.
- `server.py` — Flask server with similar functionality plus a simple echo response for generic MCP testing.
- `blog_content/` — Output directory for generated Markdown files (created automatically).
- `package.json` / `package-lock.json` — Node.js dependencies and scripts.
- `ChatGPT.md` — Background conversation that inspired the project (not required for runtime).
- `LICENSE` — Project license.

## Prerequisites
- **GitHub Personal Access Token (PAT)** with at least `repo` scope to read private repository READMEs.
- **Node.js 18+** (for `server.js`) and **npm**.
- **Python 3.9+** with `pip` (for `server.py`).
- Outbound HTTPS access to `api.github.com`.

## Setup

### Node.js dependencies
```bash
npm install
```

### Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install flask requests
```

> You can run either server independently; installing both stacks is optional.

## Running the servers

### Node.js server
```bash
npm start
# or manually
node server.js
```

Environment:
- `PORT` (optional): HTTP port (default `5000`).

### Python server
```bash
python server.py
```

Environment:
- `PORT` (optional): HTTP port (default `5000`).
- Bind address defaults to `0.0.0.0`.

## API

### POST /mcp (Node.js)
Fetches a README and stores it as Markdown.

**Request body**
```json
{
  "repo": "owner/repo",
  "token": "<github_pat>",
  "blog_path": "./blog_content"  // optional
}
```

**Behavior**
- Calls `https://api.github.com/repos/<repo>/readme` with the provided token.
- Decodes the base64 README content.
- Writes `<owner>_<repo>.md` inside `blog_path` (folder created if missing).
- Responds with `{ "success": true, "file": "<path>" }` on success or an error payload on failure.

### POST /mcp (Python)
Supports two modes:
1. `action: "import_github_readme"` — mirrors the Node.js behavior.
2. Without `action` — simple echo helper to test connectivity.

**Request body (import)**
```json
{
  "action": "import_github_readme",
  "repo": "owner/repo",
  "token": "<github_pat>",
  "blog_path": "./blog_content"  // optional
}
```

**Request body (echo)**
```json
{
  "input": "Was ist MCP?"
}
```

**Responses**
- Import: `{ "success": true, "file": "<path>" }` or `{ "error": "<message>" }`.
- Echo: `{ "response": "Du hast gefragt: <input>. MCP antwortet: Hallo Welt!" }`.

## Examples

### Create a blog-ready README (Node.js server)
```bash
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -d '{"repo":"username/repo","token":"<github_pat>"}'
```
Response:
```json
{"success": true, "file": "blog_content/username_repo.md"}
```

### Import via Python server
```bash
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -d '{"action":"import_github_readme","repo":"username/repo","token":"<github_pat>"}'
```

### Echo test (Python server)
```bash
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -d '{"input":"Was ist MCP?"}'
```
Response:
```json
{"response": "Du hast gefragt: Was ist MCP?. MCP antwortet: Hallo Welt!"}
```

## Development notes
- The output path defaults to `./blog_content`; override with `blog_path` in the payload.
- Filenames replace `/` in the repo name with `_` (e.g., `owner_repo.md`).
- Node.js implementation sets the GitHub `User-Agent` header to `MCP-Server-Node`; Python uses `MCP-Server`.
- Extend either server to render richer blog posts by transforming the README content before saving.

## Troubleshooting
- **401/403 errors from GitHub**: confirm the PAT is valid and includes `repo` scope for private repos.
- **File permission issues**: ensure the process can create and write to `blog_path`.
- **Port conflicts**: set `PORT` to a free port or stop other services using the default port.

## License
See [LICENSE](LICENSE).
