import json, pprint

def graph_writer(data):
    graph = dict()
    for item in data['nodes']:
        graph[int(item['id'])] = []

    for item in data['links']:
        graph[item['source']].append([item['target'], item['distance']])
        if [item['source'], item['distance']] not in graph[item['target']]:
            graph[item['target']].append([item['source'], item['distance']])
    pprint.pprint(graph)
    print(len(graph))
    return graph


with open('../main/solvro_city.json') as file:
    data = json.load(file)
    file.close()

with open('graph.json', 'w') as outfile:
    json.dump(graph_writer(data), outfile)
