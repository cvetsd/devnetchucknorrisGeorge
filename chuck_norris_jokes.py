import requests
import os
import logging
import sys
import inspect
import json
from os import path

myScriptName = []
if not path.exists('logs'):
    print('logs directory not found, creating')
    os.mkdir('logs')
if '/' in sys.argv[0]:
    myScriptName = sys.argv[0].split("/")
    myLen = len(myScriptName)
else:
    myScriptName.append(sys.argv[0])
    myLen = 1

logging.basicConfig(level=logging.INFO,
                    filename=f'logs/{myScriptName[myLen-1].split(".")[0]}.log', # log to this file
                    format='%(asctime)s %(message)s') # include timestamp
def mylogger(mymsg):
    logging.info(mymsg)

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def get_chuck_norris_joke(myCat = False):
    
    if myCat:
        URL = f'https://api.chucknorris.io/jokes/random?category={myCat}'
    else:
        URL = f'https://api.chucknorris.io/jokes/random'

    mysession = requests.session()
    try:
        response = mysession.get(URL)
        if response.ok:
            mylogger(f'{lineno()} Got joke. response: {response}')
        else:
            mylogger(f'{lineno()} Failed getting joke. response: {response}')
    except Exception as e:
        mylogger(f'{lineno()} Caught the exception: {e}')

    mylogger(f"{lineno()} Response json.dumps: {json.dumps(response.json(), indent=4, separators=(',', ': '))}")
    mylogger(f'{lineno()} Response text: {response.text}')
    if 'value' in response.json():
        return response.json()['value']
    else:
        return False

def get_chuck_norris_cats():
    URL = f'https://api.chucknorris.io/jokes/categories'

    mysession = requests.session()
    try:
        response = mysession.get(URL)
        if response.ok:
            mylogger(f'{lineno()} Got categories. response: {response}')
        else:
            mylogger(f'{lineno()} Failed getting categories. response: {response}')
    except Exception as e:
        mylogger(f'{lineno()} Caught the exception: {e}')

    mylogger(f"{lineno()} Response json.dumps: {json.dumps(response.json(), indent=4, separators=(',', ': '))}")
    mylogger(f'{lineno()} Response text: {response.text}')
    if response.ok:
        cleanCats = response.text
        cleanCats = cleanCats.replace('[','')
        cleanCats = cleanCats.replace(']','')
        cleanCats = cleanCats.replace(',','\n')
        cleanCats = cleanCats.replace('"','')
        return cleanCats
    else:
        return False

def main():
    myGetJoke = get_chuck_norris_joke()
    if myGetJoke:
        print(myGetJoke)
    else:
        print("Couldn't get a joke")
    
    while True:
        print ('1. Get another joke')
        print ('2. List joke categories')
        print ('3. Specify joke category')
        print ('4. Exit')
        myOption = input(f'Please enter number 1 - 4: ')
        if myOption == '1':
            myGetJoke = get_chuck_norris_joke()
            if myGetJoke:
                print(myGetJoke)
            else:
                print("Couldn't get a joke")
        elif myOption == '2':
            myJokeCategories = get_chuck_norris_cats()
            if myJokeCategories:
                os.system('clear')
                print(myJokeCategories)
            else:
                print("Couldn't get categories")
        elif myOption == '3':
            userCat = input(f'Enter category: ')
            if len(userCat) > 2:
                myGetJoke = get_chuck_norris_joke(userCat)
                if myGetJoke:
                    print(myGetJoke)
                else:
                    print("Couldn't get a joke")
        elif myOption.lower() in ['4','q','x']:
            break
        else:
            os.system('clear')



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nnSomebody pressed ctrl-c. Have a nice day!')