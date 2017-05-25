#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:46:30 2017
Simple module holding relevant classes to represent graphs.
@author: jpoeppel
"""

import copy

class Node(object):
    
    def __init__(self, name):
        self.name = name
        self.parents = {}
        self.children = {}
        
    def add_parent(self, parent):
        """
            Add or overwrites a parent node. Will not check if there already is
            a parent with the same name.
            
            Parameters
            ----------
            parent: Node
                The node to be added as parent.
        """
        self.parents[parent.name] = parent
        
    def add_child(self, child):
        """
            Add or overwrites a child node. Will not check if there already is
            a child with the same name.
            
            Parameters
            ----------
            child: Node
                The node to be added as child.
        """
        self.children[child.name] = child
        
    def remove_parent(self, parent):
        """
            Removes a parent node if it exists. If it did not exist, will do 
            nothing.
            
            Parameters
            ----------
            parent: Node
                The node to be removed as parent.
        """
        
        if parent.name in self.parents:
            del self.parents[parent.name]
            
    def remove_child(self, child):
        """
            Removes a child node if it exists. If it did not exist, will do 
            nothing.
            
            Parameters
            ----------
            child: Node
                The node to be removed as child.
        """
        if child.name in self.children:
            del self.children[child.name]
        
    def destroy(self):
        """
            "Destroys" the node by removing its link to all its neighbours.
            This will **not** destroy the actual node object. This would have
            to be taken care of elsewhere.
        """
        for p in self.parents.values():
            p.remove_child(self)
        
        for c in self.children.values():
            c.remove_parent(self)
        self.parents = {}
        self.children = {}
        
    def __hash__(self):
        """
            The hash of a node is the same as the hash of its name.
            This allows to reference nodes in dictionaries by their object
            instantiation or their name.
        """
        return hash(self.name)
        
    def __str__(self):
        """
            Overwrites the default string representation of this class to just
            return it's name.
        """
        return self.name
    
    def __repr__(self):
        """
            Overwrites the default string representation of this class to just
            return it's name.
        """
        return self.name
    
    def __eq__(self, other):
        """
            Two nodes are considered to be identical if they have the
            same name.
            In order for the access in dictionaries via the name to work, a
            random node is equal to its name as well.
        """
        try:
            return other.name == self.name
        except AttributeError:
            return other == self.name
        
    def __ne__(self, other):
        return not self.__eq__(other)

class Graph(object):
    
    def __init__(self):
        self.nodes = {}
        self.is_directed = True
        
    def add_node(self, node):
        """
            Adds a node to the graph. Will first create a new node object
            with the given name.
            
            Parameters
            ----------
            node: String or Node
                The name of the new node or the new node directly. In case
                a string is passed, a new node will be created before adding it.
        """
        if node in self.nodes:
            raise ValueError("The graph already contains a node named {}".format(node))
        
        try:
            self.nodes[node.name] = node
        except AttributeError: #We check for an attribute, rather than a type.
            self.nodes[node] = Node(node)
        
    def remove_node(self, node):
        """
            Removes the node with the given name from the graph.
            
            Parameters
            ----------
            node: String
                The name of the new node.
        """
        if not node in self.nodes:
            raise ValueError("The graph does not contain a node named {}".format(node))
        
        self.nodes[node].destroy()
        del self.nodes[node]
        
    def add_edge(self, node1, node2):
        """
            Adds a directed edge from node1 to node2. In this implementation, edges
            are only implictly represented, via parent and child relations in the
            nodes. One could alternatively explicitly represent edge objects that
            connect nodes.
            
            If the graph 
            
            Parameters
            ----------
            node1: String
                The name of the first node.
            node2: String
                The name of the second node.
        """
        try:
            self.nodes[node1].add_child(self.nodes[node2])
            self.nodes[node2].add_parent(self.nodes[node1])
            self.is_directed = True
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node1, node2))
            
    def remove_edge(self, node1, node2):
        """
            Removes an edge from node1 to node2, if it exists. Ignores incorrect
            edges.
            
            Parameters
            ----------
            node1: String
                The name of the first node.
            node2: String
                The name of the second node.
        """
        try:
            self.nodes[node1].remove_child(self.nodes[node2])
            self.nodes[node2].remove_parent(self.nodes[node1])
        except KeyError:
            raise ValueError("At least one of your specified nodes ({},{}) " \
                             "is not contained in the graph".format(node1, node2))
            
    def get_number_of_nodes(self):
        """
            Returns
            -------
            int
                The total number of nodes in the graph.
        """
        return len(self.nodes)


    def get_nodes(self):
        return self.nodes.values()


    
    def get_parents(self, node):
        """
            Parameters
            ----------
            node: String
                The name of the node whose parents are queried.
                
            Returns
            -------
            list
                A list containing all parent nodes of the specified node.
        """
        try:
            return self.nodes[node].parents.values()
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node))
            
    def get_children(self, node):
        """
            Parameters
            ----------
            node: String
                The name of the node whose children are queried.
                
            Returns
            -------
            list
                A list containing all children nodes of the specified node.
        """
        try:
            return self.nodes[node].children.values()
        except KeyError:
            raise ValueError("The graph does not contain a node called {}".format(node)) 
        
            
    def copy(self, deep=True):
        """
            Copies the current graph.
            
            Parameters
            ----------
            deep: Bool
                If true, a deep copy will be performed, i.e. all nodes are also
                copied. In a shallow copy, both graph instances will contain the
                same node references.
            
            Returns
            -------
                Graph
                Creates a (deep) copy of this graph.
        """
       
        if deep:
            return copy.deepcopy(self)
        else:
             return copy.copy(self)
            
    def to_undirected(self):
        """
            Returns an undirected copy this graph. Sine this implementation
            does not really specify edge directions, we consider a bidrectional
            graph as undirected!
            
            Returns
            -------
                Graph
                An undirected copy of this graph.
        """
        res = self.copy()
        if res.is_directed:
            for n in res.nodes.values():
                for p in n.parents.values():
                    n.add_child(p)
                    p.add_parent(n)
                for c in n.children.values():
                    c.add_child(n)
                    n.add_parent(c)
            res.is_directed = False  
        return res
