import libtorrent as lt

import os

from pydrive.auth import GoogleAuth

from pydrive.drive import GoogleDrive

# Get magnet URL from user

magnet_url = input("Enter Magnet URL: ")

# Specify the save path for downloaded files

save_path = '/content/Downloads/'  # Set the save path to the "Downloads" directory

# Download torrent file using libtorrent

ses = lt.session()

params = {

    'save_path': save_path,

    'storage_mode': lt.storage_mode_t(2),

    'paused': False,

    'auto_managed': True,

    'duplicate_is_error': True

}

handle = lt.add_magnet_uri(ses, magnet_url, params)

ses.start_dht()

print("Downloading metadata...")

while not handle.has_metadata():

    pass

print("Starting download...")

while handle.status().state != lt.torrent_status.seeding:

    s = handle.status()

    print('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (

        s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state))

    if s.is_seeding:

        break

# Authenticate with Google Drive using PyDrive

gauth = GoogleAuth()

drive = GoogleDrive(gauth)

# Define the name of the folder

folder_name = 'Movies'

# Check if the folder exists in Google Drive

existing_folders = drive.ListFile({'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

if len(existing_folders) > 0:

    folder = existing_folders[0]

    folder_id = folder['id']

else:

    # Create the folder in Google Drive

    folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}

    folder = drive.CreateFile(folder_metadata)

    folder.Upload()

    folder_id = folder['id']

# Get a list of files in the save_path directory

files = os.listdir(save_path)

# Upload each file to Google Drive

for file_name in files:

    file_path = os.path.join(save_path, file_name)

    # Create a file in Google Drive and set its properties

    file_drive = drive.CreateFile({

        'title': file_name,

        'parents': [{'id': folder_id}]

    })

    file_drive.SetContentFile(file_path)

    file_drive.Upload()

    print(f"File '{file_name}' has been uploaded to Google Drive.")

print("All files have been uploaded to Google Drive.")

