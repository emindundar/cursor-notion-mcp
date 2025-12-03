# Notion Asistanı (cursor-notion-mcp)

Cursor IDE'yi Notion ile konuşturan, notlarınızı, görevlerinizi ve kod parçacıklarınızı yapay zeka yardımıyla doğrudan Notion'a kaydetmenizi sağlayan bir Python projesidir. Artık parlak fikirlerinizi veya önemli kod bloklarını kaybetmek yok!

---

## Kurulum

Projeyi bilgisayarınıza kurup çalıştırmak sadece birkaç dakika sürer.

### Adım 1: Projeyi Klonlama

Öncelikle terminali açın ve projeyi bilgisayarınıza klonlayın:

```bash
git clone https://github.com/emindundar/cursor-notion-mcp.git
cd cursor-notion-mcp
```

### Adım 2: Sanal Ortam ve Bağımlılıklar

Projeyi sisteminizdeki diğer Python paketlerinden izole etmek için bir sanal ortam (virtual environment) oluşturalım.

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Sanal ortam aktifken, gerekli kütüphaneleri `requirements.txt` dosyasından yükleyin:

```bash
pip install -r requirements.txt
```

### Adım 3: Notion API Anahtarı ve Sayfa Kimliği

Bu asistanın Notion hesabınıza erişebilmesi için iki bilgiye ihtiyacımız var:

**1. Notion API Anahtarı (NOTION_API_KEY):**

- [Notion My Integrations](https://www.notion.so/my-integrations) sayfasına gidin.
- **"+ New integration"** butonuna tıklayın.
- Entegrasyonunuza bir isim verin (Örn: "Cursor Asistanı") ve "Submit" deyin.
- "Secrets" bölümündeki **"Internal Integration Token"** değerini kopyalayın. Bu sizin API anahtarınızdır.
- **ÖNEMLİ:** Asistanın yazacağı Notion sayfasına gidin, sağ üstteki üç noktaya (`...`) tıklayın, **"+ Add connections"** menüsünden oluşturduğunuz entegrasyonu (Örn: "Cursor Asistanı") seçin ve erişim izni verin.

**2. Kök Sayfa Kimliği (ROOT_PAGE_ID):**

- Notlarınızın, görevlerinizin ve kodlarınızın ekleneceği Notion sayfasını açın.
- Tarayıcınızın adres çubuğundaki URL'ye bakın. URL'nin sonundaki 32 karakterlik alfanümerik kod, sizin sayfa kimliğinizdir.
- **Örnek:** `https://www.notion.so/Not-Defterim-a1b2c3d4e5f678901234567890abcdef`
- Buradaki ID: `a1b2c3d4e5f678901234567890abcdef`

### Adım 4: .env Dosyasını Oluşturma

Proje klasöründeki `.env.example` dosyasını kopyalayıp `.env` adında yeni bir dosya oluşturun. Ardından bir önceki adımda aldığınız bilgileri bu dosyanın içine yapıştırın.

```ini
NOTION_API_KEY=buraya_kopyaladığınız_api_anahtarını_yapıştırın
ROOT_PAGE_ID=buraya_kopyaladığınız_sayfa_kimliğini_yapıştırın
```

---

##  Cursor'a Nasıl Eklenir?

1. Cursor'da `Ctrl/Cmd + Shift + P` tuşlarına basıp **"Configure Agent (MCP)"** seçeneğini açın.
2. Açılan `mcp.json` dosyasına aşağıdaki `providers` listesine yeni bir satır ekleyin.
3. **`command`** kısmına projenizin bilgisayarınızdaki tam yolunu yazdığınızdan emin olun.

```json
{
  "providers": [
    {
      "name": "NotionAssistant",
      "command": "python C:\\Users\\KULLANICI\\Desktop\\cursor-notion-mcp\\server.py (doğru path'i yazdığınızdan emin olun)"
    }
    // Varsa diğer provider'larınız...
  ]
}
```

>  **İpucu:** Proje klasöründeyken terminale `pwd` (macOS/Linux) veya `cd` (Windows) yazarak tam yolu kolayca alabilirsiniz.

---

##  Neler Yapabilirsin? (Örnek Promptlar)

Artık `@NotionAssistant` etiketiyle asistanı çağırabilirsin!

**Görev Eklemek İçin:**

> `@NotionAssistant Notion'a "Haftalık raporu tamamla" diye bir görev ekle.`

**Not Almak İçin:**

> `@NotionAssistant "Proje Fikirleri" başlığıyla yeni bir not oluştur. İçeriği şöyle olsun: "Notion entegrasyonu ile çalışan bir blog platformu yapabiliriz."`

**Kod Kaydetmek İçin:**

> `@NotionAssistant bu kodu "Firebase user stream" açıklamasıyla dart dilinde kaydet.`
> 
> ```dart
> Stream<User?> get userChanges => FirebaseAuth.instance.userChanges();
> ```

**Notion'da Arama Yapmak İçin:**

> `@NotionAssistant Notion'da "veritabanı şeması" diye arat.`
