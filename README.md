# Chatbot-RAG

Chatbot-RAG adalah aplikasi chatbot berbasis Retrieval-Augmented Generation (RAG) yang dapat menjawab pertanyaan dengan menggabungkan kemampuan retrieval dan generative AI. Aplikasi ini dijalankan menggunakan Streamlit.

## Fitur
- Mengambil informasi dari sumber data menggunakan retriever
- Mengekstrak dan mengolah data menggunakan parser dan style extractor
- Menghasilkan jawaban menggunakan model generatif
- Mendukung embedding untuk pencarian yang lebih relevan

## Struktur Proyek
- `app.py` : Entry point aplikasi Streamlit
- `embedder.py` : Modul untuk embedding dokumen
- `generator.py` : Modul untuk menghasilkan jawaban
- `parser.py` : Modul untuk parsing data
- `retriever.py` : Modul untuk mengambil data relevan
- `style_extractor.py` : Modul untuk ekstraksi gaya penulisan
- `requirements.txt` : Daftar dependensi Python

## Cara Menjalankan

1. **Clone repository dan masuk ke folder proyek**
   ```bash
   git clone <url-repo-anda>
   cd Chatbot-RAG
   ```

2. **Buat dan aktifkan virtual environment (opsional tapi direkomendasikan)**
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

## Catatan
- Pastikan semua file modul (`embedder.py`, `generator.py`, dll) berada dalam satu folder yang sama dengan `app.py`.
- Jika ingin menambah data atau mengubah sumber data, modifikasi file dan fungsi pada `parser.py` dan `retriever.py`.
- Untuk pengembangan lebih lanjut, pastikan untuk menambah dependensi baru ke `requirements.txt`.

## Kontak
Untuk pertanyaan atau kontribusi, silakan hubungi [email Anda] atau buat issue/pull request di repository ini.
