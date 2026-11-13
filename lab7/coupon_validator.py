from datetime import date
import math


def split_code(code):
    if not isinstance(code, str):
        return None

    parts = code.strip().upper().split('-')

    if len(parts) != 2 or not parts[0] or not parts[1]:
        return None

    if not parts[1].isdigit():
        return None

    return parts[0], int(parts[1])


def most_expensive(prices_csv):
    if not isinstance(prices_csv, str) or not prices_csv.strip():
        return None

    try:
        prices = [float(p.strip()) for p in prices_csv.split(',')]

        if not prices or any(
            not math.isfinite(p) or p < 0 for p in prices
        ):
            return None

        return max(prices)

    except ValueError:
        return None


def expiry_days(date_text):
    if not isinstance(date_text, str):
        return None

    try:
        expiry_date = date.fromisoformat(date_text)
        return (expiry_date - date.today()).days

    except ValueError:
        return None


def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    print("Days Until Expiry:", result)


if __name__ == "__main__":
    main()