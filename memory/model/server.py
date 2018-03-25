import logging.config
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from .application import application
from .settings import MODEL_SERVER_PORT, LOGGING

define("port", default=MODEL_SERVER_PORT,
       help="run on the given port", type=int)


def main():
    logging.config.dictConfig(LOGGING)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
