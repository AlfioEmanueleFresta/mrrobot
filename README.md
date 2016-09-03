# Mr Robot

A simple personal key logger in Python.


**Features include**:

* Runs on Linux (Xlib), OS X and recent Windows operating systems;
* Simple high-level Python API;
* Configurable memory buffer (with reasonable defaults), to avoid frequent write operations on disks;
* Public-key cryptography, allowing you to encrypt the data and keep the decryption key in a separate place;
* Async IO in OS X (coming soon on Windows and Linux);
* Collects timing data -- useful for timing analytics.


# Compatibility

| *Feature \ Platform* | **Linux (Xlib)**             | **Windows**                  | **OS X**  |
|----------------------|------------------------------|------------------------------|-----------|
| **Backend**          | `python3-xlib`               | `pyHook` (`pywin32`)         | `pyobjc`  |
| **Event**            | KeyDown                      | KeyDown                      | KeyDown   |
| **Captured keys**    | All ASCII, Return, Backspace | All ASCII, Return, Backspace | All ASCII |
| **Case sensitive**   | Yes                          | No                           | Yes       |


# Requirements

## Windows

* [Python 3.5](https://www.python.org/downloads/)
* [Python for Windows Extensions (pywin32)](https://sourceforge.net/projects/pywin32/files/pywin32/)
* [PyHook for Python 3](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)
* `> pip install pycrypto`

## Linux (Xlib)

On modern Ubuntu-like systems:

```bash
sudo apt-get install -y python3 python3-pip python3-xlib
sudo pip3 install pycrypto
```

## OS X

Either,

* Python 2.7 (pre-installed)
* `$ sudo pip install git+https://github.com/abarnert/pykeycode`
* `$ sudo pip install pycrypto`
* Add the Python 2.7 app to the allowed apps in **System Preferences > Security & Privacy > Accessibility**.


or,

* [Python 3.5](https://www.python.org/downloads/)
* `$ xcode-select --install`
* `$ sudo pip3 install git+https://github.com/abarnert/pykeycode`
* `$ sudo pip3 install pyobjc`
* `$ sudo pip3 install pycrypto`
* Add the Python 3.5 app to the allowed apps in **System Preferences > Security & Privacy > Accessibility**.



# Usage

## Key logger example

*Talk is cheap*, show me an `example.py`.

```python
from mrrobot.catcher import Catcher
from mrrobot.logger import FileLogger


# A file logger that writes to 'output.txt' every 32 key strokes (default buffer_size).
l = FileLogger(filename="output.txt")

# Get our platform's keys catcher, and connect it to our logger.
c = Catcher(logger=l)

# Run!
c.run()

```

## Reading the log

You can read a log written using `FileLogger` with the `get_log_entries` generator:

```python
from mrrobot.reader import get_log_entries


for entry in get_log_entries("output.txt"):

    print("Time=%s, Character='%s'" % (entry.timestamp,
                                       entry.character))
```



## Quick reference

Here are a few included included loggers (in `mrrobot.logger`):

```python
Debugger()  # Prints out all characters. Not very useful.
FileLogger("output.txt")  # Logs to a memory buffer and occasionally append text to a file.
FileLogger("output.txt", buffer_size=1)  # You can also change the buffer size.
FileLogger("output.txt.gz")  # Gzip compression (use only with default or large buffer sizes).
FileLogger("output.txt", public_key_file="id_rsa.pub")  # Use RSA encryption.
FileLogger("output.txt.gz", public_key_file="id_rsa.pub")  # Use RSA encryption + gzip compression.
```

## Encryption

You can use an pair of RSA keys, either in OpenSSH (id_rsa, id_rsa.pub) or
OpenSSL format (.pem files), to encrypt your logs.

### Generate a RSA keypair

To generate a pair of RSA keys on Linux or OS X:

```bash
$ ssh-keygen -t rsa
```


### Write example

```python
l = FileLogger(filename="output.txt",
               public_key_file="~/.ssh/id_rsa.pub")
```


### Read example

```python
for entry in get_log_entries("output.txt",
                             private_key_file="~/.ssh/id_rsa"):
    print(entry)
```


## Compression

When using a `FileLogger`, if the filename ends in `.gz`, it will automatically
be compressed using Gzip. Similarly, `get_log_entries` will decompress the file
on-the-fly.

### Write example
```python
l = FileLogger(filename="output.txt.gz")
```

### Read example
```python
for entry in get_log_entries("output.txt.gz"):
    print(entry)
```

You can also combine compression and encryption -- as the RSA encryption will
significantly increase disk usage.


# License

GPLv3

