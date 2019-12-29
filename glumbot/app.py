from glumbot.config import Config
from twitchio.ext import commands

class Bot(commands.Bot):
    _CONFIG_DEFAULTS = {
        'PREFIX': '!'
    }

    def __init__(self):
        self.config = Config(Bot._CONFIG_DEFAULTS)

    def setup(self):
        super().__init__(
            irc_token=self.config['IRC_TOKEN'], 
            client_id=self.config['CLIENT_ID'], 
            nick=self.config['NICK'], 
            prefix=self.config['PREFIX'], 
            initial_channels=self.config['INITIAL_CHANNELS']
        )

    async def event_ready(self):
        print('Bot is ready!')
    
    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='test')
    async def test_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')