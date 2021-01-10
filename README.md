# google_drive_deduplicate
A collection of Python scripts to detect and remove duplicate files across your Google Drive account

## Intro
The script is based on the Example of Google Drive API quickstart (https://developers.google.com/drive/api/v3/quickstart/python)  

The script browses across your drive account to find duplicated (based on md5 checksum of each file).
It ignores file in Trash bin of the Google Drive.

## Usage
1. Follow prerequisistes and steps 1 and 2 at https://developers.google.com/drive/api/v3/quickstart/python (create a `credentials.json` file and install python libraries in `requirements.txt`)
1. run: `python .\gdrivededup.py`
1. On the first execution the script will require you to login, the token will be saved as `token.pickle` (please ensure this file is kept/removed safely)
1. On success, the script will prompt a list of dictionaries with information for each duplicated file (if none, no output)

## TODO
This is currently work in progress. Improvments:
1. save the list as a csv file
1. document python file
2. package into an executable file