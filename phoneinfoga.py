#!/usr/bin/env python3
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests
from bs4 import BeautifulSoup
import argparse


# ========== Number Scanner ==========
def scan_number(num):
    try:
        parsed = phonenumbers.parse(num, None)
        return {
            "valid": phonenumbers.is_valid_number(parsed),
            "possible": phonenumbers.is_possible_number(parsed),
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),   # Airtel, Jio, etc.
            "timezone": timezone.time_zones_for_number(parsed)
        }
    except Exception as e:
        return {"error": str(e)}


# ========== Web Search Scanner ==========
def search_web(num):
    try:
        url = f"https://duckduckgo.com/html/?q={num}"
        headers = {"User-Agent": "Mozilla/5.0 (PhoneInfoga-Custom)"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for link in soup.select(".result__a"):
            results.append(link.get("href"))
        return results[:10]
    except Exception as e:
        return [f"Search error: {e}"]


# ========== Social Footprint Scanner ==========
def check_social(num):
    results = {}
    results["WhatsApp"] = f"Check: https://wa.me/{num.replace('+','')}"
    results["Telegram"] = f"Try: https://t.me/{num.replace('+','')}"
    results["Facebook"] = f"https://www.facebook.com/search/top?q={num}"
    results["Truecaller"] = f"https://www.truecaller.com/search/{num.replace('+','')}"
    return results


# ========== Breach Scanner ==========
def check_breaches(num):
    return {
        "Dehashed": f"https://dehashed.com/search?query={num}",
        "Intelx": f"https://intelx.io/?s={num}",
        "HaveIBeenPwned": "Requires API key (not implemented)"
    }


# ========== Device Info (Public IP) ==========
def get_public_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        return ip
    except:
        return "Could not fetch IP"


# ========== MAIN ==========
def main():
    parser = argparse.ArgumentParser(description="PhoneInfoga-Py (custom recreation)")
    parser.add_argument("--number", required=True, help="Phone number (with country code, e.g. +919876543210)")
    args = parser.parse_args()

    print("\n[+] Scanning number:", args.number)

    # Device Info
    print("\n=== DEVICE INFO ===")
    print("Public IP:", get_public_ip())

    # Number info
    print("\n=== NUMBER INFO ===")
    num_info = scan_number(args.number)
    for k, v in num_info.items():
        print(f"{k.title()}: {v}")

    # Passive search
    print("\n=== WEB SEARCH ===")
    for r in search_web(args.number):
        print(" -", r)

    # Social footprint
    print("\n=== SOCIAL FOOTPRINT ===")
    for platform, link in check_social(args.number).items():
        print(f"{platform}: {link}")

    # Breach checks
    print("\n=== BREACH CHECKS ===")
    for name, link in check_breaches(args.number).items():
        print(f"{name}: {link}")


if __name__ == "__main__":
    main()