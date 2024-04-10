from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
from datetime import timedelta
from config import COUCHBASE_URL

def couchbase_init():

    username = "Administrator"
    password = "cbaapsecure"
    bucket_name = "b1"
    scope_name = "s1"
    collection_name = "docs"

    auth = PasswordAuthenticator(
        username,
        password,
    )

    cluster = Cluster(f'couchbase://{COUCHBASE_URL}', ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)

    db = cluster.bucket(bucket_name)
    db_coll = db.scope(scope_name).collection("c3")

    ab = cluster.bucket(bucket_name)
    ab_coll = ab.scope(scope_name).collection("ca")

    eb = cluster.bucket(bucket_name)
    eb_coll = eb.scope(scope_name).collection("c6")

    rb = cluster.bucket(bucket_name)
    rb_coll = rb.scope(scope_name).collection("d1")

    wb = cluster.bucket(bucket_name)
    wb_coll = wb.scope("s3").collection("watcher")

    kbi  =cluster.bucket(bucket_name)
    kb =  kbi.scope("s1").collection("test1")

    architect = cluster.bucket(bucket_name)
    architect_coll = architect.scope(scope_name).collection("architect")

    return cb_coll,db_coll,eb_coll,rb_coll,architect_coll



def couchbase_init1():

    username = "Administrator"
    password = "cbaapsecure"
    bucket_name = "b1"
    scope_name = "s1"
    collection_name = "docs"

    auth = PasswordAuthenticator(
        username,
        password,
    )

    cluster = Cluster(f'couchbase://{COUCHBASE_URL}', ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)

    ab = cluster.bucket(bucket_name)
    ab_coll = ab.scope(scope_name).collection("ca")


    wb = cluster.bucket(bucket_name)
    wb_coll = wb.scope("s3").collection("watcher")

    kbi  =cluster.bucket(bucket_name)
    kb =  kbi.scope("s2").collection("demo")

    u = cluster.bucket(bucket_name)
    us = u.scope("users").collection("user")

    cus = cluster.bucket(bucket_name)
    c_coll = cus.scope(scope_name).collection("cnew")

    watch_c = cluster.bucket(bucket_name)
    watch_coll= watch_c.scope("s3").collection("watcher")

    return kb,cb,ab_coll,us,c_coll,watch_coll
