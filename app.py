from dependencies import *

import os
import subprocess
import shutil
import re


# Global variable to determine the redirect route
registration_status = 0


app = Flask(__name__)
app.secret_key = "hmm"


embed_model = SentenceTransformer('BAAI/bge-m3')
embed_model_i = SentenceTransformer('paraphrase-MiniLM-L6-v2')

cb_coll,db_coll,eb_coll,rb_coll,architect_coll = couchbase_init()
kb,cb,ab_coll,us,c_coll,watch_coll= couchbase_init1()

session_coll,user_info, session_list_coll, session_list_a_coll, session_list_new_coll  = couchbase_init_local()



ALLOWED_EXTENSIONS = {'pdf'}

def setter():
    global registration_status
    with open('register_check.txt', 'r') as file:
        content = file.read()
        if content[4] == 'e':
            registration_status = 1
        if content[4] == 'g':
            registration_status = 2

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += multiline_to_single_conv(page.extract_text())
    return text





def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # remove the file
                print(f"File '{filename}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")



#imagine
def call_helper(movie_name,query,text_to_image):
    main.driver_function(movie_name, query,text_to_image,embed_model,f'/static/output')


@app.route('/')
def index():
    global registration_status
   
    setter()
    if registration_status == 1:
        return redirect('/register')
    elif registration_status == 2:
        return redirect('/dashboard')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(email)
        print(password)

        with open('register_check.txt', 'w') as file:
            file.write("dontgditthistext")

        user_info.upsert(email, "0")

        with open('user_config.txt', 'w') as file:
            content = email
            file.write(content)

        return redirect('/dashboard')
    return render_template('register.html')




@app.route('/dashboard',methods=['GET'])
def dashboard():
    with open('user_config.txt', 'r') as file:
        email = file.read()
                
    result = user_info.get(str(email))
    res = result.content_as[str]
    session["email"] = email
    if(res=="1"):
        ress = user_info.get(str(email) + ":session_data")
        value  = ress.content_as[str]
        data = json.loads(value)
        
        
        session["app_name"] = data.get("app_name")
        session["couchbase_host_type"] = data.get("couchbase_host_type")
        session["username"] = data.get("username")
        session["password"] = data.get("password")
        session["bucket_name"] = data.get("bucket_name")
        session["scope_name"] = data.get("scope_name")
        session["collection_name"] = data.get("collection_name")
        session["ip_addr"] = data.get("ip_addr")
        session["index_name"] = data.get("index_name")
        session["embedding_model"] = data.get("embedding_model")
        session["model_name"] = data.get("model_name")
        session["context"] = data.get("context")
        session["iteration_count"] = data.get("iteration_count")
        session["ollama_name"] = data.get("ollama_name")
        session["quantize_level"] = data.get("quantize_level")


        new_article_data = {
        "id": session["email"],
        "image_src": "static/dashpics/dochat.png",
        "title": session["app_name"],
        "description": f'custom chatbot hosted as {session["couchbase_host_type"]} with embedder {session["embedding_model"]}',
        "link": "/doc_chat_new"
        }
        

        return render_template('dashboard_new.html',new_article=new_article_data)

    else:
        session['session_no'] = 1
        session['session_name'] = "session" + str(session['session_no'])

        session['session_no_a'] = 1
        session['session_name_a'] = "session" + str(session['session_no_a'])

        session['session_no_new'] = 1
        session['session_name_new'] = "session" + str(session['session_no_new'])


        session['history'] = ""
        session['history_list'] = []

        session['history_a'] = ""
        session['history_list_a'] = []

        session['history_new'] = ""
        session['history_list_new'] = []



        session['couchbase_host_type'] = None
        session['username']=None
        session['password']=None
        session['bucket_name']=None
        session['scope_name']=None
        session['collection_name']=None
        session['ip_addr']=None
        session['index_name']=None
        session['embedding_model']=None
        session['model_name']=None
        session['context']=None
        session['iteration_count'] =None
        session['cb_connect_var'] = None
        session['app_name'] = None
        return render_template('dashboard.html')


# app2 -------------------------------------------------------------------------------------

#doc-chat
@app.route('/doc_chat')
def launch_docchat():
    session_list = []
    
    try:
        user_mail = str(session['email'])
        query = f"SELECT RAW {{'key': META().id, 'data': a}} FROM session_array a WHERE META().id LIKE '{user_mail}:%'"
        inventory_scope = session_coll.scope('user_info')
        sql_query = query
        row_iter = inventory_scope.query(
            sql_query)
        for i in row_iter:
            print(i['key'])
            session_list.append(str(i['key'].split(":")[1]))

        session_list.sort()
        print(session_list)

        
        load_name  = session_list[-1]
        key = str(session['email']) + ":" + load_name
        result = session_list_coll.get(key)
        data = result.value
        session['history'] = str(data)
        session['history_list'] = data

        session['session_no'] = int(session_list[-1][7:])
        session['session_name'] = "session" + str(session['session_no'])


        return render_template('docchat_init.html',session_names= session_list,session_name_end = session_list[len(session_list)-1])
    except Exception as e:
        print(e)
        session_list = ["session1"]
        session["history"] = ""
        session["history_list"] = []
        session["session_no"] = 1
        session["session_name"] = "session1"
        return render_template('docchat_init.html',session_names= session_list,session_name_end = session_list[len(session_list)-1])



@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input")
    print(user_input)
    rag= request.form.get("rag")
    print(rag)
    rag = int(rag)


    if(rag==1):
    
        emb = embed_model.encode(user_input,normalize_embeddings=True)
        search_vector = emb.tolist()
        u_input = user_input.replace("\n", "")
        
        context = vector_search_chat1("cbdoc", search_vector, 6, cb_coll,u_input)
        start_time = time.time()

        context = multiline_to_single_conv(context)

        print(f"context : {context}")

        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='mistral:latest',messages = [
            {"role": "system", "content": "You are a helpful bot who reads context and conversation history and answers questions about them. Only use the context and conversation history to answer the question."},
            {"role": "user", "content": f"text :{context}. Conversation history:{session['history']}. QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            if(bot_response!=""):
                break

        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")

        session['history'] += f"Query: {user_input}. Your response:{bot_response}"
        session['history_list'].append({"user":user_input,"ai":bot_response})

        print(f"bot response : {bot_response}")

    else:
        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='mistral:latest',messages = [
            {"role": "system", "content": "You are a helpful bot who uses conversation history if needed and answers questions about them. Answer things only related to couchbase."},
            {"role": "user", "content": f"QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            if(bot_response!=""):
                break

        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")
        print("bot_response:",bot_response)

    return jsonify({"bot_response": bot_response})


#new session 
@app.route("/newsession", methods=["POST"])
def newsession():
    name = request.form.get("session_name")
    past = session['history_list']
    key = str(session['email']) + ":" + name
    result = session_list_coll.upsert(key, past)
    print(result.cas)


    session['history'] = ""
    session['history_list'] = []
    
    session_no = int(session['session_no'])
    
    print("name :",name)
    current = int(''.join(filter(str.isdigit, name)))
    print("current: ",current)
    new_val = max(current, session_no)
    print("newval:",new_val)


    new_val +=1
    session['session_no'] = new_val
    new_name = "session"+str(new_val)
    print(new_name)
    session['session_name'] = new_name
    return jsonify({"new_name":new_name})



#load session
@app.route("/loadsession", methods=["POST"])
def loadsession():
    # #log_cpu_mem_usage()
    session_no = int(session['session_no'])
    session_name  = session['session_name']

    name = request.form.get("session_name")
    past = session['history_list']
    key = str(session['email']) + ":" + session_name
    
    session_list_coll.upsert(key, past)

    key = str(session['email']) + ":" + name
    session_name = name
    result = session_list_coll.get(key)
    data = result.value

    session['history'] = str(data)
    session['history_list'] = data

    data  = json.dumps(data)
    return jsonify({"data":data})





#app3 ------------------------------------------------------------------------------------------------------------------
@app.route('/archi_chat')
def launch_docchat_a():

    session_list = []
    
    try:
        user_mail = str(session['mail'])
        query = f"SELECT RAW {{'key': META().id, 'data': a}} FROM session_array_a a WHERE META().id LIKE '{user_mail}:%'"
        inventory_scope = session_coll.scope('user_info')
        sql_query = query
        row_iter = inventory_scope.query(
            sql_query)
        for i in row_iter:
            print(i['key'])
            session_list.append(str(i['key'].split(":")[1]))



        session_list.sort()
        print(session_list)

        
        load_name  = session_list[-1]
        key = str(session['mail']) + ":" + load_name
        result = session_list_a_coll.get(key)
        data = result.value
        session['history_a'] = str(data)
        session['history_list_a'] = data

        session['session_no_a'] = int(session_list[-1][7:])
        session['session_name_a'] = "session" + str(session['session_no_a'])


        return render_template('archichat_init.html',session_names= session_list,session_name_end = session_list[len(session_list)-1])
    except Exception as e:
        print(e)
        session_list = ["session1"]
        session["history_a"] = ""
        session["history_list_a"] = []
        session["session_no_a"] = 1
        session["session_name_a"] = "session1"
        return render_template('archichat_init.html',session_names= session_list,session_name_end = session_list[len(session_list)-1])




@app.route("/chat_a", methods=["POST"])

def chat_a():
    user_input = request.form.get("user_input")
    print(user_input)
    rag= request.form.get("rag")
    print(rag)
    rag = int(rag)


    if(rag==1):
     
        emb = embed_model.encode(user_input,normalize_embeddings=True)
        search_vector = emb.tolist()
        context = vector_search_chat1("cbarchitect", search_vector, 6, architect_coll,user_input)
        context = multiline_to_single_conv(context)

        print(f"context : {context}")
    
        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='mistral:latest',messages = [
            {"role": "system", "content": "You are a helpful bot who reads context and conversation history and answers questions about them. Answer precisely and in less than 50 words. Only use the context and conversation history to answer the question."},
            {"role": "user", "content": f"text :{context}. Conversation history:{session['history_a']}. QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            if(bot_response!=""):
                break
        # print(bot)
        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")

        session['history_a'] += f"Query: {user_input}. Your response:{bot_response}"
        session['history_list_a'].append({"user":user_input,"ai":bot_response})

        print("res:",bot_response)
    else:
        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='mistral:latest',messages = [
            {"role": "system", "content": "You are a helpful bot who uses conversation history if needed and answers questions about them. Answer things only related to couchbase."},
            {"role": "user", "content": f"QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            if(bot_response!=""):
                break

        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")
        print("res:",bot_response)
    

    return jsonify({"bot_response": bot_response})


#new session 
@app.route("/newsession_a", methods=["POST"])

def newsession_a():
    name = request.form.get("session_name")
    past = session['history_list_a']
    key = str(session['mail']) + ":" + name
    result = session_list_a_coll.upsert(key, past)
    print(result.cas)


    session['history_a'] = ""
    session['history_list_a'] = []
    
    session_no = int(session['session_no_a'])
    
    print("name :",name)
    current = int(''.join(filter(str.isdigit, name)))
    print("current: ",current)
    new_val = max(current, session_no)
    print("newval:",new_val)    


    new_val +=1
    session['session_no_a'] = new_val
    new_name = "session"+str(new_val)
    print(new_name)
    session['session_name_a'] = new_name
    return jsonify({"new_name":new_name})


#load session
@app.route("/loadsession_a", methods=["POST"])

def loadsession_a():

    session_no = int(session['session_no_a'])
    session_name  = session['session_name_a']

    name = request.form.get("session_name")
    past = session['history_list_a']
    key = str(session['mail']) + ":" + session_name
    
    session_list_a_coll.upsert(key, past)

    key = str(session['mail']) + ":" + name
    session_name = name
    result = session_list_a_coll.get(key)
    data = result.value

    session['history_a'] = str(data)
    session['history_list_a'] = data

    data  = json.dumps(data)
    return jsonify({"data":data})



#app5 --------------------------------------------------------------------------------------


@app.route('/finetune')
def finetune():
    return render_template('finetune.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    model_name = data.get('modelName')
    context = data.get('context')
    iteration_count = data.get('iterationCount')
    ollama_name = data.get('ollamaName')
    quantize_level = data.get('quantizeLevel')
    
    # Process the received data as needed
    
    print("model", model_name)
    print(f"context : {context}")
    print(f"iteration count : {iteration_count}")
    print(f"preferred : {ollama_name}")
    print(f"quantization: {quantize_level}")
    
    # run_script('/Users/nishanth/test/uploaded_pdfs', 'plasma', "1", "nishu",'Q5_0','mistral 7B')
    a = run_script('uploaded_files_finetune', context, str(iteration_count),ollama_name,quantize_level,model_name)
    return "done"



@app.route('/upload_fine', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file_path = os.path.join('uploaded_pdfs', file.filename)
            file.save(file_path)
        return render_template('app_loader.html')
    

@app.route('/upload_finetune', methods=['POST'])
def upload_fine():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file_path = os.path.join('uploaded_files_finetune', file.filename)
            file.save(file_path)
        return render_template('app_loader.html')



@app.route('/download_i')    # return 'Data submitted successfully'
def download_direct():
    param1 = str(request.args.get('param1'))
    param2 = str(request.args.get('param2'))

    file_path = f'vector_search_project/fine_tuner/finetune{param1}/{param2}.gguf'
    print(file_path)

    return send_file(file_path, as_attachment=True)
    # return redirect(url_for('dashboard'))





#app6 --------------------------------------------------------------------------------------

@app.route('/create_app',methods=['GET'])
def create_app():
    return render_template('create_app.html')


@app.route('/create_app_inputs', methods=['POST'])
def create_app_inputs():
    data = request.json


    session['app_name'] = data.get('app_name')
    session['couchbase_host_type'] = data.get('host_type')
    session['username'] = data.get('username')
    session['password'] = data.get('password') 
    session['bucket_name'] = data.get('bucket')
    session['scope_name'] = data.get('scope')
    session['collection_name'] = data.get('collection')
    session['ip_addr'] = data.get('ip_addr')
    session['index_name'] = data.get('index_name')
    session['embedding_model'] = data.get('embedding_model')
    session['model_name'] = data.get('modelName')
    session['context'] = data.get('context')
    session['iteration_count'] = data.get('iterationCount')
    session['ollama_name'] = data.get('ollamaName')
    session['quantize_level'] = data.get('quantizeLevel')
    coll = connect2couchbase(session['username'], session['password'], session['bucket_name'], session['scope_name'], session['collection_name'], session['ip_addr'], timeout_seconds=5)
    session['coll'] = coll
    print(f'session coll : {session["coll"]}' )

    cb_connect_var = start_connection(session['username'], session['password'], session['bucket_name'], session['scope_name'], session['collection_name'], session['ip_addr'],session['couchbase_host_type'])
    cc = 1000
    while(cc!=0):
        file_list = os.listdir('uploaded_pdfs')
        if(file_list != []):
            print(f"dir : {file_list}")
            break
        time.sleep(1)

    time.sleep(3)
    for file in file_list:
        file = os.path.join('uploaded_pdfs', file)

        text = extract_text_from_pdf(file)
        print("Text extracted as:")
        print(text)

        title = file.split('.')[0]
        title = title.split('/')
        title = title[-1]
        print(title)

        chunked_text = chunk_text(text, title)
            
        if chunked_text:
            dimensions= embed(1, chunked_text, '_'.join(title.split()), cb_connect_var)
        

        print("Data upserted")

    ok = create_index_app(session['username'],session['password'],session['index_name'], session['ip_addr'], session['bucket_name'], session['scope_name'], session['collection_name'], 1024, field = "vector_data")
    with open('user_config.txt', 'r') as file:
        email = str(file.read())
    
    # session['email'] = email

    res = user_info.upsert(email, "1")


    session_data_push = {
    "app_name": session.get("app_name"),
    "couchbase_host_type": session.get("couchbase_host_type"),
    "username": session.get("username"),
    "password": session.get("password"),
    "bucket_name": session.get("bucket_name"),
    "scope_name": session.get("scope_name"),
    "collection_name": session.get("collection_name"),
    "ip_addr": session.get("ip_addr"),
    "index_name": session.get("index_name"),
    "embedding_model": session.get("embedding_model"),
    "model_name": session.get("model_name"),
    "context": session.get("context"),
    "iteration_count": session.get("iteration_count"),
    "ollama_name": session.get("ollama_name"),
    "quantize_level": session.get("quantize_level")
    }

    json_obj = json.dumps(session_data_push)
    ress= user_info.upsert(email+":session_data", json_obj)
    redirect_url = url_for('dashboard')
    return jsonify({'redirect_url': redirect_url})



@app.route('/doc_chat_new')
def launch_docchat_new():
    

    session_list = []
    
    try:
        user_mail = str(session['mail'])
        query = f"SELECT RAW {{'key': META().id, 'data': a}} FROM session_array_new a WHERE META().id LIKE '{user_mail}:%'"
        inventory_scope = session_coll.scope('user_info')
        sql_query = query
        row_iter = inventory_scope.query(
            sql_query)
        for i in row_iter:
            print(i['key'])
            session_list.append(str(i['key'].split(":")[1]))

        session_list.sort()
        print(session_list)

        
        load_name  = session_list[-1]
        key = str(session['mail']) + ":" + load_name
        result = session_list_new_coll.get(key)
        data = result.value
        session['history_new'] = str(data)
        session['history_list_new'] = data

        session['session_no_new'] = int(session_list[-1][7:])
        session['session_name_new'] = "session" + str(session['session_no_new'])


        return render_template('docchat_new.html',session_names= session_list,session_name_end = session_list[len(session_list)-1],app_name = session["app_name"])
    except Exception as e:
        print(e)
        session_list = ["session1"]
        session["history_new"] = ""
        session["history_list_new"] = []
        session["session_no_new"] = 1
        session["session_name_new"] = "session1"
        return render_template('docchat_new.html',session_names= session_list,session_name_end = session_list[len(session_list)-1],app_name = session["app_name"])


@app.route("/chat_new", methods=["POST"])
def chat_new():
    user_input = request.form.get("user_input")
    emb = embed_model.encode(user_input,normalize_embeddings=True)
    search_vector = emb.tolist()
    u_input = user_input.replace("\n", "")
    context_v = vector_search_chat2(session['username'],session['password'],session['index_name'], session['ip_addr'], session['bucket_name'], session['scope_name'], session['collection_name'], 1024, "vector_data",u_input,search_vector,connect2couchbase(session['username'], session['password'], session['bucket_name'], session['scope_name'], session['collection_name'], session['ip_addr'], timeout_seconds=5))
    context_v = multiline_to_single_conv(context_v)

    print(f"context : {context_v}")
    g  = 1
    bot_response = ''
    while(g):
        g+=1
        if(g==5):
            bot_response = "Sorry! There is some problem with LLM. Try again!"
            break
        user_input = user_input + "Answer in short and precise."
        response = ollama.chat(model='mistral:latest',messages = [
        {"role": "system", "content": "You are a helpful bot who reads context and conversation history and answers questions about them.Answer precisely and in less than 50 words. Only use the context and conversation history to answer the question."},
        {"role": "user", "content": f"text :{context_v}. Conversation history:{session['history_new']}. QUESTION: {user_input}"},
        ])
        bot_response = response['message']['content']
        if(bot_response!=""):
            break
    
    bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
    bot_response = bot_response.replace("\n\n","\n")


    session['history_new'] += f"Query: {user_input}. Your response:{bot_response}"
    session['history_list_new'].append({"user":user_input,"ai":bot_response})
    print("history:",session['history_new'])
    print("his list:",session['history_list_new'])
    print("res:",bot_response)
    return jsonify({"bot_response": bot_response})



#new session 
@app.route("/newsession_new", methods=["POST"])
def newsession_new():
    name = request.form.get("session_name")
    past = session['history_list_new']
    key = str(session['mail']) + ":" + name
    result = session_list_new_coll.upsert(key, past)
    print(result.cas)


    session['history_new'] = ""
    session['history_list_new'] = []
    
    session_no = int(session['session_no_new'])
    
    print("name :",name)
    current = int(''.join(filter(str.isdigit, name)))
    print("current: ",current)
    new_val = max(current, session_no)
    print("newval:",new_val)    


    new_val +=1
    session['session_no_new'] = new_val
    new_name = "session"+str(new_val)
    print(new_name)
    session['session_name_new'] = new_name
    return jsonify({"new_name":new_name})


#load session
@app.route("/loadsession_new", methods=["POST"])

def loadsession_new():

    session_no = int(session['session_no_new'])
    session_name  = session['session_name_new']

    name = request.form.get("session_name")
    past = session['history_list_new']
    key = str(session['mail']) + ":" + session_name
    
    session_list_new_coll.upsert(key, past)

    key = str(session['mail']) + ":" + name
    session_name = name
    result = session_list_new_coll.get(key)
    data = result.value

    session['history_new'] = str(data)
    session['history_list_new'] = data

    data  = json.dumps(data)
    return jsonify({"data":data})


#app1 -------------------------------------------------------------------------

@app.route('/create', methods=['POST'])
def run_task():
    movie_name = request.form.get('movie_name')
    query = request.form.get('query')
    query_enhancer = request.form.get('queryEnhancer')
    text_to_image = request.form.get('textToImage')
    quality = request.form.get('quality')

    path_var = ""
    if(text_to_image == "Stable diffusion X"):
        path_var = "sd"
    else:
        path_var = text_to_image.lower()


    print("movie:",movie_name)
    print("query:",query)
    print("query_enhancer:",query_enhancer)
    print("texttoim:",text_to_image)
    print("quality:",quality)

    session["file_name"] = path_var

    task_thread = threading.Thread(target=call_helper(movie_name,query,text_to_image))
    task_thread.start()
    return render_template('movie_result.html',path  = f'static/output/{path_var}.png')


@app.route('/create')

def create():
    return render_template('movie.html')


@app.route('/download_files', methods=['GET'])
def download_files():
    directory = './static/output/'
    file_names = [session['file_name']]
    memory_file = zipfile.ZipFile('files.zip', 'w', zipfile.ZIP_DEFLATED)

    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            memory_file.write(file_path, file_name)

    memory_file.close()
    return send_file('files.zip', as_attachment=True)





@app.route('/process_form', methods=['POST'])
def process_form():
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')

    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join('upload_raggen', filename))
            
    # Get form data
    username = request.form['username']
    password = request.form['password']
    bucket_name = request.form['bucket_name']
    scope_name = request.form['scope_name']
    collection_name = request.form['collection_name']
    host = request.form['host']
    # fts_node = request.form['fts_node']
    index_name = request.form['index_name']
    embedding_model = request.form['embedding_model']
    print(username, password, bucket_name, scope_name, collection_name, host, embedding_model)

    # Connect to Couchbase
    cb_coll = connect2couchbase(username, password, bucket_name, scope_name, collection_name, host, timeout_seconds=5)
    print("Connection worked out")

    # Get files from the form
    upload_dir = 'upload_raggen'

    # Process each file
    for filename in os.listdir(upload_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(upload_dir, filename)
            
            # Process PDF file
            text = extract_text_from_pdf(file_path)
            print("Text extracted as:")
            print(text)

            title = os.path.splitext(filename)[0]
            print(title)

            # Chunking
            chunked_text = chunk_text(text, title)

            # Embedding the chunks using the selected model
            if chunked_text:
                if embedding_model == 'BAAI/bge-m3':
                    # Embed using BAAI/bge-m3
                    dimensions = embed(1, chunked_text, title, cb_coll)
                elif embedding_model == 'paraphrase-MiniLM-L6-v':
                    # Embed using paraphrase-MiniLM-L6-v
                    dimensions = embed(0, chunked_text, title, cb_coll)
                else:
                    return "Invalid embedding model selected!"
                
                print("Data upserted, check once")

    # Vector index creation
    ok = create_index(index_name, host, bucket_name, scope_name, collection_name, dimensions, field="vector_data")

    print("Processing completed successfully!")

    return redirect(url_for('acknowledgement'))


@app.route('/process_form')
def raggen():
    clear_directory('upload_raggen')
    return render_template('raggen.html')

@app.route('/acknowledgement')

def acknowledgement():
    return render_template('acknowledgement.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5100)


