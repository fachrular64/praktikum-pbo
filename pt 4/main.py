"""
Sistem Kasir dan Pemesanan Menu - Kopi Kenangan
Pemrograman Berorientasi Objek (Python)

Jalankan:
    python main.py              -> mode demo (menampilkan semua konsep PBO)
    python main.py --interaktif -> mode kasir interaktif
"""
import sys
from abc import ABC, abstractmethod


def rupiah(angka):
    """Format angka menjadi 'Rp12,000'."""
    return f"Rp{int(angka):,}"


# =====================================================================
# ABSTRAKSI: Abstract Base Class untuk semua item menu
# =====================================================================
class MenuItem(ABC):
    """Kontrak untuk semua item menu (Kopi, NonKopi, Makanan)."""

    kategori = "Menu"  # atribut kelas, di-override subclass

    def __init__(self, kode, nama, harga_dasar):
        self.kode = kode
        self.nama = nama
        self._harga_dasar = harga_dasar  # protected: dipakai subclass

    @abstractmethod
    def hitung_harga(self):
        """Harga akhir satu porsi (tiap subclass punya aturan sendiri)."""

    @abstractmethod
    def deskripsi(self):
        """Teks rincian item (ukuran, topping, dll)."""

    # ---- method konkret: dipakai bersama oleh semua subclass ----
    def info_menu(self):
        return (f"[{self.kode}] {self.kategori:<9} "
                f"{self.deskripsi():<40} {rupiah(self.hitung_harga()):>10}")

    # ---- operator overloading ----
    def __str__(self):
        return f"{self.nama} ({rupiah(self.hitung_harga())})"

    def __lt__(self, other):
        return self.hitung_harga() < other.hitung_harga()


# =====================================================================
# INHERITANCE + POLIMORFISME (method di-override tiap subclass)
# =====================================================================
class Kopi(MenuItem):
    kategori = "Kopi"
    TAMBAHAN_UKURAN = {"Regular": 0, "Large": 5000}
    LEVEL_GULA = ("Normal", "Less", "No Sugar")

    def __init__(self, kode, nama, harga_dasar, ukuran="Regular", level_gula="Normal"):
        super().__init__(kode, nama, harga_dasar)
        self.ukuran = ukuran            # atribut unik subclass
        self.level_gula = level_gula    # lewat property (divalidasi)

    @property
    def level_gula(self):
        return self.__level_gula        # private

    @level_gula.setter
    def level_gula(self, nilai):
        if nilai not in self.LEVEL_GULA:
            raise ValueError(f"Level gula harus salah satu dari {self.LEVEL_GULA}")
        self.__level_gula = nilai

    def hitung_harga(self):
        return self._harga_dasar + self.TAMBAHAN_UKURAN[self.ukuran]

    def deskripsi(self):
        return f"{self.nama} - {self.ukuran}, gula {self.level_gula}"


class NonKopi(MenuItem):
    kategori = "Non-Kopi"
    HARGA_TOPPING = 3000

    def __init__(self, kode, nama, harga_dasar, topping=0):
        super().__init__(kode, nama, harga_dasar)
        self.topping = topping

    def hitung_harga(self):
        return self._harga_dasar + self.topping * self.HARGA_TOPPING

    def deskripsi(self):
        return f"{self.nama} + {self.topping} topping"


class Makanan(MenuItem):
    kategori = "Makanan"
    BIAYA_PEMANASAN = 2000

    def __init__(self, kode, nama, harga_dasar, dipanaskan=False):
        super().__init__(kode, nama, harga_dasar)
        self.dipanaskan = dipanaskan

    def hitung_harga(self):
        return self._harga_dasar + (self.BIAYA_PEMANASAN if self.dipanaskan else 0)

    def deskripsi(self):
        return f"{self.nama} ({'dipanaskan' if self.dipanaskan else 'dingin'})"


# =====================================================================
# KOMPOSISI: Pesanan *-- ItemPesanan (dibuat di dalam Pesanan)
# =====================================================================
class ItemPesanan:
    """Baris pesanan. Tidak bermakna tanpa Pesanan yang memilikinya."""

    def __init__(self, menu, jumlah):
        self.menu = menu
        self.jumlah = jumlah

    @property
    def jumlah(self):
        return self.__jumlah

    @jumlah.setter
    def jumlah(self, nilai):
        if nilai <= 0:
            raise ValueError("Jumlah pesanan harus lebih dari 0")
        self.__jumlah = nilai

    def subtotal(self):
        return self.menu.hitung_harga() * self.jumlah


class Pesanan:
    PPN = 0.10  # atribut kelas

    def __init__(self, nomor, nama_pelanggan):
        self.nomor = nomor
        self.nama_pelanggan = nama_pelanggan
        self.__items = []  # private

    def tambah_item(self, menu, jumlah=1):
        # KOMPOSISI: ItemPesanan dibuat langsung di dalam Pesanan
        self.__items.append(ItemPesanan(menu, jumlah))

    @property
    def items(self):
        return tuple(self.__items)

    def subtotal(self):
        return sum(i.subtotal() for i in self.__items)

    def pajak(self):
        return int(self.subtotal() * self.PPN)

    def total(self):
        return self.subtotal() + self.pajak()

    # ---- operator overloading ----
    def __len__(self):
        return sum(i.jumlah for i in self.__items)

    def __gt__(self, other):
        return self.total() > other.total()

    def __str__(self):
        return (f"Pesanan #{self.nomor:03d} a.n. {self.nama_pelanggan} "
                f"| {len(self)} item | Total {rupiah(self.total())}")


# =====================================================================
# AGREGASI: Katalog o-- MenuItem (menu dibuat di luar, lalu didaftarkan)
# =====================================================================
class Katalog:
    def __init__(self, nama_outlet):
        self.nama_outlet = nama_outlet
        self._daftar_menu = []

    def tambah_menu(self, menu):
        self._daftar_menu.append(menu)

    def cari(self, kode):
        for menu in self._daftar_menu:
            if menu.kode == kode.upper():
                return menu
        raise KeyError(f"Menu dengan kode '{kode}' tidak ditemukan")

    def tampilkan(self, urut_harga=False):
        print(f"\n=== MENU {self.nama_outlet.upper()} ===")
        daftar = sorted(self._daftar_menu) if urut_harga else self._daftar_menu
        for menu in daftar:
            print(" ", menu.info_menu())  # polimorfisme

    def __len__(self):
        return len(self._daftar_menu)


# =====================================================================
# DUCK TYPING: tiga metode bayar TIDAK berhubungan lewat pewarisan,
# tetapi semuanya punya method bayar(total)
# =====================================================================
class Tunai:
    nama = "Tunai"

    def __init__(self, uang_diterima):
        self.uang_diterima = uang_diterima

    def bayar(self, total):
        if self.uang_diterima < total:
            return False, f"Uang kurang {rupiah(total - self.uang_diterima)}"
        return True, f"Kembalian {rupiah(self.uang_diterima - total)}"


class QRIS:
    nama = "QRIS"

    def __init__(self, penyedia):
        self.penyedia = penyedia

    def bayar(self, total):
        return True, f"Scan QRIS via {self.penyedia} berhasil"


class EWallet:
    nama = "E-Wallet"

    def __init__(self, penyedia, saldo):
        self.penyedia = penyedia
        self.saldo = saldo

    def bayar(self, total):
        if self.saldo < total:
            return False, f"Saldo {self.penyedia} tidak cukup"
        self.saldo -= total
        return True, f"Saldo {self.penyedia} tersisa {rupiah(self.saldo)}"


# =====================================================================
# SRP: StrukPrinter hanya mengurus tampilan struk
# =====================================================================
class StrukPrinter:
    def cetak(self, pesanan, nama_metode, keterangan):
        garis = "-" * 52
        print(f"\n{garis}\n{'KOPI KENANGAN':^52}\n{garis}")
        print(f"No: {pesanan.nomor:03d}   Pelanggan: {pesanan.nama_pelanggan}")
        for item in pesanan.items:
            print(f"  {item.jumlah}x {item.menu.deskripsi():<36}{rupiah(item.subtotal()):>10}")
        print(garis)
        print(f"  {'Subtotal':<38}{rupiah(pesanan.subtotal()):>12}")
        print(f"  {'PPN 10%':<38}{rupiah(pesanan.pajak()):>12}")
        print(f"  {'TOTAL':<38}{rupiah(pesanan.total()):>12}")
        print(f"  Bayar via {nama_metode}: {keterangan}\n{garis}")


# =====================================================================
# ASOSIASI: Kasir menggunakan metode pembayaran lewat parameter method
# DIP   : katalog & printer disuntikkan dari luar (dependency injection)
# =====================================================================
class Kasir:
    def __init__(self, nama, katalog, printer):
        self.nama = nama
        self._katalog = katalog
        self._printer = printer
        self._counter = 0
        self.__pendapatan = 0

    @property
    def pendapatan(self):
        return self.__pendapatan

    def buat_pesanan(self, nama_pelanggan):
        self._counter += 1
        return Pesanan(self._counter, nama_pelanggan)

    def catat_item(self, pesanan, kode, jumlah=1):
        pesanan.tambah_item(self._katalog.cari(kode), jumlah)

    def proses_pembayaran(self, pesanan, metode):
        """Asosiasi: 'metode' hanya dipakai sesaat (parameter), tidak disimpan."""
        berhasil, keterangan = metode.bayar(pesanan.total())  # duck typing
        if berhasil:
            self.__pendapatan += pesanan.total()
            self._printer.cetak(pesanan, metode.nama, keterangan)
        else:
            print(f"\n[GAGAL] {pesanan} -> {keterangan}")
        return berhasil


# =====================================================================
# Fungsi pendukung
# =====================================================================
def siapkan_katalog():
    katalog = Katalog("Kopi Kenangan - Cabang Samarinda")
    # Objek menu dibuat di luar Katalog (agregasi)
    for menu in (
        Kopi("K01", "Kopi Kenangan Mantan", 20000),
        Kopi("K02", "Kopi Susu Tetangga", 18000, "Large", "Less"),
        Kopi("K03", "Americano", 16000, "Regular", "No Sugar"),
        NonKopi("N01", "Matcha Latte", 22000, topping=1),
        NonKopi("N02", "Coklat Dingin", 20000, topping=2),
        Makanan("M01", "Roti Bakar Coklat", 15000, dipanaskan=True),
        Makanan("M02", "Croissant", 18000),
    ):
        katalog.tambah_menu(menu)
    return katalog


def demo():
    print("=" * 60)
    print(" 1. BUKTI ABSTRAKSI: abstract class tidak bisa diinstansiasi")
    print("=" * 60)
    try:
        MenuItem("X01", "Menu Gaib", 10000)
    except TypeError as e:
        print(f"TypeError: {e}")

    katalog = siapkan_katalog()
    kasir = Kasir("Rina", katalog, StrukPrinter())

    print("\n" + "=" * 60)
    print(" 2. POLIMORFISME VIA PEWARISAN: satu loop, perilaku berbeda")
    print("=" * 60)
    katalog.tampilkan()
    print(f"\nJumlah menu di katalog (len): {len(katalog)}")

    print("\n" + "=" * 60)
    print(" 3. OPERATOR OVERLOADING (__lt__, __str__, __len__, __gt__)")
    print("=" * 60)
    katalog.tampilkan(urut_harga=True)  # sorted() memakai __lt__

    p1 = kasir.buat_pesanan("Budi")
    kasir.catat_item(p1, "K01", 2)
    kasir.catat_item(p1, "M01", 1)
    p2 = kasir.buat_pesanan("Sari")
    kasir.catat_item(p2, "N01", 1)
    kasir.catat_item(p2, "K03", 1)
    p3 = kasir.buat_pesanan("Andi")
    kasir.catat_item(p3, "K02", 3)
    kasir.catat_item(p3, "M02", 2)
    print()
    for p in (p1, p2, p3):
        print(p)  # __str__ & __len__
    print(f"\nPesanan Budi > Pesanan Sari ? {p1 > p2}")

    print("\n" + "=" * 60)
    print(" 4. DUCK TYPING: Tunai, QRIS, EWallet (tanpa pewarisan)")
    print("=" * 60)
    kasir.proses_pembayaran(p1, Tunai(100000))
    kasir.proses_pembayaran(p2, QRIS("GoPay"))
    kasir.proses_pembayaran(p3, EWallet("OVO", 50000))  # saldo kurang
    kasir.proses_pembayaran(p3, EWallet("DANA", 300000))
    print(f"\nTotal pendapatan kasir {kasir.nama}: {rupiah(kasir.pendapatan)}")

    print("\n" + "=" * 60)
    print(" 5. ENCAPSULATION: validasi lewat property")
    print("=" * 60)
    try:
        katalog.cari("K01").level_gula = "Super Manis"
    except ValueError as e:
        print(f"ValueError: {e}")
    try:
        ItemPesanan(katalog.cari("K01"), 0)
    except ValueError as e:
        print(f"ValueError: {e}")


def interaktif():
    katalog = siapkan_katalog()
    kasir = Kasir(input("Nama kasir: ").strip() or "Kasir", katalog, StrukPrinter())
    while True:
        pesanan = kasir.buat_pesanan(input("\nNama pelanggan (kosong = selesai): ").strip() or "")
        if not pesanan.nama_pelanggan:
            break
        katalog.tampilkan()
        print("Ketik kode menu, atau 'selesai' untuk bayar.")
        while True:
            kode = input("Kode menu: ").strip()
            if kode.lower() == "selesai":
                break
            try:
                jumlah = int(input("Jumlah: ") or 1)
                kasir.catat_item(pesanan, kode, jumlah)
            except (KeyError, ValueError) as e:
                print(f"  ! {e}")
        if len(pesanan) == 0:
            print("Pesanan kosong, dibatalkan.")
            continue
        print(pesanan)
        pilihan = input("Bayar (1=Tunai, 2=QRIS, 3=E-Wallet): ").strip()
        try:
            if pilihan == "1":
                metode = Tunai(int(input("Uang diterima: ")))
            elif pilihan == "2":
                metode = QRIS(input("Penyedia QRIS: "))
            else:
                metode = EWallet(input("Penyedia: "), int(input("Saldo: ")))
            kasir.proses_pembayaran(pesanan, metode)
        except ValueError:
            print("Input tidak valid, pesanan dibatalkan.")
    print(f"\nTutup kasir. Total pendapatan: {rupiah(kasir.pendapatan)}")


if __name__ == "__main__":
    interaktif() if "--interaktif" in sys.argv else demo()