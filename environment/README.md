# Environment Setup

This folder contains a complete working environment. Once deployed, no further installations will be needed.

- [Environment Setup](#environment-setup)
  - [Environment Overview](#environment-overview)
    - [Docker Images for the Hadoop Cluster](#docker-images-for-the-hadoop-cluster)
  - [Installation Steps](#installation-steps)
    - [Docker and Docker Compose Installation](#docker-and-docker-compose-installation)
    - [Setting Up the Work Volume](#setting-up-the-work-volume)
    - [Running the Environment](#running-the-environment)
    - [Turn Off the Environment](#turn-off-the-environment)
  - [Other Environment Settings](#other-environment-settings)
    - [Scaling the Cluster](#scaling-the-cluster)
    - [The Hadoop Network](#the-hadoop-network)
    - [IP Address Mapping: Editing the Hosts File (Optional)](#ip-address-mapping-editing-the-hosts-file-optional)
      - [Editing on Linux and macOS](#editing-on-linux-and-macos)
      - [Editing on Windows](#editing-on-windows)
  - [User Guide](#user-guide)
    - [Jupyter Notebook](#jupyter-notebook)
    - [Hadoop Namenode Interface](#hadoop-namenode-interface)
    - [Job History MapReduce](#job-history-mapreduce)
    - [Yarn Manager](#yarn-manager)
    - [Hive CLI](#hive-cli)


## Environment Overview

The environment is based on Docker containers, which offer lower computational requirements than Virtual Machines by running applications in a lightweight manner without including an operating system.

The Docker Hub repository provides user-created images for container setup. For this project, we’ll be using four specific images.

### Docker Images for the Hadoop Cluster

We will be working with the following Docker images to set up our Hadoop cluster:

1. **NameNode** - Manages the filesystem namespace and controls access to files by clients.
2. **YarnManager** - Manages resource allocation across applications.
3. **DataNode1, DataNode2, DataNode3, DataNode4** - Stores and retrieves blocks when they are told to (by NameNode).

## Installation Steps

### Docker and Docker Compose Installation

1. **Install Docker**  
   Follow the installation guide for your operating system [here](https://docs.docker.com/get-started/get-docker/).

2. **Install Docker Compose**  
   Follow the installation instructions for Docker Compose [here](https://docs.docker.com/compose/install/).

3. **Download or Create docker-compose.yaml**  
   Once Docker and Docker Compose are installed, download or create the `docker-compose.yaml` file with the following configuration to deploy the environment.

   ```yaml
   services:
     namenode:
       image: vega90/hadoop-namenode:1.0
       container_name: namenode
       hostname: namenode
       command: bash -c /etc/start.sh
       networks: 
         hadoop:
           ipv4_address: 172.18.0.2
       ports:
         - 9000:9000  # namenode
         - 9870:9870  # hadoop
         - 8888:8888  # jupyter
         - 10000:10000  # hive
         - 10002:10002  # hiveServer2
         - 41414:41414  # avro
       volumes: 
         - LOCAL_PATH:/media/notebooks
       tty: true
       stdin_open: true

     yarnmanager:
       image: vega90/hadoop-yarn:1.0
       container_name: yarnmanager
       hostname: yarnmanager
       networks: 
         hadoop:
           ipv4_address: 172.18.0.3
       ports:
         - 8088:8088  # Resource Manager
         - 19888:19888  # JobHistory

     datanode1:
       image: vega90/hadoop-datanode:1.0
       container_name: datanode1
       hostname: datanode1
       networks: 
         hadoop:
           ipv4_address: 172.18.0.4
       ports:
         - 50020:50020
         - 50021:50075
         - 8042:8042
         - 9864:9864
         - 9866:9866

     datanode2:
       image: vega90/hadoop-datanode:1.0
       container_name: datanode2
       hostname: datanode2
       networks: 
         hadoop:
           ipv4_address: 172.18.0.5

     datanode3:
       image: vega90/hadoop-datanode:1.0
       container_name: datanode3
       hostname: datanode3
       networks: 
         hadoop:
           ipv4_address: 172.18.0.6

     datanode4:
       image: vega90/hadoop-datanode:1.0
       container_name: datanode4
       hostname: datanode4
       networks: 
         hadoop:
           ipv4_address: 172.18.0.7

   networks:
     hadoop:
       driver: bridge
       ipam:
         config:
           - subnet: 172.18.0.0/16  # static IPs
   ```

### Setting Up the Work Volume

After downloading the `docker-compose.yaml` file, open it in a text editor and replace `LOCAL_PATH` with a path on your local filesystem that will be shared with the container. This directory will be accessible from both the Docker container and your local machine.

For example:
- **On Linux**: If you want the working directory to be at `/home/course-bigdata/notebooks`, update the `volumes` section as follows:
   ```yaml
   volumes:
     - /home/course-bigdata/notebooks:/media/notebooks
   ```

- **On Windows**: Set the path to the folder where you want to mount the work volume. For example:
   ```yaml
   volumes:
     - C:\Users\cpana\Documents\environment\notebooks:/media/notebooks
   ```


### Running the Environment

Once your `docker-compose.yaml` is ready, navigate to the folder where you have the file and run the following command to start the environment:

```bash
docker-compose up -d
```

This command will launch all services in detached mode. You can then begin using your Hadoop cluster. Once executed:

- We can see that it has created a network called 'entorno_hadoop', through which all the containers that have been created and deployed communicate. 
- We have 4 datanode containers.
- We have the namenode container where we will run the Jupyter Notebook and Yarn Manager to monitor the cluster.



### Turn Off the Environment

To manage the life cycle of the containers, we use the `docker compose` command followed by the appropriate arguments.


- **Stop the containers**  
  ```bash
  docker compose stop
  ```

- **Start the containers**  
  ```bash
  docker compose start
  ```

- **Remove the containers and the 'hadoop' network**  
  ```bash
  docker compose down
  ```



## Other Environment Settings

### Scaling the Cluster

Cluster scalability depends directly on the number of DataNodes, allowing for efficient management of both storage capacity and system performance.

The configured DataNode image makes cluster scaling flexible. To adjust the number of nodes in the cluster, simply modify the number of DataNode containers in the `docker-compose.yaml` file.

For example:
- **To set up a two-node cluster**: Remove the `datanode3` and `datanode4` containers from the file.
- **To expand the cluster to seven nodes**: Add three more DataNode containers to the configuration. Ensure unique container names and IP addresses for each new node.

### The Hadoop Network

The Hadoop network is configured with a subnet within the range `172.18.0.0/16`, which allows up to 65,536 IP addresses. However, two addresses should be reserved:
- **Network address**: `172.18.0.1`, typically the first IP in the range.
- **Broadcast address**: `172.18.255.255`, usually the last address in the range.

These addresses should not be assigned to any container. If you need to scale the cluster, you can select any other available IP within this range.

> **Note**: If this subnet is already in use on your system, you can modify it to another range. In this case, make sure to update the `docker-compose.yaml` file with the new subnet and assign a valid IP address to each container accordingly.

### IP Address Mapping: Editing the Hosts File (Optional)

To access services in the containers (such as `namenode`, `yarnmanager`, `datanode1`, etc.) from your browser, you can map each container's IP address to its hostname by editing the `hosts` file on your computer. This can facilitate access to cluster services through container names (e.g., `namenode` or `yarnmanager`) instead of having to remember IP addresses.

Since the `hosts` file is "READ-ONLY," you’ll need to edit it with administrator privileges, or save it to a different location before replacing the original file. If you're using the provided `docker-compose.yaml` file with four DataNodes, add the following entries to your `hosts` file:

```plaintext
# IP Mapping - Docker Containers
172.18.0.2       namenode
172.18.0.3       yarnmanager
172.18.0.4       datanode1
172.18.0.5       datanode2
172.18.0.6       datanode3
172.18.0.7       datanode4
```

#### Editing on Linux and macOS

On Linux, the `hosts` file is located at `/etc/hosts`, and on macOS, it’s located at `/private/etc/hosts`.

**Linux:** After editing the file, you’ll need to replace it with administrative privileges. For example, if you've saved the edited file to "Downloads" on an Ubuntu machine, you can replace it using the following command in the terminal:

```bash
sudo cp ~/Downloads/hosts /etc/hosts
```

Once copied, open the file again to ensure that the IP and container name mappings are included.

#### Editing on Windows

On Windows, the `hosts` file is located at `C:\Windows\System32\drivers\etc\hosts`. This file doesn’t have an extension, so be careful to keep it that way.

To edit it, open Notepad (or any text editor) with administrator privileges, make the necessary changes, and save the file.

If needed, right-click on Notepad and select "Run as administrator," then open and edit the `hosts` file.

After editing, the result should look like this:

```plaintext
# IP Mapping - Docker Containers
172.18.0.2       namenode
172.18.0.3       yarnmanager
172.18.0.4       datanode1
172.18.0.5       datanode2
172.18.0.6       datanode3
172.18.0.7       datanode4
```

> **Note**: On Windows, network settings or firewall rules may sometimes prevent access to containers by hostname even after mapping IPs in the hosts file. In such cases, you can use `localhost` for essential functions as an alternative.

## User Guide

Let's see how to access various services within a Hadoop cluster running in Docker containers.

### Jupyter Notebook

The `namenode` container is configured so that once it is running, we can access Jupyter Notebook at the following URL:


| **URL**                               | **URL with address mapping (Optional)**              |
|---------------------------------------|------------------------------------------------------|
| http://localhost:8888/tree or http://127.0.0.1:8888/tree | http://namenode:8888/tree         |


This will open the Jupyter Notebook server, where you can view the contents of the `/media/notebooks` folder in the Docker container. This folder is shared with the folder you've configured in the `docker-compose.yaml` file.

### Hadoop Namenode Interface

To access the Hadoop Namenode interface, use the following URL:

| **URL**                               | **URL with address mapping (Optional)**              |
|---------------------------------------|------------------------------------------------------|
| http://localhost:9870                 | http://namenode:9870                                 |


This will display the Hadoop interface and cluster configuration. You can view information about the DataNodes in your cluster by navigating to the "Datanodes" tab.

To access each DataNode individually, use the IP address of the DataNode and port `9864`. For example, to access DataNode 1, use:

| **URL**                               | **URL with address mapping (Optional)**              |
|---------------------------------------|------------------------------------------------------|
| http://172.18.0.4:9864                | http://datanode1:9864                                |


### Job History MapReduce

You can view the Job History for MapReduce jobs by navigating to the following URL:

| **URL**                               | **URL with address mapping (Optional)**              |
|---------------------------------------|------------------------------------------------------|
| http://localhost:19888/jobhistory     | http://yarnmanager:19888/jobhistory                  |


### Yarn Manager

To access the Yarn Manager interface, use the following URL:

| **URL**                               | **URL with address mapping (Optional)**              |
|---------------------------------------|------------------------------------------------------|
| http://localhost:8088/cluster         | http://yarnmanager:8088/cluster                      |

### Hive CLI

In this guide, we will walk through a practical example using a simple file with information about stars and constellations: **Dataset Stars Names**.

Once the environment is set up and the Hadoop network is configured, open a terminal and access the NameNode container console:

```bash
docker exec -i -t namenode /bin/bash
```

Once inside, execute the following command:

```bash
beeline -u jdbc:hive2://
```

This will open the Hive query editor. From here, we can run various commands to see results. Don’t forget the semicolon at the end of your queries. For example, you can see the tables that have been created:

```sql
show tables;
```

Execute the query to create our first external table in Hive:

```sql
CREATE EXTERNAL TABLE stars(
     Name STRING,
     Constellation STRING,
     BayernDesignation STRING,
     Designation STRING,
     ApprovalDate DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/hive-example/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

By running this, we will create the `stars` table. The `TBLPROPERTIES` command is used to tell Hive that our file has headers, and it should skip them. The result is the creation of an external table from the existing CSV file. The `LOCATION` clause indicates where the file is located. Since it’s an external table, the data will not be deleted if the table is removed.

To check, run the following command:

```sql
show tables;
```

You should see the `stars` table listed.

To get a description of the fields in the table, execute:

```sql
describe stars;
```

Finally, we will drop the table:

```sql
drop table stars;
```

Exit **Beeline** using the following command:

```bash
!q
```