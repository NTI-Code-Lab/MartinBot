from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx):
        """Test command"""
        await ctx.send("Test")


def setup(bot):
    bot.add_cog(Test(bot))
