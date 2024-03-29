
# 14813 Course Project - Option 2

For our project we decided to work on option 2, which deals with MQTT dataset. The two team members are

- Jiarui Li - jiaruil3@andrew.cmu.edu
- Zehua Zhang - zehuazha@andrew.cmu.edu

------
Table of Content

[Project Directory Structure](#ProjectDirectoryStructure)<br>
[Overview](#Overview)<br>
[Dataset Features & SQL Table](#Dataset)<br>
[ML Models](#MLModel)<br>

- [Feature Engineering Principles](#feature)<br>
- [PySpark ML Models](#pyspark)<br>
- [TensorFlow Models](#tf)<br/>

[How to Run with Docker](#docker)<br/>
[Video](video)

------

### Project Directory Structure <a id="ProjectDirectoryStructure"></a>
There are four notebooks in our submission. 
In the Checkpoint 1 directory, there are 2 notebooks. proj.ipynb is the main notebook for checkpoint 1, including certain data processing, ingestion, analysis, as well as the kafka consumer application. listener.ipynb is mostly kafka producer program. 

In the Checkpoint 2 directory, there are 2 notebooks. Data Processing.ipynb includes more data cleaning and feature engineering using Pyspark Pipeline and Pandas.
After running it, there should be 2 csv files produced as outcome, df_test_pandas.csv and df_train_pandas.csv. These two csv files will be used in pyspark_TF_models.ipynb file as the data source. 

<b>Order of notebooks: proj.ipynb, listener.ipynb, Data Processing.ipynb,pyspark_TF_models.ipynb </b>

### Overview <a id="Overview"></a>
Before working on the code, we look into the dataset and its metadata. MQTTset was built by using IoT-Flock. It is a innovative dataset built specificly for IoT network ML/AI algorithm training. The data is generated by deploying different IoT sensors, including temperature, light intensity, humidity, CO-Gas, motion, smoke, door opening/closure and fan status, connected to an MQTT broker. The capture time refers to a temporal window of one week (from Friday at 11:40 to Friday at 11:45). It is worth notice that there are two types of sampling period, periodic and random. Periodic means the sensor will sample obervations at a predefined fixed time interval (tempereture), while random means the sampling would depend on random events (motion). 

### Dataset Features & SQL Table <a id="Dataset"></a>
Basically, the dataset has the features as the simple example shown in the table below. The features can be understand in four main subparts, namely <b>tcp</b>, <b>mqtt</b>, <b>target</b> and <b>dataset</b>. 

- <i>tcp</i> <br>
    Data generated by TCP protocal. According to the underlying paper, only the attributes that can contribute to characterizing potential attacks and legitimate traffic are kept.
- <i>mqtt</i> <br>
    Data generated by mqtt protocal, which is a standard communication protocal used by IoT network system. As TCP, only the attributes that can contribute to characterizing potential attacks and legitimate traffic are kept. More details about [removed attributes](https://www.mdpi.com/1424-8220/20/22/6578/htm) and [MQTT attribute set](http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/MQTT_V3.1_Protocol_Specific.pdf).
- <i>target</i> <br>
    This column is the label / class of the data point. The main goal is to use the other features to prediction the label. It have six possible categorical values, namely <b>slowite</b>, <b>bruteforce</b>, <b>flood</b>, <b>malformed</b>, <b>dos</b>, <b>legitimate</b>
- <i>dataset</i> <br>
    This is an extra column that we added to distinguish data injested from either train (labeled as 0) or test (labeled as 1) dataset. 
</br>

Then we begin to work on our table schema which mainly involves determining the data type of each columns, depending on the data it contains and the meaning it carries.

However, we discovered that the data is quite clean in terms of the data type. Most of the data is in <b>double</b> type or integer type, which is already good numerical representation.

The following are the existing string columns.
```
|-- tcp_flags: string (nullable = true)
|-- mqtt_conack_flags: string (nullable = true)
|-- mqtt_conflags: string (nullable = true)
|-- mqtt_hdrflags: string (nullable = true)
|-- mqtt_msg: string (nullable = true)
|-- mqtt_protoname: string (nullable = true)
|-- target: string (nullable = true)
```

For the <b>flags</b>, we considered about changing them into integer, since they can be represented in integer at this stage. However, it is more reasonable to convert into one-hot encoding later when doing data engineering, since they are nominal type. Same intuition can be applied to <b>target</b> feature.

For <b>mqtt_msg</b>, it is a piece of message without specific form, so it should be kept in string type. And as I inspect <b>mqtt_protoname</b>, it appears to be another nominal feature with two possible labels. 


|         Features          |    Sample Data   |    Data Type   |  Description  |
| ------------------------- |:----------------:| --------------:|:-------------:|
|tcp.flags                  | 0x00000018 |  string  | TCP flags |
|tcp.time_delta             | 0.998867   |  double  | Time TCP stream |
|tcp.len                    | 10         |  integer | TCP Segment Len |
|mqtt.conack.flags          | 0          |  string  | Acknowledge Flags |
|mqtt.conack.flags.reserved | 0.0        |  double  | Reserved | 
|mqtt.conack.flags.sp       | 0.0        |  double  | Session Present |
|mqtt.conack.val            | 0.0        |  double  | Return Code | 
|mqtt.conflag.cleansess     | 0.0        |  double  | Clean Session Flag |
|mqtt.conflag.passwd        | 0.0        |  double  | Password Flag | 
|mqtt.conflag.qos           | 0.0        |  double  | QoS Level |
|mqtt.conflag.reserved      | 0.0        |  double  | (Reserved) |
|mqtt.conflag.retain        | 0.0        |  double  | Will Retain |
|mqtt.conflag.uname         | 0.0        |  double  | User Name Flag |
|mqtt.conflag.willflag      | 0.0        |  double  | Will Flag | 
|mqtt.conflags              | 0          |  string  | Connect Flags |
|mqtt.dupflag               | 0.0        |  double  | DUP Flag |
|mqtt.hdrflags              | 0x00000030 |  string  |  Header Flags |
|mqtt.kalive                | 0.0        |  double  | Keep Alive | 
|mqtt.len                   | 8.0        |  double  | Msg Len |
|mqtt.msg                   | 32         |  string  | Message | 
|mqtt.msgid                 | 0.0        |  double  | Message Identifier |
|mqtt.msgtype               | 3.0        |  double  | Message Type |
|mqtt.proto_len             | 0.0        |  double  | Protocol Name Length |
|mqtt.protoname             | 0          |  string  | Protocol Name |
|mqtt.qos                   | 0.0        |  double  | QoS Level | 
|mqtt.retain                | 0.0        |  double  | Retain |
|mqtt.sub.qos               | 0.0        |  double  | Requested QoS |
|mqtt.suback.qos            | 0.0        |  double  | Granted QoS |
|mqtt.ver                   | 0.0        |  double  | Version | 
|mqtt.willmsg               | 0.0        |  double  | Will Message |
|mqtt.willmsg_len           | 0.0        |  double  | Will Message Length |
|mqtt.willtopic             | 0.0        |  double  | Will Topic |
|mqtt.willtopic_len         | 0.0        |  double  | Will Topic Length |
|target                     | legitimate |  string  | Attack Class Label |
|dataset                    | 0          |  integer | Train / Test Indicator | 


### ML Models<a id="MLModel"></a>

#### feature engineering principles<a id="feature"></a>
Here we further cleaned up the data and did the feature engineering in this part. Specifically, more columns aer dropped and features are converted to proper dtype and then assembled as a feature vector ready for ML models. 
We dropped the following columns, because they has only value of 0 throughout the dataframe:

    "mqtt_conack_flags",
    "mqtt_conack_flags_reserved",
    "mqtt_conack_flags_sp", 
    "mqtt_conflag_qos", 
    "mqtt_conflag_reserved", 
    "mqtt_conflag_retain", 
    "mqtt_conflag_willflag", 
    "mqtt_willtopic", 
    "mqtt_willtopic_len", 
    "mqtt_sub_qos", 
    "mqtt_suback_qos", 
    "mqtt_willmsg",
    "mqtt_willmsg_len"

"mqtt_msg" is dropped since it is would create a variable sized encoding that would bring up error in transforming the test set. Also, the potential message is also already obscured by its own encoding and thus has less means to be utilized.

"tcp_flags", "mqtt_conflags", "mqtt_conflags" are dropped since new columns are created later in the code out of them by converting to decimal from hex string. So they are redundant right now. 

"dataset" being the indicator to distinguish between test set and train set is only useful during data ingestion to Postgresql. So it is useless here. 

For feature engineering, <b>target</b> column is converted to labels. 
All columns are converted to datatype of Double and dropped after a feature vector has been assemblied. After scaling, we could fit to the train set and use it to transform both the train set and test set. 


#### PySpark ML models. <a id="pyspark"></a>
For PySpark, we used logistic regression and multi-layer perceptron model for classfication. 

##### Logistic Regression <a id="lr"></a>
By using Logistic Regression with only default parameters, the model achieves a Train accuracy = 80.45% and test accuracy = 80.63%.
After cross validation, the test accuracy is the same. It may look wired, yet after retrieving for the best model paramter, it could be seen that the regularization parameter is 0. It makes sense as the default logistic regression model also has a regularization parameter of 0. As a result, the best model is the same as the default model, despite that maxIter parameter has barely any effect over the performance.  

##### Multi Layer Perceptron <a id="MLP"></a>
Multi Layer Perceptron is used here as a basic Neural Network. By using a basic model with layers: [30, 10, 20,  20, 6], we achieved an test accuracy of 0.7916336555221043. 

In the CrossValidation, the number of fold is set to 5. 
Through the following layers, and potential maxIter parameters (100 vs 150), we achieved a test accuracy of 0.8107035096077497 with 100 iterations and layer of [30, 10, 20, 6], indicating that a model with more layers not neccessarily have better effect while the potential harm of overfitting is increasing. 

    [30, 10, 20,  6],
    [30, 10, 20, 20,  6],
    [30, 10, 20, 40, 6],
    [30, 10, 20, 40, 20, 6]]


#### TensorFlow models. <a id="tf"></a>
For TensorFlow models, we created 2 neural network, a shallow one and a deep one. The shallow has a rather wide width for each layers and a depth of 5 in addition to the output layer. The deep one has a depth of 25 and a smaller width range(10-25). For both cross validations, another hyperparameter we tuned is the activation functions: tanh and gelu.

##### Shallow NN <a id="shallow"></a>
In the shallow NN, the widths are [15, 25, 35, 50], and the activation functions are ['tanh', 'gelu']. After cross validation, the best test accuracy is achieved with a width of 25 for each layer, and activation function equals to 'gelu.' The accuracy is 0.8269590735435486, and the loss is 0.4354126453399658. Models that use tanh in general performs worse than ones with gelu with a higher variance.

Width, Activation function  test loss, test acc: 

    15, gelu                    [0.4293350279331207, 0.8268182277679443]
    25, gelu                    [0.4188815951347351, 0.8269590735435486]
    35, gelu                    [0.42542606592178345, 0.8254702687263489]
    50, gelu                    [0.47279900312423706, 0.8188109993934631]


    15, tanh                    [0.4764169156551361, 0.8125942945480347] 
    25, tanh                    [0.4881387948989868, 0.8104214668273926]
    35, tanh                    [0.49583932757377625, 0.8076450824737549]
    50, tanh                    [0.5551455020904541, 0.7912081480026245]

##### Deep NN <a id="deep"></a>
In the Deep NN, the widths are [10, 15, 20], and the activation function options are the same as before. After cross validation, the best test accuracy is achieved with a width of 15 for each layer, and activation function equals to 'gelu.' The accuracy is 0.8267980813980103, and the loss is 0.4354126453399658. Models that use tanh in general performs worse than ones with gelu with a higher variance.
The outcomes for each model are as follows:
Width, Activation function | test loss, test acc: 

    10, gelu                    [0.4495931565761566, 0.8146061897277832] 
    15, gelu                    [0.4354126453399658, 0.8267980813980103]
    20, gelu                    [0.5503770709037781, 0.8035207986831665]

    10, tanh                    [0.8426638245582581, 0.6704355478286743] 
    15, tanh                    [1.0641387701034546, 0.5032894015312195]
    20, tanh                    [0.6486892104148865, 0.7749320864677429]

Summary:

Some potential reasons why gelu is performing better than tanh:
1. tanh would cause gradient vanishing problem, while gelu would not
2. Gelu is even better than relu in a sense that it could stop neurons from dying out with also a bound on how far negative gradient could affect the model. Comparing to Relu, which would cause the gradient to be zero in the negative regime, Gelu could help to still preserve the negativity over neurons. 

Width vs test accuracy: <br/>
While the models are expected to perform better with more neurons on each layer, what we observe is that the test accuracy is the best with a moderate number of neurons on each layer, since high width could potential cause overfitting. 

### How to Run with Docker<a id="docker"></a>
We have successfully deploy our scripts using docker. Here is the full documentation of how to run our script using docker. 

We used two dockers to run our pyspark and ML models script and Kafka script.

#### Pyspark and ML Models
This is very simple. Assuming the user already have docker installed, just follow the following steps
```
docker pull jiaruili0000/14813_project_option_2:alpha
docker run -p 10000:8888 jiaruili0000/14813_project_option_2:alpha
```
Then, the terminal will start to run the container with jyputer-notebook service. One can easily link to the service by visiting **http://\<hostname\>:10000/?token=\<token\> **.

Then, one can just upload our script into the notebook and start running.

#### Kafka
Kafka docker might need a bit more time to setup since I failed to push my prepared image due to its large size. However, one can get it working by going through the following steps./

Firstly, create a new file named ```docker-compose.yml```, and put the follwing content into the file.

```
version: '3'

services:
  zookeeper:
    image: wurstmeister/zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: localhost
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
```

Then, we start its service with docker-compose.

```
docker-compose -f docker-compose.yml up -d
```

Then, one can use this to start an interactive shell.

```
docker exec -it kafka /bin/sh
```

After get into the shell, install necessary packages using the following commands.

```
apt-get update
apt-get install python3
apt-get -y install python3-pip
pip install tweepy
pip install kafka-python
pip install pandas
pip install pyspark
```

With above, we are all set with the environment.

Then, one can transfer our script under directory ***script_for_kafka_docker*** into the docker storage by 

```
mkdir project_option_2
cd project_option_2
vim consumer.py
vim producer.py
```

and copy the code into the file.

After this, one should use 
```
docker exec -it kafka /bin/sh
```
twice time to get two interactive shells. They should run the following two commands seperately.

```
python3 consumer.py
python3 producer.py
```

Finally, make sure to modify the data path and postgres related configerations to your local setting. Otherwise, the program may not find the desired file or the database (schema, table, user, password).

### Video <a id="video"></a>
The following are videos explaining our code and final results. Feel free to refer to them.
- [Introduction](https://youtu.be/ObeVo9jJ2KY)<br/>
- [Checkpoint1](https://youtu.be/DDhFwHo0YBA)<br/>
- [Checkpoint2](https://youtu.be/KV5OPr8eGfs)<br/>
- [Cloud Postgresql](https://youtu.be/2Ab4LtN1brU)<br/>
- [Docker](https://youtu.be/2FDPavHBdxY)<br/>
