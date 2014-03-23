lazystream.py
=============

LazyStream is  a lazy (non-blocking) stream reader that collects lines from a stream (like stdout) as they become available.


Usage
-----

Suppose you need to run a system command that blocks for one second:

    from subprocess import Popen, PIPE
    command = 'sleep 1 && echo hello'
    process = Popen(command, shell=True, stdout=PIPE)

If you tried to read from process.stdout at this point, your program would pause for 1 second, before giving you 'hello'. If you don't want the blocking pause, read the stream as a lazy stream:

    import LazyStream
    stream = LazyStream(process.stdout)

Then you can check for lines in the stream periodically later on, using the `readline()` method:

    line = stream.readline()

That method will always return the latest line from the stream (or `None` if none are present yet).
