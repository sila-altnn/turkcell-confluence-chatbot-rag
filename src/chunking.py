from typing import List

class TextChunker:
    """Metni chunks'a bölme sınıfı"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, filename: str = "") -> List[dict]:
        """
        Metni belirtilen boyuta göre parçalara böler
        
        Args:
            text (str): Bölünecek metin
            filename (str): Dosya adı (metadata için)
            
        Returns:
            List[dict]: Chunk'lar ve metadata'ları
        """
        chunks = []
        
        # Paragraflar yapıldı
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        chunk_counter = 0
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append({
                        'content': current_chunk.strip(),
                        'metadata': {
                            'source': filename,
                            'chunk_id': chunk_counter,
                            'size': len(current_chunk)
                        }
                    })
                    chunk_counter += 1
                
                current_chunk = paragraph + "\n\n"
        
        # Son chunk'ı ekle
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'metadata': {
                    'source': filename,
                    'chunk_id': chunk_counter,
                    'size': len(current_chunk)
                }
            })
        
        return chunks
    
    def chunk_documents(self, documents: List[dict]) -> List[dict]:
        """
        Çoklu belgeleri chunk'lara böler
        
        Args:
            documents (List[dict]): İşlenmemiş belgeler
            
        Returns:
            List[dict]: Chunk'lar
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'], doc['filename'])
            all_chunks.extend(chunks)
            print(f"📦 {doc['filename']}: {len(chunks)} chunk oluşturuldu")
        
        return all_chunks
