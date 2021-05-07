import socket#builtin library for creating websockets
from typing import Callable, Dict, List, Optional, Tuple#just used for type hints, doesn't actually affect functionality

class Flask:
    def __init__(self,import_name:str) -> None:#constructor function
        self.import_name = import_name#currently not used
        self.paths = {}#dict to keep track of registered paths

    def route(self,path:str) -> Callable:#the @app.route decorator
        def register(func:Callable) -> Callable:#basic decorator structure/closure
            self.paths[path] = func#store path as dict key and function as value
            return func #return func to allow chaining decorators
        return register

    def match_url(self,url:str) -> Tuple[Optional[str],Dict]:
        for path in self.paths:#loop over all stored paths
            kwargs = {}
            if path == url:#if find a match exit the loop early
                return path,kwargs#return matched path and variables from url
            path_split = path.split("/")[1:]#split path into array and remove the first empty space character
            url_split = url.split("/")[1:]#split url into array and remove the first empty space character
            if len(path_split) == len(url_split):#check if the lengths of the arrays are the same, if they aren't then keep looking
                for i in range(len(path_split)):
                    a,b = path_split[i],url_split[i]
                    if a != b:#check if strings match
                        if a[0] != "<" and a[-1] != ">":#check if string is a variable or not
                            break#break early and move on to next path
                        kwargs[a[1:-1]] = b#store variable and name as key word arguments
                else:#runs if loop completes without breaking
                    return path,kwargs#return matched path and variables from url
        return None,kwargs#no matching path

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
            if len(data) < 1:#break if no data recieved
                break
            match,kwargs = self.match_url(data.split(" ")[1])#recieve the matched path and variables associated with requested url
            if match:#if match was found
                response = self.paths[match](**kwargs)#pass key word arguments into associated function and get return value
                test = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{response}\n"#pass response into string to send back to client (browser)
                client.sendall(test.encode('utf-8'))#encode to byte string and send to client 
            else:
                test = f"HTTP/1.1 404 ERR\nContent-Type: text/plain\n\n404 not found\n"#error string if no match found
                client.sendall(test.encode('utf-8'))#send error string to client
            client.close()#clean up connection to client