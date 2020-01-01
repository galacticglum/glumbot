import time
import shutil

def rmtree(path, ignore_errors=False, onerror=None, timeout=10):
    '''
    A wrapper method for 'shutil.rmtree' that waits up to the specified
    `timeout` period, in seconds.
    '''

    shutil.rmtree(path, ignore_errors, onerror)

    if path.is_dir():
        logger.warning(f'''shutil.rmtree - Waiting for \'{path}\' to be removed...''')
        # The destination path has yet to be deleted. Wait, at most, the timeout period.
        timeout_time = time.time() + timeout
        while time.time() <= timeout_time:
            if not path.is_dir():
                break

def list_join(list, conjunction_str, format_func=str, oxford_comma=True):
    '''
    Joins a list in a grammatically-correct fashion.
    :param list:
        the list to join.
    :param conjunction_str: 
        the string to use as conjunction between two items.
    :param format_func:
        a function that takes in a string and returns a formatted string (default=str, optional).
    :param oxford_comma: 
        indicates whether to use oxford comma styling (default=True, optional).
    :returns:
        a string representing the grammatically-correct joined list.
    :usage::
        >>> list_join(['apple', 'orange', 'pear'], 'and')
        apple, orange, and pear'`
    '''

    if not list: return ''
    if len(list) == 1: return format_func(list[0])
    
    first_part = ', '.join([format_func(i) for i in list[:-1]])
    comma = ',' if oxford_comma and len(list) > 2 else ''

    return f'{first_part}{comma} {conjunction_str} {format_func(list[-1])}'

def pluralize_value(value, singular_unit, plural_unit):
    return '{} {}'.format(str(value), plural_unit if value != 1 else singular_unit)