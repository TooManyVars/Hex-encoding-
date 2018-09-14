import time
import argparse
import os
import string
from pathlib import Path

"""checks for file validity."""
def isValidFile(path):

    """wrap the check for file validity in a try catch #
       so we can stop things like the user giving something other than a text file, etc.
    """
    
    try: 
        if not Path.is_file(Path(path)):
            print("\nError: file path '{}' does not exist.".format(path))
            return None
        else:
            return open(path, "r")
    except OSError:
        print("\nError: given file directory syntax is incorrect, please provide the file path as 'directory\\file.extension'.")
            
"""The file name given when encrypting multiple times needs to be monitered."""
def renameFile(path): #if a file with the given name already exists, rename with an incremental number suffix until it doesn't.

    if not Path.is_file(Path(path)): #initially check if the file doesn't exists.
        #if it doesn't, simply return the path given as there is no conflicting filename.
        return path
    
    i = 1 
    path = path.replace(".txt","")
    extension = ".txt" #remove the .txt extension so that you can add in the number suffix.
    newPath = "{0}({1}){2}".format(path,i,extension)

    while Path.is_file(Path(newPath)): #check if 'example(i).txt' doesn't exist as a file name.
        i+=1 #if so, increment i by 1 and format in the same fashion as before until there isn't a file with the same name.
        #this time it'll be something like "example(i+1).txt"
        newPath = "{0}({1}){2}".format(path,i,extension)
    return newPath


"""Done by iterating through the string, converting each letter to hex and then adding it to an array(via list comprehension),
   which is then transformed back into a string(via the ''.join method. can be, in theory, used to encode single letters.
"""
def encodeString(string): 
    return ''.join([hex(ord(index)) for index in string])


"""Takes a hexadecimal letter, converts it into a int with a base of 16 and then converts it to a char or letter."""
def decodeLetter(letter): 
    return chr(int(letter,16))

"""Iterates through a string, looking for an index '0' and a following index of 'x'.
   When found, it will put these two, with the next two digits following after that, into a 4 letter string which will be ran through the encodeLetter function.
   When decoded, this will be put into an array.
"""
"""
Modified version of the string decoding algorithim uses try catches to skip iterations of a loop if the four current characters fed into the decode letter function
Cause a valueError to be raised, or a StopIteration error if there are an irrational amount of letters/numbers
"""
def decodeString(string):
  decodedString = []
  decodingErrors = 0 #the amount of times one or more letters could not be decoded properly. reported to the user after the string is decoded.

  string_iter = iter(string)
  for index in string_iter:

    try:
      currentIndex = index 
      secondIndex = next(string_iter)
      thirdIndex = next(string_iter)
      fourthIndex = next(string_iter)
    except StopIteration:#raised when the program tries to decoded less than 4 non hexadecimal letters.
      decodingErrors += 1
      continue

    if currentIndex == "0" and secondIndex == "x":
      try:
        decodedLetter = decodeLetter(currentIndex + secondIndex + thirdIndex + fourthIndex)
        decodedString.append(decodedLetter)
        continue
      except ValueError: #raised when the program tries to decode a non hex letter.
        continue
  return ''.join(decodedString) 

"""Both encode and decodeFile simply involve taking the contents of the file and putting them into a string, operating on them, and then writing the
   changed contents into a new file, using all of the aforementioned functions above.
"""

def encodeFile(f):

    fContents = ""
    
    try:
        fContents = f.read().splitlines()
    except UnicodeDecodeError:
        print("\nError: file type must be text(.txt) only.")
        return None
        
    EncodedfContents = [encodeString(index) for index in fContents]
    
    pathName = f.name
    oFname = os.path.basename(f.name) #original filename

    newPath = pathName.replace(".txt","") #temporarily take out the ".txt" so we can add a "encoded" suffix.
    newPath = newPath.replace("-Decoded","")
    newPath = newPath.replace("-Encoded","")
    newPath = newPath + "-Encoded"

    newPath = renameFile(newPath + ".txt") #rename the file with an incremental suffix if a similar path already exists.
    f.close()
    
    with open(newPath,"a") as newEncodedFile: #open and write the encoded contents
        newEncodedFile.truncate(0)
        for index in EncodedfContents:
            newEncodedFile.write(index + "\n")
    print("\nAn encoded version of the file has been created in the same directory.")

def decodeFile(f):
    fContents = f.read().splitlines()

    decodedfContents = [decodeString(index) for index in fContents]
    
    pathName = f.name
    oFname = os.path.basename(f.name) #original filename

    newPath = pathName.replace(".txt","")
    newPath = newPath.replace("-Encoded","")
    newPath = newPath.replace("-Decoded","")
    newPath = newPath + "-Decoded"
    
    newPath = renameFile(newPath + ".txt") #rename the file with an incremental suffix if a similar path already exists.
    f.close()
        
    with open(newPath ,"a") as newDecodedFile:
        newDecodedFile.truncate(0)
        for index in decodedfContents:
            newDecodedFile.write(index + "\n")

    """check to see if the file contains any chars.
       If it doesn't this means that the file is empty or full of blankspace, and will be deleted.
    """
    nums = [num for num in range(1,9)]
    alpha = string.ascii_lowercase
    alpha = [index for index in alpha]
    chars = nums + alpha 

    charFound = False
    
    with open(newPath, "r") as newDecodedFile:
        for Index in newDecodedFile.read():
            for index in chars:
                if Index ==  index:
                    charFound = True
                    break #break to reduce the runtime of the program, at this point we've already figured out that this file isn't empty.
    
    #if there are no chars found, the file is considered empty and deleted.
    if not charFound:
        print("\nFile was already decoded-duplicate file was deleted.")
        os.remove(newPath)
    else:
        print("\nDecoded version of the file has now been created.")


#Where we handle all the argparse arguments.
parser = argparse.ArgumentParser()

parser.add_argument("filePath", help="The file you wish to operate on.",type=str) #get the file path

helpText = "Create a copy of the file with the original contents " #to avoid repeating myself when formatting strings.

group = parser.add_mutually_exclusive_group() #add the option to either encode or decode.
group.add_argument("-d","--decode", help="Create an version of the given file decoded from hexadecimal. If the file is already de-coded, this file will be deleted afterwards(Note that illegal hexadecimal characters will be ignored).".format(helpText), action="store_true")
group.add_argument("-e","--encode", help="Create hexadecimal encoded version of the given file. If the file is already encoded, it is encoded again.".format(helpText), action="store_true")

args = parser.parse_args()

f = isValidFile(args.filePath)

startTime = time.time() #the current time of the program at initialization.

if f:
    #get the file size AFTER checking it's validity.
    fSize = os.path.getsize(args.filePath)

    #file size shouldn't be more than 45mb(or 47,185,920 bytes)(test this).
    print("\nFile size: {} ".format(fSize))
    
    if fSize <= 47185920: 
        if args.encode:
            encodeFile(f)
        if args.decode:
            decodeFile(f)
        print("\nOperation runtime: {} seconds".format(round(time.time() - startTime, 3)))
    elif fSize > 47185920:
         print("\nFile is too large to be operated on. maximum file size is 47,185,920b or 47mb.")
           
