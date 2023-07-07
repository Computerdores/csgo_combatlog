import telnetlib3, re

REG_SEPARATOR = r"^[-]+$"
REG_DMG_GIVEN_HEADER = r"^Player: .* - Damage Given$"
REG_DMG_GIVEN = r"^Damage Given to \"(.*)\" - ([0-9]+) in ([0-9]+) hit[s]{0,1}$"
REG_DMG_TAKEN_HEADER = r"^Player: .* - Damage Taken$"
REG_DMG_TAKEN = r"^Damage Taken from \"(.*)\" - ([0-9]+) in ([0-9]+) hit[s]{0,1}$"

async def read_line(reader: telnetlib3.TelnetReader) -> str:
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