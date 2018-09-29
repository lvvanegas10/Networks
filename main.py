from graph_class import MGraph
import networkx as nx 

# =======================================
# Help main  
# =======================================
"""
    Print the final route from name to name2
"""
def printOptimalRoute(name, name2, flowDict):
    while(name != name2 ):
        print(name)
        d3 = flowDict[name]
        d2 = {k : v for k,v in d3.items() if v == {0:1} }
        name = list(d2.keys())[0]
        

# =======================================
# Main   
# =======================================
if __name__ == "__main__":    
    graph = MGraph()
    graph.findStartNode('Main Quad (Campus Oval Side)', 423)
    graph.G.add_node('Palo Alto Transit Center (Caltrain Platform)',  demand = 1)

    flowCost, flowDict = nx.network_simplex(graph.G)

    print(flowCost)

    name = 'Main Quad (Campus Oval Side)' + ' Start'
    name2 = 'Palo Alto Transit Center (Caltrain Platform)'
    printOptimalRoute(name, name2, flowDict)
    