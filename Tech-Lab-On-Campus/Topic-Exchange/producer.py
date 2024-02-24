
from stock import Stock  # pylint: disable=import-error
import sys
import os
import argparse
import pika

class mqProducer:
    def __init__(self, exchange_name: str) -> None:
        # Save parameters to class variables
        self.exchange_name = exchange_name

        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        connection = pika.BlockingConnection(parameters=conParams)
        
        # Establish Channel
        self.channel = connection.channel()

        # Create the topic exchange if not already present
        self.channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    def publishOrder(self, sector: str, stock: Stock) -> None:
        stock_name = stock.get_name()
        stock_price = stock.get_price

        # Create Appropiate Topic String
        topic_string = "Stock." + stock_name + "." + sector

        # Send serialized message or String
        body = stock.serialize()

        # Print Confirmation
        print("Published order: " + body)

        # Close channel and connection
        self.channel.close()

def main() -> None:
    parser = argparse.ArgumentParser(description='Producer argument parser')
    parser.add_argument('--ticker', '-t', help='Ticker')
    parser.add_argument('--price', '-p', help='Price')
    parser.add_argument('--sector', '-s', help='Sector')

    args = parser.parse_args()
    print(args)
    ticker = args.ticker
    price = args.price
    sector = args.sector
    producer = mqProducer(exchange_name="Tech Lab Exchange")
    stock = Stock(ticker, price)
    producer.publishOrder(sector, stock)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
