import libtorrent as lt

import os

from pydrive.auth import GoogleAuth

from pydrive.drive import GoogleDrive


magnet_url = ""

# Download torrent file using libtorrent

ses = lt.session()

params = {

    'save_path': '/Downloads/',

    'storage_mode': lt.storage_mode_t(2)

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

# Set the client ID and client secret

gauth.client_config = {

    "client_id": "1123530391775-vmcgl1seh9tmh48qrkvh6oga0mhd89qc.apps.googleusercontent.com",

    "client_secret": "AGOCSPX--HNcTAqpCyDfuSwkM8mzVJquLCxt",

    "redirect_uri": "https://developers.google.com/oauthplayground"

}

# Set the access token

gauth.credentials.refresh_token = "1//04_NxCGKZv736CgYIARAAGAQSNwF-L9IrsGPwuTqIMEMfiVWfKyoWTJBlj9iErueQ0uc1pw3w2sNytQOvo5P7J0RpRcGmomlKCFM"

drive = GoogleDrive(gauth)

# Upload file to Google Drive

file1 = drive.CreateFile({'title': 'Downloaded Torrent File'})

file1.Upload()

print("File has been uploaded")

                                                                                          
