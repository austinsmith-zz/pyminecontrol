# pyminecontrol
pyminecontrol is a http server that features a lightweight solution for you to control your crypto-currency miner ensuring that it's performing at it's best.

Setup -
Commands to run : <br>
  pip install pyspectator <br>
  python3 server.py <br>
  
Settings -
Be sure to change the username and password before use as admin/admin is very basic and is there for placeholders.
Be sure to install pyspectator for stats on the /stats page or it won't work as it can't get CPU information.

Purpose -
The purpose of this project is provide a open source option to securely manage your hardware externally without relying on a company/individual on security. Taking example into the solarwinds hack, it's hard to provide a central place to manage your hardware as software can be hacked or just simply misused by anyone. Pyminecontrol takes a step towards providing a option in pure python to manage your server and being able to setup your own security options that can be used for extra security as no one else will know your information or simply have your login information stored.

TODO -
* Add a control panel/dashboard theme to the http server.
* Integrate mining software more closely with pyminecontrol instead of just commands
* Convert Login over to md5
* Encryption to provide security 
