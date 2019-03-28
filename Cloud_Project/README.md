Anime.py application

#A cloud based RESTful API with cassandra and kubernetes implementation.
#uses Studio ghibli api - url shows list of films with description, release date, film name and id.    
#App includes a login page & homepage.
#Page one is login page
#Page two is homepage
#page three list of films with option to select a film in order to view more details(description, release date etc).
#page four displays further details for film selected on previous page. 

# How to deploy application:

Run ./autostart.sh file to install requirements & provide IP address for application 

# creating database table within cassandra

Step 1: Navigate to /home/tauseef494/Cloud_Project

Step 2: `docker pull cassandra:latest`

Step 3: docker run --name cassandra-test -d cassandra:latest

Step 4: wget -O mydata.csv https://tinyurl.com/yymdu7go

Step 5: docker cp mydata.csv cassandra-test:/home/mydata.csv

Step 6: docker exec -it cassandra-test cqlsh

Step 7: CREATE KEYSPACE mydata WITH REPLICATION =
        {'class' : 'SimpleStrategy', 'replication_factor' : 1};

Step 8: CREATE TABLE mydata.stats (FilmName text, FilmID text PRIMARY KEY);

Step 9: COPY mydata.stats(FilmName, FilmID)
        FROM '/home/mydata.csv'
        WITH DELIMITER=',' AND HEADER=TRUE;

Step 10: select * from mydata.stats;

# cassandra database within kubernetes  

Step 1: gcloud config set compute/zone europe-west2-b

Step 2: gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"

Step 3: wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy

Step 4: wget -O cassandra-service.yml http://tinyurl.com/y65czz8e

Step 5: wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8

Step 6: kubectl create -f cassandra-peer-service.yml

Step 7: kubectl create -f cassandra-service.yml

Step 8: kubectl create -f cassandra-replication-controller.yml

Step 9: kubectl get pods -l name=cassandra

Step 10: kubectl scale rc cassandra --replicas=3

Step 11: kubectl exec -it cassandra-2ggnn -- nodetool status

Step 12: kubectl cp mydata.csv cassandra-2ggnn:/mydata.csv

Step 13: kubectl exec -it cassandra-2ggnn cqlsh

Step 14: CREATE KEYSPACE mydata WITH REPLICATION =
        {'class' : 'SimpleStrategy', 'replication_factor' : 2};

Step 15: CREATE TABLE mydata.stats (FilmName text, FilmID text PRIMARY KEY);

Step 16: COPY mydata.stats(FilmName, FilmID)
         FROM 'mydata.csv'
         WITH DELIMITER=',' AND HEADER=TRUE;

Step 17: select * from mydata.stats;
.....console 
kubectl exec -it cassandra-2wd2f nodetool status

UN  10.12.0.11  254 KiB    256          40.7%             afcca9c9-6b5d-46a0-9c95-b0de2652dc55  Kubernetes Cluster
UN  10.12.1.5   274.15 KiB  256          40.8%             57eb1e45-3112-4ead-88e3-c578d2e85247  Kubernetes Cluster
UN  10.12.2.5   236.59 KiB  256          37.4%             f190f7d0-8453-4965-8503-a3dcd5286985  Kubernetes Cluster
UN  10.12.1.6   30.08 KiB  256          41.5%             872a67fe-3adf-49f5-8dff-ad70182c9306  Kubernetes Cluster
UN  10.12.2.6   30.06 KiB  256          39.6%             9db8267c-abad-4b1b-b436-56ec2dd3a7b6  Kubernetes Cluster
