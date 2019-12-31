async def execute(self, ctx, parameters, args):
    track = self.spotify_cog.client.current_user_playing_track()
    is_offline = await self.get_stream(str(ctx.message.channel)) is None
    if is_offline and not parameters['show_songs_offline'] or track is None or not track['is_playing']: return

    track_item = track['item']
    track_name = track_item['name']
    artists_name = ', '.join(artist['name'] for artist in track_item['artists'])
    album_name = track_item['album']['name'] if 'album' in track_item else ''

    await ctx.send(parameters['format'].format(track_name=track_name, artists_name=artists_name, album_name=album_name))