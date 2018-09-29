import pandas as pd
import networkx as nx 

# =======================================
# Graph  
# =======================================
class MGraph:

    """         
        - Read file
        - Initialize Graph, stops and data
        - Load the nodes and arc from graph
    """
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.allStops = []
        self.data = pd.ExcelFile('data.xlsx')
        self.loadRoutes()

    """
        - For each route (sheet) in file read data
        - With Pandas create dataframe 
        - Process headers
        - Add a graph for each route
        - Connect different routes (different graphs)
    """
    def loadRoutes(self):
        sheets = self.data.sheet_names
        for i in range(0, len(sheets)):
            route = sheets[i]
            df = self.data.parse(route)        
            df.columns = df.columns.str.split('.').str[0]
            df.columns = df.columns.str.replace('\xa0', '')
            stops = df.columns.str.strip(' ').values
            self.allStops = list(set(self.allStops + list(stops)))
            self.addRoute(df,route,stops)
        self.connectRoutes(sheets, self.allStops)

    """
        Add nodes and arcs for the graph
    """
    def addRoute(self, df, route, stops):

        """
            Arcs between same stop, and bus but different hours
        """        
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
                self.G.add_edge(node1, node2, weight= weight)

        """
            Arcs between different stops same bus and trip
        """ 
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
                self.G.add_edge(node1, node2, weight= weight)

        """
            Generate unique name for each node
        """ 
        def generateNodeName(i, j):
            stop = stops[j]
            time = df.iloc[i,j]
            name = "-".join([stop, route, str(time)])
            return name

        """
            Initialize the routes
            - Create nodes
                - Fictional node to represent an arrive stop *
                - Node for 
            - Create arcs
                - Arcs between same stop but different hours
                - Arcs between different stops same trip
            - Create a 0 weight arc to unify arrives to an stop * 
        """ 
        for j in range(0, df.shape[1]):
                self.G.add_node(stops[j], demand = 0)
                for i in range (0, df.shape[0]):
                    if(df.iloc[i,j] != -1):
                        name = generateNodeName(i, j)                
                        self.G.add_node(name,  demand = 0, stop=stops[j], time=df.iloc[i,j], route=route)
                        addArcSameStop(i, j, name)
                        addArcBtStops(i,j,name)
                        self.G.add_edge(name, stops[j], weight= 0)

    """
        Connect routes to simulate transfers between buses
    """
    def connectRoutes(self, routes, stops):    
        for i in stops:
            for j in routes:
                nodeStop = [y for x,y in self.G.nodes(data=True) if (('stop' in y and y['stop']==i) and ('route' in y and y['route']==j))]
                self.joinRoutes( routes, stops, nodeStop , i , j)
    
    """
        Help method to connect routes to simulate transfers between buses
    """
    def joinRoutes(self, routes, stops, nodeStop, i, j): 
        for v in nodeStop:
            for k in routes:
                if k != j:
                    nodeT= [y for x,y in self.G.nodes(data=True) if (('stop' in y and y['stop']==i) and ('route' in y and y['route']==k) and ( v['time']< y['time'] ))]
                    if(len(nodeT) != 0):
                        node1 = "-".join([v['stop'], v['route'], str(v['time'])])
                        node2 = "-".join([i, k, str(nodeT[0]['time'])])    
                        weight = nodeT[0]['time'] - v['time']    
                        self.G.add_edge(node1, node2, weight= weight)

    """
        - Set initial node
        - Add edges from inicial node to possible initial stops/buses
    """
    def findStartNode(self, name, hour):
        self.G.add_node(name + ' Start', demand = -1)    
        nodeStop = [y for x,y in self.G.nodes(data=True) if (('stop' in y and y['stop']==name) and ('time' in y and y['time']>=hour))]
        for v in nodeStop:
            node1 = name + ' Start'
            node2 = "-".join([v['stop'], v['route'], str(v['time'])])    
            weight = v['time'] - hour    
            self.G.add_edge(node1, node2, weight= weight)