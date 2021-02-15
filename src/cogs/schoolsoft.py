import json
import requests
from discord import Embed, Colour
from discord.ext import commands
from re import search


class SchoolSoft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Get the lunch from SchoolSoft"

    @commands.command(name="lunch")
    async def lunch(self, ctx):
        """Get the lunch from SchoolSoft"""
        lunch = requests.get(
            "https://apischoolsoft.herokuapp.com/v2/lunch").json()

        days = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
        embeds = Embed(title="Veckans Lunchmeny",
                       url="https://sms.schoolsoft.se/nti/jsp/student/right_student_lunchmenu.jsp?menu=lunchmenu", colour=Colour(0x46c3db))
        embeds.set_author(name="SchoolSoft", url="https://sms.schoolsoft.se/nti/jsp/student/right_student_lunchmenu.jsp?menu=lunchmenu",
                          icon_url="https://sms.schoolsoft.se/android-chrome-192x192.png")
        for day in range(0, 5):
            try:
                if len(lunch[day]) != 2:
                    embeds.add_field(
                        name=days[day], value=lunch[day][0], inline=False)
                else:
                    embeds.add_field(
                        name=days[day], value=f"{lunch[day][0]} \n {lunch[day][1]}", inline=False)
            except Exception as e:
                print(e)

        await ctx.send(embed=embeds)

    @commands.command(name="schedule")
    async def schedule(self, ctx, inputClassName: str = None, inputDay: str = None):
        """ Get the schedule from SchoolSoft by class name[required] day[Optional]"""
        ValidClassName = ["TE18", "TE19", "TE20",
                          "IT18", "IT19", "IT20", "HA18", "HA19"]
        SwedishDays = ["måndag", "tisdag", "onsdag", "torsdag", "fredag"]
        NormalDays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        dayIndex = 0

        if inputClassName is None:
            await ctx.reply("Vänligen ange klassnamnet")

        className = inputClassName.upper()

        if className not in ValidClassName:
            await ctx.reply("Klassnamnet är ogiltig")

        embed = Embed(
            url="https://sms.schoolsoft.se/nti/jsp/student/right_student_schedule.jsp?menu=schedule", colour=Colour(0x46c3db))
        embed.set_author(name="SchoolSoft", url="https://sms.schoolsoft.se/nti/jsp/student/right_student_schedule.jsp?menu=schedule",
                         icon_url="https://sms.schoolsoft.se/android-chrome-192x192.png")

        if inputDay is None:
            ToDaysSchedule = requests.get(
                f"https://apischoolsoft.herokuapp.com/v2/schedule/{className}?today=true").json()

            embed.title = f"Dagens schema"
            for index in ToDaysSchedule:

                if index['location'] == "None":
                    embed.add_field(
                        name=index["subject"], value=f"Klassen börjar kl {index['time']} men klassrum specificerades inte", inline=False)
                else:
                    embed.add_field(
                        name=index["subject"], value=f"Klassen börjar kl {index['time']} i rum {index['location']}", inline=False)

        else:

            if inputDay in SwedishDays:
                dayIndex = SwedishDays.index(inputDay, 0, 5)
            elif inputDay in NormalDays:
                dayIndex = NormalDays.index(inputDay, 0, 5)
            else:
                await ctx.reply("Ogiltig dag")

            day = NormalDays[dayIndex]

            Schedule = requests.get(
                f"https://apischoolsoft.herokuapp.com/v2/schedule/{className}?day={day}").json()

            embed.title = f"{inputDay.capitalize()} schema"
            for index in Schedule:

                if index['location'] == "None":
                    embed.add_field(
                        name=index["subject"], value=f"Klassen börjar kl {index['time']} men klassrum specificerades inte", inline=False)
                else:
                    embed.add_field(
                        name=index["subject"], value=f"Klassen börjar kl {index['time']} i rum {index['location']}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="contacts")
    async def contacts(self, ctx, name: str):
        """Get the contacts of a staff by name"""

        embed = Embed(
            url="https://sms.schoolsoft.se/nti/jsp/student/right_student_staff.jsp?menu=contactlist", colour=Colour(0x46c3db))
        embed.set_author(name="SchoolSoft", url="https://sms.schoolsoft.se/nti/jsp/student/right_student_staff.jsp?menu=contactlist",
                         icon_url="https://sms.schoolsoft.se/android-chrome-192x192.png")

        if name is not None:
            request = requests.get(
                "https://apischoolsoft.herokuapp.com/v2/contactlist").json()

            try:
                for NameOfStaff in request:
                    if search(name, NameOfStaff):
                        print(request[NameOfStaff])
                        embed.add_field(
                            name=request[NameOfStaff]["name"], value=f"{request[NameOfStaff]['role']}", inline=False)
                        embed.add_field(
                            name="Email", value=f"{request[NameOfStaff]['email']}", inline=False)
                        embed.add_field(
                            name="Phone", value=f"{request[NameOfStaff]['phone']}", inline=False)
                    else:
                        pass
            except Exception as e:
                print(e)
        else:
            await ctx.reply("ange personalen")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SchoolSoft(bot))
