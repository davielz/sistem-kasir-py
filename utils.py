def input_not_empty(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("[!] Input tidak boleh kosong. Silakan coba lagi.")


def input_int(prompt, positive_only=False):
    while True:
        try:
            value = int(input(prompt))
            if positive_only and value < 0:
                print("[!] Input harus berupa angka bulat positif. Silakan coba lagi.")
                continue
            return value
        except ValueError:
            print("[!] Input harus berupa angka bulat. Silakan coba lagi.")


def input_float(prompt, positive_only=False):
    while True:
        try:
            value = float(input(prompt))
            if positive_only and value < 0:
                print("[!] Input harus berupa angka positif. Silakan coba lagi.")
                continue
            return value
        except ValueError:
            print("[!] Input harus berupa angka. Silakan coba lagi.")


def format_rupiah(x: float) -> str:
    return f"Rp. {int(round(x)):,}".replace(",", ".")
