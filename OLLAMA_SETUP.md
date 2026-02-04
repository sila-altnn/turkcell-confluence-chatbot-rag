# 🚀 Ollama ile RAG Chatbot Kurulum Rehberi (Docker)

## Adım 1: Tüm Servisleri Docker Compose ile Başlat

```bash
docker-compose up -d
```

Bu komut aşağıdaki servisleri başlatacak:
- 🗄️ **Chroma DB**: `http://localhost:9191`
- 🤖 **Ollama**: `http://localhost:11434`
- 🎨 **Streamlit App**: `http://localhost:8501`

## Adım 2: Ollama'ya Model İndir

Ollama container'ına bağlan:
```bash
docker exec -it ollama-llm bash
```

Model indir (ilk kez yapıldığında biraz sürer):
```bash
# Seçenek 1: Mistral (Önerilir - hızlı ve iyi Türkçe desteği)
ollama pull mistral

# Seçenek 2: Llama 2 (Daha güçlü ama yavaş)
ollama pull llama2

# Seçenek 3: Neural Chat (Türkçe için optimize)
ollama pull neural-chat
```

Container'dan çık:
```bash
exit
```

## Adım 3: Markdown Belgelerini Ekle

```bash
# Türkçe belgeleri documents/ klasörüne kopyala
cp your_documents/*.md documents/
```

## Adım 4: Vektör Veritabanını Oluştur

App container'ı içinde çalıştır:
```bash
docker exec -it rag-app python src/create_vector_db.py
```

## Adım 5: Uygulamaya Erişim

Tarayıcıda aç:
```
http://localhost:8501
```

## 📝 Lokal Geliştirme (Docker olmadan)

Eğer lokal olarak çalıştırmak isterseniz:

```bash
# 1. Docker servislerini başlat (opsiyonel)
docker-compose up -d chroma ollama

# 2. Python paketlerini yükle
pip install -r requirements.txt

# 3. .env dosyasındaki URL'leri localhost olarak değiştir
# OLLAMA_BASE_URL=http://localhost:11434
# CHROMA_DB_URL=http://localhost:9191

# 4. Vektör DB oluştur
python src/create_vector_db.py

# 5. Uygulamayı çalıştır
streamlit run app.py
```

## ⚙️ Konfigürasyon (`.env`)

**Docker içinde (Recommended):**
```dotenv
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_DB_URL=http://chroma:9191
MODEL_NAME=mistral
EMBEDDING_MODEL=nomic-embed-text
DOCUMENTS_PATH=./documents
```

**Lokal geliştirme için:**
```dotenv
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DB_URL=http://localhost:9191
MODEL_NAME=mistral
EMBEDDING_MODEL=nomic-embed-text
DOCUMENTS_PATH=./documents
```

## 📊 Mevcut Modeller ve Performans

| Model | Boyut | Hız | Kalite | Türkçe |
|-------|-------|-----|--------|--------|
| mistral | 7B | ⚡⚡⚡⚡ | ⭐⭐⭐ | ✅ İyi |
| llama2 | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ İyi |
| neural-chat | 7B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ Mükemmel |
| qwen:7b | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ Mükemmel |

## 🔧 Sorun Giderme

### Streamlit görüntülenmiyor
```bash
# App loglarını kontrol et
docker logs -f rag-app

# Container'ı yeniden başlat
docker restart rag-app
```

### Ollama modeli indirmede hata
```bash
docker exec ollama-llm ollama pull mistral --verbose
```

### Bağlantı hatası
```bash
# Tüm servislerin çalışıp çalışmadığını kontrol et
docker ps

# Ağ bağlantısını kontrol et
docker network inspect rag-network
```

### Yavaş performans
- Daha küçük model kullan: `ollama pull phi` (2.7B)
- GPU desteğini aç: docker-compose.yml'de deploy section'ı uncomment et

## 📚 Yararlı Komutlar

```bash
# Tüm servisleri başlat
docker-compose up -d

# Servisleri durdur
docker-compose down

# Logları gerçek zamanlı izle
docker-compose logs -f

# Sadece Ollama loglarını göster
docker logs -f ollama-llm

# Mevcut modelleri listele
docker exec ollama-llm ollama list

# Container bash'ine gir
docker exec -it rag-app bash

# Volume'leri temizle (UYARI: veri silinir)
docker-compose down -v
```

## 🎯 Hızlı Başlama

```bash
# 1. Klon ve giş
cd turkcell-confluence-chatbot-rag

# 2. Docker'da başlat
docker-compose up -d

# 3. Model indir (ilk kez)
docker exec ollama-llm ollama pull mistral

# 4. Belgeleri ekle
# documents/ klasörüne .md dosyaları koy

# 5. Vektör DB oluştur
docker exec rag-app python src/create_vector_db.py

# 6. Tarayıcıda aç
# http://localhost:8501
```

Başarılar! 🚀
