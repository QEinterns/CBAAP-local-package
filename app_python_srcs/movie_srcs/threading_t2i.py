import threading
from app_python_srcs.movie_srcs.opendalle import opendalle
from app_python_srcs.movie_srcs.openjourney import openjourney
from app_python_srcs.movie_srcs.playground import playground
from app_python_srcs.movie_srcs.proteus import proteus
from app_python_srcs.movie_srcs.t2i_SD1 import t2i_SD1

def threadit(enhanced_query,text_to_image,path):
    model_name = "" 
    if(text_to_image=="Stable diffusion X"):
        t2i_SD1(enhanced_query)
    elif(text_to_image=="Proteus"):
        proteus(enhanced_query)
    elif(text_to_image=="Playground"):
        playground(enhanced_query)
    else:
        opendalle(enhanced_query)

    return 1    
