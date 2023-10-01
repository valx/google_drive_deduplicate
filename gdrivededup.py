from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Find duplicated files in Google Drive usaging the Drive v3 API.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    l_properties = ["id", "name", "size","md5Checksum", "parents", "webViewLink", "trashed", "owners"]
    props = ','.join(l_properties)

    # key of 
    dup_key = 'md5Checksum'
    # dictionary with information for each processed item, the key is the dup_key (i.e. the md5checksum)
    d_items = {}
    # list of duplicated items keys
    l_dup = []

    # read config json
    f = open('config.json')
    config = json.load(f)

    results = service.files().list(
        pageSize=100, fields=f"nextPageToken, files({props})").execute()
    # page token
    pt = results['nextPageToken']  
    counter = 0

    while pt is not None:
        if 'nextPageToken' in results:
            pt = results['nextPageToken']
        else:
            pt = None

        items = results.get('files', [])

        if not items:
            print('No files found.')
            pt = None
        else:
            for item in items:
                counter += 1
                if counter%500 == 0:
                    print("Processed:", counter)
                
                # ignore deleted items, ignore small files, only consider files owner by current user
                if  dup_key in item \
                    and item['trashed'] is False \
                    and 'size' in item  and int(item['size'])>1000 \
                    and item['owners'][0]['emailAddress']==config['owner_email']:
                        
                        k = item[dup_key]
                        # if the md5-checksum already exists, add key to list of duplicates
                        if k in d_items.keys():
                            # add item key to duplicated list
                            l_dup += [k]
                            #print('DUP:', item)
                        d_items[k] = d_items.get(k, []) + [item]
            
                # # print debugging info
                # if counter == 1: #for item in items:
                #      print({prop: item[prop] for prop in l_properties if prop in item})
                #      print(item['owners'][0]['emailAddress'])
                #      exit()

            results = service.files().list(
                pageToken=pt,
                pageSize=100, fields=f"nextPageToken, files({props})").execute()
                
    l_dup = list(set(l_dup))
    print('Files found:', counter)
    print('Duplicates found:',len(l_dup))

    # print duplicated items data
    for s in l_dup:
        print(d_items[s])

if __name__ == '__main__':
    main()