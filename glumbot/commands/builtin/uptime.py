import datetime
from glumbot.utils import list_join, pluralize_value

async def execute(self, ctx, parameters, args):
    current_stream = await self.get_stream(str(ctx.message.channel))
    caster_user = await self.get_caster_user(ctx.message.channel)
    if current_stream is None:
        await ctx.send(parameters['offline_message'].format(caster_name=caster_user.display_name))
    else:
        time_components = []
        
        total_seconds = (datetime.datetime.utcnow() - datetime.datetime.strptime(current_stream['started_at'],'%Y-%m-%dT%H:%M:%SZ')).total_seconds()
        hours = int(total_seconds // 3600)
        if hours > 0: time_components.append(pluralize_value(hours, 'hour', 'hours'))
        
        total_seconds -= hours * 3600
        minutes = int(total_seconds // 60)
        if minutes > 0: time_components.append(pluralize_value(minutes, 'minute', 'minutes'))

        total_seconds -= minutes * 60
        time_components.append(pluralize_value(int(total_seconds), 'second', 'seconds'))

        await ctx.send(parameters['online_message'].format(caster_name=caster_user.display_name, uptime=list_join(time_components, 'and')))