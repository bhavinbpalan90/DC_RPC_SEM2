from rpcServer import RPCServer
from rpcServer2Server import RPCServer2Server

import xmlrpc
#import xmlrpclib
from xmlrpc.server import SimpleXMLRPCServer
import sys
import os.path
import logging
import socket
import public_ip as ip



print(ip.get())
myPublicIp = ip.get()


logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

logger.info("Server Started at IP address " + str(socket.gethostbyname(socket.gethostname())))
logger.info("Server Started at Port Number " + str(8080))

serverName = str(socket.gethostbyname(socket.gethostname())) + ':' + str(8080)

fileFound = 'No'

def registerFiles(fileName):
    logger.info("Register File Executed")
    metadatafile = str(os.getcwd()) + "/metadataFile.txt"
    with open(metadatafile, 'w') as file1:
        contentLine = str(fileName)
        file1.write(contentLine + '\n')
        return 'Registered File: ' + str(contentLine)
    
def checkFileexistLocal(Platform, FileName):
    logger.info("Checking for " + Platform + " \ " + FileName + " on Local Server" )
    metadatafile = str(os.getcwd()) + "/metadataFile.txt"
    logger.info("Path for Metadata File is " + metadatafile)
    f = open(metadatafile, "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if Platform in line and FileName in line:
            fileFound = 'Yes'
            line = line.replace('\\','/')
            logger.info("Data found at line: " + line)
            finalPath = str(line)
            #print(finalPath)
            return finalPath
    return 'NotFound'

def movefile(Platform, FileName,OriginServer):
    logger.info("Inside Move file Function")
    logger.info(str(OriginServer))
    finalPath = checkFileexistLocal(Platform, FileName)
    logger.info('Response from Checking File Locally was: ' + finalPath)
    if finalPath != 'NotFound':
        try:
            with open(finalPath,"r") as handle:
                resultOutput = str(handle.read())
                logger.info('File Founded Locally and is sent')
                #logger.info(resultOutput)
                handle.close()
                return str(resultOutput)
        except:
            return 'File Not Found'
    else:
        logger.info("File not found locally. Need to check with nearby Server")
        nearestServer = '172.31.2.250'
        if OriginServer != nearestServer:
            fileFound = getFilefromCloseServer(str(nearestServer), 8080,Platform,FileName,OriginServer)
            logger.info('Response from Nearby Server: ' + fileFound)
            if fileFound != 'Not Found':
                fullpath = '../content/' + Platform + '/' + FileName
                with open(fullpath, 'w') as file1:
                    contentLine = str(fileFound)
                    file1.write(contentLine + '\n')
                return fileFound
        logger.info('Original Request Server is same as Next Server')
        return 'File Not Found'
        ## Get the Content from Another Server   
        
def getFilefromCloseServer(ipaddress, portno, platformName, fileName,OriginServer):
    logger.info('CP3: Checking with Closed server...')
    
    try:
        server2server = RPCServer2Server(str(ipaddress), int(portno))
        server2server.connect()
        Platform=str(platformName)
        fileName = str(fileName)
        if not os.path.isdir('../content'):
            os.mkdir('../content')    
        directory = '../content/' + str(Platform) + '/'
        if not os.path.isdir(directory):
            os.mkdir(directory)
            print('directory created')
        file_path  = os.path.join(directory, fileName)
        fullpath = str(Platform) + str('/') + str(fileName)
        logger.info('File requested is found at: ' + fullpath)
        handle=open(file_path,"w")
        content = str(server2server.movefile(str(Platform),str(fileName),str(OriginServer)))
        #logger.info('CP4: ' + content)
        handle.write(content)
        handle.close()
        return content
    except:
        logger.info('Could not get data from Nearby Server')
        return 'Not Found'

server = RPCServer()

server.registerMethod(registerFiles)
server.registerMethod(movefile)

server.run()
