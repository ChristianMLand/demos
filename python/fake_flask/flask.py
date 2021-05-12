import socket#builtin library for creating websockets
import os#builtin library for navigating os filestructure
from urllib.parse import unquote_plus
from typing import Any, Callable, Dict, List, Optional, Tuple#builtin library used for type hints, doesn't actually affect functionality

class Request:
    def __init__(self):
        self.client = None
        self.method = None
        self.url = None
        self.protocol = None
        self.address = None
        self.form = {}

request = Request()#TODO there has to be a better way of implementing the request object...

class Flask:
    TYPES = {
        "int" : lambda x : int(x) if x.isdigit() else None,
        "string" : lambda x : unquote_plus(x) if not x.isdigit() else None,#TODO str should be able to contain any characters other than slashes
        "float" : lambda x : float(x) if x.isdigit() or x.replace('.', '', 1).isdigit() else None,
        #TODO path type (slug formatted strings and can include slashes)
    }

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    def __init__(self,import_name:str) -> None:#constructor function
        self.import_name = import_name#currently not used
        self.paths = {}#dict to keep track of registered paths

    def route(self,path:str,methods:List[str] = ["GET"]) -> Callable:#create the @app.route decorator
        def register(func:Callable) -> Callable:#func is the function below the decorator
            self.paths[(path,*methods)] = func#store path as dict key and function as value
            return func #return func to allow chaining decorators (assign multiple routes to a single function)
        return register

    def match_url(self,method:str,url:str) -> Tuple[Optional[str],Dict]:
        for key in self.paths:#loop over all stored paths
            path,*methods = key#destructure key containing path and methods
            if method not in methods:#if methods don't match move on to next key
                continue
            if path == url:#if find a match then return early
                return self.paths[key]()#return response returned from matched path's function
            kwargs = {}#if a potential match exists at this point then it must have variables in its path
            path_split,url_split = path.split("/"),url.split("/")#split path into array
            if len(path_split) == len(url_split):#check if the lengths of the arrays are the same, if they aren't then keep looking
                for i in range(1,len(path_split)):
                    a,b = path_split[i],url_split[i]
                    if a != b:#check if strings match and are not empty
                        if not a or a[0] != "<" and a[-1] != ">":#check if string is a variable or not
                            break
                        if (a := a[1:-1]) and ":" in a:
                            var_type,var_name = a.split(":")
                            if var_type in Flask.TYPES:
                                a,b = var_name,Flask.TYPES[var_type](b)
                        kwargs[a] = b
                else:#runs if loop completes without breaking
                    return self.paths[key](**kwargs)#return response returned from matched path's function

    def run(self,host:str='127.0.0.1',port:int=5000,debug:bool=False) -> None:
        if debug:#currently does nothing but print this message
            print("running in debug mode")
        server = socket.socket()#create socket connection
        server.bind((host,port))#bind socket to port
        server.listen(5)#have socket listen for requests on given port
        print("listening on port: ",port)
        while True:#infinitely loop to check for connections
            client,address = server.accept()#recieve client socket and ip address they connected with
            data = client.recv(1024).decode()#recieve request from client and decode byte string
            if not data:#break if no data recieved
                print("shutting down server")
                break
            method,url = data.split(" ")[0:2]#pull requested method and url from request string
            global request
            request.client = client#store client connection in request object
            request.method = method#request method (http verb)
            request.url = url#requested url
            request.address = address#client ip address
            request.form = {}#any form data that was sent (reset to empty dict first)
            if method == "POST":
                for s in data.split('\r\n')[-1].split("&"):#parse form data
                    a,b = s.split("=")
                    request.form[a] = b
            response = self.match_url(method,url)#lookup requested url and return matching path and key word arguments associated with it
            if response:#if match was found
                byte_str = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\n{response}\r\n"#pass response into string to send back to client (browser)
                client.sendall(byte_str.encode('utf-8'))#encode to byte string and send to client 
            else:#TODO handle this better
                byte_str = f"HTTP/1.1 404 ERR\r\nContent-Type: text/html\r\nConnection: close\r\n\n<h1>404 not found</h1>\r\n"#error string if no match found
                client.sendall(byte_str.encode('utf-8'))#encode and send error string to client
            client.close()#clean up connection to client

def render_template(file:str, **kwargs:Any) -> str:
    with open(os.path.join(Flask.BASE_DIR,f"templates/{file}"),"r",encoding="utf-8") as f:
        parsed_html = f.read()
        return parsed_html

def redirect(path:str) -> str:
    global request
    request.client.sendall(f"HTTP/1.1 302 OK\r\nLocation: http://127.0.0.1:5000{path}\r\nConnection: close".encode('utf-8'))