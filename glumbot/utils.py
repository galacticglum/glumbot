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