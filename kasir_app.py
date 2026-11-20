"""
Project Aplikasi Kasir Toko Modern (Point of Sales)
Memenuhi seluruh kriteria tugas OOP Python:
1. Berorientasi Objek (OOP)
2. Minimal 2 Class (Terdapat 3 Class: Produk, Transaksi, AplikasiKasir)
3. Object dari class yang dibuat
4. Constructor __init__()
5. Attribute dan Method
6. Encapsulation (Private attribute __)
7. Property dan Setter (@property, @<name>.setter)
8. Class Method (@classmethod)
9. Static Method (@staticmethod)
10. Tampilan GUI (Tkinter + ttk modern)
"""

import datetime
import tkinter as tk
from tkinter import ttk, messagebox


# ==============================================================================
# CLASS 1: PRODUK (Model Data Produk)
# ==============================================================================
class Produk:
    """
    Class Produk merepresentasikan barang yang dijual di kasir.
    Menerapkan:
    - Encapsulation dengan private attributes (__kode, __nama, __harga, __stok)
    - Constructor __init__
    - Getter & Setter dengan @property
    - Static method (@staticmethod) untuk format mata uang
    - Class method (@classmethod) untuk pelacakan total jenis produk & pembuatan alternatif
    """

    # Class Attribute
    jumlah_jenis_produk = 0

    def __init__(self, kode: str, nama: str, harga: float, stok: int):
        # Private Attributes (Encapsulation)
        self.__kode = kode.strip().upper()
        self.__nama = nama.strip()
        self.__harga = 0.0
        self.__stok = 0

        # Menggunakan setter agar tervalidasi saat inisialisasi
        self.harga = harga
        self.stok = stok

        # Menambah penghitung class attribute
        Produk.jumlah_jenis_produk += 1

    # ------------------ ENCAPSULATION & PROPERTY/SETTER ------------------ #
    @property
    def kode(self) -> str:
        """Getter untuk kode produk (Read-only)"""
        return self.__kode

    @property
    def nama(self) -> str:
        """Getter untuk nama produk"""
        return self.__nama

    @nama.setter
    def nama(self, nilai: str):
        """Setter untuk nama produk dengan validasi"""
        if not nilai or not nilai.strip():
            raise ValueError("Nama produk tidak boleh kosong!")
        self.__nama = nilai.strip()

    @property
    def harga(self) -> float:
        """Getter untuk harga produk"""
        return self.__harga

    @harga.setter
    def harga(self, nilai: float):
        """Setter untuk harga dengan validasi tidak boleh bernilai negatif"""
        nilai_float = float(nilai)
        if nilai_float < 0:
            raise ValueError("Harga produk tidak boleh negatif!")
        self.__harga = nilai_float

    @property
    def stok(self) -> int:
        """Getter untuk stok produk"""
        return self.__stok

    @stok.setter
    def stok(self, nilai: int):
        """Setter untuk stok dengan validasi tidak boleh negatif"""
        nilai_int = int(nilai)
        if nilai_int < 0:
            raise ValueError("Stok produk tidak boleh bernilai negatif!")
        self.__stok = nilai_int

    # ------------------ METHODS (PERILAKU OBJECT) ------------------ #
    def kurangi_stok(self, jumlah: int) -> bool:
        """Mengurangi stok produk saat terjadi transaksi pembelian"""
        if jumlah <= 0:
            raise ValueError("Jumlah pengurangan stok harus lebih dari 0!")
        if self.__stok >= jumlah:
            self.__stok -= jumlah
            return True
        return False

    def tambah_stok(self, jumlah: int):
        """Menambah stok produk"""
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan stok harus lebih dari 0!")
        self.__stok += jumlah

    # ------------------ STATIC METHOD ------------------ #
    @staticmethod
    def format_rupiah(nominal: float) -> str:
        """
        Static method untuk memformat angka menjadi format mata uang Rupiah.
        Tidak bergantung pada state instance produk tertentu.
        Contoh: 15000 -> Rp 15.000
        """
        try:
            nominal_int = int(round(nominal))
            return f"Rp {nominal_int:,}".replace(",", ".")
        except (ValueError, TypeError):
            return "Rp 0"

    @staticmethod
    def validasi_kode_format(kode: str) -> bool:
        """Static method untuk validasi format kode produk (minimal 3 karakter alfanumerik)"""
        return bool(kode and len(kode.strip()) >= 3 and kode.strip().isalnum())

    # ------------------ CLASS METHOD ------------------ #
    @classmethod
    def get_total_jenis_produk(cls) -> int:
        """Class method untuk mendapatkan jumlah total jenis produk yang sudah dibuat"""
        return cls.jumlah_jenis_produk

    @classmethod
    def buat_produk_diskon(cls, kode: str, nama: str, harga_normal: float, persen_diskon: float, stok: int):
        """
        Class method sebagai factory method alternatif untuk membuat produk
        dengan harga yang sudah dipotong diskon.
        """
        if not (0 <= persen_diskon <= 100):
            raise ValueError("Persen diskon harus antara 0 dan 100!")
        harga_setelah_diskon = harga_normal * (1 - (persen_diskon / 100.0))
        nama_diskon = f"{nama} (Diskon {persen_diskon:.0f}%)"
        return cls(kode, nama_diskon, harga_setelah_diskon, stok)


# ==============================================================================
# CLASS 2: TRANSAKSI (Keranjang & Pembayaran Kasir)
# ==============================================================================
class Transaksi:
    """
    Class Transaksi mengelola keranjang belanja, perhitungan pajak,
    pembayaran, dan pembuatan struk transaksi.
    Menerapkan:
    - Encapsulation (__id_transaksi, __daftar_item, __pajak_persen, __uang_bayar, __waktu)
    - Constructor __init__
    - Property & Setter
    - Class method untuk auto-increment nomor transaksi
    - Static method untuk perhitungan kembalian
    """

    # Class Attribute untuk generator ID transaksi
    counter_transaksi = 1000

    def __init__(self, pajak_persen: float = 11.0):
        # Private Attributes
        self.__id_transaksi = Transaksi.generate_next_id()
        self.__daftar_item = {}  # {kode_produk: {"produk": Produk, "qty": int, "subtotal": float}}
        self.__pajak_persen = 0.0
        self.__uang_bayar = 0.0
        self.__waktu = datetime.datetime.now()

        # Gunakan setter untuk pajak
        self.pajak_persen = pajak_persen

    # ------------------ ENCAPSULATION & PROPERTY/SETTER ------------------ #
    @property
    def id_transaksi(self) -> str:
        """Getter ID transaksi (Read-only)"""
        return self.__id_transaksi

    @property
    def daftar_item(self) -> dict:
        """Getter daftar item di keranjang (Read-only view)"""
        return self.__daftar_item

    @property
    def pajak_persen(self) -> float:
        """Getter persentase pajak"""
        return self.__pajak_persen

    @pajak_persen.setter
    def pajak_persen(self, nilai: float):
        """Setter persentase pajak dengan validasi"""
        nilai_float = float(nilai)
        if nilai_float < 0:
            raise ValueError("Persentase pajak tidak boleh negatif!")
        self.__pajak_persen = nilai_float

    @property
    def uang_bayar(self) -> float:
        """Getter nominal uang bayar"""
        return self.__uang_bayar

    @uang_bayar.setter
    def uang_bayar(self, nilai: float):
        """Setter uang bayar dengan validasi"""
        nilai_float = float(nilai)
        if nilai_float < 0:
            raise ValueError("Uang pembayaran tidak boleh negatif!")
        self.__uang_bayar = nilai_float

    @property
    def waktu_str(self) -> str:
        """Getter string tanggal dan waktu transaksi"""
        return self.__waktu.strftime("%d-%m-%Y %H:%M:%S")

    # ------------------ CLASS METHOD ------------------ #
    @classmethod
    def generate_next_id(cls) -> str:
        """Class method untuk menghasilkan nomor faktur/transaksi unik secara otomatis"""
        cls.counter_transaksi += 1
        return f"TRX-{cls.counter_transaksi}"

    # ------------------ STATIC METHOD ------------------ #
    @staticmethod
    def hitung_selisih_kembalian(total_tagihan: float, uang_diterima: float) -> float:
        """
        Static method untuk menghitung kembalian uang.
        Mengembalikan nominal selisih kembalian (uang_diterima - total_tagihan).
        """
        return float(uang_diterima) - float(total_tagihan)

    # ------------------ METHODS (KALKULASI & KERANJANG) ------------------ #
    def tambah_item(self, produk: Produk, jumlah: int) -> bool:
        """Menambahkan produk ke keranjang belanja"""
        if jumlah <= 0:
            raise ValueError("Jumlah beli harus lebih dari 0!")

        # Cek ketersediaan stok
        stok_sudah_dipesan = self.__daftar_item.get(produk.kode, {}).get("qty", 0)
        if (stok_sudah_dipesan + jumlah) > produk.stok:
            return False

        if produk.kode in self.__daftar_item:
            self.__daftar_item[produk.kode]["qty"] += jumlah
            self.__daftar_item[produk.kode]["subtotal"] = (
                self.__daftar_item[produk.kode]["qty"] * produk.harga
            )
        else:
            self.__daftar_item[produk.kode] = {
                "produk": produk,
                "qty": jumlah,
                "subtotal": jumlah * produk.harga,
            }
        return True

    def hapus_item(self, kode_produk: str) -> bool:
        """Menghapus item dari keranjang berdasarkan kode produk"""
        if kode_produk in self.__daftar_item:
            del self.__daftar_item[kode_produk]
            return True
        return False

    def kosongkan_keranjang(self):
        """Mereset isi keranjang belanja"""
        self.__daftar_item.clear()
        self.__uang_bayar = 0.0

    def hitung_subtotal(self) -> float:
        """Menghitung total harga sebelum pajak"""
        return sum(item["subtotal"] for item in self.__daftar_item.values())

    def hitung_nominal_pajak(self) -> float:
        """Menghitung besaran pajak berdasarkan persentase"""
        return self.hitung_subtotal() * (self.__pajak_persen / 100.0)

    def hitung_total_akhir(self) -> float:
        """Menghitung grand total (Subtotal + Pajak)"""
        return self.hitung_subtotal() + self.hitung_nominal_pajak()

    def selesaikan_transaksi(self) -> bool:
        """
        Memproses transaksi dan mengurangi stok produk secara nyata.
        """
        total = self.hitung_total_akhir()
        if total <= 0:
            raise ValueError("Keranjang belanja masih kosong!")
        if self.__uang_bayar < total:
            raise ValueError("Uang pembayaran kurang!")

        # Potong stok produk
        for item in self.__daftar_item.values():
            produk: Produk = item["produk"]
            qty = item["qty"]
            sukses = produk.kurangi_stok(qty)
            if not sukses:
                raise ValueError(f"Stok produk {produk.nama} tidak mencukupi saat proses checkout!")

        return True

    def format_struk_teks(self) -> str:
        """Membuat teks struk belanja yang rapi dan profesional"""
        subtotal = self.hitung_subtotal()
        pajak = self.hitung_nominal_pajak()
        grand_total = self.hitung_total_akhir()
        kembalian = self.hitung_selisih_kembalian(grand_total, self.__uang_bayar)

        garis = "=" * 42
        garis_tipis = "-" * 42

        struk = []
        struk.append(garis)
        struk.append("           MINIMARKET KASIR OOP           ")
        struk.append("       Jl. Pemrograman No. 10, Jakarta    ")
        struk.append(garis)
        struk.append(f"No. Transaksi : {self.__id_transaksi}")
        struk.append(f"Tanggal/Waktu : {self.waktu_str}")
        struk.append(garis_tipis)
        struk.append(f"{'Nama Barang':<18} {'Qty':>4} {'Harga':>8} {'Total':>9}")
        struk.append(garis_tipis)

        for item in self.__daftar_item.values():
            p: Produk = item["produk"]
            nama_pendek = (p.nama[:16] + "..") if len(p.nama) > 18 else p.nama
            qty = item["qty"]
            harga_satuan = f"{int(p.harga):,}".replace(",", ".")
            sub = f"{int(item['subtotal']):,}".replace(",", ".")
            struk.append(f"{nama_pendek:<18} {qty:>4} {harga_satuan:>8} {sub:>9}")

        struk.append(garis_tipis)
        struk.append(f"{'Subtotal':<25} : {Produk.format_rupiah(subtotal):>14}")
        struk.append(f"{f'PPN ({self.__pajak_persen}%)':<25} : {Produk.format_rupiah(pajak):>14}")
        struk.append(garis_tipis)
        struk.append(f"{'TOTAL TAGIHAN':<25} : {Produk.format_rupiah(grand_total):>14}")
        struk.append(f"{'TUNAI / BAYAR':<25} : {Produk.format_rupiah(self.__uang_bayar):>14}")
        struk.append(f"{'KEMBALIAN':<25} : {Produk.format_rupiah(kembalian):>14}")
        struk.append(garis)
        struk.append("    TERIMA KASIH TELAH BERBELANJA DI SINI!   ")
        struk.append("      Barang yang dibeli tidak dapat ditukar  ")
        struk.append(garis)

        return "\n".join(struk)


# ==============================================================================
# CLASS 3: APLIKASI KASIR GUI (Tampilan Antarmuka Pengguna)
# ==============================================================================
class AplikasiKasirGUI:
    """
    Class AplikasiKasirGUI membungkus seluruh antarmuka grafis (Tkinter)
    dan berinteraksi langsung dengan object dari class Produk dan Transaksi.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistem Kasir Pintar (Point of Sale) - Python OOP")
        self.root.geometry("1100x720")
        self.root.minsize(1000, 650)

        # Database Master Produk dalam memori (List of Produk Objects)
        self.master_produk = {}
        self.inisialisasi_produk_awal()

        # Object Transaksi yang sedang aktif
        self.transaksi_aktif = Transaksi(pajak_persen=11.0)

        # Tema dan Gaya Tampilan
        self.konfigurasi_style()

        # Bangun Layout GUI
        self.buat_antarmuka()

        # Render data awal
        self.perbarui_tabel_produk()
        self.perbarui_tampilan_keranjang()

    def inisialisasi_produk_awal(self):
        """Membuat beberapa Object Produk sebagai data awal (demonstrasi object)"""
        contoh_produk = [
            Produk("BRG01", "Beras Ramos 5kg", 68000, 20),
            Produk("BRG02", "Minyak Goreng 2L", 34000, 25),
            Produk("BRG03", "Gula Pasir 1kg", 17500, 30),
            Produk("BRG04", "Kopi Bubuk 200g", 14500, 15),
            Produk("BRG05", "Susu UHT Full Cream", 19000, 40),
            Produk("BRG06", "Teh Celup Kotak", 8500, 50),
            Produk("BRG07", "Mie Instan Goreng", 3500, 120),
            # Contoh pembuatan via Class Method (Factory dengan Diskon)
            Produk.buat_produk_diskon("BRG08", "Cokelat Silverqueen", 25000, 20, 18),
        ]
        for p in contoh_produk:
            self.master_produk[p.kode] = p

    def konfigurasi_style(self):
        """Mengatur gaya widget ttk agar terlihat modern dan elegan"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Warna Tema
        self.WARNA_PRIMARY = "#1E3A8A"    # Biru Navy Tua
        self.WARNA_ACCENT = "#2563EB"     # Biru Modern
        self.WARNA_SUCCESS = "#16A34A"    # Hijau Sukses
        self.WARNA_DANGER = "#DC2626"     # Merah Hapus
        self.WARNA_BG = "#F1F5F9"         # Abu Sangat Lembut
        self.WARNA_CARD = "#FFFFFF"       # Putih

        self.root.configure(bg=self.WARNA_BG)

        # Style Treeview
        self.style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=26,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            font=("Segoe UI", 9, "bold"),
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1E3A8A")],
        )

    def buat_antarmuka(self):
        """Menyusun seluruh komponen GUI"""
        # 1. Header Atas
        header_frame = tk.Frame(self.root, bg=self.WARNA_PRIMARY, height=65)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="🛒 SISTEM KASIR MODERN (POS)",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg=self.WARNA_PRIMARY,
        )
        title_lbl.pack(side=tk.LEFT, padx=20, pady=10)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Implementasi Konsep Lengkap OOP Python (Encapsulation, Property/Setter, Class/Static Methods)",
            font=("Segoe UI", 9),
            fg="#93C5FD",
            bg=self.WARNA_PRIMARY,
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=10, pady=15)

        self.lbl_jam = tk.Label(
            header_frame,
            text=datetime.datetime.now().strftime("%d %b %Y | %H:%M"),
            font=("Segoe UI", 10, "bold"),
            fg="#FFFFFF",
            bg=self.WARNA_PRIMARY,
        )
        self.lbl_jam.pack(side=tk.RIGHT, padx=20)

        # 2. Main Container (Kiri: Katalog Produk & Form, Kanan: Keranjang & Kasir)
        main_container = tk.Frame(self.root, bg=self.WARNA_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # --- KOLOM KIRI (KATALOG & TAMBAH BARANG) ---
        left_panel = tk.Frame(main_container, bg=self.WARNA_BG, width=540)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Card Daftar Produk
        card_produk = tk.LabelFrame(
            left_panel,
            text=" 📦 Daftar Produk Tersedia ",
            font=("Segoe UI", 10, "bold"),
            bg=self.WARNA_CARD,
            fg=self.WARNA_PRIMARY,
            padx=10,
            pady=10,
        )
        card_produk.pack(fill=tk.BOTH, expand=True)

        # Pencarian Produk
        search_frame = tk.Frame(card_produk, bg=self.WARNA_CARD)
        search_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(search_frame, text="Cari Produk:", bg=self.WARNA_CARD, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.entry_cari = tk.Entry(search_frame, font=("Segoe UI", 9))
        self.entry_cari.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.entry_cari.bind("<KeyRelease>", lambda e: self.perbarui_tabel_produk())

        btn_reset_cari = tk.Button(
            search_frame,
            text="Reset",
            font=("Segoe UI", 8),
            command=self.reset_pencarian,
            bg="#E2E8F0",
            relief=tk.FLAT,
        )
        btn_reset_cari.pack(side=tk.RIGHT)

        # Tabel Master Produk
        tree_scroll_y = ttk.Scrollbar(card_produk, orient=tk.VERTICAL)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ("kode", "nama", "harga", "stok")
        self.tree_produk = ttk.Treeview(
            card_produk,
            columns=cols,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            height=9,
        )
        tree_scroll_y.config(command=self.tree_produk.yview)

        self.tree_produk.heading("kode", text="Kode")
        self.tree_produk.heading("nama", text="Nama Produk")
        self.tree_produk.heading("harga", text="Harga")
        self.tree_produk.heading("stok", text="Stok")

        self.tree_produk.column("kode", width=70, anchor=tk.CENTER)
        self.tree_produk.column("nama", width=190, anchor=tk.W)
        self.tree_produk.column("harga", width=100, anchor=tk.E)
        self.tree_produk.column("stok", width=60, anchor=tk.CENTER)

        self.tree_produk.pack(fill=tk.BOTH, expand=True)
        self.tree_produk.bind("<<TreeviewSelect>>", self.on_pilih_produk_tabel)

        # Area Aksi Produk: Tambah ke Keranjang
        aksi_frame = tk.Frame(card_produk, bg=self.WARNA_CARD, pady=8)
        aksi_frame.pack(fill=tk.X)

        tk.Label(aksi_frame, text="Jumlah Beli:", bg=self.WARNA_CARD, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.spin_qty = tk.Spinbox(aksi_frame, from_=1, to=999, width=6, font=("Segoe UI", 10))
        self.spin_qty.pack(side=tk.LEFT, padx=8)

        btn_tambah_keranjang = tk.Button(
            aksi_frame,
            text="+ Masukkan ke Keranjang",
            bg=self.WARNA_ACCENT,
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.aksi_tambah_ke_keranjang,
        )
        btn_tambah_keranjang.pack(side=tk.LEFT, padx=5)

        # Card Form Tambah Produk Baru ke Master Data
        form_produk_card = tk.LabelFrame(
            left_panel,
            text=" ➕ Tambah / Perbarui Produk Master ",
            font=("Segoe UI", 9, "bold"),
            bg=self.WARNA_CARD,
            fg="#475569",
            padx=10,
            pady=8,
        )
        form_produk_card.pack(fill=tk.X, pady=(10, 0))

        # Form Inputs Grid
        grid_f = tk.Frame(form_produk_card, bg=self.WARNA_CARD)
        grid_f.pack(fill=tk.X)

        tk.Label(grid_f, text="Kode:", bg=self.WARNA_CARD, font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.ent_new_kode = tk.Entry(grid_f, width=10, font=("Segoe UI", 9))
        self.ent_new_kode.grid(row=0, column=1, padx=4, pady=2, sticky="w")

        tk.Label(grid_f, text="Nama:", bg=self.WARNA_CARD, font=("Segoe UI", 8)).grid(row=0, column=2, sticky="w", padx=2, pady=2)
        self.ent_new_nama = tk.Entry(grid_f, width=20, font=("Segoe UI", 9))
        self.ent_new_nama.grid(row=0, column=3, padx=4, pady=2, sticky="we")

        tk.Label(grid_f, text="Harga (Rp):", bg=self.WARNA_CARD, font=("Segoe UI", 8)).grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.ent_new_harga = tk.Entry(grid_f, width=10, font=("Segoe UI", 9))
        self.ent_new_harga.grid(row=1, column=1, padx=4, pady=2, sticky="w")

        tk.Label(grid_f, text="Stok Awal:", bg=self.WARNA_CARD, font=("Segoe UI", 8)).grid(row=1, column=2, sticky="w", padx=2, pady=2)
        self.ent_new_stok = tk.Entry(grid_f, width=8, font=("Segoe UI", 9))
        self.ent_new_stok.grid(row=1, column=3, padx=4, pady=2, sticky="w")

        btn_simpan_produk = tk.Button(
            form_produk_card,
            text="Simpan Produk ke Master",
            bg="#0D9488",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            pady=3,
            cursor="hand2",
            command=self.aksi_simpan_produk_baru,
        )
        btn_simpan_produk.pack(fill=tk.X, pady=(6, 2))

        # Info Ringkas OOP di pojok kiri bawah
        self.lbl_oop_info = tk.Label(
            left_panel,
            text=f"Total Varian Produk Aktif (Class Method): {Produk.get_total_jenis_produk()}",
            font=("Segoe UI", 8, "italic"),
            bg=self.WARNA_BG,
            fg="#64748B",
            anchor="w",
        )
        self.lbl_oop_info.pack(fill=tk.X, pady=(4, 0))

        # --- KOLOM KANAN (KERANJANG, TOTAL & CHECKOUT) ---
        right_panel = tk.Frame(main_container, bg=self.WARNA_BG, width=500)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        card_keranjang = tk.LabelFrame(
            right_panel,
            text=" 🛒 Keranjang Belanja Pelanggan ",
            font=("Segoe UI", 10, "bold"),
            bg=self.WARNA_CARD,
            fg=self.WARNA_PRIMARY,
            padx=10,
            pady=10,
        )
        card_keranjang.pack(fill=tk.BOTH, expand=True)

        # Header Info Transaksi ID
        info_trx_f = tk.Frame(card_keranjang, bg=self.WARNA_CARD)
        info_trx_f.pack(fill=tk.X, pady=(0, 6))

        self.lbl_id_trx = tk.Label(
            info_trx_f,
            text=f"No. Faktur: {self.transaksi_aktif.id_transaksi}",
            font=("Segoe UI", 10, "bold"),
            bg=self.WARNA_CARD,
            fg=self.WARNA_ACCENT,
        )
        self.lbl_id_trx.pack(side=tk.LEFT)

        btn_kosongkan = tk.Button(
            info_trx_f,
            text="Kosongkan Keranjang",
            font=("Segoe UI", 8),
            bg="#FEE2E2",
            fg=self.WARNA_DANGER,
            relief=tk.FLAT,
            command=self.aksi_kosongkan_keranjang,
            cursor="hand2",
        )
        btn_kosongkan.pack(side=tk.RIGHT)

        # Tabel Keranjang
        scroll_krj_y = ttk.Scrollbar(card_keranjang, orient=tk.VERTICAL)
        scroll_krj_y.pack(side=tk.RIGHT, fill=tk.Y)

        cols_krj = ("kode", "nama", "harga", "qty", "subtotal")
        self.tree_keranjang = ttk.Treeview(
            card_keranjang,
            columns=cols_krj,
            show="headings",
            yscrollcommand=scroll_krj_y.set,
            height=7,
        )
        scroll_krj_y.config(command=self.tree_keranjang.yview)

        self.tree_keranjang.heading("kode", text="Kode")
        self.tree_keranjang.heading("nama", text="Nama Barang")
        self.tree_keranjang.heading("harga", text="Harga")
        self.tree_keranjang.heading("qty", text="Qty")
        self.tree_keranjang.heading("subtotal", text="Subtotal")

        self.tree_keranjang.column("kode", width=60, anchor=tk.CENTER)
        self.tree_keranjang.column("nama", width=150, anchor=tk.W)
        self.tree_keranjang.column("harga", width=80, anchor=tk.E)
        self.tree_keranjang.column("qty", width=45, anchor=tk.CENTER)
        self.tree_keranjang.column("subtotal", width=95, anchor=tk.E)

        self.tree_keranjang.pack(fill=tk.BOTH, expand=True)

        btn_hapus_item = tk.Button(
            card_keranjang,
            text="Hapus Item Terpilih dari Keranjang",
            bg="#FFF1F2",
            fg=self.WARNA_DANGER,
            font=("Segoe UI", 8),
            relief=tk.FLAT,
            pady=3,
            cursor="hand2",
            command=self.aksi_hapus_item_keranjang,
        )
        btn_hapus_item.pack(fill=tk.X, pady=(6, 0))

        # Panel Perhitungan & Pembayaran
        bayar_card = tk.Frame(right_panel, bg=self.WARNA_CARD, padx=12, pady=10)
        bayar_card.pack(fill=tk.X, pady=(10, 0))

        # Ringkasan Total
        calc_f = tk.Frame(bayar_card, bg=self.WARNA_CARD)
        calc_f.pack(fill=tk.X)

        tk.Label(calc_f, text="Subtotal Belanja:", font=("Segoe UI", 9), bg=self.WARNA_CARD).grid(row=0, column=0, sticky="w", pady=2)
        self.lbl_subtotal = tk.Label(calc_f, text="Rp 0", font=("Segoe UI", 9, "bold"), bg=self.WARNA_CARD)
        self.lbl_subtotal.grid(row=0, column=1, sticky="e", pady=2)

        tk.Label(calc_f, text="Pajak PPN (11%):", font=("Segoe UI", 9), bg=self.WARNA_CARD).grid(row=1, column=0, sticky="w", pady=2)
        self.lbl_pajak = tk.Label(calc_f, text="Rp 0", font=("Segoe UI", 9), bg=self.WARNA_CARD)
        self.lbl_pajak.grid(row=1, column=1, sticky="e", pady=2)

        calc_f.columnconfigure(0, weight=1)
        calc_f.columnconfigure(1, weight=1)

        sep = ttk.Separator(bayar_card, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=6)

        # Grand Total Banner
        total_banner = tk.Frame(bayar_card, bg="#EFF6FF", padx=8, pady=6)
        total_banner.pack(fill=tk.X)
        tk.Label(total_banner, text="TOTAL TAGIHAN", font=("Segoe UI", 11, "bold"), bg="#EFF6FF", fg=self.WARNA_PRIMARY).pack(side=tk.LEFT)
        self.lbl_grand_total = tk.Label(total_banner, text="Rp 0", font=("Segoe UI", 16, "bold"), bg="#EFF6FF", fg=self.WARNA_ACCENT)
        self.lbl_grand_total.pack(side=tk.RIGHT)

        # Input Pembayaran
        pay_input_f = tk.Frame(bayar_card, bg=self.WARNA_CARD, pady=8)
        pay_input_f.pack(fill=tk.X)

        tk.Label(pay_input_f, text="Uang Tunai (Rp):", font=("Segoe UI", 10, "bold"), bg=self.WARNA_CARD).pack(side=tk.LEFT)
        self.ent_uang_bayar = tk.Entry(pay_input_f, font=("Segoe UI", 11, "bold"), justify=tk.RIGHT)
        self.ent_uang_bayar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.ent_uang_bayar.bind("<KeyRelease>", lambda e: self.kalkulasi_kembalian_live())

        # Kembalian Label
        kembalian_f = tk.Frame(bayar_card, bg=self.WARNA_CARD)
        kembalian_f.pack(fill=tk.X, pady=(2, 8))
        tk.Label(kembalian_f, text="Kembalian:", font=("Segoe UI", 10), bg=self.WARNA_CARD).pack(side=tk.LEFT)
        self.lbl_kembalian = tk.Label(kembalian_f, text="Rp 0", font=("Segoe UI", 11, "bold"), bg=self.WARNA_CARD, fg=self.WARNA_SUCCESS)
        self.lbl_kembalian.pack(side=tk.RIGHT)

        # Tombol Proses Transaksi
        btn_checkout = tk.Button(
            bayar_card,
            text="💳 PROSES PEMBAYARAN & CETAK STRUK",
            bg=self.WARNA_SUCCESS,
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
            command=self.aksi_selesaikan_transaksi,
        )
        btn_checkout.pack(fill=tk.X)

    # ------------------ LOGIKA & EVENT HANDLERS ------------------ #
    def perbarui_tabel_produk(self):
        """Memperbarui data tabel produk di GUI sesuai filter pencarian"""
        keyword = self.entry_cari.get().strip().lower()

        # Kosongkan tabel produk
        for item in self.tree_produk.get_children():
            self.tree_produk.delete(item)

        # Isi kembali dengan data produk
        for p in self.master_produk.values():
            if not keyword or (keyword in p.kode.lower() or keyword in p.nama.lower()):
                # Menggunakan Static Method Produk.format_rupiah
                harga_rupiah = Produk.format_rupiah(p.harga)
                self.tree_produk.insert("", tk.END, values=(p.kode, p.nama, harga_rupiah, p.stok))

        # Perbarui label total jenis produk OOP (Class Method)
        self.lbl_oop_info.config(
            text=f"Total Varian Produk Terdaftar (Class Method): {Produk.get_total_jenis_produk()}"
        )

    def reset_pencarian(self):
        """Reset input pencarian dan reload tabel"""
        self.entry_cari.delete(0, tk.END)
        self.perbarui_tabel_produk()

    def on_pilih_produk_tabel(self, event):
        """Otomatis isi form produk baru saat salah satu produk di tabel diklik"""
        selected = self.tree_produk.selection()
        if not selected:
            return
        item_data = self.tree_produk.item(selected[0], "values")
        kode = item_data[0]
        if kode in self.master_produk:
            p = self.master_produk[kode]
            self.ent_new_kode.delete(0, tk.END)
            self.ent_new_kode.insert(0, p.kode)
            self.ent_new_nama.delete(0, tk.END)
            self.ent_new_nama.insert(0, p.nama)
            self.ent_new_harga.delete(0, tk.END)
            self.ent_new_harga.insert(0, str(int(p.harga)))
            self.ent_new_stok.delete(0, tk.END)
            self.ent_new_stok.insert(0, str(p.stok))

    def aksi_simpan_produk_baru(self):
        """Menyimpan atau memperbarui produk ke master data (Validasi dengan Property/Setter)"""
        kode = self.ent_new_kode.get().strip().upper()
        nama = self.ent_new_nama.get().strip()
        harga_raw = self.ent_new_harga.get().strip()
        stok_raw = self.ent_new_stok.get().strip()

        # Validasi format kode menggunakan static method
        if not Produk.validasi_kode_format(kode):
            messagebox.showerror(
                "Validasi Gagal",
                "Kode produk minimal 3 karakter alfanumerik (huruf/angka) tanpa simbol!"
            )
            return

        try:
            harga = float(harga_raw)
            stok = int(stok_raw)
        except ValueError:
            messagebox.showerror("Validasi Gagal", "Harga dan Stok harus berupa angka yang valid!")
            return

        try:
            if kode in self.master_produk:
                # Update produk yang sudah ada menggunakan property setter
                prod = self.master_produk[kode]
                prod.nama = nama
                prod.harga = harga
                prod.stok = stok
                messagebox.showinfo("Sukses", f"Data produk '{nama}' ({kode}) berhasil diperbarui!")
            else:
                # Buat objek Produk baru (Memanggil __init__)
                produk_baru = Produk(kode, nama, harga, stok)
                self.master_produk[kode] = produk_baru
                messagebox.showinfo("Sukses", f"Produk baru '{nama}' ({kode}) berhasil ditambahkan!")

            # Reset Form Input
            self.ent_new_kode.delete(0, tk.END)
            self.ent_new_nama.delete(0, tk.END)
            self.ent_new_harga.delete(0, tk.END)
            self.ent_new_stok.delete(0, tk.END)

            self.perbarui_tabel_produk()
        except ValueError as err:
            messagebox.showerror("Error Setter OOP", f"Validasi Error: {str(err)}")

    def aksi_tambah_ke_keranjang(self):
        """Memasukkan produk dari tabel ke keranjang transaksi aktif"""
        selected = self.tree_produk.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih produk dari tabel terlebih dahulu!")
            return

        item_data = self.tree_produk.item(selected[0], "values")
        kode = item_data[0]

        try:
            qty = int(self.spin_qty.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Jumlah Salah", "Jumlah beli harus berupa bilangan bulat positif!")
            return

        produk = self.master_produk.get(kode)
        if not produk:
            messagebox.showerror("Error", "Produk tidak ditemukan!")
            return

        if produk.stok <= 0:
            messagebox.showwarning("Stok Habis", f"Stok untuk produk '{produk.nama}' habis!")
            return

        # Panggil method tambah_item dari class Transaksi
        sukses = self.transaksi_aktif.tambah_item(produk, qty)
        if not sukses:
            messagebox.showwarning(
                "Stok Kurang",
                f"Jumlah yang diminta melebihi stok tersedia!\nStok saat ini: {produk.stok}"
            )
            return

        self.perbarui_tampilan_keranjang()

    def aksi_hapus_item_keranjang(self):
        """Menghapus baris item dari keranjang transaksi"""
        selected = self.tree_keranjang.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih item keranjang yang ingin dihapus!")
            return

        item_data = self.tree_keranjang.item(selected[0], "values")
        kode = item_data[0]

        self.transaksi_aktif.hapus_item(kode)
        self.perbarui_tampilan_keranjang()

    def aksi_kosongkan_keranjang(self):
        """Mereset isi keranjang belanja"""
        if not self.transaksi_aktif.daftar_item:
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin mengosongkan seluruh isi keranjang?"):
            self.transaksi_aktif.kosongkan_keranjang()
            self.ent_uang_bayar.delete(0, tk.END)
            self.perbarui_tampilan_keranjang()

    def perbarui_tampilan_keranjang(self):
        """Render ulang isi Treeview keranjang belanja dan angka kalkulasi"""
        for item in self.tree_keranjang.get_children():
            self.tree_keranjang.delete(item)

        for item_data in self.transaksi_aktif.daftar_item.values():
            p: Produk = item_data["produk"]
            qty = item_data["qty"]
            sub = item_data["subtotal"]
            self.tree_keranjang.insert(
                "",
                tk.END,
                values=(
                    p.kode,
                    p.nama,
                    Produk.format_rupiah(p.harga),
                    qty,
                    Produk.format_rupiah(sub),
                ),
            )

        # Hitung angka total
        subtotal = self.transaksi_aktif.hitung_subtotal()
        pajak = self.transaksi_aktif.hitung_nominal_pajak()
        grand_total = self.transaksi_aktif.hitung_total_akhir()

        self.lbl_subtotal.config(text=Produk.format_rupiah(subtotal))
        self.lbl_pajak.config(text=Produk.format_rupiah(pajak))
        self.lbl_grand_total.config(text=Produk.format_rupiah(grand_total))

        self.kalkulasi_kembalian_live()

    def kalkulasi_kembalian_live(self):
        """Menghitung kembalian secara real-time saat kasir mengetik uang bayar"""
        teks_bayar = self.ent_uang_bayar.get().replace(".", "").replace(",", "").strip()
        grand_total = self.transaksi_aktif.hitung_total_akhir()

        if not teks_bayar:
            self.lbl_kembalian.config(text="Rp 0", fg="#475569")
            return

        try:
            uang_bayar = float(teks_bayar)
            # Menggunakan Static Method dari Transaksi untuk kalkulasi kembalian
            kembalian = Transaksi.hitung_selisih_kembalian(grand_total, uang_bayar)

            if kembalian >= 0:
                self.lbl_kembalian.config(text=Produk.format_rupiah(kembalian), fg=self.WARNA_SUCCESS)
            else:
                kurang = abs(kembalian)
                self.lbl_kembalian.config(text=f"- {Produk.format_rupiah(kurang)} (Kurang)", fg=self.WARNA_DANGER)
        except ValueError:
            self.lbl_kembalian.config(text="Input Tidak Valid", fg=self.WARNA_DANGER)

    def aksi_selesaikan_transaksi(self):
        """Memproses checkout pembayaran dan menampilkan struk pop-up"""
        if not self.transaksi_aktif.daftar_item:
            messagebox.showwarning("Keranjang Kosong", "Keranjang belanja masih kosong! Silakan pilih barang.")
            return

        teks_bayar = self.ent_uang_bayar.get().replace(".", "").replace(",", "").strip()
        try:
            uang_bayar = float(teks_bayar)
        except ValueError:
            messagebox.showerror("Pembayaran Salah", "Masukkan nominal uang bayar yang valid!")
            return

        grand_total = self.transaksi_aktif.hitung_total_akhir()
        if uang_bayar < grand_total:
            kurang = grand_total - uang_bayar
            messagebox.showerror(
                "Uang Kurang",
                f"Uang pembayaran tidak cukup!\nKekurangan: {Produk.format_rupiah(kurang)}"
            )
            return

        # Simpan pembayaran ke property/setter Transaksi
        self.transaksi_aktif.uang_bayar = uang_bayar

        try:
            # Jalankan penyelesaian transaksi (kurangi stok)
            self.transaksi_aktif.selesaikan_transaksi()
        except ValueError as e:
            messagebox.showerror("Gagal Checkout", str(e))
            return

        # Generate Struk
        teks_struk = self.transaksi_aktif.format_struk_teks()

        # Tampilkan Modal Struk Belanja
        self.tampilkan_modal_struk(teks_struk)

        # Buat transaksi baru untuk pelanggan berikutnya
        self.transaksi_aktif = Transaksi(pajak_persen=11.0)
        self.lbl_id_trx.config(text=f"No. Faktur: {self.transaksi_aktif.id_transaksi}")
        self.ent_uang_bayar.delete(0, tk.END)

        # Refresh tampilan tabel dan keranjang
        self.perbarui_tabel_produk()
        self.perbarui_tampilan_keranjang()

    def tampilkan_modal_struk(self, teks_struk: str):
        """Dialog pop-up khusus untuk mencetak dan melihat struk kasir"""
        modal = tk.Toplevel(self.root)
        modal.title("Struk Pembayaran Berhasil")
        modal.geometry("450x580")
        modal.resizable(False, False)
        modal.configure(bg="#F8FAFC")
        modal.transient(self.root)
        modal.grab_set()

        # Header Dialog
        tk.Label(
            modal,
            text="✓ TRANSAKSI SELESAI",
            font=("Segoe UI", 12, "bold"),
            bg="#DCFCE7",
            fg=self.WARNA_SUCCESS,
            pady=8,
        ).pack(fill=tk.X)

        # Area Teks Struk Monospace
        text_f = tk.Frame(modal, padx=12, pady=10, bg="#F8FAFC")
        text_f.pack(fill=tk.BOTH, expand=True)

        txt_struk = tk.Text(
            text_f,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#FFFFFF",
            fg="#0F172A",
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=10,
        )
        txt_struk.insert(tk.END, teks_struk)
        txt_struk.config(state=tk.DISABLED)
        txt_struk.pack(fill=tk.BOTH, expand=True)

        # Tombol Tutup
        btn_f = tk.Frame(modal, bg="#F8FAFC", pady=10)
        btn_f.pack(fill=tk.X)

        btn_tutup = tk.Button(
            btn_f,
            text="Tutup & Transaksi Baru",
            bg=self.WARNA_PRIMARY,
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2",
            command=modal.destroy,
        )
        btn_tutup.pack()


# ==============================================================================
# ENTRY POINT PROGRAM
# ==============================================================================
def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()
    app = AplikasiKasirGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
