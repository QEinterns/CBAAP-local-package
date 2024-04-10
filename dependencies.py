from PyPDF2 import PdfReader
import nltk
nltk.download('punkt')
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
import ast
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from json import JSONEncoder
import logging










from flask import flash, Flask, render_template, jsonify, request, redirect,send_file,session, url_for
from connect import connect2couchbase
import json
import threading
import zipfile
from PyPDF2 import PdfReader
from m2s_converter import multiline_to_single_conv
from chunker import chunk_text
from embed import embed
from index import create_index
import os
from datetime import datetime
import ollama
import re
import time 
from flask_session import Session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sentence_transformers import SentenceTransformer


from app_python_srcs.vector_search_chat import vector_search_chat1,vector_search_chat,vector_search_chat2
from app_python_srcs.m2s_converter import multiline_to_single_conv
from app_python_srcs.couchbase_init import couchbase_init
from app_python_srcs.couchbase_init import couchbase_init1
import app_python_srcs.main as main

from flask import Flask, jsonify, render_template, request, send_file, redirect, url_for
import os
import json
import subprocess
from vector_search_project.automate import run_script
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename


from create_app_srcs.couchbase_connect import start_connection
from create_app_srcs.chunker import chunk_text
from create_app_srcs.embed import embed
from create_app_srcs.index import create_index
from updateindex import create_index_app

from app_python_srcs.couchbase_init_local import couchbase_init_local

