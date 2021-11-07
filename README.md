To run it :
- launch rabbitqm on vm (sudo rabbitmq-server -detached)
- cd into containers and launch a worker n each of them (celery -A app.celery worker --loglevel=info -n worker1@%h)
- launch app on vm (python app.py)
- make a request (curl http://130.238.28.111:5000/analyse)
