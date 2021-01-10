# google_drive_deduplicate
A collection of scripts to detect and remove duplicate files across your Google Drive account

## Intro
The script is based on the Example of Google Drive API.
The script browses across your drive account to find duplicated (based on md5 checksum of each file).
It ignores file in Trash bin of the Google Drive.

## Usage
1. Create a `credentials.json` file
1. run: `python .\gdrivededup.py`
1. On the first execution the script will require you to login, the token will be saved as `token.pickle` (please ensure this file is kept/removed safely)

It will prompt a list of duplicated files as dictionary of information for each file

## TODO
1. save the list as a csv file
2. package into an executable file