from glumbot.logger import init as init_logger
from glumbot.config import Config
from twitchio.ext import commands

class Bot(commands.Bot):
    _CONFIG_DEFAULTS = {
        'APP_NAME': __name__,
        'PREFIX': '!',
        'DISPLAY_MESSAGES': True,
    }

    def __init__(self):
        '''
        Initialize the bot.
        '''
        
        self.config = Config(Bot._CONFIG_DEFAULTS)

    def init_logger(self):
        '''
        Initialize the logger.
        '''
        
        self.logger = init_logger(self.config['APP_NAME'])

    def run(self):
        '''
        Setup and run the bot.
        '''

        super().__init__(
            irc_token=self.config['IRC_TOKEN'], 
            client_id=self.config['CLIENT_ID'], 
            nick=self.config['NICK'], 
            prefix=self.config['PREFIX'], 
            initial_channels=self.config['INITIAL_CHANNELS']
        )

        super().run()
        

    async def event_ready(self):
        '''
        Raised when the bot is ready.
        '''

        self.logger.info('Twitch bot is ready!')
    
    async def event_message(self, message):
        '''
        Raised when a new message is sent in one of the connected channels.
        '''

        if self.config['DISPLAY_MESSAGES']:
            self.logger.info('{}: {} (in #{})'.format(message.author.name, message.content, message.channel))

        await self.handle_commands(message)

    @commands.command(name='test')
    async def test_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')