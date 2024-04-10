# from llama_cpp import Llama
# import logging
import ollama
# def query_enhancer(context,query):

#       if(len(context)>9600):
#             context = context[:9500]

#       llm = Llama(
#             model_path='/Users/nishanth/local_finetune/vector_search_project/mistral-7b-openorca.Q4_0.gguf',
#             n_ctx=10000,
#       )
#       output = llm(
#             f"Q: plot of the movie is {context} .Query: {query} . Now enhance this query and give a detailed specific query using the above plot as context. The purpose of this is, I can feed the query to a text to image LLM. Since those models require very specific details, Give a query which is not so long or has more adjectives. Instead focus on the details and the scenario. A:", # Prompt
#             max_tokens=None,
#       )
#       print(str(output['choices'][0]['text']))
#       return str(output['choices'][0]['text'])

def query_enhancer(context,query): 
      response = ollama.chat(model='mistral:latest',messages = [
      {"role": "system", "content": "enhance this query and give a detailed specific query using the above plot as context. The purpose of this is, I can feed the query to a text to image LLM. Since those models require very specific details, Give a query which is not so long or has more adjectives. Instead focus on the details and the scenario.Answer in less than 50 words."},
      {"role": "user", "content": f"Plot of the movie is {context} .Query: {query} .A:"},
      ])
      bot_response = response['message']['content']

      print(bot_response)
      return bot_response