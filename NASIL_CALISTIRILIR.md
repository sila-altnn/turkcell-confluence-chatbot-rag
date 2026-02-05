# 🚀 Nasıl Çalıştırılır?

Bu dosya, Turkcell Confluence Chatbot RAG projesini çalıştırmak için adım adım talimatlar içerir.

## 📋 İki Farklı Kurulum Seçeneği

Bu projeyi çalıştırmanın **iki farklı yolu** vardır:

1. **🐳 Docker ile (ÖNERİLİR)** - En kolay yöntem, hiçbir şey kurmaya gerek yok
2. **🐍 Python ile (Manuel)** - OpenAI API kullanarak manuel kurulum

---

## 🐳 YÖNTEm 1: DOCKER İLE ÇALIŞTIRMA (ÖNERİLİR)

Bu yöntem Ollama kullanır (ücretsiz, lokal LLM).

### Ön Gereksinimler
- Docker ve Docker Compose kurulu olmalı
- En az 8GB RAM önerilir

### Adım 1: Docker Servislerini Başlat

```bash
docker-compose up -d
```

Bu komut 3 servisi başlatır:
- ✅ ChromaDB (Vektör veritabanı)
- ✅ Ollama (Lokal LLM)
- ✅ Streamlit Uygulaması

### Adım 2: Ollama'ya Model İndir

İlk kez çalıştırıyorsanız, model indirmeniz gerekir:

```bash
docker exec -it ollama-llm ollama pull mistral
```

Model indirme birkaç dakika sürebilir (yaklaşık 4-5 GB).

**Alternatif Modeller:**
```bash
# Türkçe için önerilir
docker exec -it ollama-llm ollama pull neural-chat

# Daha güçlü ama daha yavaş
docker exec -it ollama-llm ollama pull llama2
```

### Adım 3: Markdown Belgelerini Ekle

Kendi belgelerinizi `documents/` klasörüne ekleyin:

```bash
# Örnek: Belgelerinizi kopyalayın
cp /path/to/your/documents/*.md documents/
```

Proje zaten örnek bir belge içerir: `documents/turkcell_intro.md`

### Adım 4: Vektör Veritabanını Oluştur

```bash
docker exec -it rag-app python src/create_vector_db.py
```

**Beklenen Çıktı:**
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

### Adım 5: Web Arayüzünü Aç

Tarayıcınızda şu adresi açın:

```
http://localhost:8501
```

### 🎉 Tebrikler! Artık kullanmaya hazırsınız.

---

## 🐍 YÖNTEM 2: PYTHON İLE MANUEL KURULUM

Bu yöntem OpenAI API kullanır (ücretli).

### Ön Gereksinimler
- Python 3.10 veya üzeri
- OpenAI API anahtarı ([buradan alabilirsiniz](https://platform.openai.com/api-keys))

### Adım 1: Sanal Ortam Oluştur

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Adım 2: Paketleri Yükle

```bash
pip install -r requirements.txt
```

### Adım 3: .env Dosyası Oluştur

`.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:

```bash
# .env dosyası
OPENAI_API_KEY=sk-your-api-key-here
CHROMA_DB_PATH=./data/chroma_db
DOCUMENTS_PATH=./documents
MODEL_NAME=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
```

**NOT:** `.env.example` dosyasını kopyalayarak başlayabilirsiniz:
```bash
cp .env.example .env
# Sonra .env dosyasını editörde açıp değerleri doldurun
```

### Adım 4: Markdown Belgelerini Ekle

`documents/` klasörüne `.md` dosyalarınızı koyun. Proje zaten bir örnek içerir.

### Adım 5: Vektör Veritabanını Oluştur

```bash
python src/create_vector_db.py
```

### Adım 6: Uygulamayı Başlat

```bash
streamlit run app.py
```

Tarayıcı otomatik olarak açılacaktır. Açılmazsa:
```
http://localhost:8501
```

---

## 💬 Chatbot Nasıl Kullanılır?

1. **Soru Sor:** Chatbot arayüzünde sorunuzu yazın
   ```
   Örnek: "Turkcell'in hizmetleri nelerdir?"
   ```

2. **Yanıt Al:** Chatbot belgelerinizden bilgi çekerek yanıt verir

3. **Kaynakları Gör:** Her yanıt hangi belgeden geldiğini gösterir

4. **Yeni Belgeler Ekle:** 
   - `documents/` klasörüne yeni `.md` dosyaları ekleyin
   - Sidebar'dan "🔨 Vector DB'yi Oluştur" butonuna tıklayın
   - "🔄 Sistemi Başlat/Yenile" butonuna tıklayın

---

## 🔧 Sorun Giderme

### Docker ile ilgili sorunlar

**Problem:** Docker servisleri başlamıyor
```bash
# Çözüm: Logları kontrol edin
docker-compose logs -f
```

**Problem:** "Model bulunamadı" hatası
```bash
# Çözüm: Modeli tekrar indirin
docker exec -it ollama-llm ollama pull mistral
```

**Problem:** Port zaten kullanılıyor
```bash
# Çözüm: Portları değiştirin veya çakışan servisi durdurun
docker-compose down
docker ps  # Çalışan containerları kontrol edin
```

### Python ile ilgili sorunlar

**Problem:** "OPENAI_API_KEY is not set"
```bash
# Çözüm: 
# 1. .env dosyasının olduğundan emin olun
# 2. Dosyada OPENAI_API_KEY=... satırını kontrol edin
# 3. API anahtarınızın doğru olduğunu kontrol edin
```

**Problem:** "Hiç Markdown dosyası bulunamadı"
```bash
# Çözüm:
# 1. documents/ klasörünün var olduğunu kontrol edin
# 2. .md uzantılı dosyalar ekleyin
# 3. Dosya adının .md ile bittiğini kontrol edin
```

**Problem:** "Veritabanında belge yok"
```bash
# Çözüm: Vektör veritabanını oluşturun
python src/create_vector_db.py
```

**Problem:** ModuleNotFoundError
```bash
# Çözüm: Sanal ortamı aktifleştirin ve paketleri tekrar yükleyin
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Genel sorunlar

**Problem:** Yavaş performans
```bash
# Docker için: Daha küçük model kullanın
docker exec -it ollama-llm ollama pull phi

# Python için: Farklı model deneyin
# .env dosyasında: MODEL_NAME=gpt-3.5-turbo
```

**Problem:** Türkçe karakterler bozuk görünüyor
```bash
# Markdown dosyalarınızın UTF-8 encoding ile kaydedildiğinden emin olun
```

---

## 📊 Faydalı Komutlar

### Docker Komutları

```bash
# Tüm servisleri başlat
docker-compose up -d

# Servisleri durdur
docker-compose down

# Logları canlı izle
docker-compose logs -f

# Sadece bir servisin logunu izle
docker logs -f rag-app

# Mevcut Ollama modellerini listele
docker exec ollama-llm ollama list

# Container'a bağlan
docker exec -it rag-app bash

# Veritabanını sıfırla (dikkatli!)
docker-compose down -v
docker-compose up -d
```

### Python Komutları

```bash
# Test script çalıştır
python test_rag.py

# Veritabanını sıfırla
rm -rf data/chroma_db
python src/create_vector_db.py

# Belirli bir belgeyi test et
python test_rag.py
```

---

## 🎯 Hızlı Başlangıç Özeti

### Docker İçin (5 Adım)
```bash
# 1. Servisleri başlat
docker-compose up -d

# 2. Model indir (ilk kez)
docker exec -it ollama-llm ollama pull mistral

# 3. Belgeleri ekle (isteğe bağlı)
# documents/ klasörüne .md dosyaları koy

# 4. Veritabanı oluştur
docker exec -it rag-app python src/create_vector_db.py

# 5. Tarayıcıda aç
# http://localhost:8501
```

### Python İçin (6 Adım)
```bash
# 1. Sanal ortam oluştur ve aktifleştir
python -m venv venv
venv\Scripts\activate  # Windows
# veya: source venv/bin/activate  # Linux/Mac

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. .env dosyası oluştur
cp .env.example .env
# .env dosyasını editörde açıp OPENAI_API_KEY ekle

# 4. Belgeleri ekle (isteğe bağlı)
# documents/ klasörüne .md dosyaları koy

# 5. Veritabanı oluştur
python src/create_vector_db.py

# 6. Uygulamayı başlat
streamlit run app.py
```

---

## 📚 Daha Fazla Bilgi

- **OLLAMA_SETUP.md** - Ollama ve Docker detaylı kurulum
- **SETUP_GUIDE.md** - Detaylı setup rehberi
- **PROJECT_STRUCTURE.md** - Proje yapısı ve mimari
- **README.md** - Proje hakkında genel bilgi

---

## 🆘 Hala Sorun mu Yaşıyorsun?

1. Bu dosyadaki "Sorun Giderme" bölümüne bak
2. Terminal çıktılarını kontrol et
3. Logları incele:
   - Docker: `docker-compose logs -f`
   - Python: Terminal çıktısı

---

**İyi Çalışmalar! 🚀**
