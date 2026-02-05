# RAG Tabanlı Markdown Chatbot

Markdown dosyalarını analiz edip vektör veritabanında depolamak ve RAG yöntemiyle chatbot sorgularına yanıt vermek için oluşturulmuş bir projedir.

## 🚀 HIZLI BAŞLANGIÇ

**Türkçe Kurulum Rehberi:** [NASIL_CALISTIRILIR.md](NASIL_CALISTIRILIR.md) - Detaylı adım adım talimatlar

## Özellikler

- 📄 Markdown dosyalarını otomatik okuma ve analiz
- 🔀 Metni mantıklı chunks'a bölme
- 🗄️ ChromaDB vektör veritabanı ile embedding depolama
- 🤖 LLM ile RAG destekli soru cevaplandırma (Ollama veya OpenAI)
- 💬 Streamlit ile etkileşimli chatbot arayüzü

## Kurulum Seçenekleri

Bu projeyi iki farklı şekilde çalıştırabilirsiniz:

### 🐳 Seçenek 1: Docker ile (ÖNERİLİR)
Ollama kullanarak ücretsiz, lokal LLM ile çalışır. En kolay kurulum yöntemi.

```bash
# 1. Servisleri başlat
docker-compose up -d

# 2. Model indir
docker exec -it ollama-llm ollama pull mistral

# 3. Veritabanı oluştur
docker exec -it rag-app python src/create_vector_db.py

# 4. Tarayıcıda aç: http://localhost:8501
```

**Detaylı Kurulum:** [OLLAMA_SETUP.md](OLLAMA_SETUP.md)

### 🐍 Seçenek 2: Python ile (OpenAI)
OpenAI API kullanarak çalışır (ücretli).

```bash
# 1. Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
# veya: source venv/bin/activate  # Linux/Mac

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. .env dosyası oluştur ve OpenAI API anahtarını ekle
# OPENAI_API_KEY=sk-your-api-key-here

# 4. Veritabanı oluştur
python src/create_vector_db.py

# 5. Chatbot başlat
streamlit run app.py
```

**Detaylı Kurulum:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Proje Yapısı

```
project/
├── app.py                    # Streamlit chatbot arayüzü
├── requirements.txt          # Python bağımlılıkları
├── .env.example              # Environment şablonu
├── src/
│   ├── create_vector_db.py   # Vektör DB oluşturma
│   ├── document_processor.py # MD dosya işleme
│   ├── chunking.py           # Text chunking lojik
│   ├── rag_chain.py          # RAG pipeline
│   └── config.py             # Konfigürasyon
├── documents/                # MD dosyaları (giriş)
└── data/
    └── chroma_db/            # Vektör DB (çıkış)
```

## Dosya Formatları

Desteklenen format:
- `.md` - Markdown dosyaları

## API Anahtarı (Sadece OpenAI için)

OpenAI seçeneğini kullanıyorsanız API anahtarı gereklidir. [OpenAI Console](https://platform.openai.com/api-keys) adresinden alabilirsiniz.

Docker/Ollama seçeneğini kullanıyorsanız API anahtarına gerek yoktur.

## Lisans

MIT
