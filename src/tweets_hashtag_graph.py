__author__ = 'Roger'

import os
import json
import numpy as np


def read_in_file():
    from sys import argv
    script, input_file, output_file = argv
    script_dir = os.path.dirname(__file__)
    outfile = open(script_dir[0:len(script_dir) - 4] + output_file[1:], 'w')
    graph = []
    with open(script_dir[0:len(script_dir) - 4] + input_file[1:], 'r') as infile:
        for line in infile:
            try:
                jfile = json.loads(line)
                try:
                    current_text = json.dumps(jfile['text']).encode('ascii').decode('unicode_escape') \
                        .encode('ascii', 'ignore').decode('utf8').replace("\n", " ").replace('"', '')
                    current_time = json.dumps(jfile['created_at']).encode('ascii').decode('unicode_escape') \
                        .encode('ascii', 'ignore').decode('utf8').replace('"', '')
                    timestamp_ms = json.dumps(jfile['timestamp_ms']).encode('ascii').decode('unicode_escape') \
                        .encode('ascii', 'ignore').decode('utf8')
                    hashtags = obtain_hashtags(current_text.split('#'))
                    average_degree, graph = hashtag_graph(hashtags, graph, int(timestamp_ms[1:len(timestamp_ms)-1]))
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


def hashtag_graph(hashtags, graph, timestamp_ms):
    if len(hashtags) > 1:
        hashtags = sorted(hashtags)
        for first_hashtag in np.arange(len(hashtags) - 1):
            for second_hashtag in hashtags[first_hashtag + 1:]:
                if edge_does_not_exist(hashtags[first_hashtag], second_hashtag, graph):
                    print('new edge added')
                    graph.append([hashtags[first_hashtag], second_hashtag, timestamp_ms])
    graph = delete_old_edges(graph, timestamp_ms)
    num_edges = len(graph) * 2
    return 0, graph


def edge_does_not_exist(first, second, graph):
    if first != second:
        for edge in graph:
            if edge[0] == first and edge[1] == second:
                return False
        return True
    else:
        return False


def delete_old_edges(graph, time):
    continue_delete = len(graph) > 0
    time_threshold = time - 60 * 1000
    while continue_delete:
        if graph[0][2] < time_threshold:
            del graph[0]
        else:
            continue_delete = False
    return graph


def main():
    read_in_file()


if __name__ == '__main__':
    main()
