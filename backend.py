import csv
import os

FILE_DB = "data_kantin.csv"


class MenuItem:
    def __init__(self, nama, harga, kategori):
        self.nama = nama
        self.harga = int(harga) 
        self.kategori = kategori


class KantinManager:
    def __init__(self):

        self.daftar_menu = []
        self.load_data_awal()

    def load_data_awal(self):

        if os.path.exists(FILE_DB):
            try:
                with open(FILE_DB, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader, None) 
                    for row in reader:
                        if len(row) == 3:
                            self.tambah_menu(row[0], row[1], row[2])
            except Exception:
                self.buat_data_dummy()
        else:
            self.buat_data_dummy()

    def buat_data_dummy(self):
        self.tambah_menu("Nasi Goreng Spesial", 18000, "Makanan")
        self.tambah_menu("Ayam Geprek", 15000, "Makanan")
        self.tambah_menu("Es Teh Manis", 4000, "Minuman")
        self.tambah_menu("Kopi Susu Gula Aren", 12000, "Minuman")
        self.tambah_menu("Kentang Goreng", 8000, "Snack")


    def tambah_menu(self, nama, harga, kategori):
        self.daftar_menu.append(MenuItem(nama, harga, kategori))

    def edit_menu(self, nama_lama, nama_baru, harga_baru, kategori_baru):
        for menu in self.daftar_menu:
            if menu.nama == nama_lama:
                menu.nama = nama_baru
                menu.harga = int(harga_baru)
                menu.kategori = kategori_baru
                return True
        return False

    # [REQ 3.2] Struktur Kontrol (List Comprehension) untuk Hapus
    def hapus_menu(self, nama_menu):
        self.daftar_menu = [m for m in self.daftar_menu if m.nama != nama_menu]

    # [REQ 3.4] Fungsi Cari
    def cari_menu(self, kata_kunci):
        return [m for m in self.daftar_menu if kata_kunci.lower() in m.nama.lower()]

    def get_semua_menu(self):
        return self.daftar_menu

    # [REQ 8] Login Sederhana
    def cek_login(self, username, password):
        return username == "admin" and password == "123"

    # [REQ 8] Export CSV
    def export_ke_csv(self):
        try:
            with open(FILE_DB, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Nama Menu", "Harga", "Kategori"])
                for menu in self.daftar_menu:
                    writer.writerow([menu.nama, menu.harga, menu.kategori])
            return True
        except Exception as e:
            print(f"Error Export: {e}")
            return False

    # [REQ 3.4] Data untuk Grafik
    def get_data_grafik(self):
        data = {}
        for menu in self.daftar_menu:
            kat = menu.kategori
            data[kat] = data.get(kat, 0) + 1
        return data