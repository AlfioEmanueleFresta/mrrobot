from contextlib import contextmanager
import gzip
import json


class KeyEvent:

    def __init__(self, timestamp, character, args, kwargs):
        self.timestamp = timestamp
        self.character = character
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "<KeyEvent timestamp=%s, char='%s'>" % (self.timestamp, self.character)


def parse_event_line(line):
    dt = line[:26]
    data = line[27:]
    character, args, kwargs = json.loads(data)
    event = KeyEvent(dt, character, args, kwargs)
    return event


def get_log_lines(filename):
    function = gzip.open if '.gz' in filename else open
    with function(filename, 'rt') as f:
        for line in f:
            yield line.rstrip('\n')


def get_log_entries(filename, private_key_file=None):
    from .rsa import read_key, rsa_decrypt_string
    key = read_key(private_key_file) if private_key_file else None
    for line in get_log_lines(filename=filename):
        if key:
            line = rsa_decrypt_string(key, line)
        yield parse_event_line(line)
