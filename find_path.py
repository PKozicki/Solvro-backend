# we use the Dijkstra's algorithm
import json
import pprint


def dijkstra(start, end):
    # if source == target
    if start == end:
        return [{'name': start}], 0

    # first we need to extract data from json
    with open('solvro_city.json') as f:
        data = json.load(f)

    # check if given stops exist
    is_start = False
    is_end = False
    for dictionary in data['nodes']:
        if dictionary['stop_name'] == start:
            is_start = True
        elif dictionary['stop_name'] == end:
            is_end = True
    if not is_start or not is_end:
        return [{'name': 'błędne nazwy przystanków'}], None

    # and make graph from nodes (stops)
    graph = dict()
    for item in data['nodes']:
        graph[item['id']] = []

    for item in data['links']:
        graph[item['source']].append([item['target'], item['distance']])

    # pprint.pprint(graph)

    # graph is not directed
    for key in graph.keys():
        for connection in graph[key]:
            if [key, connection[1]] not in graph[connection[0]]:
                graph[connection[0]].append([key, connection[1]])

    # pprint.pprint(graph)

    # actual Dijkstra's algorithm
    distance_list = [float('inf')]*len(graph)

    # we will find the id of our source
    start_id = None
    for node in data['nodes']:
        if node['stop_name'] == start:
            start_id = node['id']
    # and the id of our destination
    end_id = None
    for node in data['nodes']:
        if node['stop_name'] == end:
            end_id = node['id']

    distance_list[start_id] = 0

    # this function will be necessary
    def get_key(dict, val):
        for key, value in dict.items():
            if val == value:
                return key

    list_of_predecessors = [None]*len(graph) # this will be the list of shortest paths to every stop
    queue = [graph[start_id]]
    while len(queue) > 0:
        u = queue.pop(0)
        for neighbour in u:
            u_key = get_key(graph, u)
            if distance_list[neighbour[0]] > (distance_list[u_key] + neighbour[1]):
                distance_list[neighbour[0]] = distance_list[u_key] + neighbour[1]
                list_of_predecessors[neighbour[0]] = u_key
                queue.append(graph[neighbour[0]])

    # print(list_of_predecessors)
    # print(distance_list)

    def path_finder(list_of_predecessors, source, destination):
        path = []
        current_stop = destination
        if list_of_predecessors[current_stop] is None:
            return [None]
        while current_stop != source:
            path.append(current_stop)
            current_stop = list_of_predecessors[current_stop]
        path.append(source)
        path.reverse()
        return path

    # print(start_id, end_id)
    # print(path_finder(list_of_predecessors, start_id, end_id))
    # pprint.pprint(data)

    path_list = [{'name': data['nodes'][i]['stop_name']} for i in path_finder(list_of_predecessors, start_id, end_id)]

    return path_list, distance_list[end_id]


dijkstra("Przystanek Zdenerwowany frontend developer", "Przystanek frontend developer")
