
import subprocess
import json


def vector_search_chat_f(index_name, search_vector, k, cb_coll,user_input,ip_addr):
  args = {"index_name":index_name, "search_vector":search_vector,"k":k,"ip":ip_addr}
  curl_command = """
          
  curl -XPOST -H "Content-Type: application/json" -u Administrator:password \
  http://3.88.163.135:8094/api/index/cloneapp/query \
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
