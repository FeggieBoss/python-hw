from multiprocessing import Pipe, Queue, Process, queues, connection
from time            import time
from secrets         import token_hex
from functools       import partial
import codecs
import sys
import io
import logging 

artifacts_path = f'../artifacts/task3'
kExitMessage   = 'Exit'

class Channel:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def send(self, message_token):
        if isinstance(self.output, io.TextIOWrapper):
            message, _ = message_token
            self.output.write(message)
            return
        if isinstance(self.output, queues.Queue):
            self.output.put(message_token)
            return
        if isinstance(self.output, connection.Connection):
            self.output.send(message_token)
            return
        raise Exception("Box.send: input type error")

    def receive(self):
        if isinstance(self.input, io.TextIOWrapper):
            return self.input.readline()
        if isinstance(self.input, queues.Queue):
            return self.input.get()
        if isinstance(self.input, connection.Connection):
            return self.input.recv()
        raise Exception("Box.receive: ouput type error")


# reading from channel
def stdin_watcher(channel):
    while True:
        message = channel.receive()
        token   = token_hex(5)
        logging.info(loggin_format_received.format(
            sender   = 'stdin',
            token    = token,
            message  = message
        ))

        channel.send((message, token))
        logging.info(loggin_format_send.format(
            receiver = 'lower_process',
            token    = token,
            message  = message
        ))

        if message.rstrip() == kExitMessage:
            return

# redirecting messages to stdout
def redirect_to_stdout():
    return

# lower all messages
def lower_process():
    return

# encode all messages
def encoder_process():
    return

# configuring logging
logger                = logging.getLogger(__name__)
loggin_format_received = """received message from <{sender}>\n>>> [{token}]{message}"""
loggin_format_send     = """send message to <{receiver}>\n>>> [{token}]{message}"""
logging.basicConfig(
    filename=f'{artifacts_path}/artifacts.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(funcName)15s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# generating pipeline: stdin -> handler1 -> handler2 -> ... -> handlerN -> stdout
def generate_pipeline(handlers):
    return 

running_handlers = generate_pipeline(stdin_watcher, lower_process, encoder_process, redirect_to_stdout)
for i in running_handlers:
    i.join()