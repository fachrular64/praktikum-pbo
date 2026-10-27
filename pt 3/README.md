# Sistem Kasir Kopi Kenangan

Program kasir kedai kopi sederhana pakai Python (OOP), dijalankan lewat terminal. Dibuat untuk Posttest PBO.

Ada dua jenis akun:
- **Admin**: bisa tambah, ubah, dan hapus menu, serta menambah akun kasir.
- **Kasir**: hanya bisa melihat menu dan melayani pesanan pelanggan.

Pengguna harus login dulu sebelum masuk ke menu utama.

## Cara Menjalankan

```
python kasir_kopi_kenangan.py
```

Akun untuk mencoba:

| Username | Password | Role |
|---|---|---|
| admin | admin123 | Admin |
| kasir1 | kasir123 | Kasir (shift Pagi) |
| kasir2 | kasir123 | Kasir (shift Malam) |

Akun kasir tambahan bisa dibuat oleh admin lewat menu "Tambah akun kasir baru" (password minimal 4 karakter).

## Struktur Class

- `Menu` (abstract class): induk dari `MinumanKopi` dan `MakananRingan`. Punya method abstract `hitung_harga_total()`.
- `MinumanKopi`: ada tambahan atribut `ukuran` dan `level_gula`. Harga naik sesuai ukuran (Small +0, Medium +3000, Large +6000).
- `MakananRingan`: ada tambahan atribut `jenis_kemasan`. Ada biaya kemasan Rp1.000.
- `Pengguna`: induk dari `Admin` dan `Kasir`. Menyimpan username dan password.
- `Admin`: punya atribut `level_akses`.
- `Kasir`: punya atribut `shift` dan method `layani_pelanggan()`.
- `Struk`: struk transaksi yang dibuat saat kasir melayani pesanan.
- `KopiKenangan`: class utama yang menyimpan daftar menu dan daftar pengguna, serta berisi method CRUD dan login.

## Inheritance

Ada dua pewarisan:

```
Menu (abstract)        Pengguna
 ├─ MinumanKopi         ├─ Admin
 └─ MakananRingan       └─ Kasir
```

- Semua subclass memanggil `super().__init__()` untuk mengisi atribut dari parent.
- Setiap subclass punya atribut sendiri (`ukuran`, `jenis_kemasan`, `level_akses`, `shift`).
- Method `hitung_harga_total()` dan `tampilkan_detail()` di-override di `MinumanKopi` dan `MakananRingan`. `tampilkan_detail()` juga di-override di `Admin` dan `Kasir`.
- Atribut protected `_harga_dasar` dan `_stok` ada di `Menu` dan dipakai langsung oleh subclass saat menghitung harga.
- Atribut private `__password` hanya ada di `Pengguna` dan diakses lewat property.

## Relasi UML

- **Asosiasi**: `Kasir` dan `Menu`. Kasir hanya memakai objek `Menu` lewat parameter di `layani_pelanggan()`, tidak menyimpannya.
- **Agregasi**: `KopiKenangan` dan `Menu`/`Pengguna`. Objek menu dan pengguna dibuat di luar, lalu dimasukkan ke `list_menu` dan `list_pengguna`. Kalau cabang dihapus, objek menu dan pengguna tetap ada.
- **Komposisi**: `Kasir` dan `Struk`. Objek `Struk` dibuat di dalam `layani_pelanggan()` dan hanya ada karena transaksi itu.

## Encapsulation dan Validasi

`harga_dasar`, `stok`, dan `password` diakses lewat `@property` dengan setter yang ada validasinya:
- harga dan stok tidak boleh kosong atau negatif
- password minimal 4 karakter

Kalau data tidak valid, perubahan ditolak dan nilai lama tetap dipakai.

Pembatasan hak akses ada di class `KopiKenangan`. Method `tambah_menu()`, `update_menu()`, `hapus_menu()`, dan `tambah_kasir()` mengecek `isinstance(pelaku, Admin)`, jadi kasir tetap ditolak walaupun method-nya dipanggil langsung.

## Static Method dan Class Method

- `@classmethod`: `dari_dict()` di `MinumanKopi`, `MakananRingan`, dan `Kasir` (membuat objek dari dictionary), serta `info_sistem()`.
- `@staticmethod`: `cek_ukuran_valid()`, `cek_kemasan_valid()`, `validasi_shift()`, dan `format_rupiah()`.

## Panduan Pengujian

1. Login dengan username atau password salah, harus ditolak dan diminta ulang.
2. Login sebagai `admin`, lalu coba tambah menu, update harga/stok, dan hapus menu.
3. Coba update dengan harga negatif, harus muncul pesan gagal dan harga lama tidak berubah.
4. Tambah akun kasir baru dengan password kurang dari 4 karakter, harus ditolak oleh setter.
5. Logout, lalu login sebagai `kasir1`. Menu yang tampil hanya lihat menu dan layani pelanggan.
6. Pilih layani pelanggan, masukkan ID menu (misal `MK01`), struk akan tercetak beserta totalnya.
