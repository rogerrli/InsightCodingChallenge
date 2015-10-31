__author__ = 'Roger'

import os
import json
import numpy as np

def read_in_file():
    from sys import argv
    script, input_file, output_file = argv
    script_dir = os.path.dirname(__file__)
    outfile = open(script_dir[0:len(script_dir) - 4] + output_file[1:], 'w')
    graph =[]
    with open(script_dir[0:len(script_dir)-4] + input_file[1:], 'r') as infile:
        for line in infile:
            try:
                jfile = json.loads(line)
                try:
                    current_text = json.dumps(jfile['text']).encode('ascii').decode('unicode_escape')\
                        .encode('ascii', 'ignore').decode('utf8').replace("\n", " ").replace('"', '')
                    current_time = json.dumps(jfile['created_at']).encode('ascii').decode('unicode_escape')\
                        .encode('ascii', 'ignore').decode('utf8').replace('"', '')
                    hashtags = obtain_hashtags(current_text.split('#'))
                    average_degree, graph = hashtag_graph(hashtags, graph, current_time)
                    output_line = current_text + " (timestamp: " + current_time + ")"
                    outfile.write(output_line)
                    outfile.write('\n')
                except KeyError:
                    pass
            except ValueError:
                pass
    outfile.close()


def obtain_hashtags(hashtags):
    hashtag_return = []
    if len(hashtags) > 1:
        for i in range(1, len(hashtags) - 1):
            hashtag_return.append(hashtags[i].split(' ', 1)[0].lower())
        hashtag_return = np.array(hashtag_return)
        return hashtag_return
    else:
        return []

def hashtag_graph(hashtags, graph, current_time):
    time = current_time.split()[3]
    if len(hashtags) > 1:
        hashtags = sorted(hashtags)
        for i in np.arange(len(hashtags)):
            for second_hashtag in hashtags[i:]:
                whatever = 0
    #else:
        #updateTime

    return 0, graph

def main():
    read_in_file()

if __name__ == '__main__':
    main()
