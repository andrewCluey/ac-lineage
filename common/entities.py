import networkx as nx
from common.repository import repo
import pandas as pd

class Entities:
    def __init__(self,entity_name: str = None):
        self.graph = nx.DiGraph()
        self._create_graph()
        if entity_name:
            self.graph = self._get_entity_graph(entity_name)
        
        
    def _create_graph(self):
        """
        Create a graph from nodes and edges
        Args:
            nodes: list of nodes
            edges: list of edges
        """
        nodes, edges = repo.get_graph_tables()
        
        self.graph = nx.DiGraph()

        for row in nodes.to_pylist():
            self.graph.add_node(row["node"],**row["attributes"])
            
        for row in edges.to_pylist():
            self.graph.add_edge(row["source"],row["target"],**row["attributes"])
        
            
    def _get_entity_graph(self,entity_name: str):
        """
        Get the graph
        Returns:
            graph: graph object
        """
        try:
            recursive_edges = list(nx.dfs_edges(self.graph, source=entity_name))
            subgraph = self.graph.edge_subgraph(recursive_edges).copy()
            if entity_name in subgraph.nodes:
                subgraph.nodes[entity_name]['label'] = 'root'
                #subgraph.nodes[entity_name]['size'] = 100
            return subgraph
        except Exception as e:
            raise Exception(f"Error getting graph: {e}")
        
    def get_entity_relations(self):
        """
        Get the edges of the graph
        Returns:
            edges: list of edges
        """
        result = []

        for node in self.graph.nodes:
            item = dict(self.graph.nodes[node])
            # For each node, find all incoming edges (edges where node is the target)
            incoming = self.graph.in_edges(node, data=True)
            # Collect all "relationship" attributes (which are lists of strings)
            relationships = []
            for u, v, data in incoming:
                rel = data.get('relationship')
                if rel:
                    relationships.extend(rel)
                node_info = {
                    'node': node,
                    **item,
                    'relationships': relationships
                }
                result.append(node_info)
            
        return result
    
    def get_entity_relations_filtered(self):
        """
        Get the edges of the graph with account users filtered out
        Returns:
            edges: list of edges without account user relationships
        """
        result = []

        for node in self.graph.nodes:
            item = dict(self.graph.nodes[node])
            # For each node, find all incoming edges (edges where node is the target)
            incoming = self.graph.in_edges(node, data=True)
            
            # Check if this node has any relationships from "account users"
            has_account_users = any(u == "account users" for u, v, data in incoming)
            
            # Only process the node if it doesn't have account users relationships
            if not has_account_users:
                # Collect all "relationship" attributes (which are lists of strings)
                relationships = []
                for u, v, data in incoming:
                    rel = data.get('relationship')
                    if rel:
                        relationships.extend(rel)
                
                node_info = {
                    'node': node,
                    **item,
                    'relationships': relationships
                }
                result.append(node_info)
            
        return result
    
    
    def get_nodes(self):    
        """
        Get the nodes of the graph
        Returns:
            nodes: list of nodes
        """
        if self.graph.number_of_nodes() == 0:
            raise Exception("entity not found")
        return pd.DataFrame(self.graph.nodes(data=True), columns=["node", "attributes"]).to_dict(orient="records")
    
    def get_edges(self):    
        """
        Get the nodes of the graph
        Returns:
            nodes: list of nodes
        """
        if self.graph.number_of_edges() == 0:
            raise Exception("entity not found")
        return pd.DataFrame(self.graph.edges(data=True), columns=["source", "target","relationship"]).to_dict(orient="records")
    
    