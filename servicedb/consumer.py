import logging
import os

import pika
import ujson
from aio_pika import connect_robust


def configure_logging():
    """Logging configuration for this file"""

    global logger

    logger = logging.getLogger("ConsumerLogger")
    log_handler = logging.StreamHandler()

    # Format will be: "INFO       [01.01.2022 12:00:00] TornadoLogger: Some Message"
    log_formatter = logging.Formatter(
        fmt="%(levelname) -10s [%(asctime)s] %(name) -15s: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S"
    )
    log_handler.setFormatter(log_formatter)

    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


class Consumer:
    LOGIN = os.environ.get('RABBITMQ_DEFAULT_USER', 'rabbit')
    PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS', 'mypassword')

    def __init__(self, process_callable):
        self._connection = None
        self._channel = None
        self._process_callable = process_callable

    async def consume(self, loop):
        """Connecting a queue listener"""

        connection = await connect_robust(
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            login=self.LOGIN,
            password=self.PASSWORD,
            port=5672,
            loop=loop
        )

        channel = await connection.channel()
        queue = await channel.declare_queue(os.environ.get('RABBITMQ_CONSUME_QUEUE', 'user_appeals'))

        await queue.consume(self.process_write_message_to_db, no_ack=False)

        logger.info("The queue is connected to the form")

        return connection

    async def process_write_message_to_db(self, message):
        await message.ack()

        body = message.body

        if body:
            logger.info(f"Received a message from the queue: {body}")

            self._process_callable(ujson.loads(body))

    def connect(self):
        credentials = pika.PlainCredentials(self.LOGIN, self.PASSWORD)
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get('RABBITMQ_HOST', 'localhost'),
                credentials=credentials,
                heartbeat=3600,
                connection_attempts=3,
                port=5672,
                virtual_host='/'
            )
        )
        self._channel = self._connection.channel()

    def run(self):
        configure_logging()

        logger.info("Connecting to RabbitMQ...")

        self.connect()

        logger.info("Connecting to RabbitMQ done")

    def disconnect(self):
        logger.info("Disconnecting from the queue...")

        self._connection.close()
