lazystream.py
=============

A lazy (non-blocking) stream reader that collects lines from a stream (like stdout) as they become available.


Usage
-----

Suppose you need to run a system command that blocks for a bit second::

    import subprocess
    command = 'sleep 1 && echo hello && sleep 1 && echo goodbye'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

If you try to read from process.stdout at this point, your program would pause for 2 seconds, then give you ``hello`` and ``goodbye`` all at once. If you don't want the blocking pause, read the stream as a lazy stream::

    import lazystream
    stream = lazystream.read(process.stdout)

Then you can ``pop()`` lines off the stream periodically::

    import time
    count = 1
    while count < 10:
    
        line = stream.pop()
        if line:
            print(str(line))
    
        exit_code = process.poll()
        if exit_code:
            print(str(exit_code))

        if exit_code is not None:
            break
        else:
            count += 1
            time.sleep(1)

The ``pop()`` function will always return the latest line from the stream (or ``None`` if none are present yet).
