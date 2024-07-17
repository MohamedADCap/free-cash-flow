from databricks_api import DatabricksAPI

def start_cluster(api_token, cluster_id):
    dbx = DatabricksAPI(token=api_token)
    dbx.clusters.start(cluster_id)

def stop_cluster(api_token, cluster_id):
    dbx = DatabricksAPI(token=api_token)
    dbx.clusters.stop(cluster_id)
