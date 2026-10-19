# Algoritma Smart Parcel Locker

Dokumen ini menjelaskan perilaku yang terdapat pada [program final](../WI1102_ProjekI_31_12.py). Angka baris merujuk pada berkas tersebut. Diagram lengkap tersedia pada [flowchart gabungan](Flowchart_Gabungan_Smart_Locker.svg); penjelasan laporan terdapat pada Bab 2–4 [laporan final](../documents/WI1102_ProjekI_31_12.pdf).

## 1. Inisialisasi dan hubungan data

Pada [baris 17–27](../WI1102_ProjekI_31_12.py#L17-L27), enam loker diwakili oleh sembilan list paralel. Indeks `i` yang sama menyatukan identitas, tipe, dimensi, status, nama, telepon, dan kode satu loker.

| Indeks | ID | Tipe | H × V × D (cm) |
|---:|---|---|---|
| 0 | L01 | D | 30 × 20 × 45 |
| 1 | L02 | D | 30 × 20 × 45 |
| 2 | L03 | C | 30 × 30 × 45 |
| 3 | L04 | C | 30 × 30 × 45 |
| 4 | L05 | B | 30 × 40 × 45 |
| 5 | L06 | A | 20 × 60 × 45 |

Awalnya semua `status` bernilai `Kosong`, sedangkan `nama`, `telepon`, dan `kode` berisi string kosong. `nomor_kode` dimulai dari 1001. Daftar dimensi paket dan data penerima sementara dibuat kembali ketika menu titip dipilih.

Aturan konsistensi yang dipertahankan:

1. Loker kosong tidak mempunyai nama, telepon, atau kode transaksi aktif.
2. Loker terisi mempunyai satu catatan penerima dan satu kode aktif.
3. Penitipan dan pengambilan memperbarui data pada satu indeks yang sama.
4. Jumlah loker kosong ditambah terisi selalu enam.
5. Kode aktif tidak berulang dalam satu sesi. Pengambilan tidak mengurangi `nomor_kode`.

## 2. Menu utama

Perulangan `while berjalan == True` pada [baris 49](../WI1102_ProjekI_31_12.py#L49) mempertahankan menu selama sesi berlangsung.

```text
Mulai
  Inisialisasi data dan cari batas dimensi
  Selama berjalan:
    Tampilkan menu dan baca pilihan
    Jika 1: proses penitipan
    Jika 2: proses pengambilan
    Jika 3: tampilkan ketersediaan
    Jika 4: berjalan = False
    Selain itu: tampilkan menu tidak valid
Selesai
```

Penitipan, pengambilan, status, dan pilihan tidak valid kembali ke menu setelah prosesnya selesai. Pilihan `4` menghentikan sesi. Program tidak menyimpan data ke berkas atau database.

## 3. Validasi dimensi

Program mencari sisi terpanjang seluruh loker melalui [baris 31–39](../WI1102_ProjekI_31_12.py#L31-L39). Hasilnya `batas_dimensi = 60`. Panjang, lebar, dan tinggi memakai batas yang sama karena perannya dapat bertukar ketika paket diputar.

Pada [baris 58–81](../WI1102_ProjekI_31_12.py#L58-L81), `for j in range(3)` mengisi tiga sisi paket. Setiap sisi mempunyai `while` untuk meminta ulang masukan sampai valid. Karakter dibaca satu per satu; hanya digit ASCII `0` sampai `9` diterima. Nilai dibentuk bertahap dan tidak diperbesar lagi setelah masukan dinyatakan tidak valid.

| Masukan | Hasil |
|---|---|
| `1`, `20`, `60` | Diterima sebagai dimensi |
| `00060` | Diterima sebagai 60 |
| Kosong, `0`, `-2`, `2.5`, `1e1`, huruf, atau spasi | Ditolak; sisi yang sama diminta ulang |
| `61`, `9999`, atau angka lain di atas 60 | Ditolak; sisi yang sama diminta ulang |

Lolos validasi input belum berarti paket muat. `60 × 60 × 60` valid sebagai tiga bilangan 1–60, tetapi tidak memenuhi ukuran loker mana pun.

## 4. Enam orientasi dan pencarian loker

Misalkan paket berukuran `p × l × t` dan sebuah loker mempunyai batas `H × V × D`. Enam susunan sisi diperiksa pada [baris 89–95](../WI1102_ProjekI_31_12.py#L89-L95):

| Orientasi | Terhadap H | Terhadap V | Terhadap D |
|---:|---|---|---|
| 1 | p | l | t |
| 2 | p | t | l |
| 3 | l | p | t |
| 4 | l | t | p |
| 5 | t | p | l |
| 6 | t | l | p |

Untuk satu susunan `(a, b, c)`, paket muat jika `a <= H AND b <= V AND c <= D`. Hasil keenam susunan digabung dengan `OR`: cukup satu orientasi yang memenuhi seluruh batas sisi. Jika beberapa sisi paket sama, sebagian susunan mempunyai ukuran identik.

Contoh: paket `60 × 45 × 20` muat di tipe A `20 × 60 × 45` melalui orientasi kelima: `20 <= 20`, `60 <= 60`, dan `45 <= 45`. Kecocokan tepat batas diterima. Model tidak memasukkan kemiringan diagonal, bentuk yang dapat ditekan, atau toleransi celah pintu.

Pencarian menginisialisasi `indeks = -1`, kemudian menelusuri keenam loker. Sebuah loker dipilih jika tiga syarat terpenuhi:

```text
status[i] == "Kosong" AND muat == True AND indeks == -1
```

Syarat `indeks == -1` menjaga hasil pertama agar tidak diganti kandidat berikutnya. Perulangan tetap memeriksa seluruh enam indeks. Urutannya D, D, C, C, B, A; volume tidak menurun. B dan A sama volume, sehingga B diprioritaskan ketika keduanya kosong dan sama-sama muat.

Volume saja tidak membuktikan kecocokan. Paket `30 × 30 × 45` muat di C atau B, tetapi tidak pada A yang memiliki sisi 20 cm.

## 5. Penitipan dan perubahan transaksi

Alur lengkap terdapat pada [baris 57–130](../WI1102_ProjekI_31_12.py#L57-L130).

1. Baca dan validasi tiga dimensi paket.
2. Cari loker kosong pertama yang muat dalam setidaknya satu orientasi.
3. Jika tidak ditemukan, tampilkan pesan dan kembali ke menu. Tidak ada antrean atau perubahan transaksi.
4. Jika ditemukan, tampilkan ID dan tipe loker, lalu minta nama serta telepon penerima. Isian kosong atau seluruhnya spasi/tab diminta ulang.
5. Minta konfirmasi pembayaran simulasi. Jawaban selain `y`/`t` diminta ulang.
6. Jika `t`, batalkan penitipan tanpa memperbarui data loker atau penghitung kode.
7. Jika `y`, perbarui `status`, `nama`, `telepon`, dan `kode` pada indeks terpilih; kemudian tambah `nomor_kode` satu.
8. Tampilkan kode pengambilan dan kembali ke menu.

Pembaruan pada [baris 123–127](../WI1102_ProjekI_31_12.py#L123-L127) baru terjadi setelah konfirmasi berhasil:

```python
status[indeks] = "Terisi"
nama[indeks] = data_baru[0]
telepon[indeks] = data_baru[1]
kode[indeks] = "P" + str(nomor_kode)
nomor_kode = nomor_kode + 1
```

Telepon disimpan sebagai string agar nol di depan tetap ada. Format atau kepemilikan nomor tidak diperiksa. Kode hanya ditampilkan di terminal; tidak ada pengiriman pesan atau pembayaran sungguhan.

## 6. Pengambilan paket

Alur pengambilan berada pada [baris 132–159](../WI1102_ProjekI_31_12.py#L132-L159).

1. Hitung jumlah loker terisi. Jika nol, tampilkan bahwa belum ada paket dan kembali ke menu tanpa meminta kode.
2. Jika ada paket, baca kode dan cari kecocokan persis pada loker berstatus `Terisi`.
3. Jika tidak ditemukan, tampilkan pesan penolakan lalu kembali ke menu; data tidak berubah.
4. Jika ditemukan, minta konfirmasi pengambilan. Jawaban selain `y`/`t` diminta ulang.
5. Jika `t`, batalkan pengambilan dan pertahankan seluruh transaksi.
6. Jika `y`, ubah status menjadi `Kosong` dan hapus nama, telepon, serta kode pada indeks tersebut.

```python
status[indeks] = "Kosong"
nama[indeks] = ""
telepon[indeks] = ""
kode[indeks] = ""
```

Penghapusan kode membuat kode bekas tidak berlaku lagi. Loker yang telah kosong dapat digunakan untuk transaksi baru dengan nomor kode berikutnya. Kode transaksi lain tidak ikut berubah.

## 7. Ketersediaan loker

Pada [baris 161–188](../WI1102_ProjekI_31_12.py#L161-L188), program menelusuri semua indeks untuk menampilkan ID, tipe, dimensi, dan status. Pencacah menghitung total kosong/terisi dan jumlah kosong setiap tipe.

Menu ini hanya membaca data. Nama penerima, nomor telepon, dan kode aktif tidak ditampilkan pada tabel ketersediaan.

## 8. Contoh penelusuran indeks

Tiga paket kecil `10 × 10 × 10` dititipkan berturut-turut dengan konfirmasi `y`. Dua paket pertama mengisi L01 dan L02. Pada paket ketiga, proses pencarian berjalan sebagai berikut:

| i | ID | Status sebelum pencarian | Muat? | Nilai `indeks` setelah diperiksa |
|---:|---|---|---|---:|
| 0 | L01 | Terisi | Ya | -1 |
| 1 | L02 | Terisi | Ya | -1 |
| 2 | L03 | Kosong | Ya | 2 |
| 3 | L04 | Kosong | Ya | 2 |
| 4 | L05 | Kosong | Ya | 2 |
| 5 | L06 | Kosong | Ya | 2 |

Setelah konfirmasi, hanya data transaksi pada indeks 2 yang diisi; `kode[2]` menjadi `P1003`. Penelusuran ini diuji melalui skenario `fallback_after_D_full` dalam [hasil pengujian](../tests/Hasil_Uji_Program.txt).

## 9. Hubungan diagram dan kode

Flowchart gabungan memakai konektor untuk menjaga alur satu diagram tetap terbaca. `M` kembali ke menu, sedangkan `T`, `A`, dan `K` menuju cabang titip, ambil, dan ketersediaan. Jalur input tidak valid kembali ke masukan terkait; jalur pembatalan kembali ke menu tanpa perubahan transaksi.

Dalam diagram, pemeriksaan kondisi menggunakan bentuk keputusan, input/output menggunakan jajar genjang, dan perubahan list menggunakan kotak proses. Setelah pengambilan berhasil, pembersihan seluruh data transaksi ditunjukkan sebelum pesan keberhasilan.

Dokumen ini menjelaskan implementasi saat ini. Database, autentikasi, layanan notifikasi, pembayaran nyata, dan perangkat loker fisik berada di luar ruang lingkup program.
