# This is a sample Python script.
import matplotlib.pyplot as plt
from cObjectGenerator import cObjectGenerator
import networkx as nx
import json
fOpen = open('testData.json')
data = json.load(fOpen)
G = nx.Graph()
for x in data:
    for y in range(len(x['parameters'])):
        #print(x['parameters'][y])

        if not G.__contains__(x['parameters'][y]):
            G.add_node(x['parameters'][y])
        for z in range(y + 1, len(x['parameters'])):
            if not G.__contains__(x['parameters'][z]):
                G.add_node(x['parameters'][y])
            print(x['parameters'][z])
            print(x['parameters'][y])
            if G.has_edge(x['parameters'][y], x['parameters'][z]):
                G[x['parameters'][y]][x['parameters'][z]]['weight'] += 1
            else:
                G.add_edge(x['parameters'][y], x['parameters'][z], weight=1)


pos = nx.spring_layout(G, k=10)  # For better example looking
nx.draw(G, pos, with_labels=True)
labels = {e: G.edges[e]['weight'] for e in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()



class temp:
    def __init__(self, name):
        self.functionName = name
        self.parameters = []

    def addParam(self, param):
        self.parameters.append(param)


if __name__ == '__main__':
    #This purely used to generate test json data.
    testList = [temp("temp1"), temp("temp2")]
    testList[0].addParam("int param1")
    testList[0].addParam("int param2")
    testList[1].addParam("int param1")
    testList[1].addParam("int param2")
    testList[1].addParam("int param3")
    testList[1].addParam("int param4")

    #print(json.dumps(testList,default=lambda x: x.__dict__,indent=4))


    #print("test")
