from glumbot.integrations.spotify_cog import SpotifyCog

def setup(bot):
    if bot.config['ENABLE_SPOTIFY_INTEGRATION']:
        bot.add_cog(SpotifyCog(bot))