import matplotlib.pyplot as plt
import networkx as nx
import json


class graphAnalysis:
    #Assume graph has atleast one edge
    def getLargestEdge(self, graph):
        return self.sortEdges(graph)[0]
    #Which two nodes to combine
    def getSumOfEdges(self, graph):
        return graph.size(weight="weight")
    def displayGraph(self, graph):
        pos = nx.spring_layout(graph, k=10)  # For better example looking
        nx.draw(graph, pos, with_labels=True)
        labels = {e: graph.edges[e]['weight'] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()
    #Data is our json input loaded into python
    def createGraph(self, data):
        G = nx.Graph()
        for x in data:
            for y in range(len(x['parameters'])):
                # print(x['parameters'][y])

                if not G.__contains__(x['parameters'][y]):
                    G.add_node(x['parameters'][y])
                for z in range(y + 1, len(x['parameters'])):
                    if x['parameters'][y] == x['parameters'][z]:
                        continue
                    # If Node has not been added to graph yet, add node to graph
                    if not G.__contains__(x['parameters'][z]):
                        G.add_node(x['parameters'][y])
                    # If it is checking for a combination node
                    if G.has_node(x['parameters'][y] + x['parameters'][z]):
                        continue
                    # Check if graph has combination node
                    if G.has_edge(x['parameters'][y], x['parameters'][z]):
                        G[x['parameters'][y]][x['parameters'][z]]['weight'] += 1
                    else:
                        G.add_edge(x['parameters'][y], x['parameters'][z], weight=1)
        return G
    #Data is data loaded in from json
    def buildAndShowGraph(self,data):
        self.displayGraph(self.createGraph(data))

if __name__ == "__main__":
    fOpen = open('testData2.json')
    data = json.load(fOpen)
    fOpen.close()
    test2 = graphAnalysis()
    graph = test2.createGraph(data)
    test2.displayGraph(graph)
