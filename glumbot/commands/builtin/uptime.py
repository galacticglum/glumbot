import datetime

async def execute(self, ctx, parameters, args):
    current_stream = await self.get_stream(str(ctx.message.channel))
    if current_stream is None:
        await ctx.send(parameters['offline_message'].format(caster_name=ctx.message.channel))
    else:
        delta = datetime.datetime.fromtimestamp(current_stream['started_at']) - datetime.datetime.utcnow()
        await ctx.send(parameters['online_message'].format(caster_name=ctx.message.channel, time=str(delta)))