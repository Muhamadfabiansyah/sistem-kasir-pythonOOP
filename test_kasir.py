"""
Unit Test Script untuk memvalidasi seluruh syarat OOP:
- Encapsulation & Private Attribute
- Property and Setter
- Constructor __init__
- Class Method
- Static Method
- Object Instantiation
"""

import unittest
from kasir_app import Produk, Transaksi


class TestKasirOOP(unittest.TestCase):
    def setUp(self):
        # Inisialisasi object untuk pengujian
        self.produk1 = Produk("BRG99", "Barang Uji", 10000, 50)
        self.transaksi = Transaksi(pajak_persen=10.0)

    def test_encapsulation_and_properties(self):
        # Pastikan private attribute tidak bisa diakses langsung secara bebas
        self.assertTrue(hasattr(self.produk1, "_Produk__harga"))
        self.assertTrue(hasattr(self.produk1, "_Produk__stok"))

        # Mengakses via Property (Getter)
        self.assertEqual(self.produk1.kode, "BRG99")
        self.assertEqual(self.produk1.nama, "Barang Uji")
        self.assertEqual(self.produk1.harga, 10000)
        self.assertEqual(self.produk1.stok, 50)

        # Mengubah via Setter
        self.produk1.harga = 12000
        self.assertEqual(self.produk1.harga, 12000)
        self.produk1.stok = 45
        self.assertEqual(self.produk1.stok, 45)

        # Validasi setter (tidak boleh negatif)
        with self.assertRaises(ValueError):
            self.produk1.harga = -5000
        with self.assertRaises(ValueError):
            self.produk1.stok = -10

    def test_static_methods(self):
        # Format Rupiah
        self.assertEqual(Produk.format_rupiah(15000), "Rp 15.000")
        self.assertEqual(Produk.format_rupiah(1500000), "Rp 1.500.000")

        # Validasi Kode
        self.assertTrue(Produk.validasi_kode_format("BRG01"))
        self.assertFalse(Produk.validasi_kode_format("A!"))

        # Selisih Kembalian
        selisih = Transaksi.hitung_selisih_kembalian(50000, 75000)
        self.assertEqual(selisih, 25000)

    def test_class_methods(self):
        # get_total_jenis_produk
        total_sebelum = Produk.get_total_jenis_produk()
        _ = Produk("TST01", "Item Tes", 5000, 10)
        self.assertEqual(Produk.get_total_jenis_produk(), total_sebelum + 1)

        # Factory method buat_produk_diskon
        prod_diskon = Produk.buat_produk_diskon("DSC01", "Kemeja", 100000, 20, 5)
        self.assertEqual(prod_diskon.harga, 80000)
        self.assertIn("Diskon 20%", prod_diskon.nama)

        # Generator ID Transaksi
        id_baru = Transaksi.generate_next_id()
        self.assertTrue(id_baru.startswith("TRX-"))

    def test_transaksi_flow(self):
        p1 = Produk("P01", "Buku Tulis", 5000, 10)
        self.transaksi.tambah_item(p1, 2)  # 2 * 5000 = 10000

        self.assertEqual(self.transaksi.hitung_subtotal(), 10000)
        self.assertEqual(self.transaksi.hitung_nominal_pajak(), 1000)  # 10% dari 10000
        self.assertEqual(self.transaksi.hitung_total_akhir(), 11000)

        # Coba bayar kurang
        self.transaksi.uang_bayar = 10000
        with self.assertRaises(ValueError):
            self.transaksi.selesaikan_transaksi()

        # Bayar cukup
        self.transaksi.uang_bayar = 15000
        sukses = self.transaksi.selesaikan_transaksi()
        self.assertTrue(sukses)
        # Pastikan stok berkurang dari 10 menjadi 8
        self.assertEqual(p1.stok, 8)


if __name__ == "__main__":
    unittest.main()
