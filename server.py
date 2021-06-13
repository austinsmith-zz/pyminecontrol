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
    import platform,socket,re,uuid,json,psutil,logging,time,subprocess,mimetypes
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

signin = { # This is a template for incase you don't have a login.austin file, it would generate this
    "login": "",
    "username": "admin", # TODO - Switch over to md5 to check username/password in 'login.austin'
    "password": "admin" # Also would be nice to add a way to allow changing inside program
# so that user doesn't have to find the md5 of choosen username/password.
}

data = { # This is a template for incase you don't have a config.austin file, it would generate this

    "commands": ['/stats'], # place commands here for them to be used as shortcodes
    "miner_name": "Sexy Miner",
    "file_name": "server.py",
    "version": "0.0.0",
    "404_redirect": "home.aus" # your redirect page

}

suf = [' Server - ',' Log - '] # Fancy Print Suffixes
suf_log = 1; # Mark where Log is in suf

def fprint(suffix, message): # Fancy Print
    try:
        print(str(suf[suffix] + message))
    except:
        print(str(suf[suf_log] + "Failed to do Fancy Print in " + data[file_name]))

def load_send(file_line, ip):
    k = file_line.split(" ")
    need = False
    c = -1
    for i in k:
        c += 1
        h = i.strip("~")
        w = h.split("_")
        if i in data["commands"] and not need:
            need = True
            k[c] = execute(h,ip) # K works but deletes sentence
        if w[0] in data["commands"] and not need:
            need = True
            k[c] = execute(h,ip)
    if need:
        return bytes(' '.join(k), "utf-8") 
    return bytes(file_line, "utf-8")

def execute(command, ip): # This is where we handle the connection
    message = []
    comArray = command.split("_")
    if comArray[0] == "/home" or command == "/home":
        return "Welcome home..."
    if comArray[0] == "/stats" or command == "/stats": # This is where we handle /stats
        if using_pyspectator == False:
            return "Please install pyspectator to run /stats as it is needed for CPU information."
        cpu = Cpu(monitoring_latency=1)
        try:
            comArray[1] = comArray[1]
        except:
            return "Please remember to add args to shortcodes with '_'"
        if comArray[1] == "hostname":
            return str(socket.gethostname())
        if comArray[1] == "system":
            return str(platform.system())
        if comArray[1] == "release":
            return str(platform.release())
        if comArray[1] == "version":
            return str(platform.version())
        if comArray[1] == "machine":
            return str(platform.machine())
        if comArray[1] == "processor":
            return str(platform.processor())
        if comArray[1] == "ram":
            return str(round(psutil.virtual_memory().total / (1024.0 **3)))+ " GB"
        if comArray[1] == "ip":
            return str(socket.gethostbyname(socket.gethostname()))
        if comArray[1] == "mac":
            return ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        if comArray[1] == "temp":
            return str(cpu.temperature) + " C"
        if comArray[1] == "load":
            return str(cpu.load) + "%"
        return command
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
        fprint(1, str(self.path).strip("/"))
        try:
            filepath = str(self.path).strip("/")
            f = open(filepath.strip("/"), "r")
            mimetype, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            w = filepath.split(".")
            for s in f:
                if w[1] == "css" or w[1] == "js":
                    #fprint(1, w[1])
                    self.wfile.write(bytes(s, "utf-8"))
                else:
                    self.wfile.write(load_send(s, self.client_address[0]))

            f.close()
        except:
            try:
                fprint(1, "Started backup procs...")
                filepath = str(self.path).strip("/") + ".aus"
                f = open(filepath.strip("/"), "r")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                for s in f:
                    self.wfile.write(load_send(s, self.client_address[0]))
                f.close()
            except:
                filepath = data["404_redirect"]
                f = open(filepath.strip("/"), "r")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                for s in f:
                    self.wfile.write(load_send(s, self.client_address[0]))
                f.close()
        fprint(1 ,str(self.client_address)) # Sends a print of connected client as Log
        #self.wfile.write(bytes(execute(self.path, self.client_address[0] ), "utf-8")) # Do stuff on computer

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    fprint(0 , "Started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    fprint(0, "Stopped.")
