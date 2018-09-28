import pandas as pd
import networkx as nx 
import numpy as np

data = pd.ExcelFile('data.xlsx')
G = nx.MultiDiGraph()
i = 1

route = data.sheet_names[i]
df = data.parse(route)
stops = df.columns.str.strip().values

def addRoute(df):
    for j in range(0, df.shape[1]):
            G.add_node(stops[j], demand = 0)
            for i in range (0, df.shape[0]):
                name = generateNodeName(i, j)                
                G.add_node(name,  demand = 0)
                addArcSameStop(i, j, name)
                addArcBtStops(i,j,name)
                G.add_edge(name, stops[j], weight= 0)
            
def addArcSameStop(i,j, node2):
    k = i - 1
    while(k >= 0):
        if(df.iloc[k,j] != -1):
            break
        else:
            k = k - 1
    
    if(k >= 0):
        node1 = generateNodeName(k,j)
        weight = df.iloc[i,j] - df.iloc[k,j]
        G.add_edge(node1, node2, weight= weight)

def addArcBtStops(i,j, node2):
    k = j - 1
    while(k >= 0):
        if(df.iloc[i,k] != -1):
            break
        else:
            k = k - 1
    
    if(k >= 0):
        node1 = generateNodeName(i,k)
        weight = df.iloc[i,j] - df.iloc[i,k]
        G.add_edge(node1, node2, weight= weight)

def generateNodeName(i, j):
    stop = stops[j]
    time = df.iloc[i,j]
    name = "-".join([route, stop, str(time)])
    return name

addRoute(df)
print(G.nodes())

#G.add_node('S-Oak Creek Apartments (Across Street On Sand Hill Rd)-383',  demand = -1)
#G.add_node('Stanford Guest House (In Parking Lot)',  demand = 1)

#flowCost, flowDict = nx.network_simplex(G)
#print(flowCost)
