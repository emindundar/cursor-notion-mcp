"""Notion MCP server with note, todo, code snippet, search and git summary tools."""

from __future__ import annotations

import datetime
import os
import subprocess
from typing import Iterable, List, Mapping

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from notion_client import APIResponseError, Client

# --- Environment setup -----------------------------------------------------

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"Missing environment variable '{name}'. "
            "Create a .env file with NOTION_API_KEY and NOTION_PAGE_ID."
        )
    return value


NOTION_API_KEY = _require_env("NOTION_API_KEY")
NOTION_PAGE_ID = _require_env("NOTION_PAGE_ID")


# --- Notion client and helpers --------------------------------------------

try:
    notion = Client(auth=NOTION_API_KEY)
except APIResponseError as exc:
    raise RuntimeError("Notion client could not be initialized. Check your API key.") from exc

mcp = FastMCP("NotionAssistant")


def _append_blocks(blocks: Iterable[Mapping]) -> str:
    try:
        notion.blocks.children.append(block_id=NOTION_PAGE_ID, children=list(blocks))
        return "İşlem başarıyla tamamlandı."
    except APIResponseError as exc:
        return f"Notion API hatası: {exc}"


# --- MCP tools -------------------------------------------------------------


@mcp.tool()
def add_note(content: str, title: str | None = None) -> str:
    """Add a heading + paragraph note to the configured Notion page."""
    title_text = title or datetime.datetime.now().strftime("%Y-%m-%d %H:%M Notu")
    blocks = [
        {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": title_text}}]}},
        {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}},
        {"type": "divider", "divider": {}},
    ]
    result = _append_blocks(blocks)
    return result if "başarıyla" not in result else f"Not eklendi: {title_text}"


@mcp.tool()
def add_todo(task: str) -> str:
    """Add a unchecked to-do item to the configured Notion page."""
    blocks = [
        {"type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": task}}], "checked": False}}
    ]
    result = _append_blocks(blocks)
    return result if "başarıyla" not in result else f"Görev eklendi: {task}"


@mcp.tool()
def save_code_snippet(code: str, language: str = "python", description: str = "") -> str:
    """Save a code snippet (with optional description) as a code block."""
    blocks: List[Mapping] = []
    if description:
        blocks.append(
            {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": description}}]}}
        )
    blocks.extend(
        [
            {"type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": code}}], "language": language}},
            {"type": "divider", "divider": {}},
        ]
    )
    result = _append_blocks(blocks)
    return result if "başarıyla" not in result else f"Kod parçası kaydedildi ({language})."


@mcp.tool()
def search_in_notion(query: str) -> str:
    """Search across the workspace (where the integration has access)."""
    try:
        results = notion.search(query=query, page_size=5).get("results", [])
    except APIResponseError as exc:
        return f"Arama sırasında hata: {exc}"

    if not results:
        return f"'{query}' için sonuç bulunamadı."

    lines = [f"'{query}' için bulunan sonuçlar:"]
    for item in results:
        if item.get("object") != "page":
            continue
        title_prop = next((p for p in item.get("properties", {}).values() if p.get("type") == "title"), None)
        page_title = title_prop["title"][0]["plain_text"] if title_prop and title_prop.get("title") else "Başlıksız Sayfa"
        url = item.get("url", "#")
        lines.append(f"- {page_title}\n  {url}")
    return "\n".join(lines)


@mcp.tool()
def get_git_summary(since: str = "6am", project_path: str | None = None) -> str:
    """
    Combine git log and patch output since the given time.

    since: e.g., 'yesterday', '2024-01-10 09:00', '1.day.ago'
    project_path: optional repo path; defaults to current directory.
    """
    path = project_path or "."
    if not os.path.isdir(path):
        return f"Hata: '{path}' bir dizin değil."

    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True, cwd=path)
    except subprocess.CalledProcessError:
        return f"Hata: '{os.path.abspath(path)}' bir git deposu değil."
    except FileNotFoundError:
        return "Hata: 'git' komutu bulunamadı."

    try:
        cmd = ["git", "log", f"--since={since}", "--patch", "--no-color"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding="utf-8", cwd=path)
        summary = result.stdout.strip()
        if not summary:
            return f"'{since}' zamanından beri '{os.path.abspath(path)}' deposunda commit yok."
        return f"Git özeti ({since} itibarıyla) - {os.path.abspath(path)}:\n\n{summary}"
    except subprocess.CalledProcessError as exc:
        return f"Git günlüğü alınamadı: {exc.stderr}"
    except Exception as exc:  # pragma: no cover - safeguard
        return f"Beklenmedik hata: {exc}"


if __name__ == "__main__":
    print("Notion MCP sunucusu başlatılıyor...")
    print("Araçlar: add_note, add_todo, save_code_snippet, search_in_notion, get_git_summary")
    mcp.run()
