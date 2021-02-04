import json
import requests
from discord import Embed, Colour
from discord.ext import commands

class SchoolSoft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Get the lunch from SchoolSoft"

    @commands.command(name="lunch")
    async def lunch(self, ctx):
        """Get the lunch from SchoolSoft"""
        lunch = requests.get("https://apischoolsoft.herokuapp.com/v1/lunch").json()
        
        days = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
        embeds = Embed(title="Veckans Lunchmeny",url="https://sms.schoolsoft.se/nti/jsp/student/right_student_lunchmenu.jsp?menu=lunchmenu", colour=Colour(0x46c3db))
        embeds.set_author(name="SchoolSoft", url="https://sms.schoolsoft.se/nti/jsp/student/right_student_lunchmenu.jsp?menu=lunchmenu", icon_url="https://sms.schoolsoft.se/android-chrome-192x192.png")
        for day in range(0, 5):
            try:
                if len(lunch[day]) != 2:
                    embeds.add_field(name=days[day] ,value=lunch[day][0], inline=False)
                else:
                    embeds.add_field(name=days[day] ,value=f"{lunch[day][0]} \n {lunch[day][1]}", inline=False)
            except Exception as e:
                print(e)
        
        await ctx.send(embed=embeds)
        
    @commands.command(name="schedule")
    async def schedule(self, ctx, *, className: str = None, day: str = None):
        """ Get the schedule from SchoolSoft """
        print(className)
        print(day)
        #Schedule = requests.get(f"https://apischoolsoft.herokuapp.com/v1/schedule/{className}?day=${day}").json()
        #ToDaysSchedule = requests.get(f"https://apischoolsoft.herokuapp.com/v1/schedule/{className}?today=true").json()

def setup(bot):
    bot.add_cog(SchoolSoft(bot))
