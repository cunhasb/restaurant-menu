from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import pdb


class ServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/home'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                output = ""
                output += '<html><body>Hello from Python</html></body>'

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_response(404)
            self.send_header('Content_type', 'text/html')
            self.end_headers()
            output = ""
            output += '<html><body>This is embarrassing, I could not find this page!</html></body>'
            print '404, This is embarrassing, I could not find this page! File not Found %s - ' % self.path
            send_error(404, 'File not Found %s' % self.path)


def main():
    try:
        port = 3000
        server = HTTPServer(('', port), ServerRequestHandler)
        print 'Web Server running on port %s' % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^c entered, Shutting down Server..."
        server.socket.close()


if __name__ == '__main__':

    main()
