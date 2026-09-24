# Sistem Kasir Kopi Kenangan (Versi Interaktif + Login)

Program OOP Python — Posttest 1 (Class, Object, Atribut, Method, Getter & Setter)

## Tema
Sistem kasir interaktif untuk kedai kopi **Kopi Kenangan**. Pengguna wajib **login** terlebih dulu sebelum masuk ke menu utama. Ada dua role dengan hak akses berbeda:

| Role | Bisa lihat menu | Bisa layani pelanggan | Bisa tambah/update/hapus menu | Bisa tambah akun kasir |
|---|:---:|:---:|:---:|:---:|
| **Admin** | ✅ | — | ✅ | ✅ |
| **Kasir** | ✅ | ✅ | ❌ | ❌ |

Jika Kasir mencoba mengakses fungsi Admin (mis. lewat pemanggilan method langsung), sistem akan menolak dengan pesan `[DITOLAK] ...` — validasi dilakukan lewat `isinstance(pelaku, Admin)` di dalam method `KopiKenangan`. Di CLI, opsi tersebut memang tidak ditampilkan sama sekali untuk role Kasir.

## Akun contoh (seed data)
| Username | Password | Role  | Shift |
|---|---|---|---|
| `admin`  | `admin123` | Admin | - |
| `kasir1` | `kasir123` | Kasir | Pagi |
| `kasir2` | `kasir123` | Kasir | Malam |

## 4 Pilar OOP

| Pilar | Penerapan |
|---|---|
| **Abstraction** | `Menu` adalah `abstract class` (`ABC`) dengan `@abstractmethod hitung_harga_total()`. |
| **Encapsulation** | `_harga_dasar`, `_stok` (protected) dan `__password` (private) diakses lewat `@property` getter/setter bervalidasi. |
| **Inheritance** | `MinumanKopi`, `MakananRingan` mewarisi `Menu`. `Admin`, `Kasir` mewarisi `Pengguna`. |
| **Polymorphism** | `hitung_harga_total()` & `tampilkan_detail()` di-override berbeda di tiap sub-class `Menu` maupun `Pengguna`. |

## Struktur Class
1. **Menu** *(abstract)* → **MinumanKopi**, **MakananRingan**
2. **Pengguna** *(base akun login, private `__password`)* → **Admin**, **Kasir**
3. **KopiKenangan** *(Main Container)* — menyimpan `list_menu` & `list_pengguna`, mengatur login dan hak akses tiap operasi CRUD.

## Method penting
- **Instance**: `login()`, `layani_pelanggan()`, `tambah_menu()`, `tampilkan_detail()`, dll.
- **Class method**: `dari_dict()` (factory dari dictionary), `info_sistem()`.
- **Static method**: `cek_ukuran_valid()`, `cek_kemasan_valid()`, `validasi_shift()`, `format_rupiah()`.

## Alur Program
1. Program jalan → tampil layar **login** (`username` + `password`).
2. Login gagal → diminta ulang. Login berhasil → sistem mengenali role dari tipe objek (`Admin`/`Kasir`).
3. **Menu Admin**: lihat menu, tambah menu, update menu, hapus menu, tambah akun kasir, lihat semua akun.
4. **Menu Kasir**: lihat menu, layani pelanggan (hitung total belanja) — tidak ada opsi ubah data menu/akun.
5. Logout → kembali ke layar login atau keluar program.

## Validasi input & setter
- Semua input angka (harga, stok) divalidasi lewat `input_angka()` — diulang jika bukan angka.
- Pilihan kategori/ukuran/kemasan/shift divalidasi lewat `input_pilihan()` — hanya menerima nilai dari daftar valid.
- Setter `harga_dasar`/`stok` menolak nilai kosong/negatif.
- Setter `password` menolak nilai kosong atau kurang dari 4 karakter.

## Cara Menjalankan
```bash
python3 kasir_kopi_kenangan.py
```
Ikuti instruksi login di terminal, lalu pilih menu sesuai angka yang tersedia.
