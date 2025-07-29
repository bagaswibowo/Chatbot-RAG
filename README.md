# Chatbot-RAG

Chatbot-RAG adalah aplikasi chatbot berbasis Retrieval-Augmented Generation (RAG) yang dapat menjawab pertanyaan berdasarkan riwayat chat WhatsApp Anda. Aplikasi ini dijalankan menggunakan Streamlit dan dapat digunakan secara lokal maupun di Streamlit Cloud.

## Fitur Utama
- Upload file chat WhatsApp (.txt) dan buat index pencarian otomatis
- Chatbot dapat menjawab pertanyaan dengan konteks dari chat Anda
- Ekstraksi gaya bahasa lawan bicara (kata, emoji, emosi, formalitas, dll)
- Pilih peran (sebagai siapa Anda dan lawan bicara AI)

## Struktur Proyek
- `app.py` : Entry point aplikasi Streamlit
- `embedder.py` : Modul untuk embedding chat
- `generator.py` : Modul untuk menghasilkan jawaban
- `parser.py` : Modul untuk parsing chat WhatsApp
- `retriever.py` : Modul untuk pencarian chat relevan
- `style_extractor.py` : Modul ekstraksi gaya bahasa
- `requirements.txt` : Daftar dependensi Python

## Cara Menjalankan

1. **Clone repository dan masuk ke folder proyek**
   ```bash
   git clone https://github.com/bagaswibowo/Chatbot-RAG.git
   cd Chatbot-RAG
   ```

2. **(Opsional) Buat dan aktifkan virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi dengan Streamlit**
   ```bash
   streamlit run app.py
   ```

5. **Akses aplikasi**
   Buka browser dan akses URL yang muncul di terminal, biasanya `http://localhost:8501`

## Cara Menggunakan Aplikasi
1. Upload file chat WhatsApp Anda (.txt) pada halaman utama aplikasi.
2. Tunggu proses embedding dan pembuatan index selesai (akan muncul notifikasi sukses).
3. Pilih peran (sebagai siapa Anda dan lawan bicara AI) dari daftar nama yang terdeteksi di chat.
4. Mulai chat dengan mengetik pertanyaan atau pesan di kolom input.
5. AI akan menjawab dengan gaya bahasa lawan bicara yang dipilih, berdasarkan riwayat chat Anda.
6. Jika ingin memulai ulang, klik tombol "Reset Chat".

**Catatan:**
- Data chat dan index hanya tersimpan selama aplikasi berjalan (khususnya di Streamlit Cloud).

## Fitur Lain
- Mendukung multi-user (pilih peran dan lawan bicara)
- Analisis gaya bahasa otomatis
- Chatbot tetap menjaga privasi data Anda

