import streamlit as st
import sys
import os
from datetime import datetime
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import CHROMA_DB_URL, MODEL_NAME
from src.vector_db import VectorDatabase
from src.rag_chain import RAGChain
from src.document_processor import DocumentProcessor
from src.chunking import TextChunker

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🤖 RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .chat-message {
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .source-badge {
        display: inline-block;
        background-color: #fff3cd;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        margin: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False

def initialize_rag():
    """RAG sistemini başlatır"""
    try:
        # Veritabanını yükle
        vector_db = VectorDatabase(CHROMA_DB_URL)
        vector_db.create_collection()
        
        # Bilgi al
        info = vector_db.get_collection_info()
        if info['document_count'] == 0:
            return False, "Veritabanında belge yok. Lütfen create_vector_db.py çalıştırın."
        
        # RAG Chain oluştur
        rag_chain = RAGChain(vector_db, MODEL_NAME)
        
        st.session_state.vector_db = vector_db
        st.session_state.rag_chain = rag_chain
        st.session_state.db_initialized = True
        
        return True, f"Sistem hazır ({info['document_count']} belge)"
    except Exception as e:
        return False, f"❌ Hata: {str(e)}"

def process_question(question: str) -> dict:
    """Soruyu işler ve yanıt oluşturur"""
    try:
        if not st.session_state.rag_chain:
            return {
                'answer': 'RAG sistemi initialized değil',
                'success': False
            }
        
        result = st.session_state.rag_chain.generate_answer(question, top_k=3)
        return result
    except Exception as e:
        return {
            'answer': f"❌ Hata: {str(e)}",
            'success': False
        }

# Main UI
st.markdown("<div class='main-header'><h1>🤖 RAG Tabanlı Markdown Chatbot</h1></div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    # Dosya yükleme
    st.subheader("📁 Dosyaları Yükle")
    uploaded_files = st.file_uploader(
        "Markdown dosyaları seç (.md)",
        type=["md"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("💾 Dosyaları Kaydet"):
            documents_dir = Path("documents")
            documents_dir.mkdir(exist_ok=True)
            
            with st.spinner("Dosyalar kaydediliyor..."):
                for uploaded_file in uploaded_files:
                    file_path = documents_dir / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                st.success(f"✅ {len(uploaded_files)} dosya kaydedildi!")
    
    # Veritabanı oluşturma
    st.divider()
    st.subheader("🗄️ Veritabanını Oluştur")
    
    if st.button("🔨 Vector DB'yi Oluştur"):
        with st.spinner("Vector database oluşturuluyor..."):
            try:
                # Dokumentleri yükle
                processor = DocumentProcessor()
                documents = processor.load_documents("documents")
                
                if not documents:
                    st.error("❌ documents/ klasöründe .md dosyası yok!")
                else:
                    # Chunklama yap
                    chunker = TextChunker()
                    chunks = []
                    for doc in documents:
                        doc_chunks = chunker.chunk_text(doc['content'], doc['filename'])
                        for chunk_data in doc_chunks:
                            chunks.append({
                                'content': chunk_data['content'],
                                'filename': doc['filename']
                            })
                    
                    # Vector DB'ye ekle
                    vector_db = VectorDatabase(CHROMA_DB_URL)
                    vector_db.clear()
                    vector_db.create_collection()
                    
                    ids = [f"chunk_{i}" for i in range(len(chunks))]
                    documents_list = [c['content'] for c in chunks]
                    metadatas = [{'source': c['filename']} for c in chunks]
                    
                    vector_db.add_documents(ids, documents_list, metadatas)
                    
                    st.success(f"✅ {len(chunks)} chunk oluşturuldu ve DB'ye eklendi!")
                    
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    
    # Sistem başlatma
    st.divider()
    if st.button("🔄 Sistemi Başlat/Yenile"):
        with st.spinner("Sistem başlatılıyor..."):
            success, message = initialize_rag()
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(message)
    
    # Veritabanı bilgileri
    if st.session_state.db_initialized:
        st.divider()
        info = st.session_state.vector_db.get_collection_info()
        st.metric("📊 Toplam Belgeler", info['document_count'])
        st.metric("📝 Toplam Mesajlar", len(st.session_state.messages))
    
    # Geçmiş temizle
    if st.button("🗑️  Sohbeti Temizle"):
        st.session_state.messages = []
        st.success("Sohbet temizlendi!")
        st.rerun()
    
    st.divider()
    st.markdown("""
    ### 📚 Nasıl Kullanılır?
    
    1. **Belgeleri Ekle**: `documents/` klasörüne `.md` dosyaları koy
    2. **Veritabanını Oluştur**: `python src/create_vector_db.py` çalıştır
    3. **Sistemi Başlat**: Yukarıdaki butona tıkla
    4. **Sorular Sor**: Chatbot'a sorular soruştur
    """)

# Main Chat Area
if not st.session_state.db_initialized:
    st.warning("⚠️  Sistem henüz başlatılmadı. Lütfen sidebar'daki 'Sistemi Başlat' butonuna tıklayın.")
else:
    # Chat geçmişini göster
    st.subheader("💬 Sohbet")
    
    # Mesajları göster
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message user-message'><b>👤 Siz:</b><br/>{message['content']}</div>", 
                       unsafe_allow_html=True)
        else:
            sources_html = ""
            if message.get("sources"):
                sources_html = "<br/><b>📄 Kaynaklar:</b> " + " ".join(
                    [f"<span class='source-badge'>{src}</span>" for src in message["sources"]]
                ) + ""
            st.markdown(f"<div class='chat-message bot-message'><b>🤖 Chatbot:</b><br/>{message['content']}{sources_html}</div>", 
                       unsafe_allow_html=True)
    
    # Input alanı
    st.divider()
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Soru sor:",
            placeholder="Markdown belgelerin hakkında bir soru sor...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Gönder", use_container_width=True)
    
    # Soruyu işle
    if send_button and user_input:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Yanıt oluştur
        with st.spinner("🤔 Düşünüyorum..."):
            result = process_question(user_input)
        
        # Bot mesajını ekle
        st.session_state.messages.append({
            "role": "assistant",
            "content": result['answer'],
            "sources": result.get('sources', [])
        })
        
        st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px;'>
    <p>🔐 Markdown RAG Chatbot | Powered by OpenAI & LangChain</p>
</div>
""", unsafe_allow_html=True)
