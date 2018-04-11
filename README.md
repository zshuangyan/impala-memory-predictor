# 1. Brief
IML-Predictor is a tool for predicting impala query memory limit based on Supervisored learning.
We collect certain amount of impala queries and their executing info as samples, extract features and label
them as data for trainning models, which is used to predict memory for new comming impala queries.

# 2. Installation
## 2.1. Dependencies
 - Impala: 2.9.0-cdh5.12.1 or 2.5.0-cdh5.7.2
 - python3
 - scala

## 2.2. Install
```
git clone git@gitlab.gridsum.com:data-engineering/impala-toolbox/iml-predictor.git
cd iml-predictor
sudo apt-get -y install --no-install-recommends \`cat depend_ubuntu\`
python3 -m pip install -r depend_pip3
```

## 2.3. [Edit settings of IML-Predictor](./settings_explanation.md)

## 2.4. Start/Stop
fex is the scala application for collecting impala queries and their executing info, package and upload to spark node
```
cd fex
mvn clean package
cd target
mv feature-engineering-1.0-SNAPSHOT-jar-with-dependencies.jar feature-engineering.jar
scp feature-engineering.jar username@remoteip:/home/username
```
generate a shell script for running spark task and upload to spark node
```
python generate_spark_submit.py
scp spark.sh username@remoteip:/home/username
```
login remote server to create the directory for holding feature data
```
ssh username@remoteip
hadoop fs -mkdir iml-predictor/feature
```
before building models, run spark.sh on spark node with parameters start_day and end_day in format '%Y%m%d', for example:
```
./spark.sh 20180312 20180318
```

start IML-Predictor application
```
python -m memory.server
```

# 3. Tutorials & Documentation

## 3.1. Internal Mechanism


## 3.2. Default scheduling strategy (priority schedule)
 - [code](./scheduler/priority_schedule.py)
 - [doc](./priority_schedule.md)

## 3.3. You can implement your specific scheduling strategy
  - [schedule strategy interface](./scheduler/base_schedule.py)
  - [example schedule strategy](./scheduler/example_schedule.py)
  - edit [the config file](./conf/scheduler.yml)
   - edit config item: `schedule_module_name: 'scheduler'`
   - edit config item: `schedule_py_name: 'example_schedule'`
   - edit config item: `schedule_class_name: 'DoNothing1Schedule'` or `schedule_class_name: 'DoNothing2Schedule'`

## 3.4. Send schedule report when scheduling
 - edit [the config file](./conf/scheduler.yml)
  - edit config items about `email`
  - edit config item: `enable_schedule_report: true`
 - schedule report example:
   ![image](./resources/schedule_report_example.png)


## 3.5. Utils
 - backup impala config: `./bin/scheduler_utils.sh backup`
 - rollback impala config: `./bin/scheduler_utils.sh rollback`
 - check [the scheduler config file](./conf/scheduler.yml): `./bin/scheduler_utils.sh check`

# 4. Communication
  impala-toolbox-help@gridsum.com

# 5. License
IPM-Scheduler is [licensed under the Apache License 2.0.](./LICENSE)



# impala内存预测
impala内存预测项目是基于历史的impala sql执行消耗内存上限，来预测当前sql将要消耗的内存上限，用来作为sql查询的memory_limit参数  
impala版本：cdh5.12.1 

### 1. 配置系统环境  
OS：Ubuntu  
Python：3.5+  
- 拉取代码：git clone -b feature/less_memory_use git@gitlab.gridsum.com:data-engineering/GDP-query-coordinator.git，  
并切入项目目录cd GDP-query-coordinator
- 执行sudo apt-get -y install --no-install-recommends \`cat depend_ubuntu\`  
- 执行python3 -m pip install -r depend_pip3 

Scala版本：2.10.5+  

### 2. 启动服务和测试  
- cd GDP-query-coordinator, 执行 python3 -m memory.server  
API文档链接：~~~  


### 3. 内部机制  
项目主要分为三个模块：  
1. 获取历史impala sql执行数据，生成特征向量文件，保存在HDFS中（此部分使用scala spark实现）；
2. 通过使用内存的大小对历史的样本赋予标签，使用特征向量和标签构建内存预测模型；（Python实现）
3. 接收用户的预测内存请求，解析当前sql的explain结果并生成特征，输入到模型中得到预测结果返回给用户（基于tornado的API）；

#### 特征字段说明  
| 字段| 说明 |
|-----|---|
| mLayer | explain树深度 |
| mSize | explain树中除了最右子树外的所有子树中，浏览HDFS文件大小除以执行任务的实例数的最大值 |
| mFiles | 当mSize取到最大值时，对应的浏览HDFS文件总数除以执行任务实例数的结果 |
| events | explain summary的行数 |
| agg | explain中"AGGREGATE"的次数 |
| exg | explain中"EXCHANGE"的次数 |
| alt | explain中"ANALYTIC"的次数 |
| select | explain中"SELECT"的次数 |
| hjoin | explain中"HASH JOIN"的次数|
| ljoin | explain中"LOOP JOIN"的次数|
| scan | explain中"SCAN HDFS"的次数|
| sort | explain中"SORT"的次数|
| union | explain中"UNION"的次数|
| top | explain中"TOP"的次数|
  
#### 生成样本标签 
比如对于当前集群的所有查询，允许设置memory_limit的最大值为5000MB, 那么可以通过设置类似[300, 800, 2000, 5000]作为  
分界线来把样本划分为如下几类：  
LABEL_0 : 0 < useMemMB <= 300  
LABEL_1 : 300 < useMemMB <= 800  
LABEL_2 : 800 < useMemMB <= 2000  
LABEL_3 : 2000 < useMemMB <= 5000  

用户可以在memory/model/constants.py中设置`MEMORY_SPLIT`来自定义所有可能的分解值,  
设置`CLASS_NUM`来定义最终分为几类，程序会根据分类的个数，选择出交叉验证效果最佳的分界线。  


#### 特征选择和特征处理
特征越多，需要的样本空间就越大，因此筛除掉一些特征，反而会提高预测的准确性。用户可以在memory/model/constants.py中  
设置`FEATURE_NUM`决定保留的特征个数，需要注意的是保证FEATURE_NUM >=5，系统会通过随机森林选出增益较高的特征。  

如果特征的取值是连续性的数字，那么单个特征就可能有成千上万种取值，最好能够先对特征进行归约处理，用户可以在memory/model/constants.py中  
设置`COLUMNS_CLEAN_FUNC`决定要处理的特征和对应的处理函数，类似下面这样：  
COLUMNS_CLEAN_FUNC = {'mSize': round, 'mFiles': round, 'useMemMB': round}  

#### 预测结果
使用多分类进行预测，通常会遇到这样的问题，处于分类分界线上的点容易被预测到错误的分类，以生成样本标签中的分界线为例：  
如果执行一个sql真实需要使用内存为310MB，但是它的特征很可能和LABEL_0中的样本更接近，因此更容易被分到0类中去，所以我们  
不能直接返回这个分类对应的上界，而是使用ratio*mem[i] + (1-ratio)mem[i+1]这种方式，用户可以根据自己的需要设置ratio的  
大小，满足0 < ratio < 1，通过在memory/model/constants.py中设置`MEMORY_PREDICT_RATIO`来实现。  

#### 交叉验证结果  
在构建模型的过程中可以通过设置generate_report=True以使系统生成交叉验证结果，从而帮助用户分析模型预测的可靠性。用户可以设置  
memory/model/constants.py中的`CROSS_VALIDATE_RATIO`来设置训练集和验证集的大小比例。  

#### 分池子组训练模型
集群的不同池子之间的业务差距可能较大，把执行SQL差距较大的池子分开构建模型，以尽可能提高预测的准确率并减少内存浪费。  
我们通过设置`MODEL_GROUP`来设置


