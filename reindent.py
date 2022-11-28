import argparse
import sys
from pathlib import Path
from typing import Any


def count_indent(line: str, indent: str) -> int:
    count = 0
    current = indent
    while line.startswith(current):
        count += 1
        current += indent
    return count


def reindent_file(file: Path, encoding: str, from_: str, to: str) -> None:
    tmp_file = Path(f'{file}.reindent.tmp')
    with open(file, encoding=encoding) as fp_in:
        with open(tmp_file, 'w', encoding=encoding) as fp_out:
            for line in fp_in:
                indent_count = count_indent(line, from_)
                new_line = to * indent_count + line[indent_count * len(from_):]
                fp_out.write(new_line)
    file.unlink()
    tmp_file.rename(file)


def _argparse_indent_type(arg: str) -> str:
    if arg.lower() == 'tab':
        return '\t'
    return ' ' * int(arg)


def main(args: list[str]):
    parser = argparse.ArgumentParser('reindent')
    parser.add_argument('files', help='A glob pattern of files to reindent.')
    parser.add_argument(
        'from_', type=_argparse_indent_type, metavar='from',
        help='The indentation to convert from. Parsed as either "tab" or a number of spaces.'
    )
    parser.add_argument(
        'to', type=_argparse_indent_type,
        help='The indentation to convert to. Parsed as either "tab" or a number of spaces.'
    )
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet')
    parser.add_argument('-e', '--encoding', dest='encoding', default='utf-8')

    ns = parser.parse_args(args)

    if ns.quiet:
        def maybe_print(*s: Any) -> None:
            pass
    else:
        def maybe_print(*s: Any) -> None:
            print(*s, sep='')

    for path in Path.cwd().rglob(ns.files):
        if not path.is_file():
            maybe_print('Skipped non-file ', path)
            continue
        maybe_print('Reindenting ', path, '...')
        reindent_file(path, ns.encoding, ns.from_, ns.to)


if __name__ == '__main__':
    main(sys.argv[1:])
