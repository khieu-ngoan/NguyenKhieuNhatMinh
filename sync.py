import argparse, sys, glob, os, io
import pyheif
import webp as WEBP_CONVERT
from PIL import Image
# from apiclient.http import MediaIoBaseDownload
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
httpauth = g_login.Get_Http_Object()

# from apiclient import discovery
# service = discovery.build('drive', 'v3', http=httpauth)


sys.path.append("pylibs")
from color import bcolors

current_dir = os.path.dirname(os.path.abspath(__file__))
typeAllow = ["image/jpeg","image/heif"]
def downloadFiles(path,folder_id):
    for gfile in drive.ListFile({'q': "'"+folder_id+"' in parents and trashed=false"}).GetList():
        gtype = gfile['mimeType']
        title = gfile['title']
        if gtype == "application/vnd.google-apps.folder":
            dir_check = os.path.join(path,title)
            if not os.path.exists(dir_check):
                os.makedirs(dir_check)
            downloadFiles(dir_check,gfile["id"])
        else:
            file_path = os.path.join(path,title)
            # metadata = gfile["imageMediaMetadata"]
            if not os.path.isfile(file_path):
                if gtype in typeAllow:
                    gfile.GetContentFile(file_path)
                    if gtype == "image/heif":
                        with open(file_path, 'rb') as f:
                            byteImg = f.read()
                        i = pyheif.read_heif(byteImg)
                        pi = Image.frombytes( mode=i.mode, size=i.size, data=i.data)
                        basename, _ = os.path.splitext(title)
                        pi.save(f"{path}/{basename}.jpg")    
                else :
                    print(f"not download file type:{gtype} of file {title}")

def gDriverTest(folder_id):
    #Login to Google Drive and create drive object
    
    action = 'sync'

    # for gfile in drive.ListFile({'q': "'"+folder_id+"' in parents and trashed=false"}).GetList():
    #     gtype = gfile['mimeType']
    #     title = gfile['title']
    #     if gtype == "application/vnd.google-apps.folder":
    #         dir_check = os.path.join(current_dir,title)
    #         if not os.path.exists(dir_check):
    #             os.makedirs(dir_check)
            
    #         print("check directory ",dir_check, " gfolderId",gfile["id"])
    #         downloadFiles(dir_check,gfile["id"])
            # sys.exit()


    if action == 'empty':
        file_list = drive.ListFile({'q': "'"+folder_id+"' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            # title, ext = os.path.splitext(os.path.basename(file1['title']))
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            # if ext not in ['.txt']:
            #     file = drive.CreateFile({'id': file1['id']})
            #     file.Delete()

            # sys.exit()
            # Initialize GoogleDriveFile instance with file id.
            
            # file.Trash()  # Move file to trash.
            # file.UnTrash()  # Move file out of trash.
            # file = drive.CreateFile({'id': file1['id']})
            # file.Delete()  # Permanently delete the file.

def main():
    # ap = argparse.ArgumentParser()
    folder_id = '1XNoWxuOy7RzGu6NXt3LAfNgg7f_ySu3w'
    downloadFiles(current_dir,folder_id)

if __name__ == "__main__":
    main()