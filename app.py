from menu import show_main_menu
from product import (
    add_product,
    view_products,
    update_product,
    search_product,
    delete_product,
)
import os


def main():
    show_main_menu()
    while True:
        user_choice = input("\n👉 Pilih menu: ")

        if user_choice == "0":
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        elif user_choice == "1":
            view_products()
        elif user_choice == "2":
            add_product()
        elif user_choice == "3":
            update_product()
        elif user_choice == "4":
            search_product()
        elif user_choice == "5":
            print("[!] Fitur transaksi belum tersedia.")
        elif user_choice == "6":
            print("[!] Fitur transaksi belum tersedia.")
        elif user_choice == "7":
            print("[!] Fitur transaksi belum tersedia.")
        elif user_choice.strip() == "/c":
            os.system("cls" if os.name == "nt" else "clear")
            show_main_menu()
        elif user_choice.strip() == "/d":
            delete_product()
        else:
            print("[!] Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
