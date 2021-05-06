import socket

class Flask:
    def __init__(self,import_name):#done simply to match flask
        self.import_name = import_name
        self.paths = {}

    def route(self,path):#the @app.route decorator
        def inner(func): #basic decorator structure/closure
            #remove variable names from paths to make it easier to match against later
            cleaned_path = "/".join(['<>' if var and var[0] == '<' and var[-1] == '>' else var for var in path.split("/")])
            self.paths[cleaned_path] = func #store paths and functions associated with in in a dict
            return func #return function to allow chaining decorators
        return inner

    def match_url(self,url):
        for path in self.paths:#loop over all stored paths
            variables = []
            if path == url:#if find a match exit the loop early
                return path,variables
            path_split = path.split("/")[1:]
            url_split = url.split("/")[1:]
            if len(path_split) == len(url_split):
                for a,b in zip(path_split,url_split):
                    if a == b:
                        continue
                    elif a != "<>":
                        break
                    variables.append(b)
                else:
                    return path,variables
        return None,variables

    def run(self,host='127.0.0.1',port=5000,debug=False):
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
                response = self.paths[match](*variables)
                test = f"HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{response}\n"
                client.sendall(test.encode('utf-8'))
            else:
                test = f"HTTP/1.1 404 ERR\nContent-Type: text/plain\n\n404 not found\n"
                client.sendall(test.encode('utf-8'))
            client.close()