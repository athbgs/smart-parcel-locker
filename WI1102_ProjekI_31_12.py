# Simulasi pembelajaran; bukan perangkat lunak resmi PopBox.
# Enam loker dan ukurannya adalah asumsi simulasi, bukan hasil observasi.
# Rotasi berarti pertukaran arah sisi; model mengabaikan celah pintu.

# KAMUS
# id_loker, jenis, status, nama, telepon, kode : array of string
# sisi_h, sisi_v, sisi_d, dimensi : array of integer
# label_dimensi, label_data, data_baru : array of string
# pilihan, masukan, karakter, bayar, kode_masuk, ambil : string
# i, j, indeks, p, l, t, nomor_kode : integer
# batas_dimensi, nilai_dimensi : integer
# jumlah_kosong, jumlah_terisi, kosong_a, kosong_b : integer
# kosong_c, kosong_d : integer
# berjalan, valid, ada_isi, muat : boolean

# ALGORITMA
id_loker = ["L01", "L02", "L03", "L04", "L05", "L06"]
jenis = ["D", "D", "C", "C", "B", "A"]
sisi_h = [30, 30, 30, 30, 30, 20]
sisi_v = [20, 20, 30, 30, 40, 60]
sisi_d = [45, 45, 45, 45, 45, 45]
status = ["Kosong", "Kosong", "Kosong", "Kosong", "Kosong", "Kosong"]
nama = ["", "", "", "", "", ""]
telepon = ["", "", "", "", "", ""]
kode = ["", "", "", "", "", ""]
label_dimensi = ["Panjang", "Lebar", "Tinggi"]
label_data = ["Nama penerima", "Telepon penerima"]
nomor_kode = 1001
berjalan = True

# Semua arah input memakai batas sisi terbesar karena paket dapat diputar.
batas_dimensi = 0
for i in range(6):
    if sisi_h[i] > batas_dimensi:
        batas_dimensi = sisi_h[i]
    if sisi_v[i] > batas_dimensi:
        batas_dimensi = sisi_v[i]
    if sisi_d[i] > batas_dimensi:
        batas_dimensi = sisi_d[i]

print("SIMULASI LOKER PAKET")
print("Terinspirasi PopBox; seluruh proses merupakan simulasi.")
print("Asumsi: 6 loker; satu loker menampung satu paket.")
print("Ukuran dalam cm, rotasi sisi diperbolehkan.")
print("Urutan alokasi: D, D, C, C, B, A; B/A sama volume.")
print("Pembayaran dan notifikasi hanya simulasi.")
print("Data serta kode direset ketika program dimulai ulang.")

while berjalan == True:
    print("\nMENU UTAMA")
    print("1. Titip/Kirim paket")
    print("2. Ambil paket")
    print("3. Ketersediaan loker")
    print("4. Keluar")
    pilihan = input("Pilih menu (1-4): ")

    if pilihan == "1":
        dimensi = [0, 0, 0]
        for j in range(3):
            valid = False
            while valid == False:
                masukan = input(label_dimensi[j] + " paket (bulat 1-"
                                + str(batas_dimensi) + " cm): ")
                valid = masukan != ""
                nilai_dimensi = 0
                for karakter in masukan:
                    # Setelah tidak valid, nilai tidak diperbesar lagi.
                    if valid == True:
                        if karakter < "0" or karakter > "9":
                            valid = False
                        else:
                            nilai_dimensi = nilai_dimensi * 10 + int(karakter)
                            if nilai_dimensi > batas_dimensi:
                                valid = False
                if nilai_dimensi <= 0:
                    valid = False
                if valid == False:
                    print("Ukuran harus bilangan bulat 1-"
                          + str(batas_dimensi) + " cm.")
                else:
                    dimensi[j] = nilai_dimensi

        p = dimensi[0]
        l = dimensi[1]
        t = dimensi[2]
        indeks = -1
        # Urutan volume naik; bila volume sama, B diprioritaskan atas A.
        for i in range(6):
            muat = (
                (p <= sisi_h[i] and l <= sisi_v[i] and t <= sisi_d[i]) or
                (p <= sisi_h[i] and t <= sisi_v[i] and l <= sisi_d[i]) or
                (l <= sisi_h[i] and p <= sisi_v[i] and t <= sisi_d[i]) or
                (l <= sisi_h[i] and t <= sisi_v[i] and p <= sisi_d[i]) or
                (t <= sisi_h[i] and p <= sisi_v[i] and l <= sisi_d[i]) or
                (t <= sisi_h[i] and l <= sisi_v[i] and p <= sisi_d[i])
            )
            if status[i] == "Kosong" and muat == True and indeks == -1:
                indeks = i

        if indeks == -1:
            print("Tidak ada loker kosong yang cukup untuk paket.")
            print("Kembali ke menu utama; tidak ada antrean dalam simulasi.")
        else:
            print("Loker terpilih:", id_loker[indeks], "| Tipe:", jenis[indeks])
            data_baru = ["", ""]
            for j in range(2):
                ada_isi = False
                while ada_isi == False:
                    data_baru[j] = input(label_data[j] + ": ")
                    for karakter in data_baru[j]:
                        if karakter != " " and karakter != "\t":
                            ada_isi = True
                    if ada_isi == False:
                        print("Isian tidak boleh kosong atau hanya spasi.")

            bayar = input("Pembayaran simulasi berhasil? (y/t): ")
            while bayar != "y" and bayar != "t":
                print("Jawaban harus y atau t.")
                bayar = input("Pembayaran simulasi berhasil? (y/t): ")
            if bayar == "t":
                print("Penitipan dibatalkan. Data loker tidak berubah.")
            else:
                status[indeks] = "Terisi"
                nama[indeks] = data_baru[0]
                telepon[indeks] = data_baru[1]
                kode[indeks] = "P" + str(nomor_kode)
                nomor_kode = nomor_kode + 1
                print("Paket tersimpan di " + id_loker[indeks] + ".")
                print("Notifikasi simulasi: kode ambil " + kode[indeks])
                print("Catat kode ini; tidak ada pesan sungguhan dikirim.")

    elif pilihan == "2":
        jumlah_terisi = 0
        for i in range(6):
            if status[i] == "Terisi":
                jumlah_terisi = jumlah_terisi + 1
        if jumlah_terisi == 0:
            print("Tidak ada paket tersimpan.")
        else:
            kode_masuk = input("Masukkan kode ambil (contoh P1001): ")
            indeks = -1
            for i in range(6):
                if status[i] == "Terisi" and kode[i] == kode_masuk:
                    indeks = i
            if indeks == -1:
                print("Kode tidak ditemukan atau sudah digunakan.")
            else:
                ambil = input("Konfirmasi pengambilan paket? (y/t): ")
                while ambil != "y" and ambil != "t":
                    print("Jawaban harus y atau t.")
                    ambil = input("Konfirmasi pengambilan paket? (y/t): ")
                if ambil == "t":
                    print("Pengambilan dibatalkan. Data tidak berubah.")
                else:
                    status[indeks] = "Kosong"
                    nama[indeks] = ""
                    telepon[indeks] = ""
                    kode[indeks] = ""
                    print("Paket diambil.", id_loker[indeks], "kosong.")

    elif pilihan == "3":
        print("\nKETERSEDIAAN LOKER")
        print("ID | Tipe | H x V x D (cm) | Status")
        jumlah_kosong = 0
        jumlah_terisi = 0
        kosong_a = 0
        kosong_b = 0
        kosong_c = 0
        kosong_d = 0
        for i in range(6):
            print(id_loker[i], "|", jenis[i], "|", sisi_h[i], "x",
                  sisi_v[i], "x", sisi_d[i], "|", status[i])
            if status[i] == "Kosong":
                jumlah_kosong = jumlah_kosong + 1
                if jenis[i] == "A":
                    kosong_a = kosong_a + 1
                elif jenis[i] == "B":
                    kosong_b = kosong_b + 1
                elif jenis[i] == "C":
                    kosong_c = kosong_c + 1
                else:
                    kosong_d = kosong_d + 1
            else:
                jumlah_terisi = jumlah_terisi + 1
        print("Total kosong:", jumlah_kosong)
        print("Total terisi:", jumlah_terisi)
        print("Kosong D:", kosong_d, "| C:", kosong_c,
              "| B:", kosong_b, "| A:", kosong_a)

    elif pilihan == "4":
        berjalan = False
        print("Simulasi selesai. Data tidak disimpan permanen.")
    else:
        print("Menu tidak valid. Pilih angka 1 sampai 4.")
