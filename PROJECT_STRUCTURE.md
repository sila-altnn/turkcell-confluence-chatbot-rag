# 🏗️ Proje Yapısı

```
turkcell-confluence-chatbot-rag/
│
├── 📁 docker/                          # Docker yapılandırmaları
│   ├── chroma/
│   │   └── Dockerfile                  # Chroma DB container
│   ├── ollama/
│   │   └── Dockerfile                  # Ollama LLM container
│   └── app/
│       └── Dockerfile                  # Python/Streamlit container
│
├── 📁 src/                             # Python kaynak kodları
│   ├── __init__.py
│   ├── config.py                       # Yapılandırma
│   ├── vector_db.py                    # Chroma DB entegrasyonu
│   ├── chunking.py                     # Metin parçalama
│   ├── document_processor.py           # Belge işleme
│   ├── create_vector_db.py            # VectorDB oluşturucu
│   └── rag_chain.py                    # RAG pipeline
│
├── 📁 documents/                       # Markdown belgeleri
│   └── turkcell_intro.md               # Örnek belge
│
├── 📄 docker-compose.yml               # Docker Compose konfigürasyonu
├── 📄 Dockerfile                       # Root Dockerfile (deprecated)
├── 📄 app.py                           # Streamlit uygulaması
├── 📄 test_rag.py                      # RAG test scripti
├── 📄 requirements.txt                 # Python bağımlılıkları
├── 📄 .env.example                     # Örnek environment dosyası
├── 📄 .env                             # Gerçek environment dosyası (git ignore)
├── 📄 .dockerignore                    # Docker ignore
├── 📄 .gitignore                       # Git ignore
│
├── 📚 README.md                        # Ana dokümantasyon
├── 📚 OLLAMA_SETUP.md                  # Ollama kurulum rehberi
├── 📚 SETUP_GUIDE.md                   # Setup rehberi
├── 📚 START.txt                        # Başlangıç talimatları
└── 🏗️ PROJECT_STRUCTURE.md            # Bu dosya
```

## 🚀 Hızlı Başlama

### 1. Docker ile Tüm Servisleri Başlat

```bash
docker-compose up -d
```

Çıkacak çıktı:
- ✅ chroma-db (port 9191)
- ✅ ollama-llm (port 11434)
- ✅ rag-app (port 8501)

### 2. Ollama'ya Model İndir

```bash
docker exec -it ollama-llm ollama pull mistral
```

### 3. Vektör DB Oluştur

```bash
docker exec -it rag-app python src/create_vector_db.py
```

### 4. Web Arayüzüne Erişim

- **Streamlit App**: http://localhost:8501
- **Ollama API**: http://localhost:11434
- **Chroma DB**: http://localhost:9191

## 📦 Container Yapısı

| Container | İşlev | Port | Durum Kontrol |
|-----------|-------|------|---------------|
| **chroma-db** | Vektör veritabanı (ChromaDB) | 9191 | `/api/v1/heartbeat` |
| **ollama-llm** | Local LLM (Ollama) | 11434 | `/api/tags` |
| **rag-app** | Streamlit web uygulaması | 8501 | Streamlit health |

## 📝 Dockerfile Açıklamaları

### `docker/chroma/Dockerfile`
- Resmi ChromaDB image'ını kullanır
- Health check otomatik olarak HTTP heartbeat kontrol eder

### `docker/ollama/Dockerfile`
- Resmi Ollama image'ını kullanır
- Health check API tags endpoint'ini kontrol eder

### `docker/app/Dockerfile`
- Python 3.11 slim base image
- Tüm requirements'ı yükler
- Streamlit'i `0.0.0.0:8501` üzerinde çalıştırır

## 🔄 Docker Network

Tüm containerlar `rag-network` bridge network'ünde iletişim kurar:
- `app` → `chroma:9191` (Vektör DB)
- `app` → `ollama:11434` (LLM API)

## 📚 Kullanışlı Docker Komutları

```bash
# Tüm servisleri başlat
docker-compose up -d

# Servisleri durdur
docker-compose down

# Logları izle
docker-compose logs -f

# Spesifik container'ın loglarını izle
docker logs -f rag-app

# Container bash'ine gir
docker exec -it rag-app bash

# Servislerin durumunu kontrol et
docker-compose ps

# Volume'leri temizle
docker-compose down -v
```

## 🔧 Geliştirme İpuçları

### Local geliştirme (Docker olmadan)

```bash
# 1. Venv oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. Docker servisleri başlat (opsiyonel)
docker-compose up -d chroma ollama

# 4. .env'i localhost'a ayarla
# OLLAMA_BASE_URL=http://localhost:11434
# CHROMA_DB_URL=http://localhost:9191

# 5. Uygulamayı çalıştır
streamlit run app.py
```

### Yeni paket ekleme

```bash
# 1. Paketi pip'ten yükle
pip install new-package

# 2. requirements.txt'i güncelle
pip freeze > requirements.txt

# 3. Docker image'ı yeniden build et
docker-compose build app
```

## 🐛 Sorun Giderme

### Container başlamıyor
```bash
docker logs rag-app
```

### Health check başarısız
```bash
# Chroma sağlığını kontrol et
docker exec chroma-db curl http://localhost:8000/api/v1/heartbeat

# Ollama sağlığını kontrol et
docker exec ollama-llm curl http://localhost:11434/api/tags
```

### Model bulunamadı
```bash
docker exec -it ollama-llm ollama pull mistral --verbose
```

## 📖 Daha Fazla Bilgi

- [OLLAMA_SETUP.md](OLLAMA_SETUP.md) - Ollama kurulum detayları
- [README.md](README.md) - Ana dokümantasyon
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup rehberi
