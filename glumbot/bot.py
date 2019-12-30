import json
import uuid
import inspect
import importlib.util
from jsonschema import validate as validate_json
from pathlib import Path

from glumbot.logger import init as init_logger
from glumbot.config import Config
from glumbot.nlp_qa.model import Model as NLPModel, ModelType as NLPModelType
import twitchio.ext.commands

class Bot(twitchio.ext.commands.Bot):
    _CONFIG_DEFAULTS = {
        'APP_NAME': __name__,
        'PREFIX': '!',
        'DISPLAY_MESSAGES': True,
        'DISPLAY_OWN_MESSAGES': False,
        'USE_NLP_QA': False,
        'NLP_QA_PREFIX': '>',
        'NLP_QA_DATA_FORMAT': 'csv',
        'NLP_MODEL_TYPE': NLPModelType.FAST_TEXT
    }

    _COMMANDS_JSON_SCHEMA = {
        'type': 'array',
        'items': {
            'type': 'object'
        }
    }

    _COMMAND_JSON_SCHEMA = {
        'type': 'object',
        'properties': {
                'name': {
                    'type': 'string'
                },
                'response': {
                    'type': 'string'
                },
                'script': {
                    'type': 'string'
                },
                'aliases': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            },
        'required': ['name'],
        'anyOf': [
            {'required': ['response']},
            {'required': ['email']}
        ]
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

        self._load_commands()
        self._load_nlp_qa()

        super().__init__(
            irc_token=self.config['IRC_TOKEN'], 
            client_id=self.config['CLIENT_ID'], 
            nick=self.config['NICK'], 
            prefix=self.config['PREFIX'], 
            initial_channels=self.config['INITIAL_CHANNELS']
        )

        super().run()
    
    def _load_commands(self):
        '''
        Load and initialize commands from JSON.
        '''

        # The command_json_path is relative to the working directory, NOT the instance folder.
        command_json_path = Path(self.config['COMMANDS_FILE'])
        count = 0
        with open(command_json_path, 'r') as file:
            commands = json.load(file)
            command_filepath_str = str(command_json_path.resolve())

            try:
                validate_json(instance=commands, schema=Bot._COMMANDS_JSON_SCHEMA)
            except:
                error_message = 'Could not load commands from file \'{}\'.'
                self.logger.exception(error_message.format(command_filepath_str))

            for command in commands:
                try:
                    validate_json(instance=command, schema=Bot._COMMAND_JSON_SCHEMA)
                except:
                    error_message = 'Could not load command with name {} from file \'{{}}\''.format(command['name']) if 'name' in command \
                        else 'Could not load command from file \'{}\'.'
                        
                    self.logger.exception(error_message.format(command_filepath_str))
                    continue

                command_id = str(uuid.uuid4()).replace('-', '_')
                method_name = 'commandhandler_{}_{}'.format(command['name'], command_id)
                command_aliases = command['aliases'] if 'aliases' in command else None

                script_module = None
                if 'script' in command:
                    # The script path is relative to the command JSON file...
                    script_path = (command_json_path.parent / Path(command['script'])).resolve().absolute()
                    if not script_path.exists():
                        self.logger.warn('Encountered error in processing custom script for command with name \'{}\'. \
                            Could not find the file at path \'{}\'.'.format(command['name'], str(script_path)))
                        continue
                        
                    spec = importlib.util.spec_from_file_location(script_path.stem + ''.join(script_path.suffixes), str(script_path))
                    script_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(script_module)

                    # Verify that the execute method has a valid signature...
                    if hasattr(script_module, 'execute'):
                        valid = True
                        if len(inspect.signature(script_module.execute).parameters) < 2:
                            self.logger.warn('Encountered error in processing custom script for command with name \'{}\'. \
                                The execute method has an invalid signature. At least two parameters are required for the class \
                                instance and context parameters; \'self\' and \'ctx\' respectively.'.format(command['name']))

                            valid = False
                        elif not inspect.iscoroutinefunction(script_module.execute):
                            self.logger.warn('Encountered error in processing custom script for command with name \'{}\'. \
                                The execute method must be a coroutine function (a function defined with an async def syntax).' \
                                    .format(command['name']))
                                    
                            valid = False

                        if not valid:
                            delattr(script_module, 'execute')

                @twitchio.ext.commands.command(name=command['name'], aliases=command_aliases)
                async def _command_handler(self, ctx):
                    if 'response' in command:
                        await ctx.send(command['response'])
                        if script_module and hasattr(script_module, 'execute'):
                            await script_module.execute(self, ctx)

                setattr(self.__class__, method_name, _command_handler)
                count += 1

        self.logger.info('Finished loading commands ({}).'.format(count))

    def _load_nlp_qa(self):
        if not self.config['USE_NLP_QA']: return

        data_path = str(Path(self.config['NLP_QA_DATA_PATH']).resolve().absolute())
        self.nlp_qa_model = NLPModel(self.config['NLP_MODEL_TYPE'], data_path, self.config['NLP_QA_DATA_FORMAT'])
        self.logger.info('Finished building NLP QA model.')

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
            is_own_message = message.author.name.lower() == self.config['NICK'].lower()
            display_own = self.config['DISPLAY_OWN_MESSAGES']
            if display_own or not display_own and not is_own_message:
                self.logger.info('{}: {} (in #{})'.format(message.author.name, message.content, message.channel))

        if self.config['USE_NLP_QA'] and message.content.startswith(self.config['NLP_QA_PREFIX']):
            clean_message = message.content[1:].strip()
            ctx = await self.get_context(message)

            prediction, confidence = self.nlp_qa_model.predict([clean_message])
            self.logger.info('Matched NLP query (message = "{}", prediction = \"{}\", confidence = {:.3f})' \
                .format(clean_message, prediction, confidence))

            await ctx.send(prediction)
        else:
            try:
                await self.handle_commands(message)
            except twitchio.ext.commands.errors.CommandError:
                pass
