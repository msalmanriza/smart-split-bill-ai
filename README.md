# Smart Split Bill AI

## Smart Split Bill AI adalah aplikasi berbasis AI yang digunakan untuk membaca struk belanja secara otomatis dan menghitung pembagian tagihan berdasarkan item yang dipilih oleh masing-masing peserta.

## Features
Upload receipt image

AI receipt extraction

Multi participant support

Item assignment

Automatic bill splitting

Split visualization using pie chart

Final report and validation

## Technologies
Python

Streamlit

Google Gemini

Donut OCR

Matplotlib

## Installation
pip install -r requirements.txt

## Run Application
streamlit run app.py

## Link Gdrive
dikarnakan file nya besar akses link gdrive dibawah ini:

https://drive.google.com/drive/folders/1TAPqxYL_5DYH3eyCFy71zb1y4d9V-3Cs?usp=sharing

## Project Structure
SmartSplitBillAI

│

├── services

│   ├── donut_reader.py

│   └── gemini_reader.py

│

├── utils

│   └── split_calculator.py

│

├── sample_receipts

│

├── app.py

├── requirements.txt

├── README.md

└── .env

## Workflow
Upload Receipt

      ↓
      
Extract Receipt

      ↓
      
Add Participants

      ↓
      
Assign Items

      ↓
      
Calculate Split

      ↓
      
View Report

## Model Evaluation
## 1. Donut (naver-clova-ix/donut-base-finetuned-cord-v2)

### Advantages

-Dapat dijalankan secara lokal tanpa API.

-Tidak membutuhkan OCR tradisional seperti EasyOCR atau Tesseract.

-Cocok untuk prototype offline.

### Limitations

-Akurasi kurang stabil pada receipt Indonesia.

-Nama item sering tidak terbaca dengan baik.

-Nilai total terkadang tidak sesuai dengan isi receipt.

-Inference relatif lebih lambat karena model berjalan lokal.

## 2. Gemini 2.5 Flash

### Advantages

-Akurasi ekstraksi receipt lebih baik.

-Dapat mengenali nama produk, harga, subtotal, dan total bill dengan lebih konsisten.

-Proses parsing lebih sederhana karena output langsung berbentuk struktur data.

### Limitations

-Membutuhkan koneksi internet.

-Bergantung pada quota API.

-Dapat mengalami rate limit atau temporary unavailability.

Selected Model

### Untuk prototype akhir dipilih Gemini 2.5 Flash karena memberikan hasil ekstraksi receipt yang lebih akurat dibandingkan Donut pada data uji yang digunakan.
