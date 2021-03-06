import pandas as pd
import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt

data = pd.ExcelFile('showGraph.xlsx')
G = nx.MultiDiGraph()
allStops = []

def loadRoutes(data, allStops):
    sheets = data.sheet_names
    for i in range(0, 2):
        route = sheets[i]
        df = data.parse(route)        
        df.columns = df.columns.str.split('.').str[0]
        df.columns = df.columns.str.replace('\xa0', '')
        stops = df.columns.str.strip(' ').values
        allStops = list(set(allStops + list(stops)))
        addRoute(df,route,stops)
    connectRoutes(sheets, allStops)


def addRoute(df, route, stops):
            
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
        name = "-".join([stop, route, str(time)])
        return name

    for j in range(0, df.shape[1]):
            G.add_node(stops[j], demand = 0)
            for i in range (0, df.shape[0]):
                if(df.iloc[i,j] != -1):
                    name = generateNodeName(i, j)                
                    G.add_node(name,  demand = 0, stop=stops[j], time=df.iloc[i,j], route=route)
                    addArcSameStop(i, j, name)
                    addArcBtStops(i,j,name)
                    G.add_edge(name, stops[j], weight= 0)


def connectRoutes(routes, stops):    
    for i in stops:
        for j in routes:
            nodeStop = [y for x,y in G.nodes(data=True) if (('stop' in y and y['stop']==i) and ('route' in y and y['route']==j))]
            for v in nodeStop:
                for k in routes:
                   if k != j:
                        nodeT= [y for x,y in G.nodes(data=True) if (('stop' in y and y['stop']==i) and ('route' in y and y['route']==k) and ( v['time']< y['time'] ))]
                        if(len(nodeT) != 0):
                            node1 = "-".join([v['stop'], v['route'], str(v['time'])])
                            node2 = "-".join([i, k, str(nodeT[0]['time'])])    
                            weight = nodeT[0]['time'] - v['time']    
                            G.add_edge(node1, node2, weight= weight)

def findStartNode(name, hour):
    G.add_node(name + ' Start', demand = -1)    
    nodeStop = [y for x,y in G.nodes(data=True) if (('stop' in y and y['stop']==name) and ('time' in y and y['time']>=hour))]
    for v in nodeStop:
        node1 = name + ' Start'
        node2 = "-".join([v['stop'], v['route'], str(v['time'])])    
        weight = v['time'] - hour    
        G.add_edge(node1, node2, weight= weight)


loadRoutes(data, allStops)
findStartNode('Hoover Pavilion Garage (Inside Lot 1)',400)

colors= ["#d2cab2","#008375","#008375","#008375","#d2cab2","#008375","#008375","#7fa94c","#7fa94c","#d2cab2","#7fa94c","#7fa94c","#572d57"]
 
nx.draw_shell(G, with_labels=True, font_size= 7, node_color=colors )
print(G.nodes())
print(G.number_of_nodes())

plt.savefig("path.png")