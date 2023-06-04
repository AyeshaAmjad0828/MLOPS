# MLOPS
The objective of this project is to develop an end-to-end MLOps pipeline that leverages docker containers for scalability and portability.
The pipeline will be hosted on a web server and connected to a webpage that allows anyone to use this MLOps pipeline as a service.

Clone this repository to utilize the MLOPs pipeline. 

Before running the docker-compose, we need to build the images in our docker. 

1. You can either download the latest mongo image from the HUB by using:

```
docker pull mongo
```

or you can build a new image by opening cmd, navigate to the Project\mongodb directory and run the following command:

```
docker build -t mongodb .
```

2. Build an image for automl by navigating to Project\automl directory and running the following command:

```
docker build -t automl .
```

3. Build an image for webserver by navigating to Project/webserver directory and running the following command:

```
docker build -t webserver .
```

4. Build an image for webpage by navigating to Project/webpage directory and running the following command:

```
docker build -t webpage .
```

5. Navigate to directory containing docker-compose.yml file and run the following command in the terminal

```
docker-compose up -d
```

6. To check if all containers are up and running, run following command in the terminal

```
docker ps
```

