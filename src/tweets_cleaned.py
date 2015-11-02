import os
import json

__author__ = 'Roger'


def read_decode_clean_file():
    """
    Opens the file and creates the two .txt files. Reads in the file line by line and extracts the three key JSON
    elements: text, time, and timestamp. Text is cleaned and time is appended to it to produce the first output file,
    the cleaned text is also has its hashtags extracted and placed into an edge list with its corresponding timestamp
    (which is more accurate and involves no computing on our part).
    """
    from sys import argv
    script, input_file, output_cleaned_tweets, output_edge_vertex_ratio = argv
    script_dir = os.path.dirname(__file__)
    input_file_path = str(script_dir[0:len(script_dir)-4] + input_file[1:])
    ft1_file_path = str(script_dir[0:len(script_dir) - 4] + output_cleaned_tweets[1:])
    ft2_file_path = str(script_dir[0:len(script_dir) - 4] + output_edge_vertex_ratio[1:])
    outfile_cleaned_tweets = open(ft1_file_path, 'w')
    outfile_edge_vertex_ratio = open(ft2_file_path, 'w')
    unicode_tweets = 0
    graph = []
    with open(input_file_path, 'r') as in_file:
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
    outfile_edge_vertex_ratio.close()


def obtain_hashtags(hashtags):
    """
    Obtains the an array of strings, from an original tweet that has been split by a hashtag symbol
    Returns an array of the cleaned hashtags if there is at least one hashtag (2 or more elements in the
    original array. This also eliminates any "empty" hashtags due to elimination of Unicode.
    """
    hashtag_return = []
    if len(hashtags) > 1:
        for i in range(1, len(hashtags) - 1):
            if not hashtags[i].split(' ', 1)[0].lower().isspace():
                hashtag_return.append(hashtags[i].split(' ', 1)[0].lower())
    return hashtag_return


def hashtag_graph(hashtags, graph, timestamp_ms):
    """
    Takes in an array of cleaned hashtags, the graph, and the time.
    If there is more than one hashtag, will continue to move to creating an edge between every hashtag with each other
    This is done by sorting all the hashtags so they are in alphanumerical order. Then for every hashtag, and every hashtag
    after it, an edge is formed, and a timestamp is attached. This is appended to graph.
    Graph is sorted by time, not alphabetically. This allows for delete_old_edges to perform quickly by treating the
    variable hashtag as a FIFO data structure.
    In order to check for if the edge exists, every two hashtags will create the same exact array of two elements if they
    are sorted against each other. For example, an edge between 'a' and 'b' would create [a,b,time] as an element in graph.
    There will not be an element in graph that is [b,a,time], since the hashtag pair will always be sorted. This will allow
    for only unique edges in graph.
    """
    if len(hashtags) > 1:
        for first_hashtag in range(0, len(hashtags) - 1):
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
    """
    This checks if the edge doesn't exists. Since we have preserved alphabetical order in every single element within graph,
    we can check the first words first (both of which of their respective pairs will be first alphabetically), and if that
    passes then check the second hashtag.
    """
    if first != second:
        for edge in graph:
            if edge[0] == first and edge[1] == second:
                return False
        return True
    else:
        return False


def delete_old_edges(graph, time):
    """
    This will delete old edges if they expire. Because the variable graph is a FIFO list, we can keep popping the first
    element if it's too old.
    """
    continue_delete = len(graph) > 0
    time_threshold = time - 60 * 1000
    while continue_delete:
        if graph[0][2] < time_threshold: #graph[0][2] is the timestamp of the oldest edge in the graph
            del graph[0]
        else:
            continue_delete = False
    return graph


def find_num_vertices(graph):
    """
    This finds the number of unique hashtags (all lowercase) in the graph by just looping through graph and appending
    new hashtags if it isn't there already, and does this for both hashtags in the edge.
    """
    list_of_vertices = []
    for edge in graph:
        if edge[0] not in list_of_vertices:
            list_of_vertices.append(edge[0])
        if edge[1] not in list_of_vertices:
            list_of_vertices.append(edge[1])
    return len(list_of_vertices)


def main():
    read_decode_clean_file()

if __name__ == '__main__':
    main()