import csv
import os
from utils import input_not_empty, format_rupiah, input_float
from product import get_all_product_codes, get_product_by_code

TRANSACTION_FILE = os.path.join("data", "transactions.csv")
FIELDNAMES = [
    "waktu",
    "id_transaksi",
    "kode",
    "nama",
    "qty",
    "harga",
    "subtotal",
    "total_transaksi",
]

# Pastikan folder data dan file transaction.csv ada
if not os.path.exists(TRANSACTION_FILE):
    os.makedirs("data", exist_ok=True)
    with open(TRANSACTION_FILE, "w") as f:
        w = csv.writerf(f)
        w.writerow(FIELDNAMES)


def tambah_transaksi(
    waktu, id_transaksi, kode, nama, qty, harga, subtotal, total_transaksi
):
    with open(TRANSACTION_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                waktu,
                id_transaksi,
                kode,
                nama,
                qty,
                harga,
                subtotal,
                total_transaksi,
            ]
        )


def input_transaksi():
    keranjang = []
    while True:
        kode = input_not_empty("Masukkan kode barang: ")
        if kode.lower() == "selesai":
            proses_keranjang(keranjang)
            return
        if kode not in get_all_product_codes():
            print(f"[!] Kode barang '{kode}' tidak ditemukan. Silakan coba lagi.")
            continue
        barang = get_product_by_code(kode)
        print(
            f"=> Barang dipilih: {barang['nama']} - Stok: {barang['stok']} - Harga: {format_rupiah(barang['harga'])}"
        )
        qty = int(input_not_empty("Jumlah >> "))
        if qty <= 0:
            print("[!] Jumlah barang harus lebih dari 0. Silakan coba lagi.")
            continue
        if qty > barang["stok"]:
            print(
                f"[!] Stok barang '{kode}' tidak mencukupi. Stok tersedia: {barang['stok']}. Silakan coba lagi."
            )
            continue
        keranjang.append({"kode": kode, "qty": qty})
        print(f"[+] {barang['nama']} sebanyak {qty} ditambahkan ke keranjang")


def proses_keranjang(keranjang):
    struk_item = []
    total = 0
    for item in keranjang:
        produk = get_product_by_code(item["kode"])
        nama = produk["nama"]
        harga = produk["harga"]
        qty = item["qty"]
        subtotal = harga * qty
        total += subtotal
        struk_item.append(
            {
                "kode": item["kode"],
                "nama": nama,
                "qty": qty,
                "harga": harga,
                "subtotal": subtotal,
            }
        )

    isUseDiscount = input_not_empty("[?] Pakai Diskon (y/n)? ")
    diskon = 0
    if isUseDiscount.lower() == "y":
        diskon = input_float(">> Masukkan persentase diskon (0-100): ")
        if diskon < 0:
            diskon = 0
        elif diskon > 100:
            diskon = 100

    total_diskon = total * (diskon / 100)
    total_bayar = total - total_diskon
    cetak_struk(struk_item, total, diskon, total_bayar)


def cetak_struk(struk_item, total, diskon, total_bayar):
    print("\n=== STRUK BELANJA ===")
    print(f"{'Kode':<8} {'Nama':<20} {'Qty':>3} {'Harga':>12} {'Sub':>14}")
    print("-" * 60)
    for item in struk_item:
        print(
            f"{item['kode']:<8} {item['nama']:<20} {item['qty']:>3} {format_rupiah(item['harga']):>12} {format_rupiah(item['subtotal']):>14}"
        )
    print("-" * 60)
    print(f"{'Total':<35} {format_rupiah(total)}")
    if diskon > 0:
        print(f"{'Diskon':<35} {diskon}% (-{format_rupiah(total * (diskon / 100))})")
    print(f"{'Total Bayar':<35} {format_rupiah(total_bayar)}")
    print("=====================\n")


def tampil_struk(
    keranjang: list[dict], total: float, diskon: float, total_bayar: float
) -> None:
    """Menampilkan struk belanja ke layar"""
    print("\n===== STRUK =====")

    print("-" * 60)
    for item in keranjang:
        print(
            f"{item['kode']:<8} {item['nama']:<20} {item['qty']:>3} "
            f"{format_rupiah(item['harga']):>10} {format_rupiah(item['subtotal']):>12}"
        )
    print("-" * 60)
    print()
    print(f"{'Total':<35} Rp{format_rupiah(total):>12}")
    print(f"{'Diskon':<35} Rp{format_rupiah(diskon):>12}")
    print(f"{'Total Bayar':<35} Rp{format_rupiah(total_bayar):>12}")
    print("=================\n")


def tampilkan_transaksi():
    with open(TRANSACTION_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            print(row)
