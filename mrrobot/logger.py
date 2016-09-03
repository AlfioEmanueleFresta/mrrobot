from datetime import datetime
import json
import os
import gzip


class Logger:

    def __init__(self):
        pass

    def callback(self, character, *args, **kwargs):
        raise NotImplementedError


class Debugger:

    def callback(self, character, *args, **kwargs):
        print("Received: character='%s', args=(%s), kwargs=(%s)" % (character, args, kwargs))


class Buffer(object):

    DEFAULT_BUFFER_SIZE = 32

    def __init__(self, buffer_size=DEFAULT_BUFFER_SIZE):
        self.buffer = []
        self.buffer_size = buffer_size

    def callback(self, character, *args, **kwargs):
        self.buffer.append((datetime.now(), (character, args, kwargs)))
        if len(self.buffer) >= self.buffer_size:
            self.use_buffer(self.buffer)
            self.buffer = []

    def use_buffer(self, buffer):
        raise NotImplementedError


class FileLogger(Buffer):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.compress = '.gz' in filename
        super(FileLogger, self).__init__(*args, **kwargs)

    def _prepare_line(self, line):
        return line

    def use_buffer(self, buffer):
        open_function = gzip.open if self.compress else open
        with open_function(self.filename, 'at') as f:
            for time, data in buffer:
                line = "%s %s" % (time, json.dumps(data))
                line = self._prepare_line(line)
                f.write("%s\n" % line)


class CompressedFileLogger(FileLogger):

    DEFAULT_BUFFER_SIZE = 256

    def __init__(self, *args, **kwargs):
        kwargs['filename'] = kwargs['filename'] if '.gz' in kwargs['filename'] else "%s.gz" % kwargs['filename']
        super(CompressedFileLogger, self).__init__(*args, **kwargs)


class EncryptedFileLogger(FileLogger):

    DEFAULT_BUFFER_SIZE = 8

    def __init__(self, public_key_file, *args, **kwargs):
        from .rsa import read_key
        self.public_key = read_key(public_key_file)
        super(EncryptedFileLogger, self).__init__(*args, **kwargs)

    def _prepare_line(self, line):
        from .rsa import rsa_encrypt_string
        return rsa_encrypt_string(self.public_key, line)


class FileBuffer(FileLogger):

    DEFAULT_FILE_BUFFER_SIZE = 1024

    def __init__(self, file_buffer_size=DEFAULT_FILE_BUFFER_SIZE, *args, **kwargs):
        self.file_buffer_size = file_buffer_size
        super(FileBuffer, self).__init__(*args, **kwargs)

    def use_buffer(self, buffer):
        super(FileBuffer, self).use_buffer(buffer)
        if os.path.getsize(self.filename) >= self.file_buffer_size:
            self.empty_file_buffer()

    def empty_file_buffer(self):
        raise NotImplementedError


class FileBufferDebugger(FileBuffer):

    def empty_file_buffer(self):
        print(os.path.getsize(self.filename))
