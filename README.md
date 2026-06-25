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
