# Referensi dan asal rancangan

Daftar ini mengikuti sumber pada [laporan final](../documents/WI1102_ProjekI_31_12.pdf), khususnya daftar pustaka pada halaman PDF 18. Sumber publik berikut dicatat diakses pada **19 Oktober 2026** dalam laporan. Materi kuliah dan contoh laporan yang dibagikan kepada kelompok tidak diunggah ulang di repositori ini.

## Ketentuan tugas dan materi kuliah

1. **WI1102.** *Deskripsi Projek I Semester 1 Tahun Akademik 2026/2027.* Bahan tugas kelompok, 13 halaman. Rancangan dan implementasi: hlm. 6–8; ketentuan pengumpulan: hlm. 9–12. Digunakan sebagai acuan ruang lingkup, komponen program, laporan, dan presentasi.
2. **WI1102.** *Modul Berpikir Komputasional Python 2026/2027*, berkas `python.pdf`, 25 halaman. Input: hlm. 5; kondisional: hlm. 10; loop, array, dan string: hlm. 13–16. Digunakan untuk menjaga implementasi pada materi dasar yang dipelajari.

## Konteks loker paket

3. **Kelompok 12.** *Dokumentasi visual PopBox Louvin Jatinangor.* Berkas `IMG_6670` sampai `IMG_6680`, arsip proyek 12 Oktober 2026. Dokumentasi memperlihatkan eksterior dan layar. Dimensi loker tidak diukur; foto tidak membuktikan keberhasilan transaksi atau pembayaran.
4. **PopBox Asia.** [Help Center](https://popbox.asia/help-center). Acuan gambaran layanan kirim, titip, dan ambil serta pengambilan dengan kode PIN. Program kelompok hanya menyimulasikan sebagian logikanya.
5. **PopBox Asia.** [Lokasi PopBox](https://popbox.asia/locations). Acuan keberadaan entri Apartemen Louvin Jatinangor dan Apartemen Louvin Jatinangor 2.

Enam loker, pembagian tipe, dan angka dimensinya adalah parameter simulasi. Angka tersebut tidak diperlakukan sebagai spesifikasi resmi PopBox atau hasil pengukuran lapangan.

## Berpikir komputasional dan Python

6. **Wing, J. M.** (2006). *Computational Thinking*. Communications of the ACM, 49(3), 33–35. [DOI: 10.1145/1118178.1118215](https://doi.org/10.1145/1118178.1118215). Acuan pembahasan abstraksi dan dekomposisi.
7. **Python Software Foundation.** [The Python Tutorial — An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html), bagian 3.1.3 dan 3.2. Acuan sifat list yang dapat diubah serta dasar pemrograman Python.
8. **Python Software Foundation.** [The Python Tutorial — More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html), bagian 4.1–4.3. Acuan kondisional, perulangan `for`, dan `range`.
9. **Rancangan rekan kelompok.** `Proyek Smart Locker.py`, berkas yang dibagikan untuk review. Dimensi loker dan gagasan rotasi diadaptasi; inventori enam loker, list paralel, dan alur transaksi ditetapkan dalam model kelompok.

## Acuan penyajian laporan

10. **Kelompok 6.** (2024). *Sistem Pemesanan Shuttle Bus Antarkampus ITB Jatinangor Ganesha*, `Contoh Laporan Proyek I.pdf`, halaman PDF 4–7. Acuan penyusunan asumsi dan dekomposisi.
11. **Program Python Dating Kampus 2025.** `laporanberkom.pdf`, halaman PDF 10–15. Acuan penyajian hubungan konsep, kode, dan keluaran.
12. **Kelompok 09 WI1102.** (2024). *ATEAM Sistem Proses Transaksi ATM*. [Repositori parkuskus/Tubes-Berkom-1](https://github.com/parkuskus/Tubes-Berkom-1/), commit `8b29012a`; laporan halaman PDF 7–11. Acuan pengorganisasian dokumentasi proyek dan penyajian laporan.

Ketiga contoh digunakan sebagai acuan penyajian. Isi kasus, identitas kelompok, hasil pengujian, dan implementasi ATM, shuttle, atau dating tidak diambil sebagai hasil proyek Smart Parcel Locker.

## Pengujian dan permutasi

13. **International Software Testing Qualifications Board.** (2024). [Certified Tester Foundation Level Syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), 15 September 2024. Prinsip pengujian: hlm. 17–18; TDD: hlm. 26; nilai batas dan transisi keadaan: hlm. 40–42. Digunakan untuk menjelaskan pendekatan pengujian, bukan sebagai sertifikasi program.
14. **Abramson, J., dkk.** (2021). *Precalculus 2e*, OpenStax, Rice University. [Bagian 11.5 — Counting Principles](https://openstax.org/books/precalculus-2e/pages/11-5-counting-principles). Acuan jumlah permutasi tiga arah sisi: `3! = 6`.

## Bukti implementasi kelompok

- [Kode Python](../WI1102_ProjekI_31_12.py) menjadi sumber perilaku yang didokumentasikan.
- [Hasil uji terperinci](../tests/code_test_results.json) mencatat versi sumber, masukan, keluaran, dan keadaan akhir list pada 44 skenario.
- [Ringkasan uji](../tests/Hasil_Uji_Program.txt) membedakan skenario program lengkap dari 262.144 pemeriksaan blok alokasi.
- [Rekaman terminal](Contoh_Demo.txt) memuat contoh eksekusi dengan data penerima contoh.
- [Video presentasi](https://drive.google.com/file/d/1F4LFyakFaFF9PxFglL3AjJ7lagQiUMqt/view) memuat presentasi dan demo kelompok. Rekaman video dan transkrip demo terminal merupakan dua sesi yang berbeda.

Bantuan AI dalam revisi program, pengujian otomatis, ilustrasi, dan penulisan dicatat pada laporan. Sumber eksternal digunakan sesuai perannya; klaim tentang perilaku program didasarkan pada kode dan hasil pengujian kelompok.
