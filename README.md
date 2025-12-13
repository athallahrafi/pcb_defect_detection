# PCB Defect Detection System (Sistem Deteksi Cacat PCB)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Status](https://img.shields.io/badge/Status-Educational%20Project-orange)

Project ini adalah tugas kelompok untuk mata kuliah **Teknik Pengolahan Citra**. Sistem ini dirancang untuk mendeteksi cacat pada *Printed Circuit Board* (PCB) seperti jalur putus (*open*) atau korsleting (*short*) menggunakan metode **Image Subtraction** dan **Morphological Processing**.

Sistem ini mensimulasikan prinsip kerja mesin **AOI (Automated Optical Inspection)** sederhana yang digunakan di industri elektronik.

## 📋 Daftar Isi
- [Latar Belakang](#-latar-belakang)
- [Metode & Algoritma](#-metode--algoritma)
- [Struktur Project](#-struktur-project)
- [Instalasi & Penggunaan](#-instalasi--penggunaan)
- [Anggota Kelompok](#-anggota-kelompok)

## 🔍 Latar Belakang
Inspeksi manual pada jalur PCB memakan waktu dan rentan terhadap kesalahan manusia (*human error*). Project ini bertujuan untuk mengotomatisasi proses tersebut dengan membandingkan citra PCB hasil produksi (*Test Image*) terhadap citra referensi standar (*Golden Sample*).

## 🛠 Metode & Algoritma
Alur pemrosesan citra yang digunakan adalah sebagai berikut:

1.  **Image Registration (Alignment):** Menyelaraskan posisi dan orientasi citra uji agar presisi dengan citra referensi.
2.  **Grayscaling:** Konversi citra ke format keabuan untuk efisiensi komputasi.
3.  **Image Subtraction:** Mengurangi nilai piksel citra referensi dengan citra uji untuk mendapatkan selisih absolut.
    * Rumus: `Diff = |Reference - Test|`
4.  **Binary Thresholding:** Mengkonversi hasil pengurangan menjadi citra biner (Hitam/Putih) untuk memisahkan *defect* dari *background*.
5.  **Morphological Opening:** Membersihkan *noise* kecil menggunakan operasi erosi dan dilasi.
6.  **Decision Logic:** Menghitung luas area putih. Jika `Area > 0`, maka PCB dinyatakan **REJECT/DEFECT**.

## 🖼️ Output
<img src="https://github.com/athallahrafi/pcb_defect_detection/blob/main/output.png" width="200">

