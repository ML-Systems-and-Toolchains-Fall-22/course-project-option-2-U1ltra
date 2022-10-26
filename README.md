
# 14813 Course Project - Option 2

For our project we decided to work on option 2, which deals with MQTT dataset. The two team members are

- Jiarui Li - jiaruil3@cmu.edu
- Zehua Zhang - 

------

Before working on the code, we look into the dataset and its metadata. Basically, the dataset has the features as the simple example shown in the table below. 

The features can be understand in four main subparts, namely <b>tcp</b>, <b>mqtt</b>, <b>target</b> and <b>dataset</b>. 

- <i>tcp</i> <br>
    Data generated by TCP protocal.
    > TODO: more description
- <i>mqtt</i> <br>
    Data generated by mqtt protocal, which is a standard communication protocal used by IoT network system.
    > TODO: more description
- <i>target</i> <br>
    This column is the label / class of the data point. The main goal is to use the other features to prediction the label. It have six possible categorical values, namely <b>slowite</b>, <b>bruteforce</b>, <b>flood</b>, <b>malformed</b>, <b>dos</b>, <b>legitimate</b>
- <i>dataset</i> <br>
    This is an extra column that we added to distinguish data injested from either train (labeled as 0) or test (labeled as 1) dataset. 

|         Features          |    Sample Data   |    Data Type   |
| ------------------------- |:----------------:| --------------:|
|tcp.flags                  | 0x00000018 |
|tcp.time_delta             | 0.998867   |
|tcp.len                    | 10         |
|mqtt.conack.flags          | 0          |
|mqtt.conack.flags.reserved | 0.0        |
|mqtt.conack.flags.sp       | 0.0        |
|mqtt.conack.val            | 0.0        |
|mqtt.conflag.cleansess     | 0.0        |
|mqtt.conflag.passwd        | 0.0        |
|mqtt.conflag.qos           | 0.0        |
|mqtt.conflag.reserved      | 0.0        |
|mqtt.conflag.retain        | 0.0        |
|mqtt.conflag.uname         | 0.0        |
|mqtt.conflag.willflag      | 0.0        |
|mqtt.conflags              | 0          |
|mqtt.dupflag               | 0.0        |
|mqtt.hdrflags              | 0x00000030 |
|mqtt.kalive                | 0.0        |
|mqtt.len                   | 8.0        |
|mqtt.msg                   | 32         |
|mqtt.msgid                 | 0.0        |
|mqtt.msgtype               | 3.0        |
|mqtt.proto_len             | 0.0        |
|mqtt.protoname             | 0          |
|mqtt.qos                   | 0.0        |
|mqtt.retain                | 0.0        |
|mqtt.sub.qos               | 0.0        |
|mqtt.suback.qos            | 0.0        |
|mqtt.ver                   | 0.0        |
|mqtt.willmsg               | 0.0        |
|mqtt.willmsg_len           | 0.0        |
|mqtt.willtopic             | 0.0        |
|mqtt.willtopic_len         | 0.0        |
|target                     | legitimate |
|dataset                    | 0          |





