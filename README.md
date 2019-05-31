# Mapping Violence Tools
## Data Dump Email
Command line tool for sending emails with current data attached as a JSON file.

Emails to send to are stored in `data-dump-email/emails.txt`.

Invoke the command by running in the root of this repository:
```bash
./data-dump-email/data-dump-email.sh
```
The script does not work if you invoke it from the child directory. Pull requests welcome to fix this.

## Data Processing
Python script to flatten and remove metadata to make conversion to CSV easier.

Requires Python3 to be installed.

Run the script in any directory where the data export is named `data.json`.

```bash
python3 ./flatten-and-remove-metadata.py
```
