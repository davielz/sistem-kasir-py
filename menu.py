def show_main_menu():
    app_title = "SISTEM KASIR UMKM SEDERHANA"

    head_kiri = "MANAJEMEN DATA"
    head_kanan = "TRANSAKSI"

    menu_kiri = [
        "[1] Daftar Barang",
        "[2] Tambah Barang",
        "[3] Update Stok/Harga",
        "[4] Cari Barang",
    ]

    menu_kanan = [
        "[5] Transaksi Baru",
        "[6] Riwayat Transaksi",
        "[7] Rekap Pendapatan",
        "",
    ]

    menu_bawah = [
        "[0] Keluar Aplikasi",
        "[/c] Bersihkan Layar",
        "[/d] Hapus Barang",
    ]

    # LOGIKA RESPONSIVE (Menghitung Lebar Kotak)
    padding = 12

    # Hitung lebar kolom kiri & kanan dasar
    max_len_kiri = max(len(head_kiri), max(len(x) for x in menu_kiri))
    w_kiri = max_len_kiri + padding

    max_len_kanan = max(len(head_kanan), max(len(x) for x in menu_kanan))
    w_kanan = max_len_kanan + padding

    w_total = w_kiri + w_kanan + 1

    # Cek apakah Judul ATAU Menu Bawah ada yang lebih lebar dari tabel?
    # Cari item terpanjang di menu bawah
    max_len_bawah = max(len(x) for x in menu_bawah)

    # Bandingkan lebar tabel saat ini vs Judul vs Menu Bawah
    width_needed = max(w_total, len(app_title) + 4, max_len_bawah + 4)

    # Jika butuh lebih lebar, tambahkan selisihnya ke kolom kiri & kanan
    if width_needed > w_total:
        diff = width_needed - w_total
        w_kiri += diff // 2
        w_kanan += diff - (diff // 2)
        w_total = w_kiri + w_kanan + 1

    # RENDER TAMPILAN
    # Atas & Judul
    print(f"╔{'═' * w_total}╗")
    print(f"║{app_title.center(w_total)}║")
    print(f"╠{'═' * w_kiri}╦{'═' * w_kanan}╣")

    # Header Kolom
    print(f"║{head_kiri.center(w_kiri)}║{head_kanan.center(w_kanan)}║")
    print(f"╠{'═' * w_kiri}╬{'═' * w_kanan}╣")

    # Isi Menu Kolom (Kiri & Kanan)
    for k, n in zip(menu_kiri, menu_kanan):
        print(f"║ {k.ljust(w_kiri - 1)}║ {n.ljust(w_kanan - 1)}║")

    # [BARU] Render Menu Bawah (Looping Array)
    print(f"╠{'═' * w_total}╣")
    for item in menu_bawah:
        print(f"║{item.center(w_total)}║")

    print(f"╚{'═' * w_total}╝")
