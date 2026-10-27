from abc import ABC, abstractmethod


class Menu(ABC):
    total_menu_terdaftar = 0
    kategori_tersedia = ["Minuman Kopi", "Makanan Ringan"]
    ppn_persen = 10

    def __init__(self, id_menu, nama_menu, harga_dasar, stok):
        self.id_menu = id_menu
        self.nama_menu = nama_menu
        self._harga_dasar = harga_dasar
        self._stok = stok
        Menu.total_menu_terdaftar += 1

    @property
    def harga_dasar(self):
        return self._harga_dasar

    @harga_dasar.setter
    def harga_dasar(self, nilai_baru):
        if nilai_baru is None:
            print(f"[GAGAL] Harga untuk '{self.nama_menu}' tidak boleh kosong.")
            return
        if nilai_baru < 0:
            print(f"[GAGAL] Harga untuk '{self.nama_menu}' tidak boleh negatif.")
            return
        self._harga_dasar = nilai_baru

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai_baru):
        if nilai_baru is None or nilai_baru < 0:
            print(f"[GAGAL] Stok untuk '{self.nama_menu}' tidak valid.")
            return
        self._stok = nilai_baru

    @abstractmethod
    def hitung_harga_total(self):
        pass

    def tampilkan_detail(self):
        print(f"[{self.id_menu}] {self.nama_menu} | Harga dasar: Rp{self._harga_dasar:,.0f} | Stok: {self._stok}")


class MinumanKopi(Menu):
    BIAYA_TAMBAHAN_UKURAN = {"Small": 0, "Medium": 3000, "Large": 6000}

    def __init__(self, id_menu, nama_menu, harga_dasar, stok, ukuran="Medium", level_gula="Normal"):
        super().__init__(id_menu, nama_menu, harga_dasar, stok)
        self.ukuran = ukuran
        self.level_gula = level_gula

    @classmethod
    def dari_dict(cls, data: dict):
        return cls(data["id_menu"], data["nama_menu"], data["harga_dasar"],
                   data["stok"], data.get("ukuran", "Medium"), data.get("level_gula", "Normal"))

    @staticmethod
    def cek_ukuran_valid(ukuran):
        return ukuran in MinumanKopi.BIAYA_TAMBAHAN_UKURAN

    def hitung_harga_total(self):
        subtotal = self._harga_dasar + self.BIAYA_TAMBAHAN_UKURAN.get(self.ukuran, 0)
        return subtotal * (1 + Menu.ppn_persen / 100)

    def tampilkan_detail(self):
        print(f"[{self.id_menu}] {self.nama_menu} ({self.ukuran}, gula: {self.level_gula}) "
              f"| Stok: {self._stok} | Total bayar: Rp{self.hitung_harga_total():,.0f}")


class MakananRingan(Menu):
    KEMASAN_VALID = ["Standing Pouch", "Box", "Paper Bag"]
    BIAYA_KEMASAN = 1000

    def __init__(self, id_menu, nama_menu, harga_dasar, stok, jenis_kemasan="Standing Pouch"):
        super().__init__(id_menu, nama_menu, harga_dasar, stok)
        self.jenis_kemasan = jenis_kemasan

    @classmethod
    def dari_dict(cls, data: dict):
        return cls(data["id_menu"], data["nama_menu"], data["harga_dasar"],
                   data["stok"], data.get("jenis_kemasan", "Standing Pouch"))

    @staticmethod
    def cek_kemasan_valid(jenis):
        return jenis in MakananRingan.KEMASAN_VALID

    def hitung_harga_total(self):
        subtotal = self._harga_dasar + self.BIAYA_KEMASAN
        return subtotal * (1 + Menu.ppn_persen / 100)

    def tampilkan_detail(self):
        print(f"[{self.id_menu}] {self.nama_menu} (kemasan: {self.jenis_kemasan}) "
              f"| Stok: {self._stok} | Total bayar: Rp{self.hitung_harga_total():,.0f}")


class Pengguna:
    total_pengguna_terdaftar = 0
    nama_perusahaan = "Kopi Kenangan"
    role_valid = ["Admin", "Kasir"]

    def __init__(self, id_pengguna, nama, username, password):
        self.id_pengguna = id_pengguna
        self.nama = nama
        self.username = username
        self.__password = None
        self.password = password
        Pengguna.total_pengguna_terdaftar += 1

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password_baru):
        if not password_baru or len(str(password_baru)) < 4:
            print(f"[GAGAL] Password untuk '{self.username}' minimal 4 karakter.")
            return
        self.__password = str(password_baru)

    def login(self, username_input, password_input):
        return self.username == username_input and self.__password == password_input

    def tampilkan_detail(self):
        print(f"[{self.id_pengguna}] {self.nama} (@{self.username}) - {self.__class__.__name__}")


class Admin(Pengguna):
    def __init__(self, id_pengguna, nama, username, password):
        super().__init__(id_pengguna, nama, username, password)
        self.level_akses = "Penuh"

    def tampilkan_detail(self):
        print(f"[{self.id_pengguna}] ADMIN {self.nama} (@{self.username}) | Level akses: {self.level_akses}")


class Struk:
    nomor_struk_counter = 0

    def __init__(self, nama_kasir, menu: Menu, total_bayar):
        Struk.nomor_struk_counter += 1
        self.nomor_struk = f"STR{Struk.nomor_struk_counter:04d}"
        self.nama_kasir = nama_kasir
        self.nama_menu = menu.nama_menu
        self.total_bayar = total_bayar

    def cetak(self):
        print("     ----------------------------")
        print(f"     No. Struk : {self.nomor_struk}")
        print(f"     Kasir     : {self.nama_kasir}")
        print(f"     Item      : {self.nama_menu}")
        print(f"     Total     : Rp{self.total_bayar:,.0f}")
        print("     ----------------------------")


class Kasir(Pengguna):
    shift_valid = ["Pagi", "Siang", "Malam"]

    def __init__(self, id_pengguna, nama, username, password, shift):
        super().__init__(id_pengguna, nama, username, password)
        self.shift = shift

    @staticmethod
    def validasi_shift(shift):
        return shift in Kasir.shift_valid

    @classmethod
    def dari_dict(cls, data: dict):
        return cls(data["id_pengguna"], data["nama"], data["username"], data["password"], data["shift"])

    def layani_pelanggan(self, menu: Menu):
        # asosiasi: menu hanya dipakai sementara lewat parameter
        print(f"Kasir {self.nama} (shift {self.shift}) melayani pesanan:")
        menu.tampilkan_detail()
        total = menu.hitung_harga_total()

        # komposisi: struk dibuat di dalam transaksi ini
        struk = Struk(self.nama, menu, total)
        struk.cetak()
        return struk

    def tampilkan_detail(self):
        print(f"[{self.id_pengguna}] KASIR {self.nama} (@{self.username}) | Shift: {self.shift}")


class KopiKenangan:
    total_cabang = 0
    versi_sistem = "2.0"
    mata_uang = "IDR"

    def __init__(self, nama_cabang):
        self.nama_cabang = nama_cabang
        # agregasi: menu & pengguna dibuat di luar, cabang hanya menyimpan
        self.list_menu = []
        self.list_pengguna = []
        KopiKenangan.total_cabang += 1

    def login(self, username, password):
        for pengguna in self.list_pengguna:
            if pengguna.login(username, password):
                return pengguna
        return None

    def tambah_pengguna(self, pelaku, pengguna_baru):
        self.list_pengguna.append(pengguna_baru)
        print(f"[CREATE] Akun '{pengguna_baru.nama}' ({pengguna_baru.__class__.__name__}) berhasil dibuat.")

    def tambah_kasir(self, pelaku: Pengguna, kasir_baru: Kasir):
        if not isinstance(pelaku, Admin):
            print("[DITOLAK] Hanya Admin yang boleh menambahkan akun kasir.")
            return
        self.tambah_pengguna(pelaku, kasir_baru)

    def tampilkan_semua_pengguna(self):
        print(f"\n=== Daftar Akun Cabang {self.nama_cabang} ===")
        for p in self.list_pengguna:
            p.tampilkan_detail()

    def tambah_menu(self, pelaku: Pengguna, menu_baru: Menu):
        if not isinstance(pelaku, Admin):
            print("[DITOLAK] Hanya Admin yang boleh menambahkan menu.")
            return
        self.list_menu.append(menu_baru)
        print(f"[CREATE] '{menu_baru.nama_menu}' berhasil ditambahkan ke cabang {self.nama_cabang}.")

    def tampilkan_semua_menu(self):
        print(f"\n=== Daftar Menu Cabang {self.nama_cabang} ===")
        if not self.list_menu:
            print("(belum ada menu)")
            return
        for menu in self.list_menu:
            menu.tampilkan_detail()

    def update_menu(self, pelaku: Pengguna, id_menu, harga_baru=None, stok_baru=None):
        if not isinstance(pelaku, Admin):
            print("[DITOLAK] Hanya Admin yang boleh mengubah data menu.")
            return
        menu = self.cari_menu(id_menu)
        if menu is None:
            print(f"[GAGAL] Menu dengan id '{id_menu}' tidak ditemukan.")
            return
        if harga_baru is not None:
            menu.harga_dasar = harga_baru
        if stok_baru is not None:
            menu.stok = stok_baru
        print(f"[UPDATE] Menu '{menu.nama_menu}' diperbarui.")

    def hapus_menu(self, pelaku: Pengguna, id_menu):
        if not isinstance(pelaku, Admin):
            print("[DITOLAK] Hanya Admin yang boleh menghapus menu.")
            return
        menu = self.cari_menu(id_menu)
        if menu is None:
            print(f"[GAGAL] Menu dengan id '{id_menu}' tidak ditemukan.")
            return
        self.list_menu.remove(menu)
        print(f"[DELETE] Menu '{menu.nama_menu}' dihapus dari cabang {self.nama_cabang}.")

    def cari_menu(self, id_menu):
        for menu in self.list_menu:
            if menu.id_menu == id_menu:
                return menu
        return None

    @staticmethod
    def format_rupiah(angka):
        return f"Rp{angka:,.0f}"

    @classmethod
    def info_sistem(cls):
        print(f"Sistem Kasir {Pengguna.nama_perusahaan} v{cls.versi_sistem} | Total cabang aktif: {cls.total_cabang}")


def input_angka(teks):
    while True:
        try:
            return int(input(teks).strip())
        except ValueError:
            print("Input harus berupa angka, coba lagi.")


def input_pilihan(teks, pilihan_valid):
    while True:
        nilai = input(teks).strip()
        if nilai in pilihan_valid:
            return nilai
        print(f"Pilihan tidak valid. Pilihan yang tersedia: {', '.join(pilihan_valid)}")


def buat_data_awal():
    cabang = KopiKenangan("Kopi Kenangan - Margonda")

    admin1 = Admin("A01", "Rina", "admin", "admin123")
    kasir1 = Kasir("K01", "Sari", "kasir1", "kasir123", "Pagi")
    kasir2 = Kasir.dari_dict({
        "id_pengguna": "K02", "nama": "Budi", "username": "kasir2",
        "password": "kasir123", "shift": "Malam"
    })
    cabang.list_pengguna.extend([admin1, kasir1, kasir2])

    cabang.list_menu.append(MinumanKopi("MK01", "Kopi Kenangan Mantan", 18000, 50, "Large", "Less Sugar"))
    cabang.list_menu.append(MinumanKopi.dari_dict({
        "id_menu": "MK02", "nama_menu": "Americano", "harga_dasar": 15000,
        "stok": 40, "ukuran": "Medium", "level_gula": "Normal"
    }))
    cabang.list_menu.append(MakananRingan("MR01", "Croffle Cokelat", 20000, 25, "Box"))

    return cabang


def cetak_header(judul):
    print("\n" + "=" * 60)
    print(judul.center(60))
    print("=" * 60)


def layar_login(cabang: KopiKenangan):
    cetak_header("LOGIN SISTEM KASIR KOPI KENANGAN")
    print("(Akun contoh -> admin/admin123 | kasir1/kasir123 | kasir2/kasir123)")
    while True:
        username = input("Username : ").strip()
        password = input("Password : ").strip()
        pengguna = cabang.login(username, password)
        if pengguna:
            print(f"\nLogin berhasil! Selamat datang, {pengguna.nama} ({pengguna.__class__.__name__}).")
            return pengguna
        print("Username atau password salah. Coba lagi.\n")


def menu_admin(cabang: KopiKenangan, admin: Admin):
    while True:
        cetak_header(f"MENU UTAMA - ADMIN ({admin.nama})")
        print("1. Lihat semua menu")
        print("2. Tambah menu baru")
        print("3. Update menu (harga/stok)")
        print("4. Hapus menu")
        print("5. Tambah akun kasir baru")
        print("6. Lihat semua akun pengguna")
        print("0. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            cabang.tampilkan_semua_menu()

        elif pilihan == "2":
            kategori = input_pilihan(
                f"Kategori ({'/'.join(Menu.kategori_tersedia)}): ", Menu.kategori_tersedia)
            id_menu = input("ID menu: ").strip()
            nama_menu = input("Nama menu: ").strip()
            harga = input_angka("Harga dasar: ")
            stok = input_angka("Stok: ")
            if kategori == "Minuman Kopi":
                ukuran = input_pilihan("Ukuran (Small/Medium/Large): ", ["Small", "Medium", "Large"])
                gula = input("Level gula: ").strip() or "Normal"
                menu_baru = MinumanKopi(id_menu, nama_menu, harga, stok, ukuran, gula)
            else:
                kemasan = input_pilihan(
                    f"Jenis kemasan ({'/'.join(MakananRingan.KEMASAN_VALID)}): ", MakananRingan.KEMASAN_VALID)
                menu_baru = MakananRingan(id_menu, nama_menu, harga, stok, kemasan)
            cabang.tambah_menu(admin, menu_baru)

        elif pilihan == "3":
            id_menu = input("ID menu yang akan diupdate: ").strip()
            harga_baru = input("Harga baru (kosongkan jika tidak diubah): ").strip()
            stok_baru = input("Stok baru (kosongkan jika tidak diubah): ").strip()
            try:
                harga_baru = float(harga_baru) if harga_baru else None
                stok_baru = int(stok_baru) if stok_baru else None
            except ValueError:
                print("[GAGAL] Harga dan stok harus berupa angka.")
                continue
            cabang.update_menu(admin, id_menu, harga_baru, stok_baru)

        elif pilihan == "4":
            id_menu = input("ID menu yang akan dihapus: ").strip()
            cabang.hapus_menu(admin, id_menu)

        elif pilihan == "5":
            id_baru = input("ID pengguna kasir baru: ").strip()
            nama = input("Nama kasir: ").strip()
            username = input("Username: ").strip()
            password = input("Password (min 4 karakter): ").strip()
            shift = input_pilihan("Shift (Pagi/Siang/Malam): ", Kasir.shift_valid)
            cabang.tambah_kasir(admin, Kasir(id_baru, nama, username, password, shift))

        elif pilihan == "6":
            cabang.tampilkan_semua_pengguna()

        elif pilihan == "0":
            print("Logout berhasil.\n")
            return

        else:
            print("Pilihan tidak dikenal, coba lagi.")


def menu_kasir(cabang: KopiKenangan, kasir: Kasir):
    while True:
        cetak_header(f"MENU UTAMA - KASIR ({kasir.nama})")
        print("1. Lihat semua menu")
        print("2. Layani pelanggan (proses pesanan)")
        print("0. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            cabang.tampilkan_semua_menu()

        elif pilihan == "2":
            cabang.tampilkan_semua_menu()
            id_menu = input("Masukkan ID menu yang dipesan pelanggan: ").strip()
            menu_dipesan = cabang.cari_menu(id_menu)
            if menu_dipesan is None:
                print("[GAGAL] Menu tidak ditemukan.")
                continue
            struk = kasir.layani_pelanggan(menu_dipesan)
            print(f"Total yang harus dibayar pelanggan: {KopiKenangan.format_rupiah(struk.total_bayar)}")

        elif pilihan == "0":
            print("Logout berhasil.\n")
            return

        else:
            print("Pilihan tidak dikenal, coba lagi.")


def main():
    cabang = buat_data_awal()

    while True:
        pengguna_aktif = layar_login(cabang)

        if isinstance(pengguna_aktif, Admin):
            menu_admin(cabang, pengguna_aktif)
        elif isinstance(pengguna_aktif, Kasir):
            menu_kasir(cabang, pengguna_aktif)

        lagi = input("Kembali ke layar login? (y/n): ").strip().lower()
        if lagi != "y":
            print("Terima kasih telah menggunakan Sistem Kasir Kopi Kenangan.")
            break


if __name__ == "__main__":
    main()
