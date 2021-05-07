import socket
from typing import Callable, List, Optional, Tuple

class Flask:
    def __init__(self,import_name:str):#done simply to match flask
        self.import_name = import_name
        self.paths = {}

    def route(self,path:str) -> Callable:#the @app.route decorator
        def inner(func:Callable) -> Callable: #basic decorator structure/closure
            keys = []
            for var in path.split("/"):#get variable names from paths to pass in as kwargs later
                if var and var[0] == "<" and var[-1] == ">":
                    keys.append(var[1:-1])
            self.paths[path] = keys,func#store paths and functions associated with in in a dict
            return func #return function to allow chaining decorators
        return inner

    def match_url(self,url:str) -> Tuple[Optional[str],List]:
        for path in self.paths:#loop over all stored paths
            variables = []
            if path == url:#if find a match exit the loop early
                return path,variables
            path_split = path.split("/")[1:]
            url_split = url.split("/")[1:]
            if len(path_split) == len(url_split):
                for a,b in zip(path_split,url_split):
                    if a and a[0] != "<" and a[-1] != ">":
                        break
                    elif a != b:
                        variables.append(b)
                else:
                    return path,variables
        return None,variables

    def run(self,host:str='127.0.0.1',port:int=5000,debug:bool=False) -> None:
        if debug:
            print("running in debug mode")
        server = socket.socket()
        server.bind((host,port))
        server.listen(5)
        print("listening on port: ",port)
        while True:
            client,address = server.accept()
            data = client.recv(1024).decode()
            if len(data) < 1:
                break
            match,variables = self.match_url(data.split(" ")[1])
            if match:
                keys,func = self.paths[match]
                response = func(**dict(zip(keys,variables)))
                test = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{response}\n"
                client.sendall(test.encode('utf-8'))
            else:
                test = f"HTTP/1.1 404 ERR\nContent-Type: text/plain\n\n404 not found\n"
                client.sendall(test.encode('utf-8'))
            client.close()