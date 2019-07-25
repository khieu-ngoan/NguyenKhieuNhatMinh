import sys, glob, os, csv, json, argparse, shutil
import PIL
from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))
overwrite_thumb = True

# def album_data():

def resize():
    basewidth = 300
    extensions = (".webp",".png",".jpeg",".JPG",'.jpg')
    skip_dir = ["src",'backup','thumb']
    thumb_dir = os.path.join(current_dir,'thumb')
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)

    data = []
    albums = []
    print("go to resize")
    # for extension in extensions:
    for path in glob.iglob(f"{current_dir}/*"):
        name = os.path.basename(path)
        if( os.path.isdir(path) ) and name not in skip_dir:
            file_count = os.listdir(path)

            album = {
                "src": name,
                "title": name,
                "description": "",
                "ID": name,
                "albumID": name,
                "kind": "album",
                "t_url": [],
                "t_width": [],
                "t_height": [],
                "dc": "#5e7d7f",
                "dcGIF": "name",
                "cnt": len(file_count)
            }
            
            
            # if name not in album_index :
            #     albums.append(name)
            #     album["albumID"] = albums.index(name)
            #     data.append(album)

            thumb_dir_save = os.path.join(thumb_dir,name)
            if not os.path.exists(thumb_dir_save):
                os.makedirs(thumb_dir_save)
            elif not overwrite_thumb:
                print("skip create album",name)
                continue

            for file in glob.iglob(f"{path}/*"):
                # for root, dirs, files in os.walk(myPath):

                title, ext = os.path.splitext(os.path.basename(file))
                if ext not in extensions :

                    print(f"skip check type allow [{ext}]")
                    continue

                img = Image.open(file).convert("RGB")
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img_thumb = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
                img_thumb.save(f"{thumb_dir_save}/{title}.jpg","jpeg")

                if name not in albums :
                    albums.append(name)
                    album["albumID"] = albums.index(name)
                    album['t_url'] = [f"thumb/{name}/{title}.jpg",f"thumb/{name}/{title}.jpg",f"thumb/{name}/{title}.jpg"]
                    album['t_width'] = [basewidth,basewidth,basewidth]
                    album['t_height'] = [hsize,hsize,hsize]
                    
                    # album['cnt'] = len(images_list)
                    data.append(album)
                
                album_id = albums.index(name)

                img_detail = {
                    "src": f"{name}/{title}{ext}",
                    "title":title,
                    "description":"",
                    "ID":title,
                    "albumID":name,
                    "kind":"image",
                    "t_url":[
                        f"thumb/{name}/{title}.jpg",
                        f"{name}/{title}{ext}",
                        f"thumb/{name}/{title}.jpg",
                    ],
                    "t_width":[
                        basewidth,
                        img.size[0],
                        basewidth,
                    ],
                    "t_height":[
                        hsize,
                        img.size[1],
                        hsize,
                    ],
                    "dc":"#606065",
                    "originalURL":title,
                    "imgWidth":img.size[0],
                    "imgHeight":img.size[1],
                    "dcGIF":""
                }
                
                data.append(img_detail)
                # album["albumID"] = albums.index(name)

                

    output = {
        "nano_status": "ok",
        "nano_message": "",
        "album_content": data,
        "nanophotosprovider": "1.2"
    }
    y = json.dumps(output)
    
    output_file = os.path.join(current_dir,"data.json")
    if os.path.exists(output_file):
        os.remove(output_file)
    output_file = open(output_file, "a")
    output_file.write(y)

def main():
    ap = argparse.ArgumentParser()
    resize()

if __name__ == "__main__":
    main()