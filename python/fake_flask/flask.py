import socket

class Flask:
    def __init__(self,import_name):
        self.import_name = import_name
        self.paths = {}

    def route(self,path):
        def inner(func):
            cleaned_path = "/".join(['<>' if var and var[0] == '<' and var[-1] == '>' else var for var in path.split("/")])
            self.paths[cleaned_path] = func
            return func
        return inner

    def match_url(self,path):
        for p in self.paths:
            variables = []
            path_split = path.split('/')
            p_split = p.split('/')
            if len(path_split) == len(p_split):
                for i in range(len(path_split)):
                    if path_split[i] != p_split[i]:
                        if p_split[i] != "<>":
                            break
                        variables.append(path_split[i])
                else:
                    return p,variables
        return False,variables

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
                test = f"HTTP/1.1 404 ERR\nContent-Type: text/plain\n\nError\n"
                client.sendall(test.encode('utf-8'))
            client.close()