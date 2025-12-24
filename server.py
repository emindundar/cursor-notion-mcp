# -*- coding: utf-8 -*-
import os
import datetime
import subprocess
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from notion_client import Client, APIResponseError

# --- Proje Kök Dizini ve .env Yüklemesi ---
# Ortam değişkenlerini .env dosyasından güvenli bir şekilde yükle
load_dotenv()

# --- Ayarlar ve Kontroller ---
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

if not NOTION_API_KEY or not NOTION_PAGE_ID:
    raise ValueError(
        "Lütfen .env dosyasını oluşturun ve NOTION_API_KEY ile NOTION_PAGE_ID değerlerini eksiksiz ayarlayın."
    )

# --- İstemci ve Sunucu Başlatma ---
try:
    notion = Client(auth=NOTION_API_KEY)
    mcp = FastMCP("NotionAssistant")
except APIResponseError as e:
    print(f"Hata: Notion istemcisi başlatılamadı. API anahtarınız geçersiz olabilir. Detay: {e}")
    exit(1)


# --- Notion Araçları ---
@mcp.tool()
def add_note(content: str, title: str = None) -> str:
    """Notion'a başlık ve içerikten oluşan bir not ekler."""
    if not title:
        title = datetime.datetime.now().strftime("%Y-%m-%d %H:%M Notu")

    try:
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[
                {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": f"{title}"}}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}},
                {"type": "divider", "divider": {}},
            ],
        )
        return f"Not '{title}' başlığıyla başarıyla eklendi."
    except APIResponseError as e:
        return f"Hata: Notion'a not eklenemedi. Sayfa ID'nizi kontrol ettiniz mi? Detay: {e}"


@mcp.tool()
def add_todo(task: str) -> str:
    """Notion'daki yapılacaklar listesine yeni bir görev (to-do) ekler."""
    try:
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[
                {"type": "to_do", "to_do": {"rich_text": [{"type": "text", "text": {"content": task}}], "checked": False}}
            ],
        )
        return f"Görev eklendi: {task}"
    except APIResponseError as e:
        return f"Hata: Notion'a görev eklenemedi. Detay: {e}"


@mcp.tool()
def save_code_snippet(code: str, language: str = "python", description: str = "") -> str:
    """Bir kod parçasını açıklamasıyla birlikte Notion'a kod bloğu olarak kaydeder."""
    try:
        children_blocks = []
        if description:
            children_blocks.append(
                {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"{description}"}}]}}
            )
        children_blocks.extend([
            {"type": "code", "code": {"rich_text": [{"type": "text", "text": {"content": code}}], "language": language}},
            {"type": "divider", "divider": {}},
        ])
        notion.blocks.children.append(block_id=NOTION_PAGE_ID, children=children_blocks)
        return f"Kod parçası '{language}' diliyle başarıyla kaydedildi."
    except APIResponseError as e:
        return f"Hata: Kod parçası kaydedilemedi. Desteklenmeyen bir dil adı olabilir. Detay: {e}"


@mcp.tool()
def search_in_notion(query: str) -> str:
    """Tüm Notion çalışma alanında (erişim izni olan sayfalarda) arama yapar."""
    try:
        results = notion.search(query=query, page_size=5).get("results", [])
        if not results:
            return f"'{query}' için hiçbir sonuç bulunamadı."
        
        output = f"'{query}' için bulunan sonuçlar:\n\n"
        for item in results:
            if item.get("object") == "page":
                title_prop = next((p for p in item.get("properties", {}).values() if p.get("type") == "title"), None)
                page_title = title_prop["title"][0]["plain_text"] if title_prop and title_prop["title"] else "Başlıksız Sayfa"
                url = item.get("url", "#")
                output += f"- **{page_title}**\n  [Sayfaya Git]({url})\n"
        return output.strip()
    except APIResponseError as e:
        return f"Arama sırasında bir hata oluştu: {e}"


# --- KRİTİK YENİ ARAÇ: Git Entegrasyonu ---
@mcp.tool()
def get_git_summary(since: str = "6am", project_path: str = None) -> str:
    """
    Belirtilen bir proje klasöründeki Git deposunda, belirtilen bir zamandan beri yapılan değişiklikleri özetler.
    'git log' ve 'git diff' komutlarının çıktısını birleştirerek AI'ın analiz edebileceği bir metin döndürür.
    'since' parametresi '1.day.ago', 'yesterday 6am', '2023-12-18 09:00:00' gibi değerler alabilir.
    'project_path' belirtilmezse, komutun çalıştırıldığı mevcut dizin varsayılır.
    """
    # Proje yolu belirtilmemişse, betiğin çalıştığı dizini kullan
    if project_path is None:
        project_path = "." # Mevcut dizin

    # Belirtilen yolun geçerli bir dizin olup olmadığını kontrol et
    if not os.path.isdir(project_path):
        return f"Hata: Belirtilen proje yolu '{project_path}' bulunamadı veya bir dizin değil."

    try:
        # Belirtilen dizinin bir Git deposu olup olmadığını kontrol et
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True, cwd=project_path)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"Hata: '{os.path.abspath(project_path)}' dizini bir Git deposu değil veya 'git' komutu bulunamadı."

    try:
        # Belirtilen zamandan beri yapılan commit'leri ve değişiklikleri (patch) getir
        git_log_command = ["git", "log", f"--since={since}", "--patch", "--no-color"]
        result = subprocess.run(git_log_command, check=True, capture_output=True, text=True, encoding='utf-8', cwd=project_path)

        summary = result.stdout

        if not summary:
            return f"'{since}' zamanından beri '{os.path.abspath(project_path)}' deposunda herhangi bir commit yapılmamış."

        return f"'{os.path.abspath(project_path)}' projesi için Git Özeti ('{since}' zamanından beri):\n\n---\n\n{summary}"

    except subprocess.CalledProcessError as e:
        return f"Git günlüğü alınırken bir hata oluştu: {e.stderr}"
    except Exception as e:
        return f"Beklenmedik bir hata oluştu: {str(e)}"


if __name__ == "__main__":
    print("Cursor Notion+Git Assistant sunucusu baslatiliyor...")
    print("Araclar yuklendi: add_note, add_todo, save_code_snippet, search_in_notion, get_git_summary")
    print("Asistan, Cursor'a eklenmeye hazir!")
    mcp.run()
