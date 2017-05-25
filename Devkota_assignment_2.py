"""
@author: jpoeppel
"""
# Required methods added by kdevkota to the codebase provided by Jan (jpoeppel)

"""
Import required modules.
"""
#If you use your own graph implementation, you might have to change
#this accordingly!
from  ccbase.graph import Graph, Node 
import sys
######
#
# Example networks
#
######

graph1 = Graph()

X1 = Node("X1")
X2 = Node("X2")
X3 = Node("X3")
X4 = Node("X4")
X5 = Node("X5")
X6 = Node("X6")
X7 = Node("X7")
X8 = Node("X8")

graph1.add_node(X1)
graph1.add_node(X2)
graph1.add_node(X3)
graph1.add_node(X4)
graph1.add_node(X5)
graph1.add_node(X6)
graph1.add_node(X7)
graph1.add_node(X8)

graph1.add_edge(X1, X5)
graph1.add_edge(X2, X5)
graph1.add_edge(X3, X5)
graph1.add_edge(X4, X5)
graph1.add_edge(X7, X4)
graph1.add_edge(X5, X7)
graph1.add_edge(X5, X8)
graph1.add_edge(X6, X8)


graph2 = Graph()

A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")
G = Node("G")
H = Node("H")
I = Node("I")
L = Node("L")
M = Node("M")

graph2.add_node(A)
graph2.add_node(B)
graph2.add_node(C)
graph2.add_node(D)
graph2.add_node(E)
graph2.add_node(F)
graph2.add_node(G)
graph2.add_node(H)
graph2.add_node(I)
graph2.add_node(L)
graph2.add_node(M)

graph2.add_edge(A, C)
graph2.add_edge(C, E)
graph2.add_edge(E, G)
graph2.add_edge(E, H)
graph2.add_edge(B, D)
graph2.add_edge(D, F)
graph2.add_edge(F, H)
graph2.add_edge(F, I)
graph2.add_edge(H, L)
graph2.add_edge(I, M)
graph2.add_edge(M, H)


graph3 = graph1.copy()

graph3.add_edge(graph3.nodes["X7"], graph3.nodes["X8"])
graph3.add_edge(graph3.nodes["X4"], graph3.nodes["X8"])

graph3 = graph3.to_undirected()


######
#
# Ex 1
#
######

# Helper function 1 : Get all the ancestors of a given node
def get_ancestors(dg, n_y):
    nodes = [n_y]
    ancestors = []                
    while nodes:
        for n in nodes:
            nodes = nodes + dg.get_parents(n)
            nodes.remove(n)
            ancestors = ancestors + nodes
    return list(set(ancestors))  


# Helper function 2 : Get all the descendents of a given node
def get_descendents(dg, n_y):
    nodes = [n_y]
    descendents = []                
    while nodes:
        for n in nodes:
            nodes = nodes + dg.get_children(n)
            nodes.remove(n)
            descendents = descendents + nodes
    return list(set(descendents)) 


def is_node_ancestor(dg, node_x, node_y):
    """
        Function that queries if node_x is an ancestor of node_y in the graph
        dg.
        
        Parameters
        ----------
        dg: a graph (either graph.Graph, or your own)
            The graph object that should contain node_x and node_y
        node_x: Node/String 
            The node that is tested to be an ancestor.
        node_y: Node/String
            The node that should be a descendent of node_x.
            
        Returns
        -------
            Bool
            True if node_x is an ancestor of node_y, false otherwise.
            
    """
    for a in get_ancestors(dg, node_y):
        if a == node_x:
            return True 
    return False            
    

#    if is_acyclic(dg):           ###################Something not right##############################
#        nodes = dg.get_parents(node_y) 
#        while nodes:
#            if node_x in nodes:
#                return True   
#            for n in nodes:
#                nodes = nodes + dg.get_parents(n)
#                nodes.remove(n)
#        return False
#    sys.exit("Cyclic graph!")
                                   
    #print get_ancestors(dg, node_y)
      


def is_node_descendant(dg, node_x, node_y):
    """
        Function that queries if node_x is a descendant of node_y in the graph
        dg.
        
        Parameters
        ----------
        dg: a graph (either graph.Graph, or your own)
            The graph object that should contain node_x and node_y
        node_x: Node/String 
            The node that is tested to be a descendant.
        node_y: Node/String
            The node that should be an ancestor of node_x.
            
        Returns
        -------
            Bool
            True if node_x is a descendant of node_y, false otherwise.
            
    """

    for a in get_descendents(dg, node_y):
        if a == node_x:
            return True 
    return False 
     


#    if is_acyclic(dg):
#        nodes = dg.get_children(node_y) #TODO: add a acyclic check
#        while nodes:
#            if node_x in nodes:
#                return True    
#            for n in nodes:
#                nodes = nodes + dg.get_children(n)
#                nodes.remove(n)
#        return False                                
#    sys.exit("Cyclic graph!")


def is_acyclic(dg):
    """
        Computes whether or not the graph is acyclic.
        
        Parameters
        ---------
        dg: a graph
            The graph do be tested.
            
        Returns
        ----------
            Bool
            True if there are no cycles within the provided graph, False otherwise.
    """

    # Note: added a new method get_nodes() in provided Graph class    
          
    p =[]
    for i in range(dg.get_number_of_nodes()):
        if not dg.get_parents(dg.get_nodes()[i]):    
            p.append(dg.get_nodes()[i])   # all parentless nodes
    while not len(p) == 0: # looking for children, and removing edge from p --> c        
        s = p[0]
        p = p[1:]    
        child = dg.get_children(s) 
        for c in child:
            dg.remove_edge(s,c) 
            if not dg.get_parents(c):    
                p.append(c)
    count = 0
    for i in range(dg.get_number_of_nodes()):
        if dg.get_parents(dg.get_nodes()[i]): # nodes having parent still, means cyclic
            count = count + 1  
    if count != 0:  
        return False
    else:
        return True
        


######
#
# Ex 2
#
######

def get_forks(dg):
    """
        Computes all forks within the given graph.
        
        Parameters
        ---------
        dg: a graph
            The graph whose forks are to be computed.
            
        Returns
        ----------
            [Node,]
            A list containing all Nodes (either class or their name/id) that
            represent forks in the network.
    """
    forks = []
    for node in dg.get_nodes():
        if len(dg.get_children(node)) >= 2:
            forks.append(node)    
    return forks

    
def get_colliders(dg):
    """
        Computes all colliders within the given graph.
        
        Parameters
        ---------
        dg: a graph
            The graph whose colliders are to be computed.
            
        Returns
        ----------
            [Node,]
            A list containing all Nodes (either class or their name/id) that
            represent colliders in the network.
    """
    colliders = []    
    for node in dg.get_nodes():
        if len(dg.get_parents(node)) >= 2:
            colliders.append(node)
    return colliders

    
######
#
# Ex 3
#
######

def get_ancestral_graph(dg, nodes_x, nodes_y, nodes_z):
    """
        Computes an ancestral graph of the provided graph for the node sets
        nodes_x, nodes_y and nodes_z.
        
        Parameters
        ---------
        dg: a graph
            The graph whose ancestral_graph is to be computed.
        nodes_x: iterable of Node
            The first set of nodes determining the ancestral graph.
        nodes_y: iterable of Node
            The second set of nodes determining the ancestral graph.
        nodes_z: iterable of Node
            The third set of nodes determining the ancestral graph.
            
        Returns
        ----------
            a graph
            A graph object that represents the ancestral graph of dg according
            to the three sets of nodes.
    """
    ancestral_graph = dg.copy()
    
    ### your code here

    return ancestral_graph

def moralise_graph(dg):
    """
        Computes a moralised version of the provided graph.
        
        Parameters
        ---------
        dg: a graph
            The graph to be moralised.
            
        Returns
        ----------
            a graph
            A moralised copy of the initial graph dg.
    """
    # You might have to implement this function "to_undirected()" if you use
    # your own graph class.
    moralised_graph = dg.to_undirected() 
    
    # your code
    # ...

    return moralised_graph

def separate(g, nodes_z):
    """
        Separates all nodes in nodes_z from the graph.
        
        Parameters
        ---------
        g: a graph
            The graph to be modified.
        nodes_z: iterable of Node
            The set of nodes to be separated from the graph.
            
        Returns
        ----------
            a graph
            A copy of the provided graph dg where the nodes in nodes_z have been
            separated.
    """
    # your code
    # ...

    return g

def check_independence(dg, nodes_x, nodes_y, nodes_z):
    """
        Computes whether or not nodes in nodes_x are conditionally 
        independend of nodes in nodes_y given nodes in nodes_z.
        
        Parameters
        ---------
        dg: a graph
            The graph that should contain all the nodes.
        nodes_x: iterable of Node
            The nodes that should be conditionally independent of the nodes
            in nodes_y
        nodes_y: iterable of Node
            The nodes that should be conditionally independent of the nodes
            in nodes_x                
        nodes_z: iterable of Node
            The set of nodes that should make nodes_x and nodes_y conditionally
            independent.
            
        Returns
        ----------
            Bool
            True if all nodes in nodes_x are conditionally independent of all
            nodes in nodes_y given the nodes in nodes_z, False otherwise.
    """
    
    # your code
    # ...

    return True
	


####
#   Some testcases. Most of these will fail before you implemented your code.
#   If you only want to test parts of your code, you can comment out the unrelevant
#   assertions.
####

print is_node_ancestor(graph2,"A", "M")

print is_node_descendant(graph2,'L', 'B')



#assert is_node_ancestor(graph1, X1, X8) == True, "X1 is an ancestor of X8"
#assert is_node_ancestor(graph1, X8, X7) == False, "X8 is not an ancestor of X7"  # Here, the graph is cyclic, so I think it will be erroneous and loop forever, if unckecked for acyclicness



#assert is_node_descendant(graph2, "A", "M") == False, "A is not a descendent from M"
#assert is_node_descendant(graph2, "L", "B") == True, "L is a descendent from B"


#print is_acyclic(graph1)

##assert is_acyclic(graph1) == False, "graph1 is cyclic"
##assert is_acyclic(graph2) == True, "graph2 is acyclic"


##forks = get_forks(graph2)
##trueForks = [] #You would need to fill this yourself
##assert len(forks) == len(trueForks)
##for f in forks:
##   assert f in trueForks, "{} is not a fork".format(f)
##for tf in trueForks:
##    assert tf in forks, "{} is also a fork".format(tf)

##colliders = get_colliders(graph1)
##trueColliders = [] #You would need to fill this yourself
##assert len(colliders) == len(trueColliders)
##for c in colliders:
##    assert c in trueColliders, "{} is not a collider".format(c)
##for tc in trueColliders:
##    assert tc in colliders, "{} is also a collider".format(tc)
    
##ag = get_ancestral_graph(graph2, [G], [H], [E])
##mg = moralise_graph(ag)
##sep = separate(mg, [E])

##assert check_independence(graph2, [G], [H], [E]) == True, "G and H are conditionally indepedent given E"
##assert check_independence(graph2, [E], [F], [H]) == False, "E and F are conditionally depedent given H"

#Feel free to add more complex tests for your own code as desired.
