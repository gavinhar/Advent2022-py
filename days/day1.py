f = open(f'../input/day1.txt').read().split('\n\n')
print(max(map(lambda elf: sum(map(lambda x: int(x), elf.split('\n'))), f)))
