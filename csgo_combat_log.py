import asyncio, telnetlib3
from clint.textui import colored
from console_parsing import *

OUT_HEADER = "#--------------------------------[ Combat Log ]--------------------------------#"
OUT_GIVEN = "Damage Given to   \"{0}\" - {1} in {2} hit"
OUT_TAKEN = "Damage Taken from \"{0}\" - {1} in {2} hit"

URL = "localhost"
PORT = 2121

current_line = 0
temp = False
last_log = []

def print_entry(entry: tuple[int,str,int,int]):
    template = OUT_TAKEN
    color = colored.red
    if entry[0] == 2:
        template = OUT_GIVEN
        color = colored.green
    print(template.format(entry[1], color(entry[2]), color(entry[3])))

def print_all_entries():
    print(OUT_HEADER)
    for e in last_log:
        print_entry(e)

def handle_line(line: str):
    global current_line
    global last_log
    global temp
    m = match_line(line)
    if m[0] == 1:
        current_line = 0
    elif m[0] in [2,4]:
        if current_line < len(last_log):
            if last_log[current_line] != m:
                last_log = last_log[:current_line+1]
                last_log[current_line] = m
                temp = True
                print_all_entries()
        else:
            if not temp:
                temp = True
                print_all_entries()
            last_log.append(m)
            print_entry(m)
        current_line += 1


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