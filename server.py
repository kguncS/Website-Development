from bottle import route, run,debug,default_app, static_file, template, Bottle, request
from pathlib import Path
from hashlib import sha256
import os


userips = {}

def main():
    
    global userips
    client_ip = request.headers.get("X-Forwarded-For", "127.0.0.1") 
    if client_ip in userips.keys():
        userips[client_ip] +=1
    else:
        userips[client_ip]=1
    return template('index.html',deneme_ip=userips)

def create_hash(password):               
    pw_bytestring = password.encode()    
    return sha256(pw_bytestring).hexdigest()

def cleardic(filename):
    input_pw = request.forms.password
    hsh_pw = create_hash(input_pw)
    point=request.forms.get
    while True:
        if hsh_pw =="8929c0f591767b2c16ab468b2c9d17016e2412d5fbca15615eba36c80201c190":
            userips.clear()
            return template("pwreset.html")
            
        else:
            return template("pwcheck.html")

def html_static_files(file_name):
    return static_file(file_name, root="./")


def reader(file):
    return Path(file).read_text()



def create_app():
    app = Bottle()
    app.route("/", "GET", main)
    app.route("/<file_name:path>", "GET", html_static_files)
    app.route("/<file>", "GET", reader)
    app.route('/<filename>', 'POST',cleardic)
    app.route("/index.html","GET",main)

    
    return app

application = create_app()
application.run()
    
    #host="0.0.0.0",port=int(os.environ.get("PORT",8080))

