import datetime

async def execute(self, ctx, parameters, *args):
    birthday = datetime.datetime.strptime(parameters['birthday'], '%Y-%m-%d').date()
    today =  datetime.date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    await ctx.send(parameters['response'].format(caster_name=ctx.message.channel, age=age))