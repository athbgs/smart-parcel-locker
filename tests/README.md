# Pengujian Smart Parcel Locker

Alat uji ini terpisah dari program utama. Program utama memakai materi dasar WI1102; alat uji menggunakan teknik Python yang lebih lanjut untuk memeriksa perilakunya.

Jalankan dari akar repositori dengan Python 3.9 atau lebih baru dan data zona waktu `Asia/Jakarta` tersedia:

```sh
python3 tests/test_smart_locker.py
```

Perintah ini memeriksa 44 skenario input terminal, kondisi akhir list, keunikan kode aktif, 262.144 keputusan pada blok alokasi, serta konstruksi sintaks program. Berkas `code_test_results.json` dan `Hasil_Uji_Program.txt` akan diperbarui dengan hasil dan waktu eksekusi terbaru. Program berhenti dengan kode 0 jika seluruh pemeriksaan lulus dan 1 jika ada kegagalan.

| Bukti | Isi |
|---|---|
| [Ringkasan terbaru](Hasil_Uji_Program.txt) | Nama, tujuan, dan hasil setiap skenario |
| [Hasil lengkap terbaru](code_test_results.json) | Masukan, keluaran, kondisi akhir list, dan SHA-256 kode |
| [Hasil final awal](evidence/2026-10-19_original_results.json) | Arsip hasil pengujian pada 19 Oktober 2026, sekitar 20.16 WIB |
| [Ringkasan final awal](evidence/2026-10-19_original_summary.txt) | Ringkasan arsip yang sama |

Hasil terbaru disiapkan ulang pada 19 Oktober 2026, 22.59 WIB: **44/44 skenario lulus**, **262.144 pemeriksaan alokasi cocok**, dan pemeriksaan sintaks lulus. Semua nama dan nomor telepon pada skenario adalah data contoh.

Angka 262.144 berasal dari 16 nilai per sisi, sehingga terdapat 4.096 kombinasi ukuran, dikalikan 64 pola terisi/kosong untuk enam loker. Ini bukan jumlah transaksi lengkap dan bukan pengujian seluruh ukuran. Nilai 61 diuji sebagai kasus negatif pada blok alokasi; program terminal menolak input di atas 60 cm.

Pengujian tidak mencakup perangkat fisik, pembayaran, pengiriman notifikasi, penyimpanan permanen, atau uji kegunaan bersama pengguna.

[Kembali ke halaman utama](../README.md)
