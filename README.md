To run it :
-   Install Flask, celery
-   Source your openrc.sh file
-   Clone this git : 
-     git clone https://github.com/lrobins1/Airfoil.git
-   launch the app 
-     python app.py
-   Make requests :
-     curl http://<Your_machine_IP>:5000/new_workers/<nbr> to start new workers
-     curl http://<Your_machine_IP>:5000/analyse to analyse some airfoil files
