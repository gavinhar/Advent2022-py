from typing import IO, Dict


def process_alt(f: IO) -> None:
    current_dir = '/'

    # directories: /dir1/dir2/.../dir_n/
    # files: /dir1/dir2/.../dir_n/filename#filesize
    fs = {'/'}

    # process the input file to build filesystem data (fs)
    for raw_line in f:
        line = raw_line.strip()
        if line == '$ cd ..':
            # jump up 1 directory
            current_dir = current_dir.rsplit('/', 2)[0] + '/'
        elif line.startswith('$ cd') and '/' not in line:
            current_dir = f'{current_dir}{line.split(" ")[2]}/'
            fs.add(current_dir)
        elif not line.startswith('$') and not line.startswith('dir'):
            size, new_file = line.split(' ')
            fs.add(f'{current_dir}{new_file}#{size}')

    # calculate directory sizes for all directories (fs item ending with /)
    dir_sizes: Dict[str, int] = dict()
    for d in filter(lambda x: x[-1] == '/', fs):
        # list of files in the directory (includes sub-directory files)
        files_in_dir = list(filter(lambda x: x.startswith(d) and '#' in x, fs))

        # calculate size of directory
        dir_sizes[d] = sum(map(lambda x: int(x.split('#')[1]), files_in_dir))

    # calculate sum of directory with size < 100000
    # and print result for part 1
    part1 = sum(filter(lambda x: x <= 100000, dir_sizes.values()))
    assert part1 == 1743217
    print('part 1:', part1)

    # how much space must be freed to have 30,000,000 free (assuming 70,000,000 total storage)
    must_free = 30000000 - (70000000 - dir_sizes['/'])

    # find directory with min size > must_free
    # and print result for part 2
    part2 = min(filter(lambda x: x > must_free, dir_sizes.values()))
    assert part2 == 8319096
    print('part 2:', part2)


def solution(sample: bool) -> None:
    filename = '../input/day7{}.txt'.format('-sample' if sample else '')
    with open(filename) as f:
        process_alt(f)


solution(False)
