import pandas as pd
import networkx as nx 

data = pd.ExcelFile('data.xlsx')
G = nx.MultiDiGraph()
i = 1
print(data.sheet_names[i])
x = data.parse(data.sheet_names[i])
print(x)

def addRoute(df):
    for c in df.columns:
        df[c].apply(addNodes)


def addNodes(n):
    print(n)


## addRoute(x)