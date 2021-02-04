import os
import json

try:
    import dotenv
    dotenv.load_dotenv()
except Exception as e:
    print("[-] missing module python-dotenv")
    print("[-] use -> pip install -r requirements.txt")
    print(f"[-] {e}")

try:
    import discord
    from discord.ext.commands import Bot as BotBase
    from discord.ext import commands, tasks

except Exception as e:
    print("[-] missing module discord")
    print("[-] use -> pip install -r requirements.txt")
    print(f"[-] {e}")
    
class Bot(BotBase):
        def __init__(self):
            self.ready = False
            self.VERSION = None
            self.command_prefix = str(os.getenv("DEFAULT_PREFIX"))
            self.description = "NTI Discord Bot Challenge 2021"
            super().__init__(command_prefix=self.command_prefix, help_command=discord.ext.commands.DefaultHelpCommand(),
                             description=self.description)

        def run(self, version=None):
            self.VERSION = version
            print("[?] Bot running ...")
            return super().run(str(os.getenv("TOKEN")), reconnect=True)

        @staticmethod
        async def on_connect():
            print("[+] Bot connected and is online")

        @staticmethod
        async def on_disconnect():
            print("[-] Bot disconnected")

        async def on_ready(self):
            if not self.ready:
                self.ready = True
                await self.change_presence(status=discord.Status.online,
                                           activity=discord.Activity(type=discord.ActivityType.watching,
                                                                     name=f"Over {len(bot.guilds)} Server"))
                print("Loading extensions")
                for filename in os.listdir("./src/cogs"):
                    if filename.endswith(".py"):
                        try:
                            self.load_extension(f"src.cogs.{filename[:-3]}")
                            print(f"[+] - {filename[:-3]} extension")
                        except ValueError:
                            print(f"[-] - {filename[:-3]} extension has issue")
                            print(f"[-] - {ValueError}")

            else:
                print("[!] Bot reconnecting")

bot = Bot()
