from flask import Flask, request,render_template
from azure.storage.filedatalake import DataLakeServiceClient
import datetime
import os
import logging

connstr = os.getenv("AZSTR")
container = "azc"
app = Flask(__name__)

service_client = DataLakeServiceClient.from_connection_string(connstr)
file_system_client = service_client.get_file_system_client(container)


@app.route("/updateblob", methods=["POST"])
def update_blob():
    data = request.json
    logging.info(f"POST method update_blob. with json data:{data}")
    
    message = data.get("message")
    if message:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        content = f"{current_time}: {message}\n"
      

        file_client = file_system_client.create_file(file_name)
        file_client.append_data(content, 0, len(content))
        file_client.flush_data(len(content))
        logging.info(f"POST method update_blob finished. output file:{file_name}")
        return "File updated successfully."

    else:
        return "Invalid request"

@app.route('/updateblob', methods=['GET'])
def updateblob():

    data = request.args.get('data')
    
    logging.info(f"POST method update_blob. with json data:{data}")
    
    message = data
    if message:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        content = f"{current_time}: {message}\n"
      

        file_client = file_system_client.create_file(file_name)
        file_client.append_data(content, 0, len(content))
        file_client.flush_data(len(content))
        logging.info(f"POST method update_blob finished. output file:{file_name}")
        return "File updated successfully."

    else:
        return "Invalid request"

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'

@app.route('/tg', methods=['GET'])
def hello3():
    return 'Here is a TEST!'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
