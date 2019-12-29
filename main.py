from glumbot import app

bot = app.Bot()
bot.config.from_pyfile('local_config.py')

bot.setup()
bot.run()