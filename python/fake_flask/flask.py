import socket#builtin library for creating websockets
import os#builtin library for navigating os filestructure
from typing import Any, Callable, Dict, List, Optional, Tuple#builtin library used for type hints, doesn't actually affect functionality

#TODO maybe make this a class attribute?
TYPES = {
    "int" : lambda x : int(x) if x.isdigit() else None,
    "string" : lambda x : x if not x.isdigit() else None,
}

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

#TODO refactor implementation
class Request:
    def __init__(self):
        self.method = None
        self.url = None
        self.protocol = None
        self.form = {}

request = Request()

class Flask:
    def __init__(self,import_name:str) -> None:#constructor function
        self.import_name = import_name#currently not used
        self.paths = {}#dict to keep track of registered paths

    def route(self,path:str,methods:List[str] = ["GET"]) -> Callable:#create the @app.route decorator
        def register(func:Callable) -> Callable:#func is the function below the decorator
            self.paths[path] = methods,func#store path as dict key and function as value
            return func #return func to allow chaining decorators (assign multiple routes to a single function)
        return register

    def match_url(self,method:str,url:str) -> Tuple[Optional[str],Dict]:
        for path in self.paths:#loop over all stored paths
            if method not in self.paths[path][0]:
                continue
            kwargs = {}
            if path == url:#if find a match exit the loop early
                return path,kwargs#return matched path and variables from url
            path_split = path.split("/")[1:]#split path into array and remove the first empty space character
            url_split = url.split("/")[1:]#split url into array and remove the first empty space character
            if len(path_split) == len(url_split):#check if the lengths of the arrays are the same, if they aren't then keep looking
                for a,b in zip(path_split,url_split):
                    if a != b:#check if strings match and are not empty
                        if a == "" or a[0] != "<" and a[-1] != ">":#check if string is a variable or not
                            break#break early and move on to next path
                        clean_a = a[1:-1]#remove <> from string
                        if ":" in a:#check to see if variable has been type cast
                            var_type,var_name = clean_a.split(":")#split parameter into the type and the name
                            res = TYPES[var_type](b)#pass variable into converter function for its type
                            if not res:#break if types don't match
                                break
                            kwargs[var_name] = res#store parsed variable and name as key word arguments
                        else:
                            kwargs[clean_a] = b#store variable and name as key word arguments
                else:#runs if loop completes without breaking
                    return path,kwargs#return matched path and variables from url as key word arguments in a tuple
        return None,kwargs#no matching path

    #TODO refactor, there's definitely a better way to do this...
    @staticmethod
    def process_req(req:str) -> None:
        global request#global so can import into server
        req_split = req.split('\r\n')#remove new line characters
        method,url,protocol = req_split[0].split(" ")#parse first line
        #TODO parse the rest of the request string
        if method == "POST":
            for s in req_split[-1].split("&"):#parse form data
                a,b = s.split("=")
                request.form[a] = b
        #store values in request object
        request.method = method
        request.url = url
        request.protocol = protocol

    #TODO maybe implement threading
    def run(self,host:str='127.0.0.1',port:int=5000,debug:bool=False) -> None:
        if debug:#currently does nothing but print this message
            print("running in debug mode")
        server = socket.socket()#create socket connection
        server.bind((host,port))#bind socket to port
        server.listen(5)#have socket listen for requests on given port
        print("listening on port: ",port)
        while True:#infinitely loop to check for connections
            client,address = server.accept()#recieve client socket and ip address they connected with
            req = client.recv(1024).decode()#recieve request from client and decode byte string
            if len(req) < 1:#break if no data recieved
                print("shutting down server")
                break
            method,url = req.split(" ")[0:2]#pull requested method and url from request string
            self.process_req(req)#process req and store data into request object
            match,kwargs = self.match_url(method,url)#lookup requested url and return matching path and key word arguments associated with it
            if match:#if match was found
                response = self.paths[match][1](**kwargs)#pass key word arguments into associated function and get return value
                byte_str = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response}\n"#pass response into string to send back to client (browser)
                client.sendall(byte_str.encode('utf-8'))#encode to byte string and send to client 
            else:
                byte_str = f"HTTP/1.1 404 ERR\nContent-Type: text/html\n\n404 not found\n"#error string if no match found
                client.sendall(byte_str.encode('utf-8'))#encode and send error string to client
            client.close()#clean up connection to client

def render_template(file:str, **kwargs:Any) -> str:
    with open(os.path.join(BASE_DIR,f"templates/{file}"),"r",encoding="utf-8") as f:
        #TODO parse html file and look for {{}} and compare strings to keys in kwargs, replacing the {{}} with any values for matching keys
        #TODO parse html file and perform any template logic required (if statements and for loops), returning a new processed html str to be sent to the client
        parsed_html = f.read()
        return parsed_html

#TODO functionality
def redirect(path:str) -> str:
    pass