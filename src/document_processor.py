import os
import markdown
from pathlib import Path
from typing import List

class DocumentProcessor:
    """Markdown dosyalarını işleyen sınıf"""
    
    def __init__(self, documents_path: str):
        self.documents_path = documents_path
    
    def load_markdown_files(self) -> List[dict]:
        """
        Verilen dizindeki tüm MD dosyalarını yükler
        
        Returns:
            List[dict]: Dosya adı ve içeriği içeren sözlükler
        """
        documents = []
        
        if not os.path.exists(self.documents_path):
            print(f"⚠️  Klasör bulunamadı: {self.documents_path}")
            return documents
        
        md_files = Path(self.documents_path).glob("*.md")
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        'filename': file_path.name,
                        'content': content,
                        'path': str(file_path)
                    })
                    print(f"✅ Yüklendi: {file_path.name}")
            except Exception as e:
                print(f"❌ Hata {file_path.name}: {str(e)}")
        
        return documents
    
    def parse_markdown(self, content: str) -> dict:
        """
        Markdown içeriğini ayrıştırır
        
        Args:
            content (str): Markdown içeriği
            
        Returns:
            dict: HTML ve yapılandırılmış metin
        """
        html = markdown.markdown(content)
        return {
            'html': html,
            'raw': content
        }
