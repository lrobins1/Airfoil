To run it :
2 options : 
- Use the server running on the Airfoil-gr7 VM on the cloud : directly make requests

- Setup your own server :
-   Install Flask, celery
-   Clone this git : 
-     git clone https://github.com/lrobins1/Airfoil.git
-   Setup rabbitmqserver: (create user, password, and change the broker url in the app.py file)
-   launch app (server) (python app.py)
-   Make requests :
-     curl http://<Server_IP>:5000/new_workers/<nbr> to start new workers
-     curl http://<Server_IP>:5000/analyse to analyse some airfoil files
