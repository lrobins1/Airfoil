To run it :
-   Install Flask, celery
-   Clone this git : 
-     git clone https://github.com/lrobins1/Airfoil.git
-   launch app the app (python app.py)
-   Make requests :
-     curl http://<Server_IP>:5000/new_workers/<nbr> to start new workers
-     curl http://<Server_IP>:5000/analyse to analyse some airfoil files
