# -*- coding: utf-8 -*-

"""Reads a stream lazily.

Usage: convert a stream into a lazy stream with ``read()``::

    import lazystream, time
    stream = lazystream.read(process.stdout)

Then pop lines off whenever you like with ``pop()``::

    line = lazystream.pop(stream)
    time.sleep(3)
    line = lazystream.pop(stream)

"""

from queue import Queue, Empty
from threading import Thread


def put_lines_into_queue(stream, queue):
    """Read lines from a stream and put them in a queue.

    Note: this is blocking (for the thread it runs in).

    Args:

        stream
            The stream to read lines from.

        queue
            A queue to put the stream's lines in.

    Returns:
        The queue, populated with lines.

    """
    for line in iter(stream.readline, b''):
        queue.put(line)
    stream.close()
    return queue


def pop(queue):
    """Get any new lines on the queue.

    Args:

        queue
            A queue to pop lines from.

    Returns:
        The line, or None.

    """
    try:
        return queue.get_nowait()
    except Empty:
        return None


def read(stream):
    """Stream lines into a queue.

    Args:

        stream
            The stream to read.

    Returns:
        The queue.

    """
    queue = Queue()
    thread = Thread(target=put_lines_into_queue, args=(stream, queue))
    thread.daemon = True
    thread.start()
    return queue
