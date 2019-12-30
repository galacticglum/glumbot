import os
import sys
import click
import inspect
import logging

# Add parent module to imports...
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(current_dir)
sys.path.insert(0, parentdir)

def _set_verbosity_level(logger, value):
    x = getattr(logging, value.upper(), None)
    if x is None:
        raise click.BadParameter('Must be CRITICAL, ERROR, WARNING, INFO, or DEBUG, not \'{}\''.format(value))

    logger.setLevel(x)

@click.group(invoke_without_command=True)
@click.option('--verbosity', '-v', default='INFO', help='Either CRITICAL, ERROR, WARNING, INFO, or DEBUG.')
@click.option('--config', 'config_filepath', default='local_config.py', help='The name of the configuration file. This can be an absolute or relative path.')
@click.option('--config-root', default='instance', help='The path to the root directory of the configuration file.')
@click.pass_context
def cli(ctx, verbosity, config_filepath, config_root):
    '''
    Run the bot app.
    '''

    if ctx.invoked_subcommand is not None: return    
    from glumbot.bot import Bot

    bot = Bot()
    bot.config.from_pyfile(config_filepath, config_root)
    bot.init_logger()
    _set_verbosity_level(bot.logger, verbosity)

    bot.run()

if __name__ == '__main__':
    cli()