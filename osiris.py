import time
import os

#Todo: use a database and not this file: hack

def reply(msg):

    if msg['header']['PATH'].startswith('/assets'):
        return {"code": 200, "file": msg['header']['PATH'].split('/', 1)[1]}

    elif msg['header']['PATH'] == '/transparency':
        return {"code": 301, "msg": "forward", "header": {"Location": '/transparency/', "X-Powered-By": 'OSIRIS Mach/4'}}

    elif msg['header']['PATH'].startswith('/transparency/'):
        access =  msg['header']['PATH'].split('/')[2]

        if access == '':
            access_month = int(time.strftime("%m"))
            access_year = int(time.strftime("%Y"))

            if access_month == 1:
                access_month = 12
            else:
                access_month -= 1

            return {"code": 301, "msg": "forward", "header": {"Location": "/transparency/%s%s" % (access_month,access_year), "X-Powered-By": 'OSIRIS Mach/4'}}

        else:
            access = "accounting/%s.html" % (access)

	if os.path.exists('/etc/osiris/app/donate/' + access): #poor practice
            return {"code": 200, "file": access, "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
        else:
            return {"code": 200, "msg": "no data exists for that date", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}

    else:
        return {"code": 200, "file": "index.html", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
