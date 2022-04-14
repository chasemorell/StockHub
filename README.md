## Notes from Wyatt (working on mac)
1. Open pgadmin4 on your machine -> click Servers dropdown -> right click Login/Group Roles and select Create and then click Login/Group Role... -> enter "user" as name, add "516" as the password in the Definition tab -> give user all priviledges in Privileges tab
   - These credentials match the credentials used in install.sh and setup.sh
2. cd into the StockHub directory and run install.sh
3. To run my bash scripts I had to add sh to the front of the command: "sh install.sh"
   - This will ask to create a password and then prompt you to enter the password a few times.  I have hardcoded 516 as the password otherwise we would always be overwriting each other's .flaskenv files.
   - It may also say your user is named something else, but I have also hardcoded the user as "user".
4. To run app: follow instructions in **Running/Stopping the Website**
 
## Loading Stock Data into SQL Database - Notes from Chase

* I've updated `db/create.sql` to include 2 new tables (stocks and timedata). We will need to add more, however.
* I've created a script `db/getStockData.py` that fetches stock price data using polygon API and adds data to the SQL database. Currently it is configured to get 2 years of daily market info for all S&P500 stocks. Since fetching data via the API takes a long time (throttling), I've put the fetched data in local files `db/data/sp500.csv` and `db/data/tickerYTD.obj`. Setup for you should be fast!

What you need to do (Important):
* ANYTIME install.sh IS RAN, THIS COMMAND MUST BE RE-RAN TO GET THE DATA LOADED INTO ONE'S LOCAL PGADMIN
* cd db
* `python3 getStockData.py` a to load data into database

## Running/Stopping the Website

To run your website, in your VM, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```
The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon` behind the scene.
As part of the installation procedure above, this database has been created automatically for you.
You can access the database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is running.
We recommend you open a second shell on your VM to run `psql amazon`.
After you perform some action on the website, you run a query inside `psql` to see the action has the intended effect on the database.

The `db/` subdirectory of this repository contains files useful for (re-)initializing the database if needed.
To (re-)initialize the database, first make sure that you are NOT running your Flask server or any `psql` sessions; then, from your repository directory, run `db/setup.sh`.
* You will see lots of text flying by---make sure you go through them carefully and verify there was no errors.
  Any error in (re-)initializing the database will cause your Flask server to fail, so make sure you fix them.
* If you get `ERROR:  database "amazon" is being accessed by other users`, that means you likely have Flask or another `psql` still running; terminate them and re-run `db/setup.sh`.
  If you cannot seem to find where you are running them, a sure way to get rid of them is to restart your VM.

To change the database schema, modify `db/create.sql` and `db/load.sql` as needed.
Make sure you to run `db/setup.sh` to reflect the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to initialize the database contents when you run `db/setup.sh`.
Under `db/generated/`, you will find alternate CSV files that will be used to initialize a bigger database instance when you run `db/setup.sh generated`; these files are automatically generated by running a script (which you can re-run by going inside `db/data/generated/` and running `python gen.py`.
* Note that PostgreSQL does NOT store data inside these CSV files; it store data on disk files using an efficient, binary format.
  In other words, if you change your database contents through your website or through `psql`, you will NOT see these changes reflected in these CSV files (but you can see them through `psql amazon`).
* For safety, a database should never store password in plain text; instead it stores one-way hash of the password.
  This rule applies to the password value in the CSV files too.
  To see what hashed password value you should put in a CSV file, see `db/data/gen.py` for example of how compute the hashed value.

