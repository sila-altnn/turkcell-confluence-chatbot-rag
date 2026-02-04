#!/usr/bin/env python3
"""
RAG Sistemini test etmek için basit script
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CHROMA_DB_URL, MODEL_NAME
from src.vector_db import VectorDatabase
from src.rag_chain import RAGChain

def main():
    print("=" * 60)
    print("🧪 RAG Sistemi Test Edicisi")
    print("=" * 60)
    
    # Veritabanını yükle
    print("\n📂 Veritabanı yükleniyor...")
    vector_db = VectorDatabase(CHROMA_DB_URL)
    vector_db.create_collection()
    
    info = vector_db.get_collection_info()
    print(f"✅ Belgeler: {info['document_count']}")
    
    if info['document_count'] == 0:
        print("❌ Veritabanında belge yok! Lütfen create_vector_db.py çalıştırın.")
        return
    
    # RAG Chain oluştur
    rag_chain = RAGChain(vector_db, MODEL_NAME)
    
    # Test soruları
    test_questions = [
        "Turkcell hakkında kısaca bilgi ver",
        "Turkcell'in müşteri sayısı kaçtır?",
        "Turkcell'in hizmetleri nelerdir?",
    ]
    
    print("\n" + "=" * 60)
    print("🤖 Test Soruları:")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n❓ Soru: {question}")
        print("-" * 60)
        
        result = rag_chain.generate_answer(question, top_k=2)
        
        print(f"✅ Yanıt: {result['answer']}")
        if result.get('sources'):
            print(f"📄 Kaynaklar: {', '.join(result['sources'])}")

if __name__ == "__main__":
    main()
