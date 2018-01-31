from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Hello from Python!<a href='/holla'>Spanish</a></h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/holla'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>&#161Hola de Python!<a href = '/hello'>Regressa a hello</a></h1></body></html>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            print '404, This is embarrassing, I could not find this page! File not Found %s - ' % self.path
            self.send_error(
                404, "This is embarrassing, I could not find this page! File not Found - File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2>Okay,how about this: </h2>"
            output += "<h1>%s</h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except IOError:
            pass


def main():
    try:
        port = 3000
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()

    except KeyboardInterrupt:
        print '^c entered, stopping web server...'
        server.socket.close()


if __name__ == '__main__':
    main()
