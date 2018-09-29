from graph_class import MGraph
import networkx as nx 
import datetime

# =======================================
# Help main  
# =======================================

"""
    Print the final route from name to name2
"""
def printOptimalRoute(name, name2, flowDict):
    finalRoute = []
    while(name != name2):
        finalRoute.append(name)
        d3 = flowDict[name]
        d2 = {k : v for k,v in d3.items() if v == {0:1} }
        name = list(d2.keys())[0]
    saveRoute(finalRoute)

"""
    Save final route in a file
"""
def saveRoute(fr):
    file = open('output.txt','w') 
 
    file.write('Optimal route:' + '\n') 
    file.write('Station' + '\t'+ 'Bus' + '\t' + 'Hour' + '\n' )

    for i in range(1, len(fr)):
        data = fr[i].split('-')
        time = datetime.timedelta(minutes = int(data[2]))
        file.write(data[0] + '\t'+ data[1] + '\t' + str(time) + '\n' )
    file.close() 



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
    