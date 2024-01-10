import socket


class TCPServer:
    def __init__(self, host="127.0.0.1", port=7249):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET = AddressFamily.Ipv4
        # SOCK_STREAM = TCP Socket
        s.bind((self.host, self.port))
        # connect to the port and take it.
        s.listen(5)
        # listen to up to 5 connections. Refuse any more than that.
        while True:
            # accept any new connection
            conn, addr = s.accept()
            # read the data sent by the client
            data = conn.recv(1024)
            # expose handle_request function for server to enter.
            response = self.handle_request(data)
            # send back the data to client
            conn.sendall(response)
            # close the connection
            conn.close()

    def handle_request(self, data):
        '''Implement in Subclass'''
        raise NotImplementedError

class HTTPServer(TCPServer):
    def __init__(self):
        super().__init__()    
        self.methods = ["POST", "GET"]
        self.status_codes = {
            '200': "OK",
            '400': "Bad Request",
            '406': "Method Not Allowed",
            '501': "Not Implemented"
        }

    def handle_request(self, data):
        request = HTTPRequest(data)
        response_line = b"HTTP/1.1 200 OK\r\n"

        blank_line = b"\r\n"

        response_body = b"Request received!"

        return b"".join([response_line, blank_line, response_body])

class HTTPRequest:
    def __init__(self, request):
        self.raw_request = request
        self._parse()
        self.method = ""
        self.uri = ""
        self.protocol = ""
        self.headers = {}
        self.data = ""

    def _parse(self):
        data = self.raw_request.split(b"\r\n")
        # Request Line. RFC 5.1
        request_line = data[0].split(b" ")
        print(request_line)
        self.method = str(request_line[0])
        self.uri = str(request_line[1])
        self.protocol = str(request_line[2])

    def __str__(self):
        return f'''
        METHOD: {self.method}
        URI: {self.uri}
        DATA: {self.data}
        '''
if __name__ == "__main__":
    server = HTTPServer()
    server.start()
