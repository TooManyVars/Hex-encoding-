#Right now we need to update to python 3.7 in order to make sure that the entered file is only a text file, 
#But we'll do that later down the line.

import argparse
import os
import string

"""checks for file validity."""
def isValidFile(path):
    if not os.path.exists(path): 
        print("\nError: file path '{}' does not exist.".format(path))
        return None
    else:
        return open(path, "r")

"""The file name given when encrypting multiple times needs to be monitered."""
def renameFile(path): #if a file with the given name already exists, rename with an incremental number suffix until it doesn't.

    if not os.path.exists(path): #initially check if the file doesn't exists.
        #if it doesn't, simply return the path given as there is no conflicting filename.
        return path
    
    i = 1 
    path = path.replace(".txt","")
    extension = ".txt" #remove the .txt extension so that you can add in the number suffix.
    newPath = "{0}({1}){2}".format(path,i,extension)

    while os.path.exists(newPath): #check if 'example(i).txt' doesn't exist as a file name.
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
def decodeString(string):
    decodedString = []
    for index in range(0,len(string)):
        if string[index] == "0" and string[index+1] == "x":
            decodedLetter = decodeLetter(string[index] + string[index+1] + string[index+2] + string[index+3])
            decodedString.append(decodedLetter)            
    return ''.join(decodedString)

"""Both encode and decodeFile simply involve taking the contents of the file and putting them into a string, operating on them, and then writing the
   changed contents into a new file, using all of the aforementioned functions above.
"""

def encodeFile(f):
    fContents = f.read().splitlines()
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
group.add_argument("-d","--decode", help="Create an version of the given file decoded from hexadecimal. If the file is already de-coded, this file will be deleted afterwards.".format(helpText), action="store_true")
group.add_argument("-e","--encode", help="Create hexadecimal encoded version of the given file. If the file is already encoded, it is encoded again.".format(helpText), action="store_true")

args = parser.parse_args()

f = isValidFile(args.filePath)


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
    elif fSize > 47185920:
         print("\nFile is too large to be operated on. maximum file size is 47,185,920b or 47mb.")
