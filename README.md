# monitor_microclimate

__serial_data.py__ - program for interaction with Arduino module and saving data in data base  
__prmain directory__ contains flask application  
# Flask application structure:  
* **templates and static** directories - standatd for site appearance;
* **\_\_inti\_\_.py** - construct flask application object and configurations;
* **ap.db** - sqlite database;
* **helpers.py** - defining additional functions;
* **models.py** - defining classes for databases using SQLAlchemy;
* **output.csv** - saves data in csv file;
* **run.py** - for launching entire application;
* **views.py** - handle routes during application working.

