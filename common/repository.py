from typing import List
import pandas as pd
from pyarrow import table
import os
from common.authentication import DatabricksAuthentication
import functools

class StorageInterface:
    def __init__(self) -> None:
        self.tmpdir = "/tmp/"
        self.catalog = os.environ.get("DATABRICKS_REFERENCE_CATOLOG")
        self.schema = os.environ.get("DATABRICKS_REFERENCE_SCHEMA")
        self.client = DatabricksAuthentication().client

    @functools.lru_cache(maxsize=32) 
    def get_graph_tables(self)-> List[table]:
        """
        Get all nodes and edges reference schema
        Returns:
            list of table names
        """
        with self.client.cursor() as cursor:
            nodes = (
                cursor.execute(f"SELECT * FROM {self.catalog}.{self.schema}.nodes")
                .fetchall_arrow()
            )
            
            edges = (
                cursor.execute(f"SELECT * FROM {self.catalog}.{self.schema}.edges")
                .fetchall_arrow()

            )
            return [ nodes, edges ]
            
    def refresh(self):
        self.get_graph_tables.cache_clear()
        
repo = StorageInterface()
