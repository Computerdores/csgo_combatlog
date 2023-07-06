import asyncio, telnetlib3
from clint.textui import colored
import re
import os

REG_SEPARATOR = r"^[-]+$"
REG_DMG_GIVEN_HEADER = r"^Player: .* - Damage Given$"
REG_DMG_GIVEN = r"^Damage Given to \"(.*)\" - ([0-9]+) in ([0-9]+) hit[s]{0,1}$"
REG_DMG_TAKEN_HEADER = r"^Player: .* - Damage Taken$"
REG_DMG_TAKEN = r"^Damage Taken from \"(.*)\" - ([0-9]+) in ([0-9]+) hit[s]{0,1}$"

OUT_HEADER = "#--------------------------------[ Combat Log ]--------------------------------#"
OUT_GIVEN = "Damage Given to   \"{0}\" - {1} in {2} hit"
OUT_TAKEN = "Damage Taken from \"{0}\" - {1} in {2} hit"

URL = "localhost"
PORT = 2121

LastLine = ""

async def read_line(reader) -> str:
    outp = b""
    while True:
        c = await reader.read(1)
        if c == b"\r":
            continue
        if c == b"\n":
            break
        outp += c
    LastLine = outp.decode("utf-8")
    return outp.decode("utf-8")

# return val: (type, name, damage, hits)
# type:
# -1 invalid line
#  0 separator
#  1 Damage Given Header
#  2 Damage Given
#  3 Damage Taken Header
#  4 Damage Taken
def match_line(line: str) -> tuple[int,str,int,int]:
    if re.match(REG_SEPARATOR, line):
        return (0, None, None, None)
    elif re.match(REG_DMG_GIVEN_HEADER, line):
        return (1, None, None, None)
    elif re.match(REG_DMG_TAKEN_HEADER, line):
        return (3, None, None, None)
    m = re.match(REG_DMG_GIVEN, line)
    if m:
        return (2, *m.groups())
    m = re.match(REG_DMG_TAKEN, line)
    if m:
        return (4, *m.groups())
    return (-1, None, None, None)


def handle_line(line: str):
    m = match_line(line)
    if m[0] == 1:
        print(OUT_HEADER)
    elif m[0] == 2:
        print(OUT_GIVEN.format(m[1], colored.green(m[2]), colored.green(m[3])))
    elif m[0] == 4:
        print(OUT_TAKEN.format(m[1], colored.red(m[2]), colored.red(m[3])))

async def output_parser(reader, writer):
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