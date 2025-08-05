# from django.core.management.base import BaseCommand
# from confluent_kafka import Consumer, KafkaException, KafkaError
# import json, os
# from tracker.models import LocationUpdate

# class Command(BaseCommand):
#     help = "Run kafka consumer to listen for location update"

#     def handle(self, *args, **options):
#         conf = {
#             'bootstrap.servers' : 'localhost:9092',
#             'group.id' : 'location_group',
#             'auto.offset.reset' : 'earliest'
#         }

#         consumer = Consumer(conf)
#         consumer.subscribe(['location_group'])

#         try:
#             while True:
#                 msg = consumer.poll(timeout = 1.0)

#                 if msg is None:
#                     continue
                
#                 if msg.error():
#                     if msg.error().code() == KafkaError._PARTITION_EOF:
#                         continue
#                     else:
#                         print(msg.error())
#                         break
                    
#                 data = json.loads(msg.value().decode('utf-8'))
#                 # latitude = data.get('latitude')
#                 # longitude = data.get('longitude')

#                 LocationUpdate.objects.create(
#                     latitude = data['latitude'],
#                     longitude = data['longitude']
#                 )
                
#                 print(f"Received and saved {data}")

#         except KeyboardInterrupt:
#             pass
#         finally:
#             consumer.close()


# myapp/management/commands/consume_locations.py
from django.core.management.base import BaseCommand
from confluent_kafka import Consumer
import json
from tracker.models import LocationUpdate
from confluent_kafka import KafkaError

class Command(BaseCommand):
    help = 'Consume location updates from Kafka'

    def handle(self, *args, **kwargs):
        c = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'location_group',
            'auto.offset.reset': 'earliest'
        })

        c.subscribe(['location_updates'])

        try:
            while True:
                msg = c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    # else:
                    #     print(msg.error())
                    #     break
                if msg.error():
                    print(f"Error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode('utf-8'))
                LocationUpdate.objects.create(**data)
                print("Saved:", data)

        except KeyboardInterrupt:
            pass
        finally:
            c.close()
