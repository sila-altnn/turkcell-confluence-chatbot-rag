from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
from src.vector_db import VectorDatabase
from src.config import OLLAMA_BASE_URL, MODEL_NAME

class RAGChain:
    """RAG (Retrieval-Augmented Generation) pipeline - Ollama kullanarak"""
    
    def __init__(self, vector_db: VectorDatabase, model_name: str = None):
        self.vector_db = vector_db
        self.model_name = model_name or MODEL_NAME
        
        # Ollama ile ChatOpenAI uyumlu API
        self.llm = ChatOpenAI(
            base_url=OLLAMA_BASE_URL + "/v1",
            api_key="ollama",  # Gerçek API key gerekmez
            model_name=self.model_name,
            temperature=0.7
        )
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Prompt template'lerini ayarlar"""
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""Aşağıdaki bilgileri kullanarak soruyu yanıtla:

Bilgiler:
{context}

Soru: {question}

Yanıt: Verilen bilgilere göre kısa ve doğru bir şekilde yanıtla. Eğer cevap bilgilerde yoksa "Bilgi yok" de."""
        )
    
    def retrieve(self, query: str, top_k: int = 3) -> List[dict]:
        """
        Vektör DB'den ilgili belgeleri alır
        
        Args:
            query (str): Sorgulama metni
            top_k (int): Alınacak belge sayısı
            
        Returns:
            List[dict]: Alınan belge parçaları
        """
        return self.vector_db.search(query, top_k)
    
    def format_context(self, documents: List[dict]) -> str:
        """
        Alınan belgeleri bağlam metnine formatlar
        
        Args:
            documents (List[dict]): Alınan belge parçaları
            
        Returns:
            str: Formatlanmış bağlam metni
        """
        if not documents:
            return "İlgili bilgi bulunamadı."
        
        context_parts = []
        for doc in documents:
            source = doc.get('metadata', {}).get('source', 'Bilinmeyen')
            content = doc.get('content', '')
            context_parts.append(f"[{source}]\n{content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def generate_answer(self, query: str, top_k: int = 3) -> dict:
        """
        Soruya RAG yöntemiyle yanıt oluşturur
        
        Args:
            query (str): Soru metni
            top_k (int): Kaç belge parçası kullanılacak
            
        Returns:
            dict: Yanıt ve kaynak bilgileri
        """
        # Belgeleri al
        retrieved_docs = self.retrieve(query, top_k)
        
        # Bağlamı formatla
        context = self.format_context(retrieved_docs)
        
        # LLM ile yanıt oluştur
        try:
            prompt = self.rag_prompt.format(context=context, question=query)
            answer = self.llm.predict(text=prompt)
            
            return {
                'answer': answer.strip(),
                'sources': [doc['metadata'].get('source', 'Bilinmeyen') for doc in retrieved_docs],
                'success': True
            }
        except Exception as e:
            return {
                'answer': f"❌ Hata: {str(e)}",
                'sources': [],
                'success': False
            }
