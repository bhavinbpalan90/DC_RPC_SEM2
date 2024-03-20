from rpcClient import RPCClient
import os.path

server = RPCClient('192.168.12.130', 8080)

server.connect()

try:
    Platform=input("Enter Platform : ")
    fileName = input("Enter FileName: ")
    if not os.path.isdir('Contents'):
        os.mkdir('Contents')
    directory = 'Contents/' + str(Platform) + '/'
    if not os.path.isdir(directory):
        os.mkdir(directory)
        print('directory created')
    ##file_path  = os.path.join(directory, fileName)
    file_path = str(os.getcwd()) + str('\Contents\\') + str(Platform) + str('\\') + str(fileName)
    print(file_path)
    handle=open(file_path,"w")
    content = str(server.movefile(str(Platform),str(fileName)))
    handle.write(content)
    print('File Downloaded and available at ' + str(file_path))
    handle.close()
except:
    print ('Download failed')

server.disconnect()