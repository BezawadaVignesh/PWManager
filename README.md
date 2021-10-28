# PW Manager
This password manager stores encrypeted passwords in database so even if our database is compromised our passwords are safe. And both POSTGRESQL and SQLite databases are supported.

![Screenshot (53)](https://user-images.githubusercontent.com/71720640/134124131-efd2cd8e-af53-4b49-867f-b7ae1bafb7c9.png)

## To use
1. For SQLite
   - to create database run 
   >  
      > python database_manager.py
   > 
   - to set password run
      > python password_manager.py
   > 
   - copy the text and store it in SECRET_KEY present in const.py file.
   - Now you are ready to go. run
      > python main.py
   > 
  
  
2. For Post POSTGRESQL
   - create a postgresql database
   - change host IP, port, username, databasename in const.py
   - set password by running 
      > python password_manager.py
   - copy the text and store it in SECRET_KEY present in const.py file.
   - set the POSTGRESQL database password to SHA-256 encryption of the password set in password_manager
   - change CURRENTDB_TYPE in const.py to POSTGRESQL
   - run
   
      > python main.py
