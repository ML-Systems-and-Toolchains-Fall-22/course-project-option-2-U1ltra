import pandas as pd 
import pyspark
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import SparkSession

appName = "Twitter Real-time Analytics via Kafka and Spark"
master = "local"
conf = pyspark.SparkConf().set('spark.driver.host','127.0.0.1').setAppName(appName).setMaster(master)
sc = SparkContext.getOrCreate(conf=conf)

spark = SparkSession.builder \
    .appName("Our Twitter Spark and Kafka example") \
        .getOrCreate()

from kafka import KafkaConsumer
import json

topic_name = 'mqtt_attack'
topic_name = 'testing'

kafka_consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    # auto_offset_reset='earlist',            # using earlist can let the consumer start from the beginning of the messages the topic has ever produced
    enable_auto_commit=True,
    auto_commit_interval_ms =  5000,
    fetch_max_bytes = 128,
    max_poll_records = 100,
    value_deserializer=lambda x: x.decode('utf-8'))

attacks = [
    "slowite",
    "bruteforce",
    "flood",
    "malformed",
    "dos"
]

from pyspark.sql.functions import *
from pyspark.sql.types import *

streamed_data = None
res = None
i = 0

start = True
for message in kafka_consumer:
    # I prrocess 10 msg each round
    if i%5==0 and not start:   
        print(f"{'#'*10} MSG {i} {'#'*10}")
        break
        if i % 50 == 0:
            break
    else:
        start = False
    i = i + 1
    # Read the tweet from the topic
    data = [message.value]
    tweet = spark.createDataFrame(data,"string")

    if res is None:
        streamed_data = tweet.withColumn('word', explode(split(col('value'), ' '))) \
                    .groupBy('word') \
                    .count() \
                    .sort('count', ascending=False)
        
        res = streamed_data.filter(
            col('word').like(attacks[0]) |
            col('word').like(attacks[1]) |
            col('word').like(attacks[2]) |
            col('word').like(attacks[3]) |
            col('word').like(attacks[4]) 
        )
            
    else:
        streamed_data = tweet.withColumn('word', explode(split(col('value'), ' '))) \
                    .groupBy('word') \
                    .count() \
                    .sort('count', ascending=False)

        res = res.union(
            streamed_data.filter(
                col('word').like(attacks[0]) |
                col('word').like(attacks[1]) |
                col('word').like(attacks[2]) |
                col('word').like(attacks[3]) |
                col('word').like(attacks[4])
            )
        )

res.groupBy("word").count().show()
print("done!!!!")