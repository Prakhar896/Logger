from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import mdConverter, os, json
# Load dotenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def fileContent(fileName):
    with open(fileName, 'r') as file:
        fileContent = file.read()
        return fileContent


## EXAMPLE LOG ##
## {
    ## 'type": "normal/error",
    ## "text": "<LOG TEXT>",
    ## "time": "<TIME>"
## }
################

logs = {}
if os.path.isfile('logs.txt'):
    logs = json.load(open('logs.txt', 'r'))
else:
    with open('logs.txt', 'w') as f:
        f.write('{}')
    logs = {}

@app.route('/')
def home():
    return mdConverter.convert(fileContent('home.md')), 200
    
@app.route('/newLog', methods=['POST'])
def newLog():
    if 'LogsAccessCode' in request.headers:
        if request.headers['LogsAccessCode'] == os.environ['LOGS_ACCESS_CODE']:
            if 'type' in request.json and 'text' in request.json and 'clientName' in request.json:
                if request.json['type'] != 'normal' and request.json['type'] != 'error':
                    return "Type is invalid. Type can only be `normal` or `error`.", 400
                log = {
                    'type': request.json['type'],
                    'text': request.json['text'],
                    'clientName': request.json['clientName']
                }

                logs[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = log
                json.dump(logs, open('logs.txt', 'w'))
            else:
                return "Missing `type` or `text` in request", 400
        else:
            return "Invalid access code", 403
    else:
        return "Missing `LogsAccessCode` header in request", 400
    return "Log added successfully!", 200

@app.route('/getLogs', methods=['POST'])
def getLogs():
    if 'LogsAccessCode' in request.headers:
        if request.headers['LogsAccessCode'] == os.environ['LOGS_ACCESS_CODE']:
            logsArray = []
            loopIndex = 0
            for key in logs:
                tempLog = logs[key]
                tempLog["time"] = key
                logsArray.append({"{}".format(loopIndex): tempLog})
                loopIndex += 1
            return json.dumps(logsArray), 200
        else:
            return "Invalid access code", 403
    else:
        return "Missing `LogsAccessCode` header in request", 400

@app.route('/displayLogs', methods=['GET'])
def displayLogs():
    return fileContent('logs.html'), 200

@app.route('/logsJS')
def logsJS():
    return fileContent('logs.js'), 200

if __name__ == "__main__":
    for envVariable in ['LOGS_ACCESS_CODE']:
        if envVariable not in os.environ:
            print("Missing {} environment variable".format(envVariable))
            exit(1)
    app.run(host='0.0.0.0', port=8000)