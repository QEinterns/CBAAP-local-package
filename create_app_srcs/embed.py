from json import JSONEncoder
from FlagEmbedding import BGEM3FlagModel
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import ast


class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)



def embed(flag, chunks, name, cb_coll):
    if flag:
        embed_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)
        dimensions = 1024

    else:
        embed_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        dimensions = 512

    docid_counter  = 1
    for sentence in chunks:
        if flag:
            emb = embed_model.encode(str(sentence.page_content), batch_size=12, max_length=600, )['dense_vecs']
        else:
            emb = embed_model.encode(str(sentence.page_content))


        embedding = np.array(emb)
        np.set_printoptions(suppress=True)

        json_dump =  json.dumps(embedding, cls=NumpyEncoder)
        document = { 
            "data":str(sentence.page_content),
            "vector_data":ast.literal_eval(json_dump)
        }
        
        docid = 'docid:' + str(name) + str(docid_counter)
        docid_counter+=1

        try:
            result = cb_coll.upsert(docid, document)
            print(result.cas)
        except Exception as e:
            print(e)
    
    return dimensions
        
        

