from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
from datetime import timedelta


def start_connection(username,password,bucket_name,scope_name,collection_name,host,couchbase_host_type):

    auth = PasswordAuthenticator(
        username,
        password,
    )

    if(couchbase_host_type == "vm"):
        cluster = Cluster(f'couchbase://{host}', ClusterOptions(auth))
        cluster.wait_until_ready(timedelta(seconds=5))
        cb = cluster.bucket(bucket_name)
        cb_coll = cb.scope(scope_name).collection(collection_name)
    else:
        cluster = Cluster(f'couchbase://127.0.0.1', ClusterOptions(auth))
        cluster.wait_until_ready(timedelta(seconds=5))
        cb = cluster.bucket(bucket_name)
        cb_coll = cb.scope(scope_name).collection(collection_name)

    return cb_coll