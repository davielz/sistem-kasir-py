import json
import os
from utils import (
    input_not_empty,
    input_int,
    input_float,
    format_rupiah,
)

# Data file path
PRODUCTS_FILE = os.path.join("data", "data.json")

# Pastikan folder data dan file data.json ada
if not os.path.exists(PRODUCTS_FILE):
    os.makedirs("data", exist_ok=True)
    with open(PRODUCTS_FILE, "w") as f:
        json.dump([], f)

# Muat data produk dari file
products_data = []
with open(PRODUCTS_FILE, "r") as f:
    try:
        products_data = json.load(f)
    except json.JSONDecodeError:
        products_data = []


def save_products():
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products_data, f, indent=4)


def view_products():
    # formatted_money = lambda x: f"Rp. {int(round(x)):,}".replace(",", ".")

    # copy_products = products_data.copy()
    # for item in copy_products:
    #     item["harga"] = formatted_money(item["harga"])

    # print_table_dict(
    #     headers=["kode", "nama", "stok", "harga"],
    #     rows=products_data,
    #     padding=4,
    # )

    print("\n=== DAFTAR BARANG ===")
    # Header Tabel
    print(f"{'No':<4} {'Kode':<10} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
    print("-" * 65)

    for i, b in enumerate(products_data, start=1):
        print(
            f"{i:<4} {b['kode']:<10} {b['nama']:<25} {format_rupiah(b['harga']):>12} {b['stok']:>6}"
        )
    print("-" * 65)


def add_product():
    print("\n=== Tambah Barang Baru ===")
    kode = input_not_empty(">> Kode Barang: ")

    # Cek apakah kode barang sudah ada
    for item in products_data:
        if item["kode"] == kode:
            print(f"[!] Kode barang '{kode}' sudah ada. Penambahan dibatalkan.")
            return

    nama = input_not_empty(">> Nama Barang: ")
    stok = input_int(">> Stok Awal (Bilangan bulat): ", positive_only=True)
    harga = input_float(">> Harga Satuan: ", positive_only=True)

    # Tambah barang baru ke data
    new_product = {
        "kode": kode,
        "nama": nama,
        "stok": stok,
        "harga": harga,
    }
    products_data.append(new_product)
    # Simpan data ke file
    save_products()
    print(f"[✓] Barang '{nama}' dengan kode '{kode}' berhasil ditambahkan.")


def update_product():
    kode = input_not_empty(">> Masukkan Kode Barang: ")
    if not any(item["kode"] == kode for item in products_data):
        print(f"[!] Kode barang '{kode}' tidak ditemukan.")
        return
    item = next(item for item in products_data if item["kode"] == kode)
    print(
        f"[✓] Barang ditemukan: {kode} - {item['nama']} (Stok: {item['stok']}, Harga: {format_rupiah(item['harga'])})"
    )

    print("1) Update Nama")
    print("2) Update Stok")
    print("3) Update Harga")
    choice = input_int("Pilih atribut yang ingin diupdate (1/2/3): ")
    if choice == 1:
        new_name = input_not_empty(">> Masukkan Nama Baru: ")
        item["nama"] = new_name
    elif choice == 2:
        new_stock = input_int(
            ">> Masukkan Perubahan Stok (-3 atau 2): ", positive_only=False
        )
        item["stok"] += new_stock
    elif choice == 3:
        new_price = input_float(">> Masukkan Harga Baru: ", positive_only=True)
        item["harga"] = new_price
    else:
        print("[!] Pilihan tidak valid. Update dibatalkan.")
        return
    products_data.remove(item)
    products_data.append(item)
    save_products()
    print(f"[✓] Barang dengan kode '{kode}' berhasil diupdate.")


def search_product():
    keyword = input_not_empty(">> Masukkan kata kunci pencarian (kode/nama): ").lower()
    results = [
        item
        for item in products_data
        if keyword in item["kode"].lower() or keyword in item["nama"].lower()
    ]
    if results:
        print("\n=== Hasil Pencarian ===")
        print(f"{'No':<4} {'Kode':<10} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
        print("-" * 65)
        for i, b in enumerate(results, start=1):
            print(
                f"{i:<4} {b['kode']:<10} {b['nama']:<25} {format_rupiah(b['harga']):>12} {b['stok']:>6}"
            )
        print("-" * 65)
    else:
        print("[!] Tidak ada barang yang sesuai dengan kata kunci pencarian.")


def delete_product():
    print("\n=== Hapus Barang ===")
    kode = input(">> Kode Barang (Kosongkan untuk membatalkan): ")
    if not kode.strip():
        print("[!] Penghapusan dibatalkan.")
        return
    item = next((item for item in products_data if item["kode"] == kode), None)
    if item:
        input_confirm = input(
            f"Apakah Anda yakin ingin menghapus barang '{item['nama']}' dengan kode '{kode}'? (y/n): "
        )
        if input_confirm.lower() != "y":
            print("[!] Penghapusan dibatalkan.")
            return
        products_data.remove(item)
        save_products()
        print(f"[✓] Barang dengan kode '{kode}' berhasil dihapus.")
    else:
        print(f"[!] Kode barang '{kode}' tidak ditemukan.")
