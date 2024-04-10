from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, ClusterOptions
from datetime import timedelta

def connect2couchbase(username, password, bucket_name, scope_name, collection_name, host='couchbase://localhost', timeout_seconds=5):
    auth = PasswordAuthenticator(username, password)
    cluster = Cluster(host, ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=timeout_seconds))
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)
    return cb_coll

# def connect2couchbase(username, password, host, bucket_name, scope_name, collection_name, timeout_seconds=5):
#     auth = PasswordAuthenticator(username, password)
#     options = ClusterOptions(auth)

#     # Initialize the Cluster without specifying the initial host
#     cluster = Cluster('couchbase://'+host, options)
#     cluster.wait_until_ready(timedelta(seconds=timeout_seconds))

#     # Get the bucket, scope, and collection
#     cb = cluster.bucket(bucket_name)
#     cb_coll = cb.scope(scope_name).collection(collection_name)

#     # Get a list of nodes in the cluster
#     nodes = cb.server_nodes
#     print(nodes)

#     # Find the first node with the specified service running
#     # for node in nodes:
#     #     services = node.services()
#     #     if services.get("fts") == 'running':
#     #         return cb_coll, node.hostname

#     # If no node with the specified service running is found, return None
#     return cb_coll, None
    
#     #return cb_coll