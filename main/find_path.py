# we use the Dijkstra's algorithm
import json


def get_key(dict, val):
    for key, value in dict.items():
        if val == value:
            return key


def path_finder(list_of_predecessors, source, destination):
    path = []
    current_stop = destination
    if list_of_predecessors[current_stop] is None:
        return [None]
    while current_stop != source:
        path.append(current_stop)
        current_stop = list_of_predecessors[int(current_stop)]
    path.append(source)
    path.reverse()
    return path


def graph_maker(data):
    graph = dict()
    for item in data['nodes']:
        graph[item['id']] = []

    for item in data['links']:
        graph[item['source']].append([item['target'], item['distance']])
        if [item['source'], item['distance']] not in graph[item['target']]:
            graph[item['target']].append([item['source'], item['distance']])
    return graph


def dijkstra(start, end):
    # if source == target
    if start == end:
        return None, 0, [2, "Spacerkiem :)"]

    # first we need to extract data from json
    with open('solvro_city.json') as file:
        data = json.load(file)

    # check if given stops exist
    is_start = False
    is_end = False
    for dictionary in data['nodes']:
        if dictionary['id'] == start:
            is_start = True
        elif dictionary['id'] == end:
            is_end = True
    if not is_start or not is_end:
        return None, None, [1, "Missing data"]

    # and make graph from nodes (stops)
    with open('../resources/graph.json', 'r') as graph_file:
        graph = json.load(graph_file)
        graph = {int(key): value for key, value in graph.items()} # changes keys from string to int

    # actual Dijkstra's algorithm
    distance_list = [float('inf')]*len(graph)

    distance_list[start] = 0

    list_of_predecessors = [None]*len(graph) # this will be the list of the shortest path to every stop
    queue = [graph[start]]
    while len(queue) > 0:
        stop = queue.pop(0)
        for neighbour in stop:
            stop_key = get_key(graph, stop)
            if distance_list[neighbour[0]] > (distance_list[stop_key] + neighbour[1]):
                distance_list[neighbour[0]] = distance_list[stop_key] + neighbour[1]
                list_of_predecessors[neighbour[0]] = stop_key
                queue.append(graph[neighbour[0]])

    path_list = {stop_key: data['nodes'][stop_key]['stop_name'] for stop_key in path_finder(list_of_predecessors, start, end)}

    return path_list, distance_list[end], [0, "Path successfully found"]


if __name__ == '__main__':
    print(dijkstra(0, 29))
