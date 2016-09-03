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


class Buffer:

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

    def __init__(self, filename, compress=False, *args, **kwargs):
        self.filename = filename
        self.compress = compress
        super(FileLogger, self).__init__(*args, **kwargs)

    def use_buffer(self, buffer):
        open_function = gzip.open if self.compress else open
        with open_function(self.filename, 'at') as f:
            for time, data in buffer:
                f.write("%s %s\n" % (time, json.dumps(data)))


class CompressedFileLogger(FileLogger):

    DEFAULT_BUFFER_SIZE = 256

    def __init__(self, *args, **kwargs):
        kwargs['compress'] = True
        super(CompressedFileLogger, self).__init__(*args, **kwargs)


class FileBuffer(FileLogger):

    DEFAULT_FILE_BUFFER_SIZE = 1024

    def __init__(self, *args, file_buffer_size=DEFAULT_FILE_BUFFER_SIZE, **kwargs):
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