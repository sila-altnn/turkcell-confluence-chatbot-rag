import chromadb
from typing import List, Dict
import os

class VectorDatabase:
    """ChromaDB ile çalışan vektör veritabanı sınıfı"""
    
    def __init__(self, db_url: str, collection_name: str = "rag_documents"):
        self.db_url = db_url if db_url else "http://chroma:8000"
        self.collection_name = collection_name
        self.collection = None
        
        # ChromaDB HTTP client başlat - doğru host ve port ile
        try:
            # Docker container'da chroma:8000 adresine bağlan
            self.client = chromadb.HttpClient(host="chroma", port=8000)
            print(f"✅ Chroma DB'ye bağlandı: {self.client}")
        except Exception as e:
            print(f"❌ Chroma DB bağlantı hatası: {str(e)}")
    
    def create_collection(self):
        """Yeni collection oluşturur"""
        try:
            # Mevcut collection'ları kontrol et
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                print(f"ℹ️  Mevcut collection kullanılıyor: {self.collection_name}")
            except Exception as e_get:
                # Collection yoksa oluştur
                print(f"   Collection oluşturuluyor... ({str(e_get)[:50]})")
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                print(f"✅ Collection oluşturuldu: {self.collection_name}")
        except Exception as e:
            print(f"❌ Collection hatası: {str(e)}")
    
    def add_documents(self, chunks: List[dict]):
        """
        Chunks'ları vektör veritabanına ekler
        
        Args:
            chunks (List[dict]): Chunk'lar ve metadata'ları
        """
        if not self.collection:
            self.create_collection()
        
        try:
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"chunk_{i}_{chunk['metadata'].get('source', 'unknown')}"
                ids.append(chunk_id)
                documents.append(chunk['content'])
                metadatas.append(chunk['metadata'])
            
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            print(f"✅ {len(chunks)} chunk DB'ye eklendi")
                
        except Exception as e:
            print(f"❌ Ekleme hatası: {str(e)}")
    
    def search(self, query: str, top_k: int = 3) -> List[dict]:
        """
        Sorguya benzer chunks'ları arar
        
        Args:
            query (str): Arama sorgusu
            top_k (int): Döndürülecek sonuç sayısı
            
        Returns:
            List[dict]: Benzer chunks'lar
        """
        if not self.collection:
            print("⚠️  Collection yüklenmedi")
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            documents = []
            
            if results and results.get('documents'):
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results.get('metadatas') else {},
                        'distance': results['distances'][0][i] if results.get('distances') else 0
                    })
            
            return documents
            
        except Exception as e:
            print(f"❌ Arama hatası: {str(e)}")
            return []
    
    def get_collection_info(self) -> dict:
        """Collection hakkında bilgi döndürür"""
        if not self.collection:
            return {"status": "Collection yüklenmedi"}
        
        count = self.collection.count()
        return {
            'name': self.collection_name,
            'document_count': count,
            'status': 'ready'
        }
    
    def clear(self):
        """Tüm collection'ı temizler"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = None
            print(f"✅ Collection temizlendi: {self.collection_name}")
        except Exception as e:
            print(f"❌ Temizleme hatası: {str(e)}")
