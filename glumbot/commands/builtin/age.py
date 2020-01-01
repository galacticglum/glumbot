import datetime

async def execute(self, ctx, parameters, args):
    birthday = datetime.datetime.strptime(parameters['birthday'], '%Y-%m-%d').date()
    today =  datetime.date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    caster_user = await self.get_caster_user(ctx.message.channel)
    await ctx.send(parameters['response'].format(caster_name=caster_user.display_name, age=age))