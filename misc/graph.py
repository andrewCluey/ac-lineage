# Databricks notebook source
# MAGIC %pip install networkx==3.4.2
# MAGIC %restart_python

# COMMAND ----------

dbutils.widgets.text("environment", "dev")
env=dbutils.widgets.get("environment")
dbutils.widgets.text("account", "id")
acc=dbutils.widgets.get("account")
dbutils.widgets.text("workspaces",'["name","name","name"]')
workspaces=dbutils.widgets.get("workspaces")
dbutils.widgets.text("target_catalog",'_data')
target_catalog=dbutils.widgets.get("target_catalog")
dbutils.widgets.text("target_schema",'_lineage')
target_schema=dbutils.widgets.get("target_schema")



# COMMAND ----------

from databricks.sdk import WorkspaceClient, AccountClient
import logging
from typing import List, Tuple

def get_clients(env: str) -> Tuple[WorkspaceClient, AccountClient]:
    """
    Returns a tuple of WorkspaceClient and AccountClient.
    Args:
        env (str): The environment name.
        Returns:
        Tuple[WorkspaceClient, AccountClient]: A tuple of WorkspaceClient and AccountClient.
    """
    ws = WorkspaceClient()

    scope = f"{env}-scope"
    return ws, AccountClient(
        host="https://accounts.azuredatabricks.net/",
        account_id=acc,
        azure_tenant_id= ws.dbutils.secrets.get(scope=scope, key="tenant-id"),
        azure_client_id= ws.dbutils.secrets.get(scope=scope, key="client-id"),
        azure_client_secret= ws.dbutils.secrets.get(scope=scope, key="client-secret"),
    )
ws, ac = get_clients(env)

# COMMAND ----------


included_workspaces = [workspace for workspace in ac.workspaces.list() if workspace.workspace_name in workspaces]       
authorised_ws_clients = []
for workspace in included_workspaces:
    ws = ac.get_workspace_client(workspace)
    try:
        ws.get_workspace_id()
        logging.info(f"Workspace {workspace.workspace_name} is accessible")
        authorised_ws_clients.append(ws)
    except Exception as e:
        logging.error(f"Workspace {workspace.workspace_name} is not accessible")

# COMMAND ----------

from databricks.sdk.service import iam as i, catalog as CAT

def get_warehouse_id_by_name(ws: WorkspaceClient, cluster_name: str) -> str:
    """
    Returns the ID of a SQL warehouse (cluster) in Databricks.
    Args:
        ws (WorkspaceClient): The Databricks workspace client.
        cluster_name (str): The name of the SQL cluster (SQL warehouse) to find the ID for.
        Returns:
        str: The ID of the SQL cluster (SQL warehouse) if found, otherwise None.
        Raises ValueError if the cluster is not found.
    """
    warehouses = ws.warehouses.list()
    
    for w in warehouses:
        if w.name == cluster_name:
            return w.id
    raise ValueError(f"Cluster with name '{cluster_name}' not found.")



assets_data = []
for ws in authorised_ws_clients:
    for catalog in ws.catalogs.list():
        catalog_grant = ws.grants.get(CAT.SecurableType.CATALOG, full_name=catalog.name)
        if catalog_grant is not None:
            for cp in catalog_grant.privilege_assignments:
                assets_data.append({
                "entity_name" : cp.principal,
                "asset_type" : "catalog",
                "asset_name": catalog.name,
                "privilege" : [priv.name for priv in cp.privileges]
                })
            for schema in ws.schemas.list(catalog_name=catalog.name):
                schema_grant = ws.grants.get(CAT.SecurableType.SCHEMA, full_name=catalog.name+"."+schema.name)
                if schema_grant is not None:
                    for sp in schema_grant.privilege_assignments:
                            assets_data.append({
                            "entity_name" : sp.principal,
                            "asset_type" : "schema",
                            "asset_name": f"{catalog.name}.{schema.name}",
                            "privilege" : [priv.name for priv in sp.privileges]
                            })

    for warehouse in ws.warehouses.list():    
        perm =  ws.warehouses.get_permissions(get_warehouse_id_by_name(ws,warehouse.name))
        for principal in perm.access_control_list:
                for priviledge in principal.all_permissions:
                    assets_data.append({
                        "entity_name" : principal.group_name or principal.user_name or principal.service_principal_name,
                        "asset_type" : "warehouse",
                        "asset_name": warehouse.name,
                        "privilege" : [priviledge.permission_level.name]
                        })
                    
    for cluster in ws.clusters.list():    
        permissions =  ws.clusters.get_permissions(cluster.cluster_id)
        for principal in permissions.access_control_list:
                for priviledge in principal.all_permissions:
                    assets_data.append({
                        "entity_name" : principal.group_name or principal.user_name or principal.service_principal_name,
                        "asset_type" : "cluster",
                        "asset_name": cluster.cluster_name,
                        "privilege" : [priviledge.permission_level.name]
                        })                
            

# COMMAND ----------


principals = [{"id":p.id,"name":p.display_name} for p in ac.service_principals.list()]
users = [{"id":user.id,"name": user.user_name} for user in ac.users.list()]
#API changed in August 2025 see:  As of 08/22/2025, this endpoint will not return members. Instead, members should be retrieved by iterating through Get group details.
#https://docs.databricks.com/api/account/accountgroups/list
groups = [{"id":group.id,"name":group.display_name,"members":group.members} for group in [ac.groups.get(group.id) for group in ac.groups.list()]]


def is_member_a_group(ref: str) -> bool:
    return ref.startswith("Groups")

def recursive_member_checker(entity_id: str,entity_name: str, depth: int = 0, max_depth: int = 5, visited: set = None) -> list:
    if visited is None:
        visited = set()
    if depth > max_depth or entity_id in visited:
        return []
    visited.add(entity_id)
    results = []
    for group in groups:
        for member in group["members"]:
            if member.value == entity_id:
                #print(f"Found user {entity_id} in group {group['id']}")
                results.append({"entity_id": entity_id,"entity_name": entity_name, "member_of_group": group["id"], "member_of_group_name": group["name"], "depth": depth})
                results.extend(recursive_member_checker(group["id"],group["name"], depth + 1, max_depth, visited))
    return results

all_membership_data = []
for user in users:
    all_membership_data.extend(recursive_member_checker(user["id"],user["name"]))
for principal in principals:
    all_membership_data.extend(recursive_member_checker(principal["id"],principal["name"]))


# COMMAND ----------

# MAGIC %md 
# MAGIC Question why are some entity names null

# COMMAND ----------

import networkx as nx
import pandas as pd
# Initialize a graph
G = nx.DiGraph()

unique_entities = set()

for row in all_membership_data:
    unique_entities.add(row["entity_name"])
    unique_entities.add(row["member_of_group_name"])

for row in assets_data:
    unique_entities.add(row["entity_name"])

for row in unique_entities:
    if row:
        G.add_node(row, label="entity")
# Add nodes and edges for entity-group relationships
for row in all_membership_data:
    # Add edge
    if row["entity_name"]:
        G.add_edge(row["entity_name"], row["member_of_group_name"], relationship=["IS_MEMBER"])

# Add nodes and edges for entity-type-asset relationships
for row in assets_data:
    if row["asset_name"]:
        # Add nodes
        G.add_node(f"{row['asset_type']}_{row['asset_name']}", label=str(row['asset_type']))
        G.add_edge(row["entity_name"], f"{row['asset_type']}_{row['asset_name']}", relationship=row['privilege'])

(
    spark.createDataFrame(pd.DataFrame(G.edges(data=True), columns=["source", "target", "attributes"]))
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(f"{target_catalog}.{target_schema}.edges")
)
(
    spark.createDataFrame(pd.DataFrame(G.nodes(data=True), columns=["node", "attributes"]))
    .write.format("delta")
    .mode("overwrite")
    .saveAsTable(f"{target_catalog}.{target_schema}.nodes")
)