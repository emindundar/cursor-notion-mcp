# Cursor Notion Assistant - Stajyerinizin Yeni En İyi Arkadaşı

Kod yazarken aklınıza gelen parlak fikirleri, yapılacaklar listesini veya o kritik kod parçasını anında Notion'a kaydetmek ne kadar güzel olurdu, değil mi? Peki ya gün sonunda "Bugün ne yaptım?" diye düşünmek yerine, tek bir komutla tüm Git geçmişinizi özetleyip rapor haline getirebilseydiniz?

**Cursor Notion Assistant** tam olarak bunu yapıyor. Cursor IDE'nizin içinden ayrılmadan, Notion'ı kişisel veritabanınız, Git'i ise hafızanız gibi kullanmanızı sağlar.

## 🎯 Neler Yapabilir?

- **💾 Hafızanız Olsun:** Kod bloklarını, notları, görevleri doğrudan Notion'a kaydedin.
- **📊 Günlük Rapor Asistanı:** `git log` ve `git diff` komutlarını çalıştırarak gün içinde yaptığınız tüm değişiklikleri analiz için hazırlar. Siz sadece "Bu özeti Notion'a rapor olarak ekle" deyin, gerisini o halletsin.
- **🔍 Notion'da Arayın:** "Geçen hafta kaydettiğim o API linki neredeydi?" diye düşünmeyin. Asistan sizin için tüm Notion çalışma alanınızda arama yapar.
- **✅ Görevlerinizi Yönetin:** Aklınıza gelen bir yapılacak işi anında Notion'daki görev listenize ekleyin.

---

## 🚀 Kurulum (Sadece 5 Dakika)

> **⚠️ ÖNEMLİ:** Bu proje **Python 3.10 veya üzeri** gerektirir. Sisteminizde Python 3.9 veya daha eski bir sürüm varsa, önce Python 3.10+ kurmanız gerekir.

### Adım 0: Python Sürümünü Kontrol Edin

Terminalde şu komutu çalıştırın:

```bash
python3 --version
```

Eğer sürüm 3.10'dan küçükse (örn: Python 3.9.6), aşağıdaki adımları izleyin:

**macOS için Homebrew ile Python 3.12 Kurulumu:**

```bash
# Homebrew yoksa önce kurun:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.12'yi kurun:
brew install python@3.12

# Kurulumu doğrulayın:
python3.12 --version
```

**Linux için:**

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### Adım 1: Projeyi Bilgisayarınıza İndirin

Terminali açın ve bu klasöre gidin:

```bash
cd /Users/emindundar/ProjeBelgeleri/cursor-notion-mcp/notion_mcp_v2
```

### Adım 2: Sanal Ortam ve Kütüphaneler

Projeyi sisteminizden izole bir sanal ortama kuralım.

- **macOS / Linux (Python 3.10+ kuruluysa):**
  ```bash
  # Python 3.12 kurduysanız:
  python3.12 -m venv venv
  source venv/bin/activate
  
  # VEYA sistem Python'unuz 3.10+ ise:
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

### Adım 3: Notion API Anahtarı Nasıl Alınır?

1. [Notion My Integrations](https://www.notion.so/my-integrations) sayfasına gidin ve **"+ New integration"** oluşturun.
2. Entegrasyona bir isim verin (örn: "Cursor Assistant") ve "Submit" deyin.
3. "Secrets" bölümündeki **"Internal Integration Token"** değerini kopyalayın.
4. **⚠️ En Önemli Adım:** Notlarınızı ekleyeceğiniz Notion sayfasına gidin, sağ üstteki üç noktaya (`...`) tıklayın, **"+ Add connections"** menüsünden az önce oluşturduğunuz entegrasyonu seçip izin verin.

### Adım 4: `.env` Dosyasını Oluşturun

`.env.example` dosyasını kopyalayıp `.env` adıyla yeni bir dosya oluşturun:

```bash
cp .env.example .env
```

İçine Notion'dan aldığınız **API Anahtarını** ve notlarınızı eklemek istediğiniz **Sayfa Kimliğini** (URL'deki 32 haneli kod) yapıştırın.

```ini
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_PAGE_ID=a1b2c3d4e5f678901234567890abcdef
```

> **💡 İpucu:** Notion sayfa URL'si şu şekilde görünür:
> `https://www.notion.so/My-Page-a1b2c3d4e5f678901234567890abcdef`
> Son 32 karakterlik kısım (`a1b2c3d4e5f678901234567890abcdef`) sizin Page ID'nizdir.

---

## 🔧 Cursor'a Entegrasyon

1. Cursor'da `Ctrl/Cmd + Shift + P` ile komut paletini açın ve **"Configure Agent (MCP)"** seçin.
2. Açılan `mcp.json` dosyasına aşağıdaki konfigürasyonu ekleyin:

```json
{
  "mcpServers": {
    "notion-assistant": {
      "command": "/Users/emindundar/ProjeBelgeleri/cursor-notion-mcp/notion_mcp_v2/venv/bin/python",
      "args": [
        "/Users/emindundar/ProjeBelgeleri/cursor-notion-mcp/notion_mcp_v2/server.py"
      ]
    }
  }
}
```

> **⚠️ ÖNEMLİ:** 
> - `command` kısmında **sanal ortamın Python'unu** kullanın (tam yol)
> - `args` içindeki yolu kendi sisteminize göre düzenleyin
> - Proje klasöründeyken terminale `pwd` yazarak tam yolu alabilirsiniz
> - Windows'ta yol şu şekilde olur: `C:\\Users\\...\\notion_mcp_v2\\venv\\Scripts\\python.exe`

3. Dosyayı kaydedin ve Cursor'ı yeniden başlatın.

---

## 💬 Örnek Promptlar

Artık `@NotionAssistant` ile sohbet etmeye hazırsınız!

### 📝 Gün Sonu Raporu Oluşturma (2 Adımda)

1. **Git özetini çıkarın:**
   ```
   @NotionAssistant bugün yaptığım tüm git değişikliklerinin bir özetini çıkar.
   ```

2. **Notion'a kaydedin:**
   ```
   @NotionAssistant bu metni "Bugünün Gün Sonu Raporu" başlığıyla Notion'a ekle.
   ```

### 💻 Kod Kaydetme

```
@NotionAssistant bu kodu "Kullanıcı girişi için özel hook" açıklamasıyla javascript dilinde kaydet.
```

### ✅ Görev Ekleme

```
@NotionAssistant "Yeni UI bileşenlerini test et" diye bir görev ekle.
```

### 🔍 Arama Yapma

```
@NotionAssistant Notion'da "Stripe API anahtarları" diye arat.
```

### 📌 Not Ekleme

```
@NotionAssistant "Bugün öğrendiğim React hooks pattern'i" başlığıyla bir not ekle: "useState ve useEffect'i birlikte kullanırken dependency array'e dikkat etmek gerekiyor."
```

---

## 🛠️ Mevcut Araçlar

| Araç | Açıklama | Parametreler |
|------|----------|--------------|
| `add_note` | Notion'a başlık ve içerikli not ekler | `content` (zorunlu), `title` (opsiyonel) |
| `add_todo` | Yapılacaklar listesine görev ekler | `task` (zorunlu) |
| `save_code_snippet` | Kod parçacığını syntax highlighting ile kaydeder | `code` (zorunlu), `language` (varsayılan: python), `description` (opsiyonel) |
| `search_in_notion` | Notion workspace'inde arama yapar | `query` (zorunlu) |
| `get_git_summary` | Git commit ve patch özetini çıkarır | `since` (varsayılan: 6am), `project_path` (opsiyonel) |

---

## 🐛 Sorun Giderme

### "Missing environment variable" hatası alıyorum

- `.env` dosyasının `notion_mcp_v2` klasöründe olduğundan emin olun
- `NOTION_API_KEY` ve `NOTION_PAGE_ID` değerlerinin doğru girildiğini kontrol edin

### "Notion client could not be initialized" hatası

- API anahtarınızın geçerli olduğundan emin olun
- Notion entegrasyonunuzun aktif olduğunu kontrol edin

### "Notion API hatası" alıyorum

- Entegrasyonunuza hedef sayfada erişim izni verdiğinizden emin olun
- Sayfa ID'nizin doğru olduğunu kontrol edin

### Git özeti çalışmıyor

- Proje klasörünüzün bir Git deposu olduğundan emin olun
- `git` komutunun sisteminizde kurulu olduğunu kontrol edin

---

## 📄 Lisans

Bu proje açık kaynak kodludur ve özgürce kullanılabilir.

---

## 🤝 Katkıda Bulunma

Hata bildirimleri, özellik istekleri ve pull request'ler memnuniyetle karşılanır!

---

**Keyifli kodlamalar! 🚀**
