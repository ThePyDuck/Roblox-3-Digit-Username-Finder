"""
Roblox 3-Character Username Checker
by ThePYDuck
"""

import asyncio
import random
from aiohttp import ClientSession, ClientTimeout
from aiohttp_socks import ProxyConnector
from fake_useragent import UserAgent

class RobloxNameChecker:
    def __init__(self):
        self.available = []
        self.bad_proxies = set()
        self.ua = UserAgent()
        self.checked = 0
        
        # My collected proxies
        self.proxies = [
            "socks4://72.195.34.42:4145",
            "socks4://172.232.162.85:22001",
            "http://65.21.52.41:8888",
            "http://185.155.99.114:8118",
            "socks4://184.178.172.14:4145",
            "http://119.3.113.150:9094",
            "socks4://103.83.252.61:1080"
        ]

    async def check_name(self, session, name):
        try:
            async with session.get(
                "https://auth.roblox.com/v2/usernames/validate",
                params={"request.username": name, "request.birthday": "2000-01-01"}
            ) as res:
                self.checked += 1
                if res.status == 429:
                    await asyncio.sleep(random.uniform(3, 8))
                    return await self.check_name(session, name)
                
                data = await res.json()
                if data.get("code") == 0:
                    print(f"\n[FOUND] {name}")
                    self.available.append(name)
                else:
                    print(f"Checked: {self.checked} | Current: {name}", end="\r")
        
        except Exception as e:
            if "proxy" in str(e).lower():
                self.bad_proxies.add(session.connector.proxy)
            await asyncio.sleep(1)

    async def get_session(self):
        working = [p for p in self.proxies if p not in self.bad_proxies]
        if not working:
            return ClientSession(headers={"User-Agent": self.ua.random})
        
        proxy = random.choice(working)
        try:
            return ClientSession(
                connector=ProxyConnector.from_url(proxy),
                headers={"User-Agent": self.ua.random},
                timeout=ClientTimeout(total=10)
            )
        except:
            self.bad_proxies.add(proxy)
            return await self.get_session()

    async def run(self, names):
        tasks = []
        async with await self.get_session() as session:
            for name in names:
                task = asyncio.create_task(self.check_name(session, name))
                tasks.append(task)
                await asyncio.sleep(random.uniform(0.1, 0.3))
            await asyncio.gather(*tasks)

        print(f"\n\nFound {len(self.available)} available names:")
        for name in self.available:
            print(f"https://www.roblox.com/signup?username={name}")

def load_names():
    with open("names.txt") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    print("Roblox 3-Char Name Finder - ThePYDuck\n")
    checker = RobloxNameChecker()
    asyncio.run(checker.run(load_names()))