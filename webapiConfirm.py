from flask import Flask, request
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeFileClient, DataLakeServiceClient
import datetime
import os

connstr = os.getenv("azurestroageconnectstring")
container = "azc"
app = Flask(__name__)

service_client = DataLakeServiceClient.from_connection_string(connstr)
file_system_client = service_client.get_file_system_client(container)


@app.route("/update_blob", methods=["POST"])
def update_blob():
    data = request.json
    message = data.get("message")
    if message:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        content = f"{current_time}: {message}\n"
      

        file_client = file_system_client.create_file(file_name)
        file_client.append_data(content, 0, len(content))
        file_client.flush_data(len(content))

        return "File updated successfully."

    else:
        return "Invalid request"

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
