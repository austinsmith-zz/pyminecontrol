# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pyspectator.processor import Cpu
import platform,socket,re,uuid,json,psutil,logging
import subprocess
using_distro = False
try:
    import distro
    using_distro = True
except ImportError:
    pass

hostName = "localhost"
serverPort = 8080

info = {}

def getSystemInfo():
    try:
        info = {}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return ' <br> '.join(' = '.join((key,val)) for (key,val) in info.items())
    except Exception as e:
        return str(logging.exception(e))

def execute(command):
    message = []
    comArray = command.split("_")
    if comArray[0] == "/stats" or command == "/stats":
        cpu = Cpu(monitoring_latency=1)
        message.append(getSystemInfo())
        message.append(" CPU Temp - " + str(cpu.temperature) + " <br> ")
        message.append(" CPU Load - " + str(cpu.load) + " <br> ")
        return ' <br> '.join(message)
    if comArray[0] == "/run":
        try:
            output = subprocess.getoutput(str(str(comArray[1]) + " " + str(comArray[2]) + " " + str(comArray[3]) + " " + str(comArray[4]) + " " + str(comArray[5]) + " " + str(comArray[6]) + " " + str(comArray[7])).strip())
            return str(output)
        except:
            return "run didn't work."
    return "False"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(execute(self.path), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
