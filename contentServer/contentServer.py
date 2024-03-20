from rpcContentServer import RPCContentServer
import pathlib
import streamlit as st
from io import StringIO
import os
import pandas as pd


if not os.path.isdir('../content/Netflix'):
            os.mkdir('../content/Netflix')
if not os.path.isdir('../content/Prime'):
            os.mkdir('../content/Prime')
if not os.path.isdir('../content/HBO'):
            os.mkdir('../content/HBO')

def save_uploadedfile(uploadedfile,platformName):
     filepath = '../content/' + platformName + '/' + str(uploadedfile.name)
     with open(filepath,"wb") as f:
         f.write(uploadedfile.getbuffer())
         update_server()
     return st.success("File registed with the server")



def update_server():
    server = RPCContentServer(socket.gethostbyname(socket.gethostname()), 8080)
    server.connect()
    Content = pathlib.Path('../content/')
    for files in Content.rglob('*.*'):
        print(files.resolve())
        print(server.registerFiles(str(files.resolve())))
    server.disconnect()

platform = st.selectbox(
    'Please select the Platform for which you want to update the content',
    ('Netflix', 'Prime', 'HBO'))

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    save_uploadedfile(uploaded_file,platform)
    

