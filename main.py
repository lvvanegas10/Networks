from graph_class import MGraph
import networkx as nx 
import datetime

# =======================================
# Help main  
# =======================================

"""
    Print the final route from name to name2
"""
def printOptimalRoute(name, name2, flowDict, flowCost):
    finalRoute = []
    n1 = name
    while(name != name2):
        finalRoute.append(name)
        d3 = flowDict[name]
        d2 = {k : v for k,v in d3.items() if v == {0:1} }
        name = list(d2.keys())[0]
    saveRoute(finalRoute, flowCost, n1, name2)

"""
    Save final route in a file
"""
def saveRoute(fr, flowCost, name, name2):
    file_name = '-'.join([name, name2])
    file = open('data/output/'+ file_name +'.txt','w') 
 
    file.write('Optimal route:' + '\n') 
    file.write('Cost: ' + str(flowCost) + ' minutes'+ '\n') 
    file.write('Station' + '\t'+ 'Bus' + '\t' + 'Hour' + '\n' )

    for i in range(1, len(fr)):
        data = fr[i].split('-')
        time = datetime.timedelta(minutes = int(data[2]))
        file.write(data[0] + '\t'+ data[1] + '\t' + str(time) + '\n' )
    file.close() 

"""
    Print if there is no optimal route
"""
def printError(n, n2):
    file_name = '-'.join([n, n2])
    file = open('data/output/'+ file_name +'.txt','w')  
    file.write('Optimal route:' + '\n') 
    file.write('There`s no an optimal route between these stops')    
    file.close() 

# =======================================
# Main   
# =======================================
if __name__ == "__main__":

    file = open('data/inputfile.txt','r')  

    for line in file:
        data = line.split('-')
        name = data[0]
        name2 = data[1]
        time = int(data[2])

        graph = MGraph()
           
        try:
            graph.findStartNode(name, time)
            graph.G.add_node(name2,  demand = 1)
            flowCost, flowDict = nx.network_simplex(graph.G)    
            printOptimalRoute(name + ' Start', name2, flowDict, flowCost) 
        except:
            printError(name, name2)