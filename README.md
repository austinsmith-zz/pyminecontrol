# pyminecontrol
pyminecontrol is a http server that features a lightweight solution for you to control your crypto-currency miner ensuring that it's performing at it's best.
<br>
Look at wiki for pictures. <br>
<br>
Setup - <br>
Commands to run : <br>
* Linux --- sudo apt-get install python3 python3-pip
* Windows --- Go find python3 and download it, remember it's free.
* pip install pyspectator <br>
* python3 server.py <br>
  
***NOTICE*** <br>
This project uses a theme from html5 template (windows) to provide a graphical frontend for people to manage their servers. The only piece of data that is licensed in the license provided by this github is the 'server.py' and only that file is licensed as GPL v2.0 while html5 template requires you to leave on the footer link while using their themes. Guides will be made for you to understand how to convert your own themes. 
  
Settings - <br>
Be sure to change the username and password before use as admin/admin is very basic and is there for placeholders.
Be sure to install pyspectator for stats on the /stats page or it won't work as it can't get CPU information.

Use Case(s) - <br>
In order to provide some use to this program, I decided that I'm going to look into how I can make it more stable for developers to take and use for whatever even if it isn't crypto-currency mining but instead wanted a more friendly http backend to provide system information or to do commands on their external server. The python script will feature shortcodes that can be developed to whatever you need to it be so that you can use it how you like it, future development is built upon the idea of the purpose and use cases combined.

Purpose - <br>
The purpose of this project is provide a open source option to securely manage your hardware externally without relying on a company/individual on security. Taking example into the solarwinds hack, it's hard to provide a central place to manage your hardware as software can be hacked or just simply misused by anyone. Pyminecontrol takes a step towards providing a option in pure python to manage your server and being able to setup your own security options that can be used for extra security as no one else will know your information or simply have your login information stored.

TODO - <br>
* Add a control panel/dashboard theme to the http server. **DONE**
* Fill in theme to what is needed of the miner such as filling in the window content.
* Integrate mining software more closely with pyminecontrol instead of just commands.
* Convert Login over to md5.
* Encryption for more security.
