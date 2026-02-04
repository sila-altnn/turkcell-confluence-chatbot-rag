# RAG Tabanlı Markdown Chatbot

Markdown dosyalarını analiz edip vektör veritabanında depolamak ve RAG yöntemiyle chatbot sorgularına yanıt vermek için oluşturulmuş bir projedir.

## Özellikler

- 📄 Markdown dosyalarını otomatik okuma ve analiz
- 🔀 Metni mantıklı chunks'a bölme
- 🗄️ ChromaDB vektör veritabanı ile embedding depolama
- 🤖 OpenAI GPT modeli ile RAG destekli soru cevaplandırma
- 💬 Streamlit ile etkileşimli chatbot arayüzü

## Kurulum

### 1. Sanal Ortam Oluştur
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Paketleri Yükle
```bash
pip install -r requirements.txt
```

### 3. Environment Değişkenleri
`.env` dosyası oluştur ve OpenAI API anahtarını ekle:
```
OPENAI_API_KEY=your_api_key_here
```

### 4. Dokumentasyon Dosyaları Ekle
`documents/` klasörüne Markdown (.md) dosyalarını koy.

## Kullanım

### Veritabanı Oluştur
```bash
python src/create_vector_db.py
```

### Chatbot Başlat
```bash
streamlit run app.py
```

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

## API Anahtarı

OpenAI API anahtarı gereklidir. [OpenAI Console](https://platform.openai.com/api-keys) adresinden alabilirsiniz.

## Lisans

MIT
