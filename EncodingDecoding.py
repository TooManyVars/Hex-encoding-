from time import sleep

#Main funtions for encryption/decryption
##########################################################


def encryptString(string):
  return ''.join([hex(ord(index)) for index in string]) #converts the string to an array in which each index is in hexadecimal version, and then returns it.

def decryptLetter(hexLetter): #returns the decrypted version of a hexadecimal letter.
  return chr(int(hexLetter,16))

def decryptString(phrase):
  decryptedString = [] #where we will store the decrytped string.

  for index in range(0,len(phrase)): #iterate through the string
    if phrase[index] == "0" and phrase[index+1] == "x": #look for an 0x prefix
      decryptedLetter = chr(int(phrase[index]+phrase[index+1]+phrase[index+2]+phrase[index+3],16)) #take the next 2 indexes, plus that 0x prefix and put them into a combined seperate string, converting this string (for example "0x60" to an int and then a letter.)
      decryptedString.append(decryptedLetter) 


  return ''.join(decryptedString)


#functions for file handling
##########################################################

def getFilePath(): #gets the desired file(exception safe)

  print("\n\nEnter the deisred file name/file path:")
  loop = True 

  while(loop):

    try:
      path = input()

      if path.lower() == "ex":
        return None
      else:
        with open(path,"r") as file: #read contents of the file to check to see if the file is valid/exists or not. if not, this behaviour will raise the fileNotFoundError.
          f = file.read() 
        loop = False #if an exception is not raised by this point, the file is valid, meaning that we can exit the loop.
    except FileNotFoundError:
        print("\nFile does not exist.\nPlease re-enter the path name and try again, or type 'ex' to return to the main menu")
    except Exception:
        print("\nSomething went wrong. please re-enter the file directory and try again.")

  return path
      

def encryptFile(path):
  fileContents = [] #declare the file contents as an array so that we can put readlines() into it.
  encryptedFileContents = [] 
  
  with open(path, "r") as file:
    fileContents = file.read().splitlines()
  
  encryptedFileContents = [encryptString(fileContents[index]) for index in range(0,len(fileContents))]

  with open(path,"a+") as file:
    file.truncate(0)
    for index in encryptedFileContents:
      file.write(index)
      file.write("\n")
  print("File successfully encrypted.\n")
    

def decryptFile(path):
  warning = str(input("\nWarning: decryption process will ignore/overwrite any plaintext characters. proceed?"))

  if warning.lower() == "no": #small little proceed message before decryption.
      return None

  fileContents = []
  decryptedFileContents = []

  with open(path, "r") as file:
    fileContents = file.read().splitlines()

  decryptedFileContents = [decryptString(fileContents[index]) for index in range(0,len(fileContents))]

  with open(path,"a+") as file:
    file.truncate(0)
    for index in decryptedFileContents:
      file.write(index)
      file.write("\n")
  print("File successfully decrypted.")
  


#function for the CLI 
##########################################################


def showInterfaceActions():
  print("-(De)crypt\n-(En)crypt\n-(Ex)it")

def interface():

  print("File encryption/decryption script\n")
  sleep(1)

  print("Menu:")
  showInterfaceActions()

  #De = decrypt file
  #En = encrypt file
  #Ex = exit
  #upper/lower case is irrelevant when entering these commands.
  action = str(input("Enter desired command:"))
  action = action.lower()
  
  while action != "de" and action != "en" and action != "ex":
    print("\nCommand is invalid; please re enter, using one of the following:")
    showInterfaceActions()
    action = str(input())
    action = action.lower() 
  
  if action == "ex":
    exit()

  elif action == "de" or "en":
    path = getFilePath()

    if path != None and action == "en":
     encryptFile(path)
    elif path != None and action == "de":
     decryptFile(path)

  sleep(1)
  print("\nTerminating program...")
  sleep(1)


#All of the main functions.
#encryptFile(getFilePath())
#decryptFile(getFilePath())
interface()
