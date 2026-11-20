# 🛒 Proyek Aplikasi Kasir Toko Modern (Point of Sales)

Aplikasi kasir berbasis GUI (Desktop) yang dibangun menggunakan bahasa pemrograman **Python** dengan menerapkan prinsip-prinsip lengkap **Object-Oriented Programming (OOP)**.

---

## 📋 Pemenuhan Kriteria Tugas

Semua kriteria tugas telah dipenuhi dan diimplementasikan secara terstruktur di dalam file [`kasir_app.py`](kasir_app.py):

| No | Kriteria Tugas | Implementasi dalam Kode | Penjelasan |
|---|---|---|---|
| 1 | **Bahasa Pemrograman Python** | File `.py` | Seluruh aplikasi dibangun dengan Python murni dan standar library Tkinter. |
| 2 | **Konsep OOP** | Class, Object, Encapsulation, Methods | Pemisahan tanggung jawab berbasis objek (Model Produk, Transaksi, & GUI). |
| 3 | **Minimal 2 Class** | `Produk`, `Transaksi`, `AplikasiKasirGUI` | Terdapat **3 class** terpisah dengan fungsi dan tanggung jawab masing-masing. |
| 4 | **Object dari Class** | `Produk(...)`, `Transaksi(...)`, `AplikasiKasirGUI(root)` | Instansiasi berbagai objek produk, objek transaksi aktif, serta objek aplikasi. |
| 5 | **Constructor `__init__()`** | `def __init__(self, ...)` pada setiap class | Digunakan untuk menginisialisasi atribut awal setiap objek yang dibuat. |
| 6 | **Attribute & Method** | Berbagai instance attributes & methods | Contoh method: `kurangi_stok()`, `tambah_item()`, `hitung_total_akhir()`, dll. |
| 7 | **Encapsulation** | Private attributes `__kode`, `__harga`, `__stok`, `__id_transaksi`, `__daftar_item` | Melindungi data penting agar tidak dapat dimodifikasi sembarangan dari luar class. |
| 8 | **Property & Setter** | `@property` & `@<attr>.setter` | Digunakan untuk getter dan setter dengan validasi data (misal: harga & stok tidak boleh negatif). |
| 9 | **Class Method** | `@classmethod` | - `Produk.get_total_jenis_produk()`<br>- `Produk.buat_produk_diskon()` (Factory method)<br>- `Transaksi.generate_next_id()` |
| 10 | **Static Method** | `@staticmethod` | - `Produk.format_rupiah()`<br>- `Produk.validasi_kode_format()`<br>- `Transaksi.hitung_selisih_kembalian()` |
| 11 | **Tampilan GUI** | Tkinter & `ttk` | Tampilan antarmuka grafis modern, interaktif, responsif, dan dilengkapi pop-up cetak struk belanja. |

---

## 📂 Struktur File

```text
Projec_kasir/
├── kasir_app.py     # Source code utama aplikasi kasir (Semua Class & GUI)
├── test_kasir.py    # Unit test otomatis untuk memvalidasi seluruh konsep OOP
├── run.bat          # File launcher praktis (cukup klik 2x di Windows)
└── README.md        # Dokumentasi lengkap proyek
```

---

## 🚀 Cara Menjalankan Aplikasi

### Cara 1: Menggunakan File Batch (Paling Mudah di Windows)
Cukup **klik dua kali (double-click)** pada file [`run.bat`](run.bat). File ini akan secara otomatis mendeteksi instalasi Python dan membuka GUI kasir.

### Cara 2: Melalui Terminal / Command Prompt
Jalankan perintah berikut:
```bash
python kasir_app.py
```
atau jika menggunakan Python launcher:
```bash
py kasir_app.py
```
atau menggunakan path Python langsung:
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" kasir_app.py
```

---

## 🧪 Menjalankan Pengujian (Unit Test)

Untuk memverifikasi bahwa seluruh konsep OOP (Encapsulation, Setter Validation, Class Method, Static Method, dan Kalkulasi Transaksi) berjalan 100% benar:
```bash
python test_kasir.py
```

---

## 💻 Fitur Utama Aplikasi Kasir GUI

1. **Katalog Produk & Pencarian Real-Time**: Melihat daftar barang, stok, dan harga, serta fitur pencarian instan.
2. **Form Master Produk**: Kasir dapat menambahkan produk baru atau memperbarui stok/harga produk yang sudah ada secara langsung dengan validasi OOP.
3. **Keranjang Belanja Interaktif**: Memilih barang, menentukan kuantitas beli, mengecek stok secara otomatis, dan menghapus item dari keranjang.
4. **Kalkulasi Otomatis**: Menghitung Subtotal, PPN (11%), Grand Total, serta kembalian uang secara real-time saat mengetik nominal pembayaran.
5. **Cetak Struk Belanja**: Menampilkan nota pembelian resmi bergaya monospace yang rapi dan memotong stok produk secara otomatis setelah transaksi berhasil.
