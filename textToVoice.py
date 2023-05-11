import requests
from gtts import gTTS
from ftplib import FTP, error_perm
import sys
from progress.bar import Bar
import os

def main():
    url = "https://agigames.cz/apiout/vypsani_prijmeni_ktera_nejsou_zpracovana_do_audio_souboru.php"
    names = get_list(url)
    
    #create a bar from Bar class imported from progress.bar
    bar = Bar("Processing ", max=len(names))

    for name in names:
        print(f"processing: {name}")
        write_ftp(text_to_speech(name))
        bar.next()
        print()
    bar.finish()
    requests.get("https://agigames.cz/robot/vypsani_prijmeni_ktera_nejsou_zpracovana_do_audio_souboru.php")



def write_ftp(name):
    #connect to host, default port
    ftp = FTP('210568.w68.wedos.net')

    #try login, user, password
    try:
        ftp.login('w210568_pythonprijmeni', 'j4kTEwW9')

    #except error_perm <- exception from ftplib library, sys.exit()
    except error_perm:
        print("Unsuccessful connection")
        os.remove(name)
        sys.exit("Unsuccessful connection")

    #if no error
    else:
        #open mp3 in rb mode - read binary
        with open(name, 'rb') as f:
            # saves as binary in name
            ftp.storbinary(f"STOR {name}", f)
            #close ftp
            ftp.quit()
        #remove file from dir
        os.remove(name)


def text_to_speech(name):
    #use library to create audio file, language = czech, slow = false
    audio = gTTS(text=name, lang="cs", slow=False)

    #create a filename from parametr and file type
    filename = f"{name}.mp3"

    #save audio as a filename
    audio.save(filename)

    #return filename to open from dir
    return filename

#create a function using requests library that takes the list of names from php site and creates a list
def get_list(url):

    #create a response object from request.get(url)
    response = requests.get(url)

    #take out content from response object, decode using utf-8
    content = response.content.decode('utf-8')

    #return the content split by lines
    list = content.splitlines()
    return [x.strip()  for x in list]


if __name__ == "__main__":
    main()