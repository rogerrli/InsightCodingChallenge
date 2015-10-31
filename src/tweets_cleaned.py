__author__ = 'Roger'

import os
import json

def read_in_file():
    from sys import argv
    script, input_file, output_file = argv
    script_dir = os.path.dirname(__file__)
    outfile = open(script_dir[0:len(script_dir) - 4] + output_file[1:], 'w')
    unicode_tweets = 0
    with open(script_dir[0:len(script_dir)-4] + input_file[1:], 'r') as infile:
        for line in infile:
            try:
                jfile = json.loads(line)
                try:
                    if "\\u" in json.dumps(jfile['text']):
                        unicode_tweets += 1
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
    outfile.write(str(unicode_tweets) + " number of tweets with Unicode")
    outfile.close()


def main():
    read_in_file()

if __name__ == '__main__':
    main()
