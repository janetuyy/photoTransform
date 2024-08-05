import glob
import os
from pathlib import WindowsPath
import json
from PIL import Image

data = {
    'folder': '',
    'images': []
}

def transformFile(folderpath, foldername, file):

    # get the path of the file
    filepath = os.path.join(folderpath, file)

    # open the image and watermark
    picture = Image.open(filepath)
    watermark = Image.open('watermark.png')

    # get new folder path
    new_folder_path = f"{os.getcwd()}/{foldername}_New"
    if not os.path.isdir(new_folder_path):
        os.mkdir(new_folder_path)

    # save base_image
    picture.save(f"{new_folder_path}/{file}",
                 "JPEG")
    # save min_image
    picture.save(f"{new_folder_path}/Min_{file}",
                 "JPEG",
                 optimize=True,
                 quality=30)

    position = (100, 100)

    # add and save MinWater_image
    picture.paste(watermark, position, watermark)
    picture.save(f"{new_folder_path}/MinWater_{file}",
                 "JPEG",
                 optimize=True,
                 quality=30)
    return

def main():

    formats = ('.jpg', '.jpeg')

    # looping through all the files in a current directory
    folders = glob.glob('*/')
    for folder in folders:
        folderpath = os.path.join(os.getcwd(), folder)
        foldername = WindowsPath(folderpath).name
        # add folder name to data
        data['folder'] = str(foldername)
        count = 0
        # transform all jpeg and jpg
        for file in os.listdir(folderpath):
            if os.path.splitext(file)[1].lower() in formats:
                print('compressing', file)
                transformFile(folderpath, foldername, file)
                count += 1
                # add image to data
                new_image = {
                    'name': file,
                    'min': f"Min_{file}",
                    'water': f"MinWater_{file}"
                }
                data['images'].append(new_image)
        print("from folder: ", foldername, "  processed images: ", count)
        # convert to JSON and save
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        with open(os.path.join(f"{os.getcwd()}/{foldername}_New", "data.json"), "w", encoding="utf-8") as file:
            file.write(json_data)

        # print(data)

    print("Done ")
    input("Press Enter to exit")

# Driver code
if __name__ == "__main__":
    main() 