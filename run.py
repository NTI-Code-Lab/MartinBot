import discord

from src import main as Client

VERSION = "0.0.1"

def main():
    Client.bot.run(VERSION)


if __name__ == "__main__":
    print("[!] NTI Discord Bot Challenge 2021")
    print("[!] This project was develop by https://github.com/Simple-MAX")
    print(f"[!] discord.py version {discord.__version__}")
    main()
