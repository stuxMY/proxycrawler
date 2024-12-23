#!/usr/bin/env python3
import os
import re
import requests
import subprocess

SOCKS4_URL = "https://vakhov.github.io/fresh-proxy-list/socks4.txt"
SOCKS5_URL = "https://vakhov.github.io/fresh-proxy-list/socks5.txt"

PROXY_DIR = "proxy_lists"
SOCKS4_FILE = os.path.join(PROXY_DIR, "socks4.txt")
SOCKS5_FILE = os.path.join(PROXY_DIR, "socks5.txt")
SOCKS4_FILTERED_FILE = os.path.join(PROXY_DIR, "socks4_filtered.txt")
SOCKS5_FILTERED_FILE = os.path.join(PROXY_DIR, "socks5_filtered.txt")
SOCKS4_LIVE_FILE = os.path.join(PROXY_DIR, "socks4-live.txt")
SOCKS5_LIVE_FILE = os.path.join(PROXY_DIR, "socks5-live.txt")

os.makedirs(PROXY_DIR, exist_ok=True)

def download_proxies(url, save_path):
    print(f"Downloading proxies from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "w") as file:
        file.write(response.text.strip())
    print(f"Proxies saved to {save_path}.")

def filter_and_format_proxies(input_file, output_file, protocol):
    print(f"Filtering and formatting {protocol.upper()} proxies from {input_file}...")
    valid_proxies = []
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if re.match(r"^\d{1,3}(\.\d{1,3}){3}:\d{1,5}$", line):
                valid_proxies.append(f"{protocol}://{line}")

    with open(output_file, "w") as file:
        file.write("\n".join(valid_proxies))
    print(f"Formatted {protocol.upper()} proxies saved to {output_file}.")

def check_live_proxies(input_file, output_file):
    print(f"Checking live proxies from {input_file}...")
    try:
        subprocess.run(
            ["mubeng", "-f", input_file, "-o", output_file, "-c", "5"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"Live proxies saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running mubeng: {e}")

def main():
    download_proxies(SOCKS4_URL, SOCKS4_FILE)
    download_proxies(SOCKS5_URL, SOCKS5_FILE)

    filter_and_format_proxies(SOCKS4_FILE, SOCKS4_FILTERED_FILE, "socks4")
    filter_and_format_proxies(SOCKS5_FILE, SOCKS5_FILTERED_FILE, "socks5")

    check_live_proxies(SOCKS4_FILTERED_FILE, SOCKS4_LIVE_FILE)
    check_live_proxies(SOCKS5_FILTERED_FILE, SOCKS5_LIVE_FILE)

if __name__ == "__main__":
    main()
