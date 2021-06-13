# Python 3 server example
# If you use built in iso than you can use the following to donate to developer. (Or to test)
# /root/cpuminer-opt/cpuminer -a yespowerr16 -o stratum+tcp://yenten-pool.info:63368 -u YWFmLx79SEDfhUVe53BxgohyQmmTrEZQkC
using_http_server = False
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    using_http_server = True
except ImportError:
    print("You got the http.server module?")
    exit
using_pyspectator = False
try:
    from pyspectator.processor import Cpu
    using_pyspectator = True
except ImportError:
    print("You got the pyspectator module?")
    print("***WARNING*** Can't do stats without pyspectator")
    pass
using_mega = False # Mega just describes how much to import
try:
    import platform,socket,re,uuid,json,psutil,logging,time,subprocess
    using_mega = True
except ImportError:
    exit
using_distro = False
try:
    import distro
    using_distro = True
except ImportError:
    pass

hostName = "localhost" # This starts the web server to be only localhost, set to 0.0.0.0 for external support
serverPort = 8080 # This sets the web server to http://localhost:8080 instead of just http://localhost but if you want to change
# than set it to 80 as that's default for web applications.

info = {}

signin = { # This is a template for incase you don't have a login.austin file, it would generate this
    "login": "",
    "username": "admin", # TODO - Switch over to md5 to check username/password in 'login.austin'
    "password": "admin" # Also would be nice to add a way to allow changing inside program
# so that user doesn't have to find the md5 of choosen username/password.
}

data = { # This is a template for incase you don't have a config.austin file, it would generate this

    "miner_name": "Sexy Miner",
    "file_name": "server.py",
    "version": "0.0.0"

}

suf = [' Server - ',' Log - '] # Fancy Print Suffixes
suf_log = 1; # Mark where Log is in suf

def fprint(suffix, message): # Fancy Print
    try:
        print(str(suf[suffix] + message))
    except:
        print(str(suf[suf_log] + "Failed to do Fancy Print in " + data[file_name]))

def execute(command, ip): # This is where we handle the connection
    message = []
    comArray = command.split("_")
    if comArray[0] == "/home" or command == "/home":
        return "Welcome home..."
    if comArray[0] == "/stats" or command == "/stats": # This is where we handle /stats
        if using_pyspectator == False:
            return "Please install pyspectator to run /stats as it is needed for CPU information."
        cpu = Cpu(monitoring_latency=1)
        message.append(" HostName - " + str(socket.gethostname()))
        message.append(" System - " + platform.system())
        message.append(" System Release - " + platform.release())
        message.append(" System Version - " + platform.version())
        message.append(" Architecture - " + platform.machine())
        message.append(" Processor - " + platform.processor())
        message.append(" RAM - " + str(round(psutil.virtual_memory().total / (1024.0 **3)))+ " GB")
        message.append(" IP Address - " + str(socket.gethostbyname(socket.gethostname())))
        message.append(" MAC Address - " + ':'.join(re.findall('..', '%012x' % uuid.getnode())))
        message.append(" CPU Temp - " + str(cpu.temperature) + " C")
        message.append(" CPU Load - " + str(cpu.load) + "%")
        return ' <br> '.join(message)
    if comArray[0] == "/signin":
        if comArray[1] == signin["username"] and comArray[2] == signin["password"]:
            signin["login"] = str(ip)
            return "Signed in."
        return "Not signed in."
    if comArray[0] == "/signout":
        if str(ip) == signin["login"]:
            signin["login"] = ""
            return "Signed out."
        return "Not signed in."
    if comArray[0] == "/run":
        if str(ip) != signin["login"]:
            return "101, Not signed in."
        try:
            output = subprocess.getoutput(str(str(comArray[1]) + " " + str(comArray[2]) + " " + str(comArray[3]) + " " + str(comArray[4]) + " " + str(comArray[5]) + " " + str(comArray[6]) + " " + str(comArray[7])).strip())
            return str(output)
        except:
            return "102, Command did not work."
    return "False"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        ### TODO - need to add control panel template into the html so that the miner can look
        ### nice and professional giving any miner the options they need to securely host their
        ### miners online.
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        fprint(1 ,str(self.client_address)) # Sends a print of connected client as Log
        self.wfile.write(bytes(execute(self.path, self.client_address[0] ), "utf-8")) # Do stuff on computer

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    fprint(0 , "Started http://%s:%s" % (hostName, serverPort))
    login = ""

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    fprint(0, "Stopped.")
