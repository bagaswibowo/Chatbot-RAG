import streamlit as st
import tempfile
import json
from parser import parse_whatsapp_txt
from embedder import ChatEmbedder
from retriever import ChatRetriever
from generator import build_prompt, ask_huggingface
from style_extractor import extract_user_style

st.set_page_config(page_title="WhatsApp RAG Chatbot", layout="centered")
st.markdown("""
<style>
.wa-chat-container {
    background: #f7f7f7;
    border-radius: 10px;
    padding: 16px;
    max-height: 500px;
    overflow-y: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.wa-bubble-left {
    background: #fff;
    border-radius: 8px 8px 8px 0;
    padding: 10px 14px;
    display: inline-block;
    color: #222;
    margin-bottom: 4px;
    max-width: 70%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.wa-bubble-right {
    background: #d2f8d2;
    border-radius: 8px 8px 0 8px;
    padding: 10px 14px;
    display: inline-block;
    color: #222;
    margin-bottom: 4px;
    max-width: 70%;
    float: right;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.wa-sender {
    font-size: 12px;
    color: #888;
    margin-bottom: 2px;
}
.wa-chatbox {
    clear: both;
    margin-bottom: 12px;
}
.wa-input-area {
    margin-top: 16px;
    display: flex;
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'peran' not in st.session_state:
    st.session_state.peran = None
if 'lawan' not in st.session_state:
    st.session_state.lawan = None
if 'chats' not in st.session_state:
    st.session_state.chats = None
if 'user_names' not in st.session_state:
    st.session_state.user_names = None
if 'index_built' not in st.session_state:
    st.session_state.index_built = False

st.title("WhatsApp RAG Chatbot")

if st.session_state.chats is None:
    st.markdown("## Upload Riwayat Chat WhatsApp")
    uploaded_file = st.file_uploader("Upload file .txt chat WhatsApp kamu", type=["txt"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        chats = parse_whatsapp_txt(tmp_path)
        st.session_state.chats = chats
        st.session_state.user_names = list(set(c['sender'] for c in chats))
        progress = st.progress(0, text="Proses embedding chat...")
        def update_progress(percent):
            progress.progress(percent, text=f"Embedding... {percent}%")
        embedder = ChatEmbedder()
        embedder.embed_chats(chats, progress_callback=update_progress)
        embedder.save()
        progress.progress(100, text="Embedding selesai!")
        st.session_state.index_built = True
        st.success("Chat berhasil diupload dan index sudah dibuat!")
        st.rerun()
else:
    # Pilih peran dan lawan bicara
    if st.session_state.peran is None or st.session_state.lawan is None:
        st.markdown("## Pilih Peran dan Lawan Bicara")
        col1, col2 = st.columns(2)
        with col1:
            peran = st.selectbox("Sebagai siapa kamu?", st.session_state.user_names)
        with col2:
            lawan = st.selectbox("Jawaban AI sebagai siapa?", [n for n in st.session_state.user_names if n != peran])
        if st.button("Mulai Chat", use_container_width=True):
            st.session_state.peran = peran
            st.session_state.lawan = lawan
            st.rerun()
    else:
        st.markdown(f"## Chat WhatsApp dengan AI sebagai {st.session_state.lawan}")
        st.markdown("<div class='wa-chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            sender = chat['sender']
            msg = chat['message']
            align = 'right' if sender == st.session_state.peran else 'left'
            bubble_class = f"wa-bubble-{align}"
            sender_class = "wa-sender"
            st.markdown(f'<div class="wa-chatbox"><span class="{sender_class}">{sender}</span><br><span class="{bubble_class}">{msg}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.form(key="wa-chat-form"):
            question = st.text_input("Ketik pesan kamu...", key="chat_input")
            col_send, col_reset = st.columns([3,1])
            send_clicked = col_send.form_submit_button("Kirim")
            reset_clicked = col_reset.form_submit_button("Reset Chat")
            if send_clicked and question:
                st.session_state.chat_history.append({"sender": st.session_state.peran, "message": question})
                with st.spinner(f"{st.session_state.lawan} sedang mengetik..."):
                    retriever = ChatRetriever()
                    contexts = retriever.search(question, top_k=5)
                    # Ekstrak gaya bahasa lawan dari chat history
                    style = extract_user_style(st.session_state.chats, st.session_state.lawan)
                    # Buat deskripsi gaya bahasa dan analisis tambahan
                    style_desc = f"Gaya bahasa {st.session_state.lawan}: "
                    if style['top_words']:
                        style_desc += f"Kata sering dipakai: {', '.join(w for w,_ in style['top_words'])}. "
                    if style['top_emojis']:
                        style_desc += f"Emoji sering dipakai: {', '.join(e for e,_ in style['top_emojis'])}. "
                    style_desc += f"Panjang rata-rata pesan: {int(style['avg_length'])} karakter. "
                    style_desc += f"Emosi dominan: {style['emosi']}. "
                    style_desc += f"Gaya formalitas: {style['formalitas']}."
                    # Gabungkan ke prompt
                    prompt = build_prompt(contexts, question, st.session_state.peran, st.session_state.lawan, max_tokens=2000)
                    prompt = f"{style_desc}\n{prompt}"
                    answer = ask_huggingface(prompt)
                    st.session_state.chat_history.append({"sender": st.session_state.lawan, "message": answer})
                st.rerun()
            if reset_clicked:
                st.session_state.chat_history = []
                st.session_state.peran = None
                st.session_state.lawan = None
                st.rerun()
