from clint.textui import colored

OUT_HEADER = "#--------------------------------[ Combat Log ]--------------------------------#"
OUT_GIVEN = "Damage Given to   \"{0}\" - {1} in {2} hit"
OUT_TAKEN = "Damage Taken from \"{0}\" - {1} in {2} hit"

def print_entry(type: int, name: str, damage: int, hits: int):
    template = OUT_TAKEN
    color = colored.red
    if type == 2:
        template = OUT_GIVEN
        color = colored.green
    print(template.format(name, color(damage), color(hits)))

def print_all_entries(entries: list[tuple[int,str,int,int]]):
    print(OUT_HEADER)
    for e in entries:
        print_entry(*e)