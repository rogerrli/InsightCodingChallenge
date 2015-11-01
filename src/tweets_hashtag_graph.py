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
                    timestamp_ms = json.dumps(jfile['timestamp_ms']).encode('ascii').decode('unicode_escape') \
                        .encode('ascii', 'ignore').decode('utf8')
                    hashtags = obtain_hashtags(current_text.split('#'))
                    average_degree, graph = hashtag_graph(hashtags, graph, int(timestamp_ms[1:len(timestamp_ms)-1]))
                    outfile.write(str(average_degree))
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
                    graph.append([hashtags[first_hashtag], second_hashtag, timestamp_ms])
    graph = delete_old_edges(graph, timestamp_ms)
    num_vertices = find_num_vertices(graph)
    num_edges = len(graph) * 2
    if num_vertices > 0:
        ratio = num_edges / num_vertices
    else:
        ratio = np.NaN
    return ratio, graph


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


def find_num_vertices(graph):
    list_of_vertices = []
    for edge in graph:
        if edge[0] not in list_of_vertices:
            list_of_vertices.append(edge[0])
        if edge[1] not in list_of_vertices:
            list_of_vertices.append(edge[1])
    return len(list_of_vertices)


def main():
    read_in_file()


if __name__ == '__main__':
    main()
