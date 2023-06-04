FROM mongo:latest

COPY data.csv /data.csv

CMD mongoimport --host mymongo --db customer --collection churn --type csv --headerline --file /data.csv tail -f /dev/null
