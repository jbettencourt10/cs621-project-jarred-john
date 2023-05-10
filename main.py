import copy
import random
import matplotlib.pyplot as plt
from cObjectGenerator import cObjectGenerator
import networkx as nx
import json
fOpen = open('testData.json')

data2 = json.load(fOpen)
fOpen.close()
G = nx.Graph()
#Creating very cyclic graph
class findParamterPacking:
    def __init__(self):
        print("initiliaze")
    def sortEdges(self, graph):
        return sorted(graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    #Assume graph has atleast one edge
    def getLargestEdge(self, graph):
        return self.sortEdges(graph)[0]
    #Which two nodes to combine
    def simplifyJson(self,node1, node2, data):
        tempData = copy.deepcopy(data)
        for j in tempData:
            if node1 == node2:
                continue
            if node1 in j['parameters'] and node2 in j['parameters']:
                j['parameters'].remove(node1)
                j['parameters'].remove(node2)
                j['parameters'].append(node1+node2)
        return tempData
    def getSumOfEdges(self, graph):
        return graph.size(weight="weight")
    def displayGraph(self, graph):
        pos = nx.spring_layout(graph, k=10)  # For better example looking
        nx.draw(graph, pos, with_labels=True)
        labels = {e: graph.edges[e]['weight'] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()
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
    def simplifyGraph(self,data):
        graphOriginal = self.createGraph(data)
        originalSize = self.getSumOfEdges(graphOriginal)
        bestEdgeSize = -1
        bestEdge = None
        for l in self.sortEdges(graphOriginal):
            newData = self.simplifyJson(l[0],l[1],data)
            graph2 = test2.createGraph(newData)
            newSize = test2.getSumOfEdges(graph2)
            if originalSize - newSize > bestEdgeSize:
                bestEdge = l
                bestEdgeSize = originalSize - newSize
        if bestEdgeSize == -1:
            return data
        newData = self.simplifyJson(bestEdge[0], bestEdge[1], data)
        return newData
change = 1000
data = data2
test2 = findParamterPacking()
newdata = data
while change > 1:
    graph = test2.createGraph(newdata)
    print(graph)
    edges1 = test2.getSumOfEdges(graph)
    newdata = test2.simplifyGraph(newdata)
    graph2 = test2.createGraph(newdata)

    edges2 = test2.getSumOfEdges(graph2)

    change = edges1 - edges2
    print(change)
print(test2.createGraph(newdata).nodes.__sizeof__())
print(test2.createGraph(newdata).nodes)
inte1 = 0
for x in test2.createGraph(newdata).nodes:
    inte1 += 1
    print(inte1)
    print(x)

test2.displayGraph(test2.createGraph(newdata))




class temp:
    def __init__(self, name):
        self.functionName = name
        self.parameters = []

    def addParam(self, param):
        self.parameters.append(param)


if __name__ == '__main__':
    print("run")
    #This purely used to generate test json data.
    testList = []
    random.seed(0)
    totalParams = 0
    for i in range(100):
        testList.append(temp('function' + str(i)))
        numberOfParams = random.randint(2,5)
        for y in range(numberOfParams):
            testList[i].addParam("int param" + str(random.randint(0,10)))
            totalParams += 1

    #print(totalParams)
    #print(json.dumps(testList,default=lambda x: x.__dict__,indent=4))
    #fOpen2 = open('testData.json', 'w')

    #json.dump(testList,default=lambda x: x.__dict__,indent=4,fp=fOpen2)

    #print("test")
