import subprocess
import json
from config import COUCHBASE_URL



def vector_search_chat1(index_name, search_vector, k, cb_coll,query):
  print("query :",query)

  args = {"index_name":index_name, "search_vector":search_vector,"k":k,"query":query,"couchbase_url":COUCHBASE_URL}
  
  curl_command = """
          
  curl -XPOST -H "Content-Type: application/json" -u Administrator:cbaapsecure \
  http://{couchbase_url}:8094/api/bucket/b1/scope/s1/index/{index_name}/query  \
  -d '{{
    "query": {{
      "query":"{query}"
    }},
    "size": 6,
    "knn": [
      {{
        "field": "vector_data",
        "k": {k},
        "vector":{search_vector}
      }}
    ],
    "from": 0
  }}'
  """.format(**args)

  try:
    print(curl_command)
    similar_chunks = ""
    result = subprocess.run(curl_command, shell=True, check=True,stdout=subprocess.PIPE)
    print("Context chunks retrieved successfully")
    a = result.stdout
    string_data = a.decode('utf-8')
    json_data = json.loads(string_data)
    print(json_data)
    c = json_data['hits']
    for i in c:
      docid = i['id']
      try:
          result = cb_coll.get(docid)
          data = result.value['data']
          similar_chunks += data
      except Exception as e:
          print(e)
      
  except subprocess.CalledProcessError as e:
      print(f"Error executing curl command: {e}")
    
  return similar_chunks



  
def vector_search_chat(index_name, search_vector, k, cb_coll):
  args = {"index_name":index_name, "search_vector":search_vector,"k":k,"couchbase_url":COUCHBASE_URL}
  curl_command = """
          
  curl -XPOST -H "Content-Type: application/json" -u Administrator:cbaapsecure \
  http://54.226.22.243:8094/api/bucket/b1/scope/s1/index/test11/query \
  -d '{{
    "query": {{
      "match_none": {{}}
    }},
    "explain": true,
    "knn": [
      {{
        "field": "vector_data",
        "k": {k},
        "vector":{search_vector}
      }}
    ],
    "size": 10,
    "from": 0
  }}'
  """.format(**args)

  # Execute the curl command using subprocess
  try:
      similar_chunks = ""
      result = subprocess.run(curl_command, shell=True, check=True,stdout=subprocess.PIPE)
      print("Context chunks retrieved successfully")
      a = result.stdout
      print(curl_command)
      print(a)
      string_data = a.decode('utf-8')
      json_data = json.loads(string_data)
      c = json_data['hits']
      for i in c:
        docid = i['id']
        try:
            result = cb_coll.get(docid)
            data = result.value['data']
            similar_chunks += data
        except Exception as e:
            print(e)
      
  except subprocess.CalledProcessError as e:
      print(f"Error executing curl command: {e}")
    
  return similar_chunks



# import requests

# def vector_search_chat(index_name, search_vector, k, cb_coll):
#   similar_chunks = ""
#   try:
#       args = {"index_name":index_name, "search_vector":search_vector,"k":k}
#       curl_command = """
              
#       curl -XPOST -H "Content-Type: application/json" -u Administrator:password \
#       http://172.23.108.107:8094/api/index/{index_name}/query \
#       -d '{{
#         "query": {{
#           "match_none": {{}}
#         }},
#         "explain": true,
#         "knn": [
#           {{
#             "field": "vector_data",
#             "k": {k},
#             "vector":{search_vector}
#           }}
#         ],
#         "size": 10,
#         "from": 0
#       }}'
#       """.format(**args)
#       result = requests.get(curl_command)  # Assuming curl_command is a valid URL
#       result.raise_for_status()  # Raise an exception for non-2xx responses
#       print("Context chunks retrieved successfully")
      
#       json_data = result.json()
#       for hit in json_data.get('hits', []):
#           docid = hit.get('id')
#           if docid:
#               try:
#                   result = cb_coll.get(docid)
#                   data = result.value.get('data')
#                   if data:
#                       similar_chunks += data
#               except Exception as e:
#                   print(f"Error retrieving document {docid}: {e}")
#   except requests.RequestException as e:
#       print(f"Error retrieving context chunks: {e}")

#   return similar_chunks





def vector_search_chat2(username,password,index_name, host, bucket, scope, collection, dimensions, field,query,search_vector,cb_coll):

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
    "type_string":f"{scope}.{collection}",
    "query":query,
    "search_vector":search_vector
  }
  curl_command = """
          
  curl -XPOST -H "Content-Type: application/json" -u {username}:{password} \
  http://{host}:8094/api/bucket/{bucket}/scope/{scope}/index/{index_name}/query  \
  -d '{{
    "query": {{
      "query":"{query}"
    }},
    "size": 6,
    "knn": [
      {{
        "field": "vector_data",
        "k": 6,
        "vector":{search_vector}
      }}
    ],
    "from": 0
  }}'
  """.format(**args)

  try:
    print(curl_command)
    similar_chunks = ""
    result = subprocess.run(curl_command, shell=True, check=True,stdout=subprocess.PIPE)
    print("Context chunks retrieved successfully")
    a = result.stdout
    string_data = a.decode('utf-8')
    json_data = json.loads(string_data)
    print(json_data)
    c = json_data['hits']
    for i in c:
      docid = i['id']
      try:
          result = cb_coll.get(docid)
          data = result.value['data']
          similar_chunks += data
      except Exception as e:
          print(e)
      
  except subprocess.CalledProcessError as e:
      print(f"Error executing curl command: {e}")
    
  return similar_chunks
