# HDFS – Hadoop File System
- [HDFS – Hadoop File System](#hdfs--hadoop-file-system)
  - [HDFS Basic Concepts](#hdfs-basic-concepts)
  - [HDFS specifics](#hdfs-specifics)
  - [File Storage Mechanism](#file-storage-mechanism)
  - [Components](#components)
  - [Accessing HDFS](#accessing-hdfs)
    - [Copying Local Data To and From HDFS](#copying-local-data-to-and-from-hdfs)
    - [Exercise: verify Hadoop installation and basic HDFS operations](#exercise-verify-hadoop-installation-and-basic-hdfs-operations)
    - [Hadoop fs Examples](#hadoop-fs-examples)
  - [File Read and Write](#file-read-and-write)
    - [Anatomy of a HDFS File Read](#anatomy-of-a-hdfs-file-read)
    - [Anatomy of a HDFS File Write](#anatomy-of-a-hdfs-file-write)
  - [Replication Details](#replication-details)
  - [Name Node](#name-node)
    - [General details](#general-details)
    - [NameNode High Availability](#namenode-high-availability)
    - [Block Management by NameNode](#block-management-by-namenode)
  - [Communicate with HDFS](#communicate-with-hdfs)


## HDFS Basic Concepts

- HDFS, written in **Java**, is a file system inspired by Google’s GFS.
  - Google's GFS (Google File System) is a distributed file system developed by Google to meet the demands of their massive-scale data storage requirements.
- It's a distributed file system designed for storing data across a network of machines, prioritizing **scalability** and **fault tolerance**.
- HDFS leverages the native file systems of its host **nodes**, supporting both Unix and Windows environments.
- Renowned for its **massive redundant storage** capabilities, HDFS stands as one of Hadoop's most widely utilized components.
- Demonstrating **remarkable scalability**, HDFS has handled immense data volumes, including 200 PB, distributed across 4500 servers, and billions of files.


## HDFS specifics
- HDFS **favors larger files** over numerous small ones, with a minimum block size typically exceeding 100 MB.
- It adopts a **"write once" policy**, prohibiting data overwrites or modifications within files. Any such attempts result in errors, emphasizing data integrity as paramount.
- Optimized for **streaming data access**, HDFS minimizes seek latency to facilitate high-throughput reads.




## File Storage Mechanism
- Following a hierarchical **directory structure** akin to Unix-like file systems, HDFS organizes files.
- Files are **partitioned into blocks** ranging from 64 to 128 MB, each distributed across different nodes in the network.
- To ensure fault tolerance and data availability, blocks are **replicated**, typically three times.

![](/img/02_01.png)


## Components
- **Client**: Initiates file operations such as input and output file requests.
- **Namenode**: Acts as the master node, responsible for storing block locations within each file namespace and logging all transactions.
- **Datanodes**: Store the actual data blocks distributed across the network.
- **Secondary Namenode**: Serves as a checkpoint for the namenode, aiding in its fault tolerance and recovery mechanisms.


![](/img/02_02.png)


## Accessing HDFS
Accessing HDFS is facilitated through various methods:

- Applications can read and write to HDFS directly using the **Java API**.
- Files are typically created on a local filesystem and then moved into HDFS.
- Conversely, files in HDFS may need to be moved back to the machine’s local filesystem when necessary.
- Client access to HDFS from the command line is achieved with the `hadoop fs` command.


### Copying Local Data To and From HDFS
To copy data between the client machine and the Hadoop cluster:

From Client Machine to Hadoop Cluster:
```
hadoop fs -put sales.txt /reports
```

From Hadoop Cluster to Client Machine:
```
hadoop fs -get /reports/sales.txt
```

### Exercise: verify Hadoop installation and basic HDFS operations
This exercise aims to verify the installation of Hadoop and related components, as well as practicing basic file operations with HDFS and exploring data stored within a MySQL database.


**Check Hadoop installation:**

Start terminal and list the contents of the root directory in HDFS:
```
hadoop fs -ls /
```

**Check SQL database:**
Access a MySQL database:
```
mysql -u retail_dba -h localhost -p
```
When prompt for password, type "cloudera".

Logged in the database, type:
```
mysql> show databases; 
mysql> use retail_db; 
mysql> show tables; 
mysql> exit;
```

It shows the available databases, selects the `retail_db`, lists the tables in the database, and then exits the MySQL prompt.


**Move files to HDFS**

Navigate to a spcecific directory and display the content of a CSV file:
```
> cd $HOME/dh-course
> less customers.csv
```

Upload (put) the customers.csv file to HDFS and list the contents of the current directory in HDFS:
```
> hadoop fs –put customers.csv
> hadoop fs –ls
```
Also list the contents of the user's home directory in HDFS:
```
> hadoop fs –ls /user/cloudera
> # look at the browser, users can also explore the file system using the web browser.
```

### Hadoop fs Examples
Display the contents of a file in HDFS:
```
hadoop fs -cat customers.csv
```

Move a file to the local disk and rename it:

```
hadoop fs -get customers.csv customers-local.csv
```

Create a directory (by default under the user's home directory: /user/[user-name]):

```
hadoop fs -mkdir data
```

Create a directory at a specific location:

```
hadoop fs -rmdir data
```

Delete a directory and all its contents recursively:
```
hadoop fs -rm -r data
```

## File Read and Write
### Anatomy of a HDFS File Read
1. The HDFS client initiates a connection to the distributed file system.
2. The distributed file system queries the namenode to retrieve block locations, which holds the metadata about where the data is stored.
3. The HDFS client begins reading from the FSDataInputStream.
4. The FSDataInputStream reads data from the respective DataNodes.
5. Upon completion, the HDFS client closes the FSDataInputStream.

![](/img/02_03.png)

### Anatomy of a HDFS File Write
1. The HDFS client creates a connection to the distributed file system.
2. The distributed file system establishes communication with the Namenode.
3. The HDFS client writes data to the FSDataOutputStream.
4. The FSDataOutputStream writes data packets to the DataNodes, which replicate the information across multiple nodes.
5. DataNodes acknowledge the receipt of data packets to the FSDataOutputStream (ack packet).
6. Upon completion, the HDFS client closes the FSDataOutputStream.

![](/img/02_04.png)



## Replication Details
- By default, data blocks are **replicated three times** for fault tolerance.
- Balancing between reliability and bandwidth usage is critical.
- HDFS **intelligently places replicas** based on the cluster's topology configuration.
  - The first replica (block) is placed on the same node as the client (or randomly on a not-too-busy node if external).
  - The second replica is stored on a different rack.
  - The third replica is located on the same rack as the second but on a different node.
- HDFS considers network distance to optimize data placement.

![](/img/02_05.png)





## Name Node 
### General details
- The **NameNode daemon** must run continuously for cluster accessibility.
  - Its primary function is to store and manage the metadata of the HDFS file system.
  - NameNode retains all block locations in memory for quick access.
  - It periodically saves memory snapshots to a file for crash recovery.
- The **Secondary NameNode** assists the NameNode in certain tasks.
  - It does not serve as a backup for the NameNode.
  - Responsibilities include updating block-file mappings between snapshots via the fsimage file and edit-log of filesystem operations.


### NameNode High Availability

- NameNode metadata replication and Secondary NameNode checkpoints mitigate data loss but don't ensure high availability.
  - Recovery could take over 30 minutes due to tasks like loading the namespace image into memory and replaying the edit log.
- Employing two NameNodes —Active and Standby— establishes high availability.
  - If the Active NameNode fails, the Standby takes over.
  - The Standby also functions as a Secondary NameNode, eliminating the need for an additional Secondary NameNode.
- Installation decisions are made by administrators, with failover configurations set automatically or requiring human intervention.
- In detail:
  - Datanodes are responsible for sending block reports to both namenodes, which helps in storing block mappings in memory.
  - To synchronize state, the namenodes utilize a shared, highly available storage system for sharing the edit log. This shared storage can be achieved through either a Network File System (NFS) file or a Quorum Journal Manager (QJM), which ensures redundancy with three writes.
  - In case of failover, the standby namenode can swiftly assume the active role. This rapid transition is facilitated by the standby namenode's access to the synchronized state stored in the shared storage.
  - Clients possess a mechanism for determining the active NameNode. They attempt to connect to the namenode URI, trying different possibilities until successful.
  - Automatic failover is orchestrated by a failover controller, which relies on ZooKeeper to determine the active NameNode. In the case of QJM, it allows only one NameNode to write while the other can read. For NFS, a fencing mechanism is employed, metaphorically referred to as "shooting the other node in the head," to ensure only the active NameNode operates.




### Block Management by NameNode
- Small files present a challenge for NameNode memory management.
  - Files smaller than the block size occupy space proportional to their size on disk but are accounted for as full blocks (e.g. 128 MB) by the NameNode.
  - Each small file consumes approximately 200 bytes of NameNode memory.
- Accumulation of numerous small files can exhaust NameNode memory.
- Solutions include creating larger files in a staging area before uploading to HDFS or utilizing Hadoop archive files.
  - Hadoop archives merge small files into a single HDFS file, reducing memory consumption.
  - Although individual files can be listed, their contents are merged as a collection of records within the archive.

The below commands illustrate creating and using Hadoop archive files to manage small files efficiently within HDFS:
```
$ echo hola,1 > test1.txt
$ echo hola,2 > test2.txt
$ hadoop archive -archiveName h.har -p /tmp test1.txt test2.txt /tmp

$ hadoop fs -ls /tmp
$ hadoop fs -ls /tmp/arch.har

$ hadoop fs -ls /tmp/h.har/part-0
$ hadoop fs -cat /tmp/h.har/_index
```

## Communicate with HDFS
There are 3 ways to communicate with HDFS. Each method serves different use cases depending on whether you need interactive command line access, programmatic access within a Java application, or networked access via HTTP.

- **Command Line Client:** Use `hadoop hdfs` commands for quick, manual file system operations from the command line.
- **Java API:** Utilize the `FileSystem`, `FSDataInputStream`, and `FSDataOutputStream` classes for programmatic access to HDFS within Java applications.
- **WebHDFS:** Use HTTP REST API for interacting with HDFS from non-Java applications or over the network using standard HTTP methods.



