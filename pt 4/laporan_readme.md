# Laporan Posttest PBO: Sistem Kasir Kopi Kenangan

## 1. Deskripsi Program
Program ini merupakan sistem kasir dan pemesanan menu berbasis Pemrograman Berorientasi Objek (PBO) menggunakan bahasa Python. Sistem mengelola katalog menu (*Kopi*, *Non-Kopi*, *Makanan*), kalkulasi harga dinamis berdasarkan varian/servis, pencatatan transaksi pesanan, hingga pemrosesan berbagai metode pembayaran (*Tunai*, *QRIS*, *E-Wallet*).

---

## 2. Class Diagram & Relasi Kelas

### Class Diagram (UML Sederhana)
```
+-------------------------------------------------------+
|                   <<Abstract>>                        |
|                     MenuItem                          |
+-------------------------------------------------------+
| # _harga_dasar: float                                 |
| + kode: str                                           |
| + nama: str                                           |
+-------------------------------------------------------+
| + hitung_harga()* : float                             |
| + deskripsi()* : str                                  |
| + info_menu() : str                                   |
+-------------------------------------------------------+
         ^                   ^                   ^
         |                   |                   |
+-----------------+ +-----------------+ +-----------------+
|      Kopi       | |     NonKopi     | |     Makanan     |
+-----------------+ +-----------------+ +-----------------+
| - __level_gula  | | + topping       | | + dipanaskan    |
| + ukuran        | +-----------------+ +-----------------+
+-----------------+ | + hitung_harga()| | + hitung_harga()|
| + hitung_harga()| | + deskripsi()   | | + deskripsi()   |
| + deskripsi()   | +-----------------+ +-----------------+
+-----------------+

+-------------------------+              +-------------------------+
|         Katalog         | o----------- |        MenuItem         |
+-------------------------+ (Agregasi)   +-------------------------+
| + nama_outlet: str      |
| - _daftar_menu: list    |
+-------------------------+
| + tambah_menu(menu)     |
| + cari(kode)            |
| + tampilkan()           |
+-------------------------+

+-------------------------+              +-------------------------+
|         Pesanan         | *----------- |       ItemPesanan       |
+-------------------------+ (Komposisi)  +-------------------------+
| + nomor: int            |              | - __jumlah: int         |
| + nama_pelanggan: str   |              +-------------------------+
| - __items: list         |              | + subtotal() : float    |
+-------------------------+              +-------------------------+
| + tambah_item()         |
| + total() : float       |
+-------------------------+

+-------------------------+              +-------------------------+
|          Kasir          | ------------ | Pembayaran (Duck Type)  |
+-------------------------+ (Asosiasi)   | (Tunai / QRIS / EWlet)  |
+-------------------------+              +-------------------------+
| + proses_pembayaran()   |              | + bayar(total) : tuple  |
+-------------------------+              +-------------------------+
```

### Penjelasan Relasi Kelas
1. **Asosiasi (`Kasir` $\rightarrow$ Metode Pembayaran `Tunai` / `QRIS` / `EWallet`)**:
   - Class `Kasir` berhubungan dengan objek metode pembayaran melalui parameter method `proses_pembayaran(pesanan, metode)`. Relasi ini dinamakan *Asosiasi* karena `Kasir` hanya menggunakan objek pembayaran saat proses kalkulasi transaksi berlangsung tanpa menyimpannya sebagai atribut permanen.
2. **Agregasi (`Katalog` $\circ\rightarrow$ `MenuItem`)**:
   - Class `Katalog` menyimpan daftar objek `MenuItem`. Relasinya adalah *Agregasi* karena objek `MenuItem` (seperti `Kopi`, `NonKopi`, `Makanan`) dibuat terpisah di luar `Katalog` lalu didaftarkan. Jika objek `Katalog` dihapus, objek `MenuItem` tetap ada di memori dan dapat digunakan secara independen.
3. **Komposisi (`Pesanan` $\bullet\rightarrow$ `ItemPesanan`)**:
   - Class `Pesanan` memiliki relasi *Komposisi* dengan `ItemPesanan`. Objek `ItemPesanan` diinstansiasi secara langsung di dalam method `tambah_item()` milik `Pesanan`. Keberadaan `ItemPesanan` sepenuhnya bergantung pada `Pesanan`; jika `Pesanan` dihapus, seluruh `ItemPesanan` di dalamnya ikut hancur.

---

## 3. Penerapan Abstraksi (Abstract Base Class)

Program menerapkan abstraksi menggunakan module `abc` (`ABC` dan `@abstractmethod`).

- **Abstract Base Class**: `MenuItem`
- **Abstract Methods** (minimal 2):
  1. `hitung_harga()`: Mewajibkan subclass menghitung harga akhir item.
  2. `deskripsi()`: Mewajibkan subclass memberikan rincian opsi pesanan.
- **Subclass Implementasi**: Class `Kopi`, `NonKopi`, dan `Makanan` mengimplementasikan kedua `@abstractmethod` tersebut.
- **Method Konkret**: `info_menu()` pada `MenuItem`, yaitu method biasa yang memanfaatkan hasil keluaran `hitung_harga()` dan `deskripsi()` untuk format tampilan seragam.

### Bukti Abstraksi (Abstract Class Tidak Bisa Diinstansiasi)
Ketika mencoba melakukan instansiasi langsung pada `MenuItem`:
```python
try:
    MenuItem("X01", "Menu Gaib", 10000)
except TypeError as e:
    print(f"TypeError: {e}")
```
**Output Exception:**
```text
TypeError: Can't instantiate abstract class MenuItem with abstract methods deskripsi, hitung_harga
```

---

## 4. Penerapan Polimorfisme

### A. Polimorfisme via Pewarisan (Method Overriding)
Class `Kopi`, `NonKopi`, dan `Makanan` meng-override method `hitung_harga()` dan `deskripsi()` dengan logika spesifik:
- `Kopi`: Menambahkan biaya sesuai ukuran (`Regular`/`Large`).
- `NonKopi`: Menambahkan biaya per ekstra topping.
- `Makanan`: Menambahkan biaya jika dipanaskan.

Dipanggil secara polimorfis melalui satu iterasi loop pada `Katalog.tampilkan()`:
```python
for menu in self._daftar_menu:
    print(" ", menu.info_menu())  # Memanggil deskripsi() & hitung_harga() sesuai subclass
```

### B. Duck Typing
Class `Tunai`, `QRIS`, dan `EWallet` tidak terikat hubungan pewarisan, namun ketiganya mengimplementasikan method dengan nama dan argumen yang sejenis: `bayar(total)`. 

Class `Kasir` mengeksekusi pembayaran tanpa memeriksa tipe objek (`isinstance` / `type`):
```python
def proses_pembayaran(self, pesanan, metode):
    berhasil, keterangan = metode.bayar(pesanan.total())  # Dynamic Method Lookup (Duck Typing)
```

### C. Operator Overloading (Magic Methods)
1. `__lt__` pada `MenuItem`: Memungkinkan pengurutan katalog berdasarkan harga (`sorted(self._daftar_menu)`).
2. `__str__` pada `MenuItem` dan `Pesanan`: Menyediakan format string deskriptif saat objek di-print.
3. `__len__` pada `Pesanan` (total kuantitas item) dan `Katalog` (jumlah item menu).
4. `__gt__` pada `Pesanan`: Membandingkan total nominal bayar antara dua transaksi pesanan (`p1 > p2`).

---

## 5. Penerapan Prinsip SOLID (Nilai Plus)

1. **Single Responsibility Principle (SRP)**:
   - Tanggung jawab mencetak format nota/struk dipisahkan sepenuhnya ke dalam kelas khusus `StrukPrinter`, sehingga kelas `Kasir` dan `Pesanan` fokus pada logika bisnis.
2. **Open/Closed Principle (OCP)**:
   - Penambahan metode pembayaran baru (misalnya `CreditCard`) atau varian menu baru tidak perlu mengubah kode pada kelas `Kasir` atau `Katalog`. Cukup buat subclass/kelas baru yang memiliki struktur method yang sejalan.
3. **Dependency Inversion Principle (DIP)**:
   - Class `Kasir` menerima ketergantungan (`Katalog` dan `StrukPrinter`) melalui *Dependency Injection* pada konstruktor `__init__`, bukan melakukan instansiasi langsung di dalam kelasnya.

---

## 6. Petunjuk Penggunaan & Cara Menjalankan

### Mode Demo (Uji Konsep PBO & Bukti Abstraksi)
Jalankan perintah berikut untuk menampilkan eksekusi otomatis seluruh pilar PBO:
```bash
python main.py
```

### Mode Kasir Interaktif (CLI Input)
Jalankan perintah berikut untuk membuka menu input kasir secara langsung:
```bash
python main.py --interaktif
```

---

## 7. Tangkapan Layar Output Program

### Output Mode Demo
```text
============================================================
 1. BUKTI ABSTRAKSI: abstract class tidak bisa diinstansiasi
============================================================
TypeError: Can't instantiate abstract class MenuItem with abstract methods deskripsi, hitung_harga

============================================================
 2. POLIMORFISME VIA PEWARISAN: satu loop, perilaku berbeda
============================================================

=== MENU KOPI KENANGAN - CABANG SAMARINDA ===
  [K01] Kopi      Kopi Kenangan Mantan - Regular, gula Normal       Rp20,000
  [K02] Kopi      Kopi Susu Tetangga - Large, gula Less             Rp23,000
  [K03] Kopi      Americano - Regular, gula No Sugar                Rp16,000
  [N01] Non-Kopi  Matcha Latte + 1 topping                          Rp25,000
  [N02] Non-Kopi  Coklat Dingin + 2 topping                         Rp26,000
  [M01] Makanan   Roti Bakar Coklat (dipanaskan)                    Rp17,000
  [M02] Makanan   Croissant (dingin)                                Rp18,000

Jumlah menu di katalog (len): 7

============================================================
 3. OPERATOR OVERLOADING (__lt__, __str__, __len__, __gt__)
============================================================

=== MENU KOPI KENANGAN - CABANG SAMARINDA ===
  [K03] Kopi      Americano - Regular, gula No Sugar                Rp16,000
  [M01] Makanan   Roti Bakar Coklat (dipanaskan)                    Rp17,000
  [M02] Makanan   Croissant (dingin)                                Rp18,000
  [K01] Kopi      Kopi Kenangan Mantan - Regular, gula Normal       Rp20,000
  [K02] Kopi      Kopi Susu Tetangga - Large, gula Less             Rp23,000
  [N01] Non-Kopi  Matcha Latte + 1 topping                          Rp25,000
  [N02] Non-Kopi  Coklat Dingin + 2 topping                         Rp26,000

Pesanan #001 a.n. Budi | 3 item | Total Rp62,700
Pesanan #002 a.n. Sari | 2 item | Total Rp45,100
Pesanan #003 a.n. Andi | 5 item | Total Rp115,500

Pesanan Budi > Pesanan Sari ? True

============================================================
 4. DUCK TYPING: Tunai, QRIS, EWallet (tanpa pewarisan)
============================================================

----------------------------------------------------
                   KOPI KENANGAN                    
----------------------------------------------------
No: 001   Pelanggan: Budi
  2x Kopi Kenangan Mantan - Regular, gula Normal    Rp40,000
  1x Roti Bakar Coklat (dipanaskan)                 Rp17,000
----------------------------------------------------
  Subtotal                                          Rp57,000
  PPN 10%                                            Rp5,700
  TOTAL                                             Rp62,700
  Bayar via Tunai: Kembalian Rp37,300
----------------------------------------------------

[GAGAL] Pesanan #003 a.n. Andi | 5 item | Total Rp115,500 -> Saldo OVO tidak cukup

Total pendapatan kasir Rina: Rp223,300

============================================================
 5. ENCAPSULATION: validasi lewat property
============================================================
ValueError: Level gula harus salah satu dari ('Normal', 'Less', 'No Sugar')
ValueError: Jumlah pesanan harus lebih dari 0
```