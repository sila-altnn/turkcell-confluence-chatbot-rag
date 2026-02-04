# RAG Tabanlı Markdown Chatbot - Kurulum ve Kullanım Rehberi

## 📋 Proje İçeriği

```
turkcell-confluence-chatbot-rag/
├── app.py                      # Streamlit Chatbot UI
├── test_rag.py                 # Test Script
├── requirements.txt            # Python bağımlılıkları
├── .env.example               # Environment şablonu
├── .gitignore                 # Git ignore dosyası
├── src/
│   ├── __init__.py
│   ├── config.py              # Konfigürasyon yönetimi
│   ├── document_processor.py  # Markdown dosya işleme
│   ├── chunking.py            # Text chunking algoritması
│   ├── vector_db.py           # ChromaDB entegrasyonu
│   ├── rag_chain.py           # RAG Pipeline
│   └── create_vector_db.py    # Veritabanı oluşturma
├── documents/                 # Markdown dosyaları (GİRİŞ)
│   └── turkcell_intro.md     # Örnek Markdown
└── data/
    └── chroma_db/             # Vektör veritabanı (ÇIKTI)
```

## 🚀 Hızlı Başlangıç

### 1. Python Ortamını Kur

```bash
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
venv\Scripts\activate  # Windows
# veya
source venv/bin/activate  # Linux/Mac
```

### 2. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 3. API Anahtarını Ayarla

`.env` dosyası oluştur:

```
OPENAI_API_KEY=sk-your-api-key-here
CHROMA_DB_PATH=./data/chroma_db
DOCUMENTS_PATH=./documents
MODEL_NAME=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
```

**OpenAI API anahtarını almak için:**
1. [OpenAI Console](https://platform.openai.com/api-keys) ziyaret et
2. API anahtarı oluştur
3. `.env` dosyasına ekle

### 4. Markdown Dosyaları Ekle

`documents/` klasörüne `.md` dosyalarını koy:

```bash
documents/
├── turkcell_intro.md        # Örnek (zaten var)
├── your_document.md         # Kendi dosyalarını ekle
└── another_doc.md
```

### 5. Vektör Veritabanını Oluştur

```bash
python src/create_vector_db.py
```

**Çıktı:**
```
============================================================
🚀 Vektör Veritabanı Oluşturucu
============================================================

📂 Markdown dosyaları yükleniyor...
✅ 1 belge yüklendi

✂️  Belgeler chunk'lara bölünüyor...
📦 turkcell_intro.md: 5 chunk oluşturuldu
✅ Toplam 5 chunk oluşturuldu

🗄️  Vektör veritabanına ekleniyor...
✅ 5 chunk DB'ye eklendi

============================================================
📊 Veritabanı İstatistikleri:
   Collection: rag_documents
   Belgeler: 5
   Durum: ready
============================================================

✅ Veritabanı başarıyla oluşturuldu!
```

### 6. Chatbot'u Başlat

```bash
streamlit run app.py
```

Tarayıcı otomatik olarak `http://localhost:8501` adresini açacak.

## 💬 Chatbot Arayüzü

### Ana Özellikler

- ✅ **Sohbet Geçmişi**: Tüm mesajlar görüntülenir
- 📊 **İstatistikler**: Veri tabanı bilgileri sidebar'da
- 📄 **Kaynak Gösterme**: Her yanıtla kaynaklar gösterilir
- 🔄 **Sistemi Yenile**: Yeni belgeler için DB'yi güncelle
- 🗑️  **Sohbeti Temizle**: Geçmiş silme seçeneği

### Kullanım Örneği

1. **Soru Sor:**
   ```
   Turkcell'in hizmetleri nelerdir?
   ```

2. **Yanıt Al:**
   ```
   Turkcell aşağıdaki hizmetleri sunmaktadır:
   
   Mobil Hizmetler: Sesli arama, SMS/MMS, İnternet, Mobil ödeme
   Sabit Hizmetler: İnternet, Telefon, TV (Turkcell TV+)
   Dijital Hizmetler: Bulut, Oyun, Müzik, Video
   ```

3. **Kaynakları Gör:**
   ```
   📄 Kaynaklar: turkcell_intro.md
   ```

## 🧪 Sistemi Test Et

```bash
python test_rag.py
```

Test script, RAG sistemini birkaç örnek soruyla test eder.

## 📚 Mimarisi

### 1. Document Processor (`document_processor.py`)
- Markdown dosyalarını okur
- İçeriği ayrıştırır

### 2. Text Chunking (`chunking.py`)
- Uzun metni 500 karakterlik parçalara böler
- 100 karakterlik overlap sağlar

### 3. Vector Database (`vector_db.py`)
- ChromaDB kullanır
- Embedding'ler otomatik oluşturulur
- Semantik arama sağlar

### 4. RAG Chain (`rag_chain.py`)
- Sorguya ilgili chunk'ları bulur
- OpenAI GPT'ye gönderir
- Yapılandırılmış yanıt döndürür

### 5. Streamlit UI (`app.py`)
- Interaktif sohbet arayüzü
- Session state yönetimi
- Responsive tasarım

## ⚙️ Konfigürasyon

`src/config.py` dosyasında ayarlar:

```python
CHUNK_SIZE = 500              # Chunk boyutu
CHUNK_OVERLAP = 100           # Chunk'lar arası overlap
MODEL_NAME = "gpt-3.5-turbo" # LLM modeli
```

## 🔍 Gelişmiş Kullanım

### Özel Chunk Boyutu

```python
from src.chunking import TextChunker

chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
```

### Vektör DB'yi Temizle

```bash
python
>>> from src.vector_db import VectorDatabase
>>> db = VectorDatabase("./data/chroma_db")
>>> db.clear()
```

### Manuel RAG Sorgusu

```python
from src.vector_db import VectorDatabase
from src.rag_chain import RAGChain

vector_db = VectorDatabase("./data/chroma_db")
vector_db.create_collection()
rag = RAGChain(vector_db)

result = rag.generate_answer("Turkcell hakkında bilgi ver")
print(result['answer'])
```

## 🐛 Sorun Giderme

### "OPENAI_API_KEY is not set"
```bash
1. .env dosyası oluşturduğunu kontrol et
2. Dosyada OPENAI_API_KEY=... satırını kontrol et
3. Dosya kaydedildiğini kontrol et
```

### "Hiç Markdown dosyası bulunamadı"
```bash
1. documents/ klasörünün var olduğunu kontrol et
2. .md uzantılı dosyalar ekle
3. Dosya adının .md ile bittiğini kontrol et
```

### "Veritabanında belge yok"
```bash
python src/create_vector_db.py
# Komutunu çalıştır
```

### ChromaDB hatası
```bash
# ChromaDB'yi sıfırla
rm -r data/chroma_db
python src/create_vector_db.py
```

## 📝 Kendi Markdown Dosyalarını Ekle

Örnek Markdown yapısı:

```markdown
# Başlık

Paragraf metni buraya gelir.

## Alt Başlık

- Madde 1
- Madde 2
- Madde 3

### Daha Alt Başlık

Daha fazla bilgi...
```

## 🔐 Güvenlik

- API anahtarını asla repository'ye commit etme
- `.env` dosyasını `.gitignore`'a ekle (zaten eklendi)
- Production'da secrets manager kullan

## 📊 Performance İpuçları

1. **Chunk Boyutu**: Büyük belgeler için chunk_size'ı artır
2. **Top K**: Daha fazla kaynak için top_k parametresini artır
3. **Model**: Hızlı yanıt için gpt-3.5-turbo, kalite için gpt-4

## 🎓 Öğrenme Kaynakları

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/)

## 📞 Destek

Sorun yaşarsan:
1. Terminal çıktılarını kontrol et
2. `.env` dosyasını doğrula
3. API anahtarının aktif olduğunu kontrol et

## 📄 Lisans

MIT License

---

**Başarılar! 🚀**
