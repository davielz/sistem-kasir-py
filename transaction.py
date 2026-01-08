import csv
import os
from datetime import datetime
from utils import input_not_empty, format_rupiah, input_float
from product import get_all_product_codes, get_product_by_code, set_product

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
        w = csv.writer(f)
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
        kode = input_not_empty(
            "Ketik 'SELESAI' untuk mengakhiri input barang\n>> Kode barang : "
        )
        if kode.lower() == "selesai" or kode.lower() == "/s":
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
        set_product(kode, stok=-qty)
        print(f"[+] {barang['nama']} sebanyak {qty} ditambahkan ke keranjang")


def proses_keranjang(keranjang):
    struk_items = []
    total = 0
    for item in keranjang:
        produk = get_product_by_code(item["kode"])
        nama = produk["nama"]
        harga = produk["harga"]
        qty = item["qty"]
        subtotal = harga * qty
        total += subtotal
        struk_items.append(
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
    cetak_struk(struk_items, total, diskon, total_bayar)

    uang_bayar = input_float(">> Uang bayar (Rp): ")
    if uang_bayar < total_bayar:
        for item in struk_items:
            set_product(kode=item["kode"], stok=item["qty"])
        print("[!] Uang kurang. Transaksi dibatalkan!")
        return
    elif uang_bayar > total_bayar:
        kembalian = uang_bayar - total_bayar
        print(f"[+] Kembalian: {format_rupiah(kembalian)}")
        save_transaction(struk_items, total_bayar)
        print("[√] Transaksi berhasil disimpan.")
    else:
        save_transaction(struk_items, total_bayar)
        print("[√] Transaksi berhasil disimpan.")


def save_transaction(struk_items, total_bayar):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = generate_id_transaksi()
    for item in struk_items:
        tambah_transaksi(
            waktu,
            id_transaksi,
            kode=item["kode"],
            nama=item["nama"],
            qty=item["qty"],
            harga=item["harga"],
            subtotal=item["subtotal"],
            total_transaksi=total_bayar,
        )


def cetak_struk(struk_items, total, diskon, total_bayar):
    print("\n=== STRUK BELANJA ===")
    print(f"{'Kode':<8} {'Nama':<20} {'Qty':>3} {'Harga':>12} {'Sub':>14}")
    print("-" * 60)
    for item in struk_items:
        print(
            f"{item['kode']:<8} {item['nama']:<20} {item['qty']:>3} {format_rupiah(item['harga']):>12} {format_rupiah(item['subtotal']):>14}"
        )
    print("-" * 60)
    print(f"{'Total':<35} {format_rupiah(total)}")
    if diskon > 0:
        print(f"{'Diskon':<35} {diskon}% (-{format_rupiah(total * (diskon / 100))})")
    print(f"{'Total Bayar':<35} {format_rupiah(total_bayar)}")
    print("=====================\n")


def tampilkan_riwayat_transaksi(limit: int = 20):
    rows = []
    with open(TRANSACTION_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("\n[!] Belum ada transaksi.\n")
        return

    # Ambil data terakhir sesuai limit
    rows = rows[-limit:]

    print("\n=== RIWAYAT TRANSAKSI (TERAKHIR) ===")
    print(
        f"{'Waktu':<19} {'ID':<16} {'Kode':<8} {'Qty':>3} {'Subtotal':>12} {'TotalTrx':>12}"
    )

    print("-" * 80)
    for r in rows:
        print(
            f"{r['waktu']:<19} {r['id_transaksi']:<16} {r['kode']:<8} "
            f"{int(float(r['qty'])):>3} "
            f"{format_rupiah(float(r['subtotal'])):>12} "
            f"{format_rupiah(float(r['total_transaksi'])):>12}"
        )
    print("-" * 80)


def rekap_pendapatan():
    pendapatan = 0
    list_trx_id = []

    with open(TRANSACTION_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["id_transaksi"] in list_trx_id:
                continue
            pendapatan += float(r["total_transaksi"])
            list_trx_id.append(r["id_transaksi"])

    if not list_trx_id:
        print("[!] Belum ada transaksi.")
        return
    print("\n===== REKAP PENDAPATAN =====")
    print(f"Jumlah transaksi : {len(list_trx_id)}")
    print(f"Total pendapatan : {format_rupiah(pendapatan)}\n")


def generate_id_transaksi() -> str:
    """Membuat ID transaksi berdasarkan waktu saat ini"""
    return datetime.now().strftime("TRX%Y%m%d%H%M%S")
