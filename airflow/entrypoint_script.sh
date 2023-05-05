python /initdb/init.py
airflow db init
airflow users delete -u admin
airflow users create  -e zhuh16@lancaster.ac.uk -f Hongwei -l Zhu -p admin -r Admin  -u admin
nohup airflow scheduler &
nohup airflow webserver &
tail -f /dev/null