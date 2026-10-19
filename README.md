# Smart Parcel Locker

Proyek I **WI1102 Berpikir Komputasional** — Kelas 31, Kelompok 12.

Simulasi loker paket melalui terminal, terinspirasi alur layanan PopBox. Program menggunakan sekuens, kondisional, perulangan, dan array yang direpresentasikan dengan list Python.

**[Buka source code](WI1102_ProjekI_31_12.py)**

## Menjalankan program

Unduh file Python di atas, buka terminal pada folder tempat file disimpan, lalu jalankan:

```sh
python3 WI1102_ProjekI_31_12.py
```

Program memerlukan Python 3 dan tidak membutuhkan pustaka tambahan.

## Fitur

- **Titip/kirim paket:** memeriksa dimensi dalam enam orientasi, memilih loker kosong pertama yang sesuai, lalu menyimpan data penerima dan kode pengambilan setelah konfirmasi pembayaran simulasi.
- **Ambil paket:** mencari kode yang masih aktif, meminta konfirmasi, lalu mengosongkan loker beserta data transaksinya.
- **Ketersediaan loker:** menampilkan ukuran dan status setiap loker, total kosong/terisi, serta jumlah loker kosong per tipe.
- **Validasi input:** setiap dimensi harus berupa bilangan bulat 1–60 cm; nama dan telepon tidak boleh kosong atau hanya berisi spasi/tab; konfirmasi memakai `y` atau `t`.

Data loker disimpan dalam list paralel. Indeks yang sama merujuk pada loker yang sama pada seluruh list. Pencarian dan pembaruan data menggunakan `for`, sedangkan menu dan pengulangan input menggunakan `while`.

## Inventori simulasi

| ID loker | Tipe | H × V × D (cm) |
|---|---|---|
| L01, L02 | D | 30 × 20 × 45 |
| L03, L04 | C | 30 × 30 × 45 |
| L05 | B | 30 × 40 × 45 |
| L06 | A | 20 × 60 × 45 |

Pemeriksaan mengikuti urutan L01–L06. Tipe B dan A memiliki volume yang sama; B diperiksa lebih dahulu. Batas input 60 cm berasal dari sisi terbesar inventori dan berlaku pada ketiga dimensi karena paket dapat diputar. Lolos validasi input belum berarti paket pasti muat: ketiga sisinya tetap dibandingkan dengan ukuran loker dalam enam orientasi.

## Batas simulasi

Jumlah dan ukuran loker merupakan asumsi proyek, bukan spesifikasi resmi atau hasil pengukuran PopBox. Setiap loker menampung satu paket berbentuk balok. Rotasi berupa pertukaran arah sisi; model tidak memperhitungkan celah pintu.

Pembayaran dan notifikasi hanya ditampilkan di terminal. Program tidak terhubung dengan pintu fisik, sensor, layanan pembayaran, atau pengiriman pesan. Nomor telepon hanya diperiksa agar tidak kosong, bukan diverifikasi sebagai nomor yang aktif. Data dan urutan kode pengambilan kembali ke kondisi awal ketika program dijalankan ulang.

## Pengujian versi final

Pengujian otomatis pada **19 Oktober 2026** mencatat **44 dari 44 skenario perilaku lulus**. Pemeriksaan terpisah pada blok alokasi menghasilkan **262.144 kecocokan** dengan pemeriksa pembanding: 4.096 kombinasi ukuran × 64 pola keterisian. Angka kedua merupakan pemeriksaan blok alokasi, bukan jumlah transaksi yang dijalankan melalui menu.

SHA-256 source code yang diuji:

```text
bc986a4a9cf8564d3b2ed7a305c99e4854f5eb2dd9b54e5a72a665ccf521cb21
```
