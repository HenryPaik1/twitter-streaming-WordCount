# Count Words from Twitter Using SparkStream
- Prerequisite: spark 2.4.0, kafka 2.2
- **Producer**: `kafka-connect-twitter`(https://github.com/Eneco/kafka-connect-twitter)
	- it has no more update and need to edit few file:
		- `connect-sink-standalone.properties`
  		- `connect-source-standalone.properties`
  		- `pom.xml`
	- Please refer to https://github.com/Eneco/kafka-connect-twitter/pull/56/files for details.
	- I made repo with modified file for the purpose of study 
- **Consumer**
	- SparkStream
		- `kafka_sparkstream.py`: processing data by spark_stream
- `kafka_app.py`: deploy flask & dash server 
- Result
<img src="pic.png" width=2000>

## Implementation
Clone this repo, fill `twitter-source.properties` with your info and follow the code below:
~~~
# example code
## run zookeeper server(terminal1)
$ kafka/bin/zookeeper-server-start.sh config/zookeeper.properties

## run kafka server(terminal2)
$ kafka/bin/kafka-server-start.sh config/server.properties

## create topic: twitter(terminal3)
$ kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic twitter

## check the topic
$ kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
>> twitter

## set the PATH(terminal4)
$ export CLASSPATH=path/to/kafka-connect-twitter/target/kafka-connect-twitter-0.1-jar-with-dependencies.jar

## run twitter stream
$ path/to/kafka/bin/connect-standalone.sh path/to/kafka-connect-twitter/connect-simple-source-standalone.properties path/to/kafka-connect-twitter/twitter-source.properties

## run flask and dash server 
$ python3 kafka_app.py

## run spark_stream
$ path/to/spark/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 kafka_sparkstream.py
~~~
