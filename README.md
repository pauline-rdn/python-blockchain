**Activate the virtual environments**

````
source blockchain-env/bin/activate
````

**Install all packages**

````
pip3 install -r requirements.txt
````

**Run the tests**

Make sure to activate the virtual environment
In Python, the assert statement is used to continue the execute if the given condition evaluates to True.

````
python3 -m pytest backend/tests
````

**Run the application and API**

Make sure to activate the virtual environment


````
python3 -m backend.app
````