#!/usr/bin/env python3
"""
Vektör veritabanını oluşturan script
Markdown dosyalarını yükler, chunk'lara böler ve DB'ye ekler
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import DOCUMENTS_PATH, CHROMA_DB_URL, CHUNK_SIZE, CHUNK_OVERLAP
from src.document_processor import DocumentProcessor
from src.chunking import TextChunker
from src.vector_db import VectorDatabase

def main():
    print("=" * 60)
    print("🚀 Vektör Veritabanı Oluşturucu")
    print("=" * 60)
    
    # 1. Belgeleri yükle
    print("\n📂 Markdown dosyaları yükleniyor...")
    processor = DocumentProcessor(DOCUMENTS_PATH)
    documents = processor.load_markdown_files()
    
    if not documents:
        print("⚠️  Hiç Markdown dosyası bulunamadı!")
        print(f"   Lütfen {DOCUMENTS_PATH} dizinine .md dosyaları ekleyin")
        return
    
    print(f"✅ {len(documents)} belge yüklendi")
    
    # 2. Chunk'lara böl
    print("\n✂️  Belgeler chunk'lara bölünüyor...")
    chunker = TextChunker(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = chunker.chunk_documents(documents)
    print(f"✅ Toplam {len(chunks)} chunk oluşturuldu")
    
    # 3. Vektör DB'ye ekle
    print("\n🗄️  Vektör veritabanına ekleniyor...")
    vector_db = VectorDatabase(CHROMA_DB_URL)
    vector_db.create_collection()
    vector_db.add_documents(chunks)
    
    # 4. İstatistikler
    info = vector_db.get_collection_info()
    print("\n" + "=" * 60)
    print("📊 Veritabanı İstatistikleri:")
    print(f"   Collection: {info['name']}")
    print(f"   Belgeler: {info['document_count']}")
    print(f"   Durum: {info['status']}")
    print("=" * 60)
    
    print("\n✅ Veritabanı başarıyla oluşturuldu!")
    print("   Chatbot'u başlatmak için: streamlit run app.py")

if __name__ == "__main__":
    main()
