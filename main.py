from flask import Flask, render_template, request
import myhelp.filework as mf
import myhelp.interface as mi
import subprocess

app = Flask(__name__)
sys = input("OS [WIN|LIN] > ")
if sys == "WIN":
    slash = "\\"
else:
    slash = "/"
    username = input("OS USERNAME > ")

def getInputLog():
    logs = mf.load("consoleinput.json", 2)
    return logs

def addInputLog(text: str, type: str):
    newLog = {"text": text, "type": type}
    logs.append(newLog)
    mf.jsDump("consoleinput.json", logs)
    return logs

def cleanInputLog():
    newLogs = [{"text": "You started command line!", "type": "system"}]
    mf.jsDump("consoleinput.json", newLogs)
    return newLogs

def indexPage(inputLogs):
    return render_template('index.html', logs=inputLogs, lenlogs=len(inputLogs))

cleanInputLog()
logs = getInputLog()

@app.route('/')
def base():
    return indexPage(getInputLog())

@app.route('/sendcommand', methods=['POST'])
def sendcommand():
    data = request.form
    usercommand = data["command"]
    addInputLog(f" > {usercommand}", "user")
    comintp = subprocess.check_output(usercommand.split(), shell=True, env={"HOME": "/home/"})
    addInputLog(comintp, "input")
    return indexPage(getInputLog())
    

@app.errorhandler(404)
def not_found_error(error):
    return "Error 404", 404

@app.errorhandler(500)
def internal_error(error):
    return "Error 500", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")