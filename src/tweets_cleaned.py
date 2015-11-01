import os
import json
import numpy as np

__author__ = 'Roger'


def read_in_file():
    from sys import argv
    script, input_file, output_cleaned_tweets, output_edge_vertex_ratio = argv
    script_dir = os.path.dirname(__file__)
    outfile_cleaned_tweets = open(script_dir[0:len(script_dir) - 4] + output_cleaned_tweets[1:], 'w')
    outfile_edge_vertex_ratio = open(script_dir[0:len(script_dir) - 4] + output_edge_vertex_ratio[1:], 'w')
    unicode_tweets = 0
    graph = []
    with open(script_dir[0:len(script_dir)-4] + input_file[1:], 'r') as in_file:
        for line in in_file:
            j_file = json.loads(line)
            try:
                if "\\u" in json.dumps(j_file['text']):
                    unicode_tweets += 1
                current_text = json.dumps(j_file['text']).encode('ascii').decode('unicode_escape')\
                    .encode('ascii', 'ignore').decode('utf8').replace("\n", " ").replace('"', '')
                current_time = json.dumps(j_file['created_at']).encode('ascii').decode('unicode_escape')\
                    .encode('ascii', 'ignore').decode('utf8').replace('"', '')
                timestamp_ms = json.dumps(j_file['timestamp_ms']).encode('ascii').decode('unicode_escape') \
                    .encode('ascii', 'ignore').decode('utf8')
                cleaned_tweet = current_text + " (timestamp: " + current_time + ")"
                hashtags = obtain_hashtags(current_text.split('#'))
                average_degree, graph = hashtag_graph(hashtags, graph, int(timestamp_ms[1:len(timestamp_ms)-1]))
                outfile_edge_vertex_ratio.write(str(average_degree))
                outfile_edge_vertex_ratio.write('\n')
                outfile_cleaned_tweets.write(cleaned_tweet)
                outfile_cleaned_tweets.write('\n')
            except KeyError:
                pass
    outfile_cleaned_tweets.write(str(unicode_tweets) + " number of tweets with Unicode")
    outfile_cleaned_tweets.close()
    print('Cleaned tweets saved in: ' + output_cleaned_tweets[1:])
    outfile_edge_vertex_ratio.close()
    print('Edge to vertex ratio of hashtag graph saved in: ' + output_edge_vertex_ratio[1:])


def obtain_hashtags(hashtags):
    hashtag_return = []
    if len(hashtags) > 1:
        for i in range(1, len(hashtags) - 1):
            if not hashtags[i].split(' ', 1)[0].lower().isspace():
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
        ratio = round(num_edges / num_vertices, 2)
    else:
        ratio = 0
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
