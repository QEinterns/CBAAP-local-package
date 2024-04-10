from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
from datetime import timedelta
from config import COUCHBASE_URL

def couchbase_init_local():

    username = "Administrator"
    password = "cbaapsecure"
    bucket_name = "local"

    auth = PasswordAuthenticator(
        username,
        password,
    )

    cluster = Cluster(f'couchbase://{COUCHBASE_URL}', ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=5))


    session_coll = cluster.bucket(bucket_name)

    user_i = cluster.bucket(bucket_name)
    user_info = user_i.scope("user_info").collection("user_session")

  
    session_list_coll = user_i.scope("user_info").collection("session_array")

    session_list_a_coll = user_i.scope("user_info").collection("session_array_a")

    session_list_new_coll = user_i.scope("user_info").collection("session_array_new")

    return session_coll, user_info, session_list_coll, session_list_a_coll, session_list_new_coll
