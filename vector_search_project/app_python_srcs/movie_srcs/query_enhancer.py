from llama_cpp import Llama
import logging
import os



def query_enhancer(context,query,path):

      if(len(context)>9600):
            context = context[:9500]

      llm = Llama(
            model_path=path + "/mistral-7b-openorca.Q4_0.gguf",
            n_ctx=10000,
      )
      output = llm(
            f"Q: plot of the movie is {context} .Query: {query} . Now enhance this query and give a detailed specific query using the above plot as context. The purpose of this is, I can feed the query to a text to image LLM. Since those models require very specific details, Give a query which is not so long or has more adjectives. Instead focus on the details and the scenario. A:", # Prompt
            max_tokens=None,
      )
      print(str(output['choices'][0]['text']))
      return str(output['choices'][0]['text'])
