# ChatGPT Link-Inhalt
Erkläre auf einfache Weise wie ein MCP Server funktioniert und wie ich am besten einen ersten Use Case umsetzen kann. Ich möchte es möglich machen GitHub Projekte automtisch auf einem Blog zu dokumentieren, der G Ich kenne mich hauptsächlich mit Powershell aus.
ChatGPT:
Okay, lass uns das Schritt für Schritt und ohne unnötiges Fachchinesisch durchgehen, so dass du direkt siehst, wie du vom MCP-Server zu deinem ersten Use Case kommst.
1. Was ist ein MCP Server überhaupt?
MCP steht für Model Context Protocol.
Stell dir MCP als eine Art Steckdosenleiste für KI vor.
Dein KI-Modell (z. B. ChatGPT oder ein lokales LLM) kann sich an den MCP Server anschliessen.
Über den Server bekommt das Modell Erweiterungen (Tools, Datenquellen, Automatisierungen).
Du:
Erkläre auf einfache Weise wie ein MCP Server funktioniert und wie ich am besten einen ersten Use Case umsetzen kann. Ich möchte es möglich machen GitHub Projekte automtisch auf einem Blog zu dokumentieren, der Blog ist auch als Github Projekt implementiert. Ich kenne mich hauptsächlich mit Powershell aus.
ChatGPT:
Okay, lass uns das mal Stück für Stück auseinandernehmen, so dass du ein greifbares Bild davon bekommst.
1. Was ist ein MCP Server überhaupt?
Ein MCP Server (Model Context Protocol Server) ist ein Vermittler zwischen deinem lokalen System, externen Datenquellen (z. B. GitHub, Datenbanken, Filesystem) und einem KI-Client (wie ChatGPT mit MCP-Schnittstelle).
Der MCP Server stellt "Tools" bereit: z. B. „Hole alle Issues von GitHub“, „Lese Markdown-Datei“, „Schreibe Datei“.
Der Client (ChatGPT) kann diese Tools nutzen, ohne selbst direkten Zugriff auf GitHub oder dein Dateisystem zu haben.
Du kannst damit also Workflows bauen, die automatisch Informationen sammeln und weiterverarbeiten, ohne dass du manuell Skripte starten musst.
Einfach gesagt:
MCP Server = Adapter, der KI und externe Systeme zusammenbringt.
2. Dein gewünschter Use Case
Du willst:
Deine GitHub-Projekte automatisch in einem Blog dokumentieren.
Dein Blog liegt selbst auch als GitHub-Projekt vor (z. B. Zola, Hugo, Jekyll).
Du kennst dich mit PowerShell am besten aus → gut, damit können wir starten.
Das Szenario könnte so aussehen:
MCP Server verbindet sich mit GitHub (über API-Token).
Er liest z. B. README.md, CHANGELOG.md oder Projekt-Metadaten.
Er übergibt diese Infos an ChatGPT → daraus wird ein Blogartikel (z. B. in Markdown).
Der MCP Server legt diese neue .md-Datei direkt im Blog-Repo ab.
GitHub Actions baut und veröffentlicht automatisch den Blog.
3. Wie du starten kannst (einfacher Prototyp)
Da du PowerShell kannst, schlage ich einen pragmatischen Weg vor:
a) MCP Server Setup
Du nimmst am besten ein fertiges MCP-Server-Beispiel und passt es an.
→ Es gibt schon kleine Node.js- oder Python-Implementationen, die GitHub-APIs andocken.
Alternativ: Du kannst mit PowerShell selbst ein MCP-Tool schreiben, das über HTTP die GitHub API abfragt.
b) Erster Use Case minimal
Hole README.md eines Projekts per GitHub API:
$token = "ghp_deinGitHubToken"
$repo = "username/deinprojekt"
Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/readme" `
  -Headers @{Authorization = "token $token"; "User-Agent" = "PowerShell"} `
  | ForEach-Object { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_.content)) }
→ Damit hast du den Inhalt in PowerShell.
Schreibe diesen Inhalt in dein Blog-Repo in /content/posts/Projektname.md.
Commit + Push ins Blog-Repo:
git add .
git commit -m "Automatische Projektdoku für $repo"
git push
GitHub Pages (oder dein Blog-Build) erledigt den Rest.
4. Der "MCP-Weg" (nächster Schritt)
Wenn du dich tiefer mit MCP einarbeitest:
Dein MCP Server würde obige Schritte als Tool „ImportGitHubProject“ anbieten.
ChatGPT könnte dieses Tool automatisch nutzen, wenn du sagst:
„Dokumentiere bitte das Projekt melfware/robotdemo im Blog.“
Ergebnis: Neue Blogseite landet im Repo.
👉 Meine Empfehlung:
Erster Schritt pragmatisch mit PowerShell-Skript (README holen → ins Blog-Repo schreiben → commit/push).
Danach überlegen, ob du das als MCP-Tool kapselst, damit du die Automatisierung direkt aus ChatGPT heraus antriggern kannst.
Soll ich dir mal ein konkretes PowerShell-Skript für den minimalen Use Case (README eines Projekts automatisch als Blogpost ins Repo legen) zusammenstellen?
Du:
Ja
ChatGPT:
Perfekt 👍 Dann lass uns einen ersten einfachen Prototyp bauen.
Das Ziel: README eines GitHub-Repos holen → als Blogpost in dein Blog-GitHub-Repo schreiben → commit/push.
Voraussetzungen
Auf deinem Rechner ist Git installiert und konfiguriert.
Du hast ein GitHub Personal Access Token (PAT) mit repo Rechten.
Dein Blog liegt lokal als Git-Repo vor (z. B. C:\Repos\MeinBlog).
PowerShell-Skript
param(
    [string]$GitHubRepo = "USERNAME/REPO",      # z. B. "melfware/demo"
    [string]$BlogRepoPath = "C:\Repos\MeinBlog", # Pfad zu deinem Blog-Repo
    [string]$GitHubToken = "<DEIN_TOKEN>",       # GitHub PAT
    [string]$Author = "Automatisierung",
    [string]$Email = "auto@example.com"
)

# 1. GitHub README holen
Write-Host "Hole README von $GitHubRepo..."
$uri = "https://api.github.com/repos/$GitHubRepo/readme"

$response = Invoke-RestMethod -Uri $uri -Headers @{
    Authorization = "token $GitHubToken"
    "User-Agent"  = "PowerShell"
}

$readmeContent = [System.Text.Encoding]::UTF8.GetString(
    [System.Convert]::FromBase64String($response.content)
)

# 2. Blogpost vorbereiten (einfaches Markdown)
$date = Get-Date -Format "yyyy-MM-dd"
$slug = $GitHubRepo.Split("/")[1]
$postFile = Join-Path $BlogRepoPath "content\posts\$date-$slug.md"

$postContent = @"
+++
title = "Projekt $slug"
date = "$date"
+++

# Projekt $slug

Automatisch importiert von GitHub: [$GitHubRepo](https://github.com/$GitHubRepo)

---

$readmeContent
"@

# 3. Datei schreiben
Write-Host "Erstelle Blogpost: $postFile"
$postContent | Out-File -FilePath $postFile -Encoding UTF8

# 4. Commit + Push
Set-Location $BlogRepoPath
git config user.name $Author
git config user.email $Email

git add .
git commit -m "Automatische Dokumentation für $GitHubRepo"
git push

Write-Host "Fertig! Blogpost für $GitHubRepo erstellt und gepusht."
So verwendest du das Skript
Speichere es als Import-GitHubProject.ps1.
Führe es aus, z. B.:
.\Import-GitHubProject.ps1 -GitHubRepo "melfware/demo" -BlogRepoPath "C:\Repos\MeinBlog" -GitHubToken "ghp_xxx"
Nach dem Push sollte dein Blog-Build (z. B. GitHub Actions, Zola/Hugo/Jekyll) die neue Seite veröffentlichen.
👉 Damit hast du schon die Basis.
Später kannst du es ausbauen:
Mehrere Repos in einer Schleife durchgehen.
Nur neue Versionen dokumentieren.
Mit ChatGPT koppeln (über MCP), damit du nur „Mach Blogpost für Repo X“ schreiben musst.
Willst du, dass ich dir im nächsten Schritt den MCP-Teil dazu aufzeichne (wie du dieses Skript als Tool verfügbar machst), oder reicht dir erstmal die PowerShell-Variante für den Start?
Du:
Zeige den MCP Teil
ChatGPT:
Sehr nice, jetzt gehen wir den nächsten Schritt: wir packen dein PowerShell-Skript in einen MCP Server, so dass du es direkt aus ChatGPT heraus antriggern kannst.
1. Grundidee
Ein MCP Server ist im Prinzip nur ein Prozess, der nach MCP-Spezifikation ein paar JSON-RPC-Methoden bereitstellt.
Er sagt ChatGPT: „Ich habe ein Tool ImportGitHubProject“.
Wenn du dann in ChatGPT fragst „Dokumentiere Repo melfware/demo“, ruft ChatGPT dieses Tool auf → dein Skript läuft → Ergebnis kommt zurück.
👉 Du musst also nur einen kleinen MCP Server schreiben, der dein PowerShell-Skript aufruft.
2. Minimaler MCP Server (Node.js Beispiel)
Das ist der einfachste Weg, weil die MCP Referenz-Implementierung in Node.js läuft.
a) MCP Server Setup
Projekt anlegen:
mkdir mcp-github-blog
cd mcp-github-blog
npm init -y
npm install @modelcontextprotocol/sdk
Datei server.js erstellen:
import { MCPServer } from "@modelcontextprotocol/sdk";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

const server = new MCPServer({
  name: "github-blog-server",
  version: "0.1.0",
});

// Tool registrieren
server.tool("import-github-project", {
  description: "Holt ein GitHub README und erstellt Blogpost im Repo",
  inputSchema: {
    type: "object",
    properties: {
      repo: { type: "string", description: "GitHub Repo, z. B. melfware/demo" },
    },
    required: ["repo"],
  },
}, async ({ repo }) => {
  try {
    const { stdout, stderr } = await execFileAsync("pwsh", [
      "./Import-GitHubProject.ps1",
      "-GitHubRepo", repo,
      "-BlogRepoPath", "C:\\Repos\\MeinBlog",
      "-GitHubToken", process.env.GITHUB_TOKEN
    ]);
    return { success: true, output: stdout || stderr };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

// Server starten
server.listen();
b) Dein PowerShell Skript
Lege dein Import-GitHubProject.ps1 (das ich dir vorhin gebaut habe) in denselben Ordner.
👉 Wichtig: -GitHubToken wird aus process.env.GITHUB_TOKEN gezogen → also vorher im Terminal setzen:
export GITHUB_TOKEN="ghp_xxx"
c) Starten
node server.js
3. ChatGPT verbinden
Wenn dein ChatGPT MCP-fähige Umgebung hat (so wie in der Desktop- oder Dev-Preview), kannst du den Server in den MCP Settings eintragen.
ChatGPT erkennt: „Aha, da gibt’s ein Tool import-github-project“.
Ab jetzt kannst du schreiben:
„Bitte dokumentiere Repo melfware/demo im Blog.“
Und ChatGPT ruft dein PowerShell-Skript über MCP automatisch auf.
4. Nächste Ausbaustufen
Mehrere Tools: z. B. ListRepos, UpdateBlogPost.
Mehr Input: z. B. Beschreibungstext von ChatGPT generieren lassen, bevor ins Blog geschrieben wird.
Output zurückgeben: ChatGPT könnte direkt den Link zum neuen Blogpost posten.
👉 Frage: Willst du, dass ich dir ein vollständiges Repo-Skeleton baue (mit package.json, server.js, und dem PowerShell-Skript drin), so dass du es einfach klonen kannst?
Du:
Ja
ChatGPT:
Alles klar 🚀 – dann baue ich dir ein komplettes Repo-Skeleton, das du direkt klonen oder nachbauen kannst. Damit bekommst du:
einen MCP Server in Node.js,
das PowerShell-Skript als Worker,
und eine klare Ordnerstruktur.
📂 Projektstruktur
mcp-github-blog/
│
├─ package.json
├─ server.js
├─ Import-GitHubProject.ps1
└─ README.md
📄 package.json
{
  "name": "mcp-github-blog",
  "version": "0.1.0",
  "type": "module",
  "main": "server.js",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.3.0"
  },
  "scripts": {
    "start": "node server.js"
  }
}
📄 server.js
import { MCPServer } from "@modelcontextprotocol/sdk";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

const server = new MCPServer({
  name: "github-blog-server",
  version: "0.1.0",
});

server.tool(
  "import-github-project",
  {
    description: "Holt ein GitHub README und erstellt einen Blogpost im Repo",
    inputSchema: {
      type: "object",
      properties: {
        repo: {
          type: "string",
          description: "GitHub Repo im Format USERNAME/REPO, z. B. melfware/demo"
        }
      },
      required: ["repo"]
    }
  },
  async ({ repo }) => {
    try {
      const { stdout, stderr } = await execFileAsync("pwsh", [
        "./Import-GitHubProject.ps1",
        "-GitHubRepo", repo,
        "-BlogRepoPath", "C:\\Repos\\MeinBlog",   // TODO: anpassen
        "-GitHubToken", process.env.GITHUB_TOKEN
      ]);

      return {
        success: true,
        output: stdout || stderr
      };
    } catch (err) {
      return {
        success: false,
        error: err.message
      };
    }
  }
);

server.listen();
📄 Import-GitHubProject.ps1
param(
    [string]$GitHubRepo,
    [string]$BlogRepoPath,
    [string]$GitHubToken,
    [string]$Author = "Automatisierung",
    [string]$Email = "auto@example.com"
)

Write-Host "Hole README von $GitHubRepo..."
$uri = "https://api.github.com/repos/$GitHubRepo/readme"

$response = Invoke-RestMethod -Uri $uri -Headers @{
    Authorization = "token $GitHubToken"
    "User-Agent"  = "PowerShell"
}

$readmeContent = [System.Text.Encoding]::UTF8.GetString(
    [System.Convert]::FromBase64String($response.content)
)

$date = Get-Date -Format "yyyy-MM-dd"
$slug = $GitHubRepo.Split("/")[1]
$postFile = Join-Path $BlogRepoPath "content\posts\$date-$slug.md"

$postContent = @"
+++
title = "Projekt $slug"
date = "$date"
+++

# Projekt $slug

Automatisch importiert von GitHub: [$GitHubRepo](https://github.com/$GitHubRepo)

---

$readmeContent
"@

Write-Host "Erstelle Blogpost: $postFile"
$postContent | Out-File -FilePath $postFile -Encoding UTF8

Set-Location $BlogRepoPath
git config user.name $Author
git config user.email $Email

git add .
git commit -m "Automatische Dokumentation für $GitHubRepo"
git push

Write-Host "Fertig! Blogpost für $GitHubRepo erstellt und gepusht."
📄 README.md
# MCP GitHub Blog Server

Dieser MCP Server stellt ein Tool bereit, um GitHub-Repos automatisch als Blogposts zu dokumentieren.

## Installation

```bash
git clone https://github.com/deinuser/mcp-github-blog.git
cd mcp-github-blog
npm install
Nutzung
Setze dein GitHub Token als Umgebungsvariable:
export GITHUB_TOKEN="ghp_xxx"
Passe den Pfad zu deinem Blog-Repo in server.js an:
"-BlogRepoPath", "C:\\Repos\\MeinBlog"
Starte den Server:
npm start
Verbinde in ChatGPT als MCP Server.
Danach kannst du schreiben:
„Dokumentiere Repo melfware/demo im Blog.“
Der Server erstellt automatisch einen neuen Blogpost im GitHub-Blog-Repo.

---

## 🔧 Nächster Schritt für dich
- Du klonst das Skeleton oder legst es bei dir an.  
- In `server.js` stellst du deinen echten **BlogRepoPath** ein.  
- Token exportieren → `npm start` → ChatGPT verbinden.  

---

👉 Soll ich dir zusätzlich noch eine **GitHub Actions Workflow-Datei** (`.github/workflows/blog.yml`) machen, damit der Blog automatisch neu gebaut wird, sobald der MCP Server ein neues Post committed?