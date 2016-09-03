# Mr Robot

A simple personal key logger for modern Windows, Linux and OS X systems.

# Requirements

## Windows

* [Python 3.5](https://www.python.org/downloads/)
* [Python for Windows Extensions (pywin32)](https://sourceforge.net/projects/pywin32/files/pywin32/)
* [PyHook for Python 3](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)

## OS X

Either,

* Python 2.7 (pre-installed)
* ```bash
  sudo pip install git+https://github.com/abarnert/pykeycode
  ```
* Add the Python 2.7 app to the allowed apps in **System Preferences > Security & Privacy > Accessibility**.


or,

* [Python 3.5](https://www.python.org/downloads/)
* ```bash
  xcode-select --install
  ```
* ```
  sudo pip3 install git+https://github.com/abarnert/pykeycode
  sudo pip3 install pyobjc
  ```
* Add the Python 3.5 app to the allowed apps in **System Preferences > Security & Privacy > Accessibility**.


## Linux (Xlib)

On modern Ubuntu-like systems:

```bash
sudo apt-get install -y python3 python3-pip python3-xlib
```

# Usage

*Talk is cheap*, show me an `example.py`.

```python
from mrrobot.catcher import Catcher
from mrrobot.logger import FileLogger


# A file logger that writes to 'output.txt' every 8 characters.
# Obviously, you may want to increase the buffer size.
# With a very large buffer size, you can also use compress=True and a .gz filename.
l = FileLogger(filename="output.txt",
               buffer_size=8)

# Get our platform's keys catcher, and connect it to our logger.
c = Catcher(logger=l)

# Run!
c.run()

```

## Other loggers

Here are a few included included loggers (in `mrrobot.logger`):

```python
Debugger()  # Prints out all characters. Not very useful.
FileLogger("output.txt")  # Logs to a memory buffer and occasionally append text to a file.
FileLogger("output.txt", buffer_size=1)  # You can also change the buffer size.
FileLogger("output.txt.gz", buffer_size=1024)  # Gzip compression (use only with large buffer sizes).
CompressedFileLogger("output.txt.gz")  # Alias for the previous logger.
```

There are also a few abstract interfaces (with non-implemented methods):

```python
Logger()  # A simple logger.
Buffer(buffer_size=32)  # A simple logger with a configurable memory buffer.

# As above, but a file is used as a higher level buffer.
# Ideally, to be used if you want occasional network operations but
# want to persist frequently to disk.
FileBuffer("buffer.txt", buffer_size=32, file_buffer_size=1024)
```

## Reading

You can read a log written using `FileLogger` or `CompressedFileLogger` with the `get_log_entries` generator:

```python
from mrrobot.reader import get_log_entries


for entry in get_log_entries("output.txt"):
# for entry in get_log_entries("output.txt.gz"):

    print("Time=%s, Character='%s'" % (entry.timestamp,
                                       entry.character))
```


# License

GPLv3

