Description:
- Records visits to the program, with ip address, name, and datetime of visit
- Records are recorded in a local file: 'records.db'




Prerequisites:
1. Must have python installed

Set-up:
1. Open a terminal in the project folder
2. Create a python virtual environment
  - python -m venv .venv
3. Activate virtual environment
  - In powershell: .venv/Scripts/Activate.ps1
4. Install python dependencies
  - python -m pip install -r requirements.txt

Running the program:
1. Activate virtual environment (if you have not done so already)
  - In powershell: .venv/Scripts/Activate.ps1
2. Run the main script
  - python main.py


Find you ip address:
  - Run ipconfig, and look for a private IP Address


To test, visit the link:
http://localhost:5000?name=John+Doe

* To add a space, add a plus sign:
  * For John Doe, link is ?name=John+Doe
  * For Jane Smith Doe, link is ?name=Jane+Smith+Doe
* If no name is specified, name will be blank, but IP Address is still recorded


Then, read the records by visiting:
http://localhost:5000/getRecords


You can also replace localhost with the ip address of your own computer, found with the ipconfig command.



Records are kept in a local file: 'records.db'
To clear, simply delete this file.