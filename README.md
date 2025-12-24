# Cursor Notion Assistant - Stajyerinizin Yeni En İyi Arkadaşı

Kod yazarken aklınıza gelen parlak fikirleri, yapılacaklar listesini veya o kritik kod parçasını anında Notion'a kaydetmek ne kadar güzel olurdu, değil mi? Peki ya gün sonunda "Bugün ne yaptım?" diye düşünmek yerine, tek bir komutla tüm Git geçmişinizi özetleyip rapor haline getirebilseydiniz?

**Cursor Notion Assistant** tam olarak bunu yapıyor. Cursor IDE'nizin içinden ayrılmadan, Notion'ı kişisel veritabanınız, Git'i ise hafızanız gibi kullanmanızı sağlar.

## Neler Yapabilir?

- **Hafızanız Olsun:** Kod bloklarını, notları, görevleri doğrudan Notion'a kaydedin.
- **Günlük Rapor Asistanı:** `git log` ve `git diff` komutlarını çalıştırarak gün içinde yaptığınız tüm değişiklikleri analiz için hazırlar. Siz sadece "Bu özeti Notion'a rapor olarak ekle" deyin, gerisini o halletsin.
- **Notion'da Arayın:** "Geçen hafta kaydettiğim o API linki neredeydi?" diye düşünmeyin. Asistan sizin için tüm Notion çalışma alanınızda arama yapar.
- **Görevlerinizi Yönetin:** Aklınıza gelen bir yapılacak işi anında Notion'daki görev listenize ekleyin.

---

## Kurulum (Sadece 5 Dakika)

### Adım 1: Projeyi Bilgisayarınıza İndirin

Terminali açın ve projeyi klonlayın:

```bash
git clone https://github.com/KULLANICI_ADINIZ/cursor-notion-mcp.git
cd cursor-notion-mcp
```

### Adım 2: Sanal Ortam ve Kütüphaneler

Projeyi sisteminizden izole bir sanal ortama kuralım.

- **Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

### Adım 3: Notion API Anahtarı Nasıl Alınır?

- [Notion My Integrations](https://www.notion.so/my-integrations) sayfasına gidin ve **"+ New integration"** oluşturun.
- Entegrasyona bir isim verin ve "Submit" deyin.
- "Secrets" bölümündeki **"Internal Integration Token"** değerini kopyalayın.
- **En Önemli Adım:** Notlarınızı ekleyeceğiniz Notion sayfasına gidin, sağ üstteki üç noktaya (`...`) tıklayın, **"+ Add connections"** menüsünden az önce oluşturduğunuz entegrasyonu seçip izin verin.

### Adım 4: `.env` Dosyasını Oluşturun

`.env.example` dosyasını kopyalayıp `.env` adıyla yeni bir dosya oluşturun. İçine Notion'dan aldığınız **API Anahtarını** ve notlarınızı eklemek istediğiniz **Sayfa Kimliğini** (URL'deki 32 haneli kod) yapıştırın.

```ini
NOTION_API_KEY=secret_...
NOTION_PAGE_ID=a1b2c3d4e5f678901234567890abcdef
```

---

## Cursor'a Entegrasyon

1. Cursor'da `Ctrl/Cmd + Shift + P` ile komut paletini açın ve **"Configure Agent (MCP)"** seçin.
2. `mcp.json` dosyasına, projenizin tam yolunu gösteren aşağıdaki satırı ekleyin.

```json
{
  "providers": [
    {
      "name": "NotionAssistant",
      "command": "python /path/to/your/project/cursor-notion-mcp/server.py"
    }
  ]
}
```

> **İpucu:** Proje klasöründeyken terminale `pwd` (macOS/Linux) veya `cd` (Windows) yazarak tam yolu kolayca alabilirsiniz.

---

## Örnek Promptlar

Artık `@NotionAssistant` ile sohbet etmeye hazırsınız!

- **Gün Sonu Raporu Oluşturma (2 Adımda):**
  1. `@NotionAssistant bugün yaptığım tüm git değişikliklerinin bir özetini çıkar.`
  2. (Gelen özeti kopyalayın ve...) `@NotionAssistant bu metni "Bugünün Gün Sonu Raporu" başlığıyla Notion'a ekle.`

- **Kod Kaydetme:**
  > `@NotionAssistant bu kodu "Kullanıcı girişi için özel hook" açıklamasıyla javascript dilinde kaydet.`

- **Görev Ekleme:**
  > `@NotionAssistant "Yeni UI bileşenlerini test et" diye bir görev ekle.`

- **Arama Yapma:**
  > `@NotionAssistant Notion'da "Stripe API anahtarları" diye arat.`
