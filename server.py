from mcp.server.fastmcp import FastMCP
from notion_client import Client
from dotenv import load_dotenv
import datetime
import os

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# --- AYARLAR ---
# API Key ve Sayfa ID'sini .env dosyasından güvenli bir şekilde al
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
ROOT_PAGE_ID = os.getenv("ROOT_PAGE_ID")

# Ayarların eksik olup olmadığını kontrol et
if not NOTION_API_KEY or not ROOT_PAGE_ID:
    raise ValueError("Lütfen .env dosyasını oluşturun ve NOTION_API_KEY ile ROOT_PAGE_ID değerlerini ayarlayın.")

# Notion istemcisini ve MCP sunucusunu başlat
try:
    notion = Client(auth=NOTION_API_KEY)
    mcp = FastMCP("NotionAssistant")
except Exception as e:
    # Notion client başlatılırken oluşabilecek kimlik doğrulama hatalarını yakala
    print(f"Notion istemcisi başlatılamadı: {e}")
    print("Lütfen NOTION_API_KEY'inizin doğru olduğundan emin olun.")
    exit(1)


@mcp.tool()
def add_note(content: str, title: str = None) -> str:
    """
    Notion'a başlık ve içerikten oluşan standart bir not ekler.
    Eğer başlık belirtilmezse, notun eklendiği tarih ve saat başlık olarak kullanılır.
    """
    if not title:
        title = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        notion.blocks.children.append(
            block_id=ROOT_PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": f"📝 {title}"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}
                },
                {"object": "block", "type": "divider", "divider": {}}
            ]
        )
        return f" Not '{title}' başlığıyla başarıyla eklendi."
    except Exception as e:
        return f" Hata: Notion'a not eklenemedi. Detay: {str(e)}"

@mcp.tool()
def add_todo(task: str) -> str:
    """
    Notion sayfasına 'yapılacaklar' listesine yeni bir görev ekler.
    Örnek: "Bugün Flutter provider konusuna çalış"
    """
    try:
        notion.blocks.children.append(
            block_id=ROOT_PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [{"type": "text", "text": {"content": task}}],
                        "checked": False
                    }
                }
            ]
        )
        return f" Görev eklendi: {task}"
    except Exception as e:
        return f" Hata: Notion'a görev eklenemedi. Detay: {str(e)}"

@mcp.tool()
def save_code_snippet(code: str, language: str = "python", description: str = "") -> str:
    """
    Bir kod parçasını açıklamasıyla birlikte Notion'a 'Kod Bloğu' olarak kaydeder.
    Args:
        code (str): Kaydedilecek kodun kendisi.
        language (str): Kodun dili (ör: python, dart, javascript). Varsayılan: python.
        description (str): Kodun ne işe yaradığına dair kısa açıklama.
    """
    try:
        children_blocks = []
        
        if description:
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f" {description}"}}]}
            })

        children_blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": code}}],
                "language": language
            }
        })
        
        children_blocks.append({"object": "block", "type": "divider", "divider": {}})

        notion.blocks.children.append(block_id=ROOT_PAGE_ID, children=children_blocks)
        return f" Kod parçası '{language}' diliyle başarıyla kaydedildi."
    except Exception as e:
        return f"Hata: Kod parçası kaydedilemedi. Detay: {str(e)}"

@mcp.tool()
def search_in_notion(query: str) -> str:
    """
    Tüm Notion çalışma alanında (erişim izni olan sayfalarda) arama yapar.
    """
    try:
        results = notion.search(query=query, page_size=5).get("results", [])
        
        if not results:
            return f" '{query}' için hiçbir sonuç bulunamadı."
            
        output = f"🔍 '{query}' için bulunan sonuçlar:\n\n"
        for item in results:
            if item.get("object") == "page":
                page_title = "Başlıksız Sayfa"
                properties = item.get("properties", {})
                
                # Sayfa başlığını almak için farklı olasılıkları dene
                title_prop = next((prop for prop_name, prop in properties.items() if prop.get("type") == "title"), None)
                if title_prop and title_prop.get("title"):
                    page_title = title_prop["title"][0].get("text", {}).get("content", page_title)

                url = item.get("url", "#")
                output += f"- **{page_title}**\n  [Sayfaya Git]({url})\n"
                
        return output.strip()
    except Exception as e:
        return f" Arama sırasında bir hata oluştu: {str(e)}"

if __name__ == "__main__":
    print("Notion Assistant MCP sunucusu başlatılıyor...")
    print("Araçlar: add_note, add_todo, save_code_snippet, search_in_notion")
    print("Cursor'a eklemeye hazır!")
    mcp.run()
