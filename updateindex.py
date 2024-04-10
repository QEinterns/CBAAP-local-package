import subprocess
def create_index_app(username,password,index_name, host, bucket, scope, collection, dimensions, field):

    args = {
        "index_name": index_name,
        "host": host,  
        "bucket": bucket,
        "scope": scope,
        "collection": collection,
        "dimensions": int(dimensions),
        "field": field,
        "username":username,
        "password":password,
        "name":f"{bucket}.{scope}.{index_name}",
        "type_string":f"{scope}.{collection}"
    }

    curl_command = """
curl -XPUT -H "Content-Type: application/json" -u {username}:{password} \
http://{host}:8094/api/bucket/{bucket}/scope/{scope}/index/{index_name} -d \
'{{
  "type": "fulltext-index",
  "name": "{name}",
  "sourceType": "gocbcore",
  "sourceName": "{bucket}",
  "planParams": {{
    "maxPartitionsPerPIndex": 1024,
    "indexPartitions": 1
  }},
  "params": {{
    "doc_config": {{
      "docid_prefix_delim": "",
      "docid_regexp": "",
      "mode": "scope.collection.type_field",
      "type_field": "type"
    }},
    "mapping": {{
      "analysis": {{}},
      "default_analyzer": "standard",
      "default_datetime_parser": "dateTimeOptional",
      "default_field": "_all",
      "default_mapping": {{
        "dynamic": true,
        "enabled": false
      }},
      "default_type": "_default",
      "docvalues_dynamic": false,
      "index_dynamic": true,
      "store_dynamic": false,
      "type_field": "_type",
      "types": {{
        "{type_string}": {{
          "dynamic": false,
          "enabled": true,
          "properties": {{
            "data": {{
              "dynamic": false,
              "enabled": true,
              "fields": [
                {{
                  "docvalues": true,
                  "include_in_all": true,
                  "include_term_vectors": true,
                  "index": true,
                  "name": "data",
                  "store": true,
                  "type": "text"
                }}
              ]
            }},
            "vector_data": {{
              "dynamic": false,
              "enabled": true,
              "fields": [
                {{
                  "dims": {dimensions},
                  "index": true,
                  "name": "vector_data",
                  "similarity": "l2_norm",
                  "type": "vector",
                  "vector_index_optimized_for": "recall"
                }}
              ]
            }}
          }}
        }}
      }}
    }},
    "store": {{
      "indexType": "scorch",
      "segmentVersion": 16
    }}
  }},
  "sourceParams": {{}}
}}'
""".format(**args)

    print(curl_command)
    try:
        subprocess.run(curl_command, shell=True, check=True)
        print(f"{index_name} Index created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating the index: {e}")




