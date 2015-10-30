__author__ = 'Roger'

import os
import json

def openFile():
    from sys import argv
    script, input_file, output_file = argv
    script_dir = os.path.dirname(__file__)
    output_file = script_dir[0:len(script_dir) - 4] + output_file[1:]
    input_file = script_dir[0:len(script_dir)-4] + input_file[1:]
    outfile = open(output_file, 'w')
    with open(input_file, 'r') as infile:
        for line in infile:
            try:
                jfile = json.loads(line)
                try:
                    current_text = json.dumps(jfile['text']).encode('ascii').decode('unicode_escape')\
                        .encode('ascii', 'ignore').decode('utf8').replace("\n", " ").replace('"', '')
                    current_time = json.dumps(jfile['created_at']).encode('ascii').decode('unicode_escape')\
                        .encode('ascii', 'ignore').decode('utf8').replace('"', '')
                    output_line = current_text + " (timestamp: " + current_time + ")"
                    outfile.write(output_line)
                    outfile.write('\n')
                except KeyError:
                    pass
            except ValueError:
                pass
    outfile.close()

def main():
    openFile()

if __name__ == '__main__':
    main()
