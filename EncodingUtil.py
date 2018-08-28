import argparse
import os

def isValidFile(path):
    if not os.path.exists(path):
        print("Error: file path '{}' does not exist.".format(path))
        return None
    else:
        return open(path, "r")
    
def encodeString(string):
    return ''.join([hex(ord(index)) for index in string])

def decodeLetter(letter):
    return chr(int(letter,16))

def decodeString(string):

    decodedString = []
    
    for index in range(0,len(string)):
        if string[index] == "0" and string[index+1] == "x":
            decodedLetter = decodeLetter(string[index] + string[index+1] + string[index+2] + string[index+3])
            decodedString.append(decodedLetter)
            
    return ''.join(decodedString)

def encodeFile(f):
    fContents = f.read().splitlines()
    EncodedfContents = [encodeString(index) for index in fContents]
    
    pathName = f.name
    oFname = os.path.basename(f.name) #original filename

    newPath = pathName.replace(".txt","-Encoded") #temporarily take out the ".txt" so we can add a "encoded" suffix.
    newPath = newPath.replace("-Decoded","")
    
    with open(newPath + ".txt","a") as newEncodedFile: #open and write the encoded contents
        for index in EncodedfContents:
            newEncodedFile.write(index + "\n")
    print("\nAn encoded version of the file has been created in the same directory.")

def decodeFile(f):
    fContents = f.read().splitlines()

    decodedfContents = [decodeString(index) for index in fContents]
    
    pathName = f.name
    oFname = os.path.basename(f.name) #original filename

    newPath = pathName.replace(".txt","-Decoded")
    newPath = newPath.replace("-Encoded","")
    
    with open(newPath + ".txt","a") as newDecodedFile: 
        for index in decodedfContents:
            newDecodedFile.write(index + "\n")
    print("\nA decoded version of the file has been created in the same directory.")
    
    


parser = argparse.ArgumentParser()

parser.add_argument("filePath", help="The file you wish to operate on.",type=str) #get the file path

helpText = "Create a copy of the file with the original contents " #to avoid repeating myself when formatting strings.

group = parser.add_mutually_exclusive_group() #add the option to either encode or decode.
group.add_argument("-d","--decode", help="Create an version of the given file decoded from hexadecimal. If the file is already de-coded, this file will be deleted afterwards.".format(helpText), action="store_true")
group.add_argument("-e","--encode", help="Create hexadecimal encoded version of the given file. If the file is already encoded, it is encoded again.".format(helpText), action="store_true")

args = parser.parse_args()

f = isValidFile(args.filePath)

if f:
    if args.encode:
        encodeFile(f)
    if args.decode:
        decodeFile(f)
