import requests
import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

from pyspark.sql.types import *
from pyspark.sql.functions import *

spark.sparkContext.setLogLevel("ERROR")

# define input DataFrame
kafka_df = spark.readStream.format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "twitter").load()

# print(kafka_df.printSchema())

# define type
kafka_df_string = kafka_df.select\
    (col("key").cast("STRING").alias("key")\
    ,col("value").cast("STRING").alias("value"))

kafka_df_string_2 = kafka_df_string.select(col("value"))
kafka_df_tags = kafka_df_string_2\
    .select(explode(split('value', ' ')).alias('tag'))\
        .filter(col('tag').startswith('#'))

# define output DataFrame
kafka_df_tag_count = kafka_df_tags\
    .groupBy('tag').count().withColumnRenamed('count', 'tag_count')\
        .orderBy(col('count').desc())

# query
query = kafka_df_tag_count\
    .writeStream\
        .outputMode("complete")\
            .format("console")\
                .option("truncate", "false")\
                    .trigger(processingTime="3 seconds").start()

query.awaitTermination()




