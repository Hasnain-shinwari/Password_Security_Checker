import string
import time
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def check_password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_lower, has_upper, has_digit, has_symbol])

    if length < 12:
        return 0, "Too short. Must be at least 12 characters."

    if score < 4:
        return 1, "Password must include lowercase, uppercase, digits, and symbols."

    return 2, "Strong password!"

def estimate_crack_time(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        return "Invalid charset."

    combinations = charset ** len(password)
    guesses_per_second = 1_000_000_000  # 1 billion guesses per second
    seconds = combinations / guesses_per_second

    return seconds_to_readable(seconds)

def seconds_to_readable(seconds):
    units = [
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
        ("seconds", 1),
    ]

    result = []
    for name, count in units:
        value = seconds // count
        if value >= 1:
            result.append(f"{int(value)} {name}")
            seconds %= count

    return ", ".join(result) if result else "less than a second"

def show_loading_bar(duration=2, steps=20):
    print(Fore.BLUE + "Estimating crack time:")
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = "█" * i + "-" * (steps - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()  # new line

def main():
    print(Fore.CYAN + "\n=== Password Security Checker ===")
    print(Fore.YELLOW + "Rules: Use at least 12 characters, with uppercase, lowercase, digits, and symbols.\n")

    password = input("Enter a password to test: ").strip()

    strength, message = check_password_strength(password)

    if strength == 0:
        print(Fore.RED + "Weak password: " + message)
    elif strength == 1:
        print(Fore.RED + "Moderate password: " + message)
    else:
        print(Fore.GREEN + "✔ " + message)

    # Show crack time regardless of strength
    show_loading_bar()
    crack_time = estimate_crack_time(password)
    print(Fore.MAGENTA + f"Estimated time to crack: {crack_time}")


if __name__ == "__main__":
    main()
