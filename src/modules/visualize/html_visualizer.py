import os.path
import matplotlib.pyplot as plt
import networkx as nx
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape


class HTMLVisualizer:
    def __init__(self, filename):
        self.filename = filename.split(".")[0]

    def visualize(self):

        oldData = json.load(open(self.filename + ".json"))
        newData = json.load(open(self.filename + "_updated.json"))
        packs = json.load(open(self.filename + "_packed.json"))

        filepath = os.path.dirname(self.filename + ".json")

        self.buildAndSaveGraph(oldData, self.filename+"_image1")
        self.buildAndSaveGraph(newData, self.filename+"_image2")
        self.generateReport(oldData, newData, packs)

    env = Environment(
        loader=FileSystemLoader(searchpath="./src/modules/visualize/templates"),
        autoescape=select_autoescape()
    )

    # Data is our json input loaded into python
    def createGraph(self, data):
        G = nx.Graph()
        for x in data:
            for y in range(len(x['parameters'])):
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

    # Data is data loaded in from json
    def buildAndSaveGraph(self, data, imageName):
        plt.close()
        graph = self.createGraph(data)
        pos = nx.spring_layout(graph, k=10)  # For better example looking
        nx.draw(graph, pos, with_labels=True)
        labels = {e: graph.edges[e]['weight'] for e in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.savefig(imageName, format='png')

    def countOccurences(self, data, paramName):
        occurences = 0
        for x in data:
            for z in x['parameters']:
                if z == paramName:
                    occurences += 1
        return occurences

    def generateReport(self, originalData, newData, packedParams):
        originalParamList = []
        # Generate Data for original parameters
        for x in originalData:
            for y in x['parameters']:
                if y not in originalParamList:
                    originalParamList.append(y)
        occurenceDict = dict()
        for z in packedParams:
            occurenceDict[z['packed_param']] = self.countOccurences(newData, z['packed_param'])
        functionsDict = dict()
        for z in packedParams:
            for x in newData:
                for y in x['parameters']:
                    if z['packed_param'] == y:
                        if z['packed_param'] in functionsDict:
                            functionsDict[z['packed_param']].append(x['functionName'])
                        else:
                            functionsDict[z['packed_param']] = [x['functionName']]
        template = self.env.get_template("report.html")
        output = template.render(image1file=os.path.basename(self.filename+"_image1"),
                                 image2file=os.path.basename(self.filename+"_image2"),
                                 originalParamList=originalParamList, packedParams=packedParams,
                                 occurenceDict=occurenceDict, functionsDict=functionsDict
                                 )

        out_file = open(self.filename+"_report.html", "w")
        out_file.write(output)
