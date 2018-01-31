from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>Hello from Python!</body></html>'
                self.wfile.write(output)
                print output
                return

        except IOError:
            print '404, This is embarrassing, I could not find this page! File not Found %s - ' % self.path
            self.send_error(
                404, "This is embarrassing, I could not find this page! File not Found - File Not Found %s" % self.path)


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
