# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pika
import os
import json

class mqConsumer:
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        # Save parameters to class variables
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        self.con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=self.con_params)
        
        # Establish Channel
        self.channel = self.connection.channel()
        
        # Create Queue if not already present
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        
        # Create the exchange if not already present
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")
        
        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            exchange=self.exchange_name,
            queue=self.queue_name,
            routing_key=self.binding_key,
        )
        
        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_message_callback,
            auto_ack=False,
        )

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        
        #Print message
        message = json.loads(body)
        print(" [x] Received %r" % message)
        
        # Close channel and connection
        channel.close()
        self.connection.close()
        

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print(" [*] Waiting for messages. To exit press CTRL+C")
        
        # Start consuming messages
        self.channel.start_consuming()
