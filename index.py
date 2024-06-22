from flask import Flask, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

connect_str = "DefaultEndpointsProtocol=https;AccountName=testingchris239s;AccountKey=Fv3mkeKBRbqBcczbNQCRBKb7Q2F3bbc3kzg8UEQtxEJKNxmr1gqJlcw6y5Si+pRUK59ztroH6J21+AStuGi8vQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "images"
container_client = blob_service_client.get_container_client(container_name)

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Image</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f2f2f2;
                }
                .container {
                    text-align: center;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                form {
                    margin-top: 20px;
                }
                input[type="file"] {
                    padding: 10px;
                    margin: 10px 0;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-decoration: none;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 5px;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Upload Image</h1>
                <form method="post" action="/upload" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file)
        return redirect(url_for('home'))
    return "No file uploaded", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


