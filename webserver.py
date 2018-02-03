from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from crud_restaurant import RestaurantCrud
import cgi
import pdb


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            if self.path.endswith('/'):
                self.path = "/hello"

            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                restaurants = RestaurantCrud()
                # pdb.set_trace()

                output = ""
                output += "<html><body><h1>Hello from Python!<a href='/holla'>Spanish</a></h1>"
                output += "<h3 > <a href ='/new' > Create New Restaurant </a> </h3 >"
                for idx, el in enumerate(restaurants.read().all()):
                    output += (
                        "<li id=\"%s\">%s<a href=\"\edit\% s\"> Edit</a><a href=\"\delete\%s\"> Delete</a></li>" % (el.id, el.name, el.id, el.id))
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/holla'):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                restaurants = RestaurantCrud()

                output = ""
                output += "<html > <body > <h1 > &#161Hola de Python!< a href = '/hello' > Regressa a hello < /a > < / h1 >"
                output += "<h3 > <a href ='/new' > Nuevo Restaurant < /a > < / h3 >"
                output += "<ul>"
                for idx, el in enumerate(restaurants.read().all()):
                    output += (
                        "<li id=\"%s\">%s<a href=\"\edit\% s\"> Edit</a><a href=\"\delete\%s\"> Delete</a></li>" % (el.id, el.name, el.id, el.id))
                    output += "</ul>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Create</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/new'><input name='name'type='text' placeholder='Name'><input type ='submit' value='Create'></form>"
                output += "<a href='/hello'>Go Home</a></body></html>"
                self.wfile.write(output)
                return

            if [i for i in self.path.split("/") if i][0] == "edit":
                id = [i for i in self.path.split("/")if i][1]
                restaurant = RestaurantCrud("", id)
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Update</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/edit/%s'><input name='new_name'type='text' placeholder='Name' value='%s'><input type ='submit' value='Submit'></form>" % (
                    id, restaurant.find().name)
                output += "<a href='/hello'>Go Home</a></body></html>"
                self.wfile.write(output)
                return
                # pdb.set_trace()

            if [i for i in self.path.split("/")if i][0] == "delete":
                id = [i for i in self.path.split("/")if i][1]
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                restaurant = RestaurantCrud(id)
                output = ""
                output += "<html><h1>Are you sure you want to delete this item?</h1>"
                output += "<form method='POST' action='/delete/%s'></input><button type='submit'>Yes</button><button type='reset' formaction='/hello' >No</button></form></body></html>" % id
                self.wfile.write(output)
                return
                # pdb.set_trace()

        except IOError:
            print '404, This is embarrassing, I could not find this page! File not Found %s - ' % self.path
            self.send_error(
                404, "This is embarrassing, I could not find this page! File not Found - File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    # pdb.set_trace()
                    restaurant = RestaurantCrud(messagecontent[0])
                    response = restaurant.create()
                    print response

                    if response:
                        self.send_response(201)
                        self.end_headers()

                        output = ""
                        output += "<html><body><h1>Create</h1>"
                        output += "<form method = 'POST' enctype='multipart/form-data' action='/new'><input name='name'type='text' placeholder='Name'><input type ='submit' value='Submit'></form>"
                        output += "<a href='/hello'>Go Home</a></body></html>"
                        self.wfile.write(output)
                        return
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.send_header('Content_type', 'text/html')
                        output = ""
                        output += "<html><body><h1>Oops!!! Something Happened!</h1>"
                        output += "<a href='/hello'>Go Home</a></body></html>"
                        self.wfile.write(output)
                        return

            if [i for i in self.path.split("/") if i][0] == "edit":
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_name')
                    id = [i for i in self.path.split("/")if i][1]
                    restaurant = RestaurantCrud("", id)
                    response = restaurant.update(messagecontent[0])
                    print restaurant.name
                    # pdb.set_trace()
                    if response.name:
                        self.send_response(201)
                        self.end_headers()
                        output = ""
                        output += "<html><body><h1>Record Created sucessfully!</h1>"
                        output += '<h1>Update</h1>'
                        output += "<form method = 'POST' enctype='multipart/form-data' action='/edit/%s'><input name='name'type='text' placeholder='Name'><input type ='submit' value='Submit'></form>"
                        output += "<a href='/hello'>Go Home</a></body></html>"
                        self.wfile.write(output)
                        return
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.send_header('Content_type', 'text/html')
                        output = ""
                        output += "<html><body><h1>Oops!!! Something Happened!</h1>"
                        output += "<a href='/hello'>Go Home</a></body></html>"
                        self.wfile.write(output)
                        return

            if [i for i in self.path.split("/") if i][0] == "delete":
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                # if ctype == 'multipart/form-data':
                #     fields = cgi.parse_multipart(self.rfile, pdict)
                #     messagecontent = fields.get('delete')
                id = [i for i in self.path.split("/")if i][1]
                # pdb.set_trace()
                restaurant = RestaurantCrud("", id)
                response = restaurant.delete()
                # print restaurant.name
                # pdb.set_trace()
                if response:
                    self.send_response(200)
                    self.end_headers()
                    output = ""
                    output += "<html><body><h1>Record Deleted sucessfully!</h1>"
                    output += "<a href='/hello'>Go Home</a></body></html>"
                    self.wfile.write(output)
                    return
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.send_header('Content_type', 'text/html')
                    output = ""
                    output += "<html><body><h1>Oops!!! Something Happened!</h1>"
                    output += "<a href='/hello'>Go Home</a></body></html>"
                    self.wfile.write(output)
                    return

            self.send_response(301)
            self.end_headers()
            # pdb.set_trace()
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
