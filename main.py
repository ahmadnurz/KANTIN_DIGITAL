import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import KantinManager


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


COLOR_BG_MAIN = "#0F172A"       # Slate 900
COLOR_SIDEBAR = "#1E293B"       # Slate 800
COLOR_CARD = "#334155"          # Slate 700
COLOR_PRIMARY = "#3B82F6"       # Blue 500
COLOR_SUCCESS = "#10B981"       # Emerald 500
COLOR_WARNING = "#F59E0B"       # Amber 500
COLOR_DANGER = "#EF4444"        # Red 500


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Sistem - Kantin Digital")
        self.geometry("850x500")
        self.resizable(False, False)
        self.manager = KantinManager()
        self.selected_nama_lama = None
        self.keranjang = []
        self.total_harga = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel Kiri (Branding)
        self.frame_kiri = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_PRIMARY)
        self.frame_kiri.grid(row=0, column=0, sticky="nswe")
        
        ctk.CTkLabel(self.frame_kiri, text="KANTIN\nDIGITAL", font=("Montserrat", 32, "bold"), text_color="white").pack(pady=(120, 20))
        ctk.CTkLabel(self.frame_kiri, text="Sistem Manajemen Menu & Order", font=("Roboto", 14), text_color="#DBEAFE").pack()
        ctk.CTkLabel(self.frame_kiri, text="Created by Kelompok 2\nTeknik Komputer 2025", font=("Arial", 10), text_color="#DBEAFE").pack(side="bottom", pady=30)

        # Panel Kanan (Form)
        self.frame_kanan = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_MAIN)
        self.frame_kanan.grid(row=0, column=1, sticky="nswe")

        self.login_box = ctk.CTkFrame(self.frame_kanan, fg_color="transparent")
        self.login_box.pack(expand=True)

        ctk.CTkLabel(self.login_box, text="LOGIN ADMIN", font=("Arial", 20, "bold"), text_color="white").pack(pady=(0, 20))

        self.entry_user = ctk.CTkEntry(self.login_box, placeholder_text="Username", width=260, height=40)
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self.login_box, placeholder_text="Password", show="•", width=260, height=40)
        self.entry_pass.pack(pady=10)

        ctk.CTkButton(self.login_box, text="LOGIN", command=self.aksi_login, width=260, height=40, 
                      fg_color=COLOR_PRIMARY, hover_color="#2563EB", font=("Arial", 12, "bold")).pack(pady=20)

        # [BARU] Tombol Masuk User/Tamu
        ctk.CTkButton(self.login_box, text="Lihat Menu Saja (Tamu)", command=self.masuk_tamu, width=260, height=30, 
                      fg_color="transparent", border_width=1, border_color="gray", hover_color="#334155", font=("Arial", 11)).pack(pady=5)

        ctk.CTkLabel(self.login_box, text="Silahkan login", text_color="gray", font=("Arial", 10)).pack()
        self.bind('<Return>', self.aksi_login)

    def aksi_login(self, event=None):
        if self.manager.cek_login(self.entry_user.get(), self.entry_pass.get()):
            self.destroy()
            buka_aplikasi_utama(is_admin=True)
        else:
            messagebox.showerror("Akses Ditolak", "Username atau Password salah!")

    def masuk_tamu(self):
        self.destroy()
        buka_aplikasi_utama(is_admin=False) # Kirim sinyal Tamu


# --- JENDELA UTAMA (DASHBOARD) ---
class AplikasiKantin(ctk.CTk):
    def __init__(self, is_admin=True):
        super().__init__()

        self.is_admin = is_admin # Simpan status
        
        role_title = "Administrator" if self.is_admin else "Mode Tamu (View Only)"
        self.title(f"Dashboard {role_title} - Kantin Digital")
        self.geometry("1200x750")
        self.configure(fg_color=COLOR_BG_MAIN)
        self.manager = KantinManager()
        self.selected_nama_lama = None
        self.keranjang = []      
        self.total_harga = 0     


        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === SIDEBAR ===
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        
        ctk.CTkLabel(self.sidebar, text="KANTIN", font=("Montserrat", 22, "bold"), text_color=COLOR_PRIMARY).pack(pady=(35, 10))
        ctk.CTkLabel(self.sidebar, text="KAMPUS", font=("Arial", 12), text_color="gray").pack(pady=(0, 40))

        # [LOGIKA] Hanya tampilkan tombol Export & Grafik jika ADMIN
        if self.is_admin:
            self.create_sidebar_btn("📂  Export CSV", self.aksi_export)
            self.create_sidebar_btn("📊  Lihat Grafik", self.tampil_grafik)
        else:
            ctk.CTkLabel(self.sidebar, text="Menu Anda terbatas\nmemilih makanan.", font=("Arial", 11), text_color="gray").pack()

        ctk.CTkButton(self.sidebar, text="Log Out", fg_color=COLOR_DANGER, hover_color="#B91C1C", 
                      width=160, height=35, command=self.aksi_logout).pack(side="bottom", pady=40)

        # === AREA UTAMA ===
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nswe", padx=25, pady=25)

        # [LOGIKA] Form Input HANYA muncul jika ADMIN
        if self.is_admin:
            self.card_input = ctk.CTkFrame(self.main_area, fg_color=COLOR_CARD, corner_radius=12)
            self.card_input.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(self.card_input, text="Kelola Menu Makanan", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=(15, 5))

            self.form_frame = ctk.CTkFrame(self.card_input, fg_color="transparent")
            self.form_frame.pack(padx=10, pady=10, fill="x")

            self.entry_nama = ctk.CTkEntry(self.form_frame, placeholder_text="Nama Item", width=250)
            self.entry_nama.grid(row=0, column=0, padx=10, pady=10)
            
            self.entry_harga = ctk.CTkEntry(self.form_frame, placeholder_text="Harga (Rp)", width=150)
            self.entry_harga.grid(row=0, column=1, padx=10, pady=10)
            
            self.combo_kategori = ctk.CTkComboBox(self.form_frame, values=["Makanan", "Minuman", "Snack"], width=150)
            self.combo_kategori.grid(row=0, column=2, padx=10, pady=10)
            self.combo_kategori.set("Makanan")

            self.btn_simpan = ctk.CTkButton(self.form_frame, text="+ Tambah", width=100, fg_color=COLOR_SUCCESS, hover_color="#059669", command=self.aksi_tambah)
            self.btn_simpan.grid(row=0, column=3, padx=5)
            
            self.btn_edit = ctk.CTkButton(self.form_frame, text=" Update", width=100, fg_color=COLOR_WARNING, hover_color="#D97706", command=self.aksi_edit)
            self.btn_edit.grid(row=0, column=4, padx=5)
            
            self.btn_hapus = ctk.CTkButton(self.form_frame, text=" Hapus", width=100, fg_color=COLOR_DANGER, hover_color="#B91C1C", command=self.aksi_hapus)
            self.btn_hapus.grid(row=0, column=5, padx=5)

        # Card Tabel
        self.table_card = ctk.CTkFrame(self.main_area, fg_color=COLOR_CARD, corner_radius=12)
        self.table_card.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(self.header_frame, text="Daftar Menu Tersedia", font=("Arial", 16, "bold")).pack(side="left")
        
        self.entry_cari = ctk.CTkEntry(self.header_frame, placeholder_text="🔍 Cari menu...", width=220)
        self.entry_cari.pack(side="right")
        self.entry_cari.bind("<KeyRelease>", self.aksi_cari_realtime)

        # Style Tabel
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background=COLOR_SIDEBAR, foreground="white", fieldbackground=COLOR_SIDEBAR, rowheight=35, borderwidth=0, font=("Arial", 11))
        self.style.configure("Treeview.Heading", background="#475569", foreground="white", font=("Arial", 11, "bold"), relief="flat")
        self.style.map("Treeview", background=[('selected', COLOR_PRIMARY)]) 

        self.tabel = ttk.Treeview(self.table_card, columns=("nama", "harga", "kategori"), show="headings")
        self.tabel.heading("nama", text="NAMA ITEM")
        self.tabel.heading("harga", text="HARGA (IDR)")
        self.tabel.heading("kategori", text="KATEGORI")
        
        self.tabel.column("nama", width=350, anchor="w")
        self.tabel.column("harga", width=150, anchor="center")
        self.tabel.column("kategori", width=150, anchor="center")
        
        self.tabel.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tabel.bind("<<TreeviewSelect>>", self.saat_tabel_diklik)

        # === PANEL KERANJANG UNTUK USER TAMU (tempel di sini) ===
        if not self.is_admin:
            self.cart_frame = ctk.CTkFrame(self.main_area, fg_color=COLOR_CARD, corner_radius=12)
            self.cart_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(
                self.cart_frame, text="Keranjang Belanja", 
                font=("Arial", 16, "bold")
            ).pack(anchor="w", padx=15, pady=10)

            # Listbox keranjang (tk.Listbox digunakan)
            self.list_keranjang = tk.Listbox(
                self.cart_frame, height=6, bg=COLOR_SIDEBAR, fg="white", 
                font=("Arial", 12), selectbackground="#475569", activestyle="none"
            )
            self.list_keranjang.pack(fill="x", padx=15, pady=5)

            # Total Harga
            self.label_total = ctk.CTkLabel(
                self.cart_frame, text="Total: Rp 0", 
                font=("Arial", 15, "bold"), text_color=COLOR_SUCCESS
            )
            self.label_total.pack(padx=15, pady=(10, 5))

            # Tombol hapus
            ctk.CTkButton(
                self.cart_frame, text="Hapus Item Terpilih", 
                fg_color=COLOR_DANGER, hover_color="#B91C1C",
                command=self.hapus_item_keranjang
            ).pack(padx=15, pady=5)

            # Tombol bersihkan
            ctk.CTkButton(
                self.cart_frame, text="Bersihkan Keranjang",
                fg_color=COLOR_WARNING, hover_color="#D97706",
                command=self.bersihkan_keranjang
            ).pack(padx=15, pady=(0,15))

        self.update_tabel()
        
        # [FITUR PENTING] Deteksi klik di sembarang tempat untuk cancel seleksi
        self.bind("<Button-1>", self.cek_klik_kosong)

    # --- HELPER METHOD ---
    def create_sidebar_btn(self, text, command):
        ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", border_width=1, border_color="#475569", 
                      hover_color="#334155", command=command, width=160, anchor="w").pack(pady=8)

    # --- LOGIKA CANCEL SELEKSI ---
    def cek_klik_kosong(self, event):
        if not self.is_admin: 
            return # User (tamu) tidak perlu fitur cancel seleksi form admin

        widget_klik = event.widget
        str_widget = str(widget_klik)
        if str(self.tabel) in str_widget: 
            return
        if "button" in str_widget.lower() or "entry" in str_widget.lower() or "combobox" in str_widget.lower(): 
            return

        if self.tabel.selection():
            self.tabel.selection_remove(self.tabel.selection())
            self.bersihkan_form()
            self.focus()
            
    # --- CRUD ---
    def update_tabel(self, data=None):
        for item in self.tabel.get_children(): 
            self.tabel.delete(item)
        if data is None: 
            data = self.manager.get_semua_menu()
        for m in data: 
            harga_fmt = f"Rp {m.harga:,.0f}".replace(",", ".")
            self.tabel.insert("", "end", values=(m.nama, harga_fmt, m.kategori))

    # [UBAH] Update logika saat tabel diklik
    def saat_tabel_diklik(self, event):
        sel = self.tabel.selection()
        if not sel:
            return

        vals = self.tabel.item(sel)['values']

        # Jika TAMU: tambahkan item ke keranjang
        if not self.is_admin:
            # harga pada tabel berformat "Rp 12.000"
            harga_str = str(vals[1]).replace("Rp ", "").replace(".", "")
            try:
                harga = int(harga_str)
            except ValueError:
                harga = 0

            self.keranjang.append({
                "nama": vals[0],
                "harga": harga
            })
            self.update_keranjang()
            return

        # Jika ADMIN: isi form untuk edit
        harga_bersih = str(vals[1]).replace("Rp ", "").replace(".", "")
        self.selected_nama_lama = vals[0]
        # Pastikan entry tersedia (hanya dibuat untuk admin)
        try:
            self.entry_nama.delete(0, "end"); self.entry_nama.insert(0, vals[0])
            self.entry_harga.delete(0, "end"); self.entry_harga.insert(0, harga_bersih)
            self.combo_kategori.set(vals[2])
        except Exception:
            # Jika ada masalah (mis. widget tidak ada), jangan crash
            pass

    def aksi_tambah(self):
        # Hanya admin punya tombol tambah
        if not self.is_admin:
            return
        try:
            if not self.entry_nama.get() or not self.entry_harga.get():
                return
            self.manager.tambah_menu(self.entry_nama.get(), int(self.entry_harga.get()), self.combo_kategori.get())
            self.update_tabel(); self.bersihkan_form()
            messagebox.showinfo("Sukses", "Menu berhasil ditambahkan")
        except ValueError:
            messagebox.showerror("Error", "Harga harus angka!")

    def aksi_edit(self):
        if not self.is_admin:
            return
        if not self.selected_nama_lama: return
        try:
            if self.manager.edit_menu(self.selected_nama_lama, self.entry_nama.get(), int(self.entry_harga.get()), self.combo_kategori.get()):
                self.update_tabel(); self.bersihkan_form()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui")
        except ValueError:
            messagebox.showerror("Error", "Harga harus angka!")

    def aksi_hapus(self):
        if not self.is_admin:
            return
        if not self.selected_nama_lama: return
        if messagebox.askyesno("Konfirmasi", f"Hapus menu '{self.selected_nama_lama}'?"):
            self.manager.hapus_menu(self.selected_nama_lama)
            self.update_tabel(); self.bersihkan_form()

    def aksi_cari_realtime(self, event):
        self.update_tabel(self.manager.cari_menu(self.entry_cari.get()))

    def bersihkan_form(self):
        # Hanya bersihkan jika ada entry admin
        try:
            self.entry_nama.delete(0, "end")
            self.entry_harga.delete(0, "end")
        except Exception:
            pass
        self.selected_nama_lama = None

    def aksi_export(self):
        if self.manager.export_ke_csv(): messagebox.showinfo("Export Berhasil", "Data disimpan ke CSV")

    def tampil_grafik(self):
        data = self.manager.get_data_grafik()
        top = ctk.CTkToplevel(self)
        top.title("Statistik"); top.geometry("600x450"); top.attributes('-topmost', True)
        
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(list(data.keys()), list(data.values()), color=['#3B82F6', '#10B981', '#F59E0B'])
        ax.set_title("Menu per Kategori"); ax.set_ylabel("Jumlah")
        
        FigureCanvasTkAgg(fig, master=top).get_tk_widget().pack(fill="both", expand=True)

    def aksi_logout(self):
        if messagebox.askyesno("Logout", "Keluar dari sistem?"):
            self.destroy(); buka_login_window()

    # === FUNGSI KERANJANG KHUSUS TAMU ===
    def update_keranjang(self):
        # Hanya untuk tamu
        if self.is_admin:
            return

        # Kosongkan listbox dulu
        self.list_keranjang.delete(0, "end")
        total = 0

        for item in self.keranjang:
            tamp = f"{item['nama']} - Rp {item['harga']:,.0f}".replace(",", ".")
            self.list_keranjang.insert("end", tamp)
            total += item["harga"]

        self.total_harga = total
        # update label total
        try:
            self.label_total.configure(text=f"Total: Rp {total:,}".replace(",", "."))
        except Exception:
            pass

    def hapus_item_keranjang(self):
        # Hanya tamu
        if self.is_admin:
            return

        sel = self.list_keranjang.curselection()
        if not sel:
            return
        idx = sel[0]
        # Hapus dari list data
        try:
            del self.keranjang[idx]
        except Exception:
            pass
        self.update_keranjang()

    def bersihkan_keranjang(self):
        if self.is_admin:
            return
        self.keranjang.clear()
        self.update_keranjang()


# --- EKSEKUSI ---
def buka_login_window():
    app = LoginWindow()
    app.mainloop()

def buka_aplikasi_utama(is_admin=True):
    app = AplikasiKantin(is_admin=is_admin) # Pass parameter
    app.mainloop()

if __name__ == "__main__":
    buka_login_window()
