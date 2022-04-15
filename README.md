## Semi-Standard Project Option

## Fun Team Name: StockHub

## Github Repo
* https://github.com/chasemorell/StockHub

## Running the Website
1. source env/bin/activate [activates your virtual environment]
2. Open pgadmin4 on your machine -> click Servers dropdown -> right click Login/Group Roles and select Create and then click Login/Group Role... -> enter "user" as name, add "516" as the password in the Definition tab -> give user all priviledges in Privileges tab
3. sh install.sh - DO ONCE, will ask you for passwords, ALWAYS enter 516 [updates/downloads dependencies, creates database & populates the tables]
4. flask run [TO ACTUALLY ACTIVATE WEBSITE, hosts on http://127.0.0.1:5000/]
5. Ctrl-C [deactivate website]

## Team Member Contributions
1. Wyatt - Making withdraws/deposits, interacting with past purchases made by a user, sorting past purchases based on different attributes
2. Chase - Displaying stock performance history and graphs, viewing stocks in Explore Stocks, searching and sorting stocks based on different attributes, all advice article functionality. 
3. Jose - Buying/selling stock functionality, writing queries for different website functionalities
4. Angel - Buying/selling stock functionality, creating home page, building out html templates for display
