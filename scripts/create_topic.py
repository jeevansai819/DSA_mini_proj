"""
Helper script to create Kafka topic 'traffic-events' if it doesn't already exist.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

try:
    from kafka.admin import KafkaAdminClient, NewTopic
    from kafka.errors import TopicAlreadyExistsError
except ImportError:
    from kafka_python_ng.admin import KafkaAdminClient, NewTopic
    from kafka_python_ng.errors import TopicAlreadyExistsError

def init_kafka_topic(topic_name=KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS):
    print(f"Connecting to Kafka Admin at {bootstrap_servers}...")
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    existing_topics = admin.list_topics()
    print(f"Existing topics: {existing_topics}")
    
    if topic_name in existing_topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        print(f"Creating topic '{topic_name}' with 1 partition, replication factor 1...")
        new_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        try:
            admin.create_topics([new_topic])
            print(f"Topic '{topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists.")
    admin.close()

if __name__ == "__main__":
    init_kafka_topic()
