import argparse
import itertools
import json
import subprocess
import shutil
import sys


def tdk2dict(args):
    input, output = args.input, args.out
    outfile_name = f"{output}.txt"
    outfile = open(outfile_name, 'w', encoding='utf-8')
    with open(input, encoding='utf-8') as file:
        for line in itertools.islice(file, args.start, args.end, 1):
            j = json.loads(line)
            word = j['madde']
            s = f':{word}:'
            definitions = j.get('anlamlarListe', [])
            for i, definition in enumerate(definitions):
                s += f"{i+1}. "
                properties = definition.get('ozelliklerListe', [])
                prop_str = ', '.join(prop['tam_adi']
                                     for prop in properties)
                if prop_str:
                    s += f'({prop_str}) '
                s += f'{definition["anlam"]}\n'
                examples = definition.get('orneklerListe', [])
                for example in examples:
                    s += f'\t"{example["ornek"]}"'
                s += '\n'
            outfile.write(s)
    outfile.close()
    proc = subprocess.Popen([
        shutil.which(
            'dictfmt'), '--utf8', '--allchars', '-s', args.name, '-j', args.out
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(input=open(outfile_name, mode='rb').read())
    proc.wait()
    print(out.decode(encoding='utf-8'))
    print(err.decode(encoding='utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts a JSON file taken from sozluk.gov.tr or ogun/guncel-turkce-sozluk and outputs two files in the DICT format.')
    parser.add_argument('input', metavar='FILE',
                        help='the JSON file to process')
    parser.add_argument(
        '--name', help='specify the name of the dictionary', default='Turkish Dictionary')
    parser.add_argument(
        '--out', metavar='FILE', help='specify name of the produced .index and .dict files', default='trdict')
    parser.add_argument(
        '--start', type=int, help='start importing from the entry with the specified index', default=0)
    parser.add_argument(
        '--end', type=int, help='stop importing before the entry with the specified index', default=sys.maxsize)
    args = parser.parse_args()
    tdk2dict(args)
