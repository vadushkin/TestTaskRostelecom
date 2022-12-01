import logging
import uuid

import tornado.ioloop
import tornado.web
import ujson
from tornado.options import define, options

from publisher import Publisher


def configure_logging():
    """Logging configuration for this file"""

    global logger

    logger = logging.getLogger("TornadoLogger")
    log_handler = logging.StreamHandler()

    # Format will be: "INFO       [01.01.2022 12:00:00] TornadoLogger: Some Message"
    log_formatter = logging.Formatter(
        fmt="%(levelname) -10s [%(asctime)s] %(name) -15s: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S"
    )
    log_handler.setFormatter(log_formatter)

    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/appeal", AppealHandler),
        ]
        settings = dict(
            title="Form of appeals",
            cookie_secret=uuid.uuid4().int,
            xsrf_cookies=False,
            debug=False,
        )
        super(Application, self).__init__(handlers, **settings)


class AppealHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(AppealHandler, self).__init__(*args, **kwargs)

        self.set_header("Cache-Control",
                        "no-store, no-cache, must-   revalidate, max-age=0")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods",
                        "POST, GET, PUT, DELETE, OPTIONS")

    def options(self, *_):
        self.set_status(204)
        self.finish()

    async def post(self):
        logger.info("Getting data from a form...")

        data = ujson.loads(self.request.body)

        message = f"\nReceived data:" \
                  f"\n- FirstName: {data['first_name']}" \
                  f"\n- LastName: {data['last_name']}" \
                  f"\n- Patronymic: {data['patronymic']}" \
                  f"\n- Phone: {data['phone_number']}" \
                  f"\n- Message: {data['message']}"

        logger.info(msg=message)

        # added the message in the queue.
        publisher.publish(body=self.request.body)
        self.set_status(200)


def main():

    global publisher

    configure_logging()
    publisher = Publisher()

    try:
        publisher.run()

        app = Application()
        app.listen(options.port)

        tornado.ioloop.IOLoop.current().start()

    except (KeyboardInterrupt, Exception):
        publisher.disconnect()


if __name__ == "__main__":
    main()
