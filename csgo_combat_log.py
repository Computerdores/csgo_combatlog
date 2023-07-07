import asyncio, telnetlib3
from clint.textui import colored
from console_parsing import *

OUT_HEADER = "#--------------------------------[ Combat Log ]--------------------------------#"
OUT_GIVEN = "Damage Given to   \"{0}\" - {1} in {2} hit"
OUT_TAKEN = "Damage Taken from \"{0}\" - {1} in {2} hit"

URL = "localhost"
PORT = 2121


def handle_line(line: str):
    m = match_line(line)
    if m[0] == 1:
        print(OUT_HEADER)
    elif m[0] == 2:
        print(OUT_GIVEN.format(m[1], colored.green(m[2]), colored.green(m[3])))
    elif m[0] == 4:
        print(OUT_TAKEN.format(m[1], colored.red(m[2]), colored.red(m[3])))

async def output_parser(reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter):
    print("connected")
    while True:
        outp = await read_line(reader)
        if not outp:
            break
        else:
            handle_line(outp)

def main():
    while True:
        loop = asyncio.get_event_loop()
        coro = telnetlib3.open_connection(URL, PORT, shell=output_parser, encoding=None)
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)
        print("disconnected")

if __name__ == "__main__":
    main()