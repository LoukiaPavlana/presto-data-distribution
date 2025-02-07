## Presto Deployment

### References

Instructions found here: https://prestodb.github.io/docs/current/installation/deployment.html

Connectors: https://prestodb.github.io/docs/current/connector.html

### Overview

Presto is an open source, distributed SQL query engine designed for fast, interactive queries on data in HDFS, and others. Unlike Hadoop/HDFS, it does not have its own storage system. Thus, Presto is complimentary to Hadoop, with organizations adopting both to solve a broader business challenge.

### Requirements

#### Java

```jsx
sudo apt install openjdk-8-jre-headless
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

### **Download Presto 0.289 Manually**

```bash
wget https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.290/presto-server-0.290.tar.gz
```

### **Unpack the Presto server tarball**

```jsx
tar -xvzf presto-server-0.290.tar.gz
```

### **Create an `etc` directory inside the installation directory. This will hold the following configuration:**

- Node Properties: environmental configuration specific to each node
- JVM Config: command line options for the Java Virtual Machine
- Config Properties: configuration for the Presto server. See the [Properties Reference](https://prestodb.io/docs/current/admin/properties.html) for available configuration properties.
- Catalog Properties: configuration for [Connectors](https://prestodb.io/docs/current/connector.html) (data sources). The available catalog configuration properties for a connector are described in the respective connector documentation.
- Another file called catalog. In /etc/catalog we configure the way Trino will be able to connect to our databases
    
    To create the files:
    

```jsx
kdtouch node.properties
touch config.properties
touch jvm.config
touch log.properties
mkdir catalog
```

![image](https://github.com/user-attachments/assets/8b75e331-5793-4039-8eff-7699c787b222)


### In the [node.properties](http://node.properties) we added the following lines:

For MySQL: 

```jsx
node.environment=production
node.id=mysql_coordinator
node.data-dir=/var/presto/data
```

For MongoDB: 

```jsx
node.environment=production
node.id=mongo_worker
node.data-dir=/var/presto/data
```

For Memory: 

```jsx
node.environment=production
node.id=memory_worker
node.data-dir=/var/presto/data
```

For Machine 4:

```jsx
node.environment=production
node.id=machine4
node.data-dir=/var/presto/data
```

### In the jvm.config we added the following lines: /code

```jsx
-server
-Xmx16G
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
```

### In the [config.properties](http://config.properties) we added the following lines:

For MySQL: 

```jsx
coordinator=false
#node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=2GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
#discovery-server.enabled=true
discovery.uri=http://83.212.75.178:8080
```

For MongoDB:

```jsx
coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=2GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
#discovery-server.enabled=true
discovery.uri=http://83.212.75.178:8080
```

For Memory: 

```jsx
coordinator=false
http-server.http.port=8080
query.max-memory=2GB
query.max-memory-per-node=1GB
query.max-total-miscovery.uri=http://83.212.75.178:8080
```

For machine 4: 

```jsx
coordinator=false
http-server.http.port=8080
query.max-memory=2GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
discovery.uri=http://83.212.75.178:8080
```

[log.properties](http://log.properties) (optional)

```jsx
io.prestosql=INFO
```

### **Inside the presto/etc/catalog directory we add the following connectors:**

In mysql.properties:

```jsx
connector.name=mysql
connection-url=jdbc:mysql://localhost:3306/?useSSL=false
connection-user=mysql_presto_user
connection-password=Str0ng!Passw0rd
```

In mongodb.properties:

```jsx
connector.name=mongodb
mongodb.seeds=83.212.75.178:27017
```

In memory.properties:

```jsx
connector.name=memory
memory.max-data-per-node=128MB
```

In tpcds.properties:

```jsx
connector.name=tpcds
```

### Run Presto

To start Presto we execute the command: 

```jsx
./launcher start
```

This starts Presto as a backround process. To run Trino in the foreground and get active logs we execute: 

```jsx
./launcher run
```

### Presto CLI

```jsx
wget https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.290/presto-cli-0.290-executable.jar
```

Rename the JAR file with the following command: 

```jsx
mv  presto-cli-0.290-executable.jar presto
```

Use `chmod +x` to make the renamed file executable:

```jsx
chmod +x presto
```

Run Presto CLI:

```jsx
./presto
```
