from pathlib import Path
import csv
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "expenses.csv"

MENU = """
=== KALKULATOR WYDATKÓW (CLI) ===
1) Dodaj wydatek
2) Pokaż wszystkie wydatki
3) Suma za miesiąc (YYYY-MM)
4) Zakończ
Wybierz opcję: """

def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])  # nagłówki

def add_expense():
    today = datetime.today().strftime("%Y-%m-%d")
    date = input(f"Data (Enter = {today}): ").strip() or today
    category = input("Kategoria (np. jedzenie, transport): ").strip() or "inne"
    description = input("Opis: ").strip() or "-"
    amount_str = input("Kwota (np. 23.50): ").strip()
    try:
        amount = round(float(amount_str.replace(",", ".")), 2)
    except ValueError:
        print("❗ Błąd: kwota musi być liczbą. Spróbuj ponownie.")
        return

    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, description, f"{amount:.2f}"])
    print("✅ Zapisano wydatek.")

def read_all():
    if not CSV_PATH.exists():
        print("Brak danych.")
        return []
    rows = []
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def show_all():
    rows = read_all()
    if not rows:
        print("Brak wydatków.")
        return
    print("\n--- LISTA WYDATKÓW ---")
    for r in rows:
        print(f"{r['date']} | {r['category']:<10} | {r['description']:<30} | {r['amount']} zł")
    print("----------------------\n")

def sum_for_month():
    ym = input("Podaj miesiąc (YYYY-MM): ").strip()
    try:
        datetime.strptime(ym, "%Y-%m")
    except ValueError:
        print("❗ Błędny format. Użyj YYYY-MM, np. 2025-09.")
        return
    rows = read_all()
    total = 0.0
    for r in rows:
        if r["date"].startswith(ym):
            try:
                total += float(r["amount"])
            except ValueError:
                pass
    print(f"💰 Suma za {ym}: {total:.2f} zł")

def main():
    ensure_storage()
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_all()
        elif choice == "3":
            sum_for_month()
        elif choice == "4":
            print("Do zobaczenia!")
            break
        else:
            print("Nieprawidłowa opcja.")

if __name__ == "__main__":
    main()