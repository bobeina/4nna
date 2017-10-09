#!/usr/bin/env python
#
# 测试一下websocket
#


import concurrent.futures
import pymongo
import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options



HOST = '192.168.0.111'
define("port", default=10010, help="run on the given port", type=int)

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/w", GameMessageDebugPageHandler),
            (r"/websocket", WebSocketHandler)
        ]
        settings = dict(
            website_title=u"山局座的野望",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            xsrf_cookies=False, # True
            cookie_secret="GD2mRmaZXE5fdUukVmERgWEDMMZ2n1VF9Qad31xwBr7fmvbQOFaRKtlVTA2TykAn",
            debug=True
        )
        super(Application, self).__init__(handlers, **settings)
        client = pymongo.MongoClient("mongodb://localhost")
        self.db = client.tgame


# class BaseHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         return self.application.db
#
#     def get_current_user(self):
#         user_id = self.get_secure_cookie("jar_user")
#
#         if not user_id:
#             return None
#         usernm = "".join([chr(x) for x in user_id])
#         user = self.application.db.recorders.find_one({'name': usernm})
#         return user
#
#     def any_author_exists(self):
#         one = self.db.recorders.find_one()
#         return bool(one)
#
#     def current_author_exists(self, username, email):
#         query = {
#             '$or': [
#                 {'name': {'$exists': True}},
#                 {'email': {'$exists': True}}
#             ]
#         }
#         one = self.db.recorders.find_one(query)
#         return bool(one)


class GameMessageDebugPageHandler(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    def get(self):
        # self.set_secure_cookie("scene", "your_home")
        self.render("debug.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        """
        设置场景
        :return:
        """
        self.uid = None
        self.write_message('Connection established.')

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        self.write_message('Bye.')
        pass

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
