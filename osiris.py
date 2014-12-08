import time
import os

month_lookup = {1: "January", 2: "Febuary", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

expense = [{"name": "Server 1","value": "10.00"},{"name": "botnet+", "value": "50.00"},{"name": "DNS", "value": "5.00"},{"name": "SJW donations", "value": "1.00"}]
income = [{"name": "paypal","value": "10.00"},{"name": "NSA bribes","value": "500.00"}]

i_total = 0.0 #this is a hack
e_total = 0.0

def gen_table_data(i,expense,income):
        html = "  <tr>\r\n"
        global e_total
        global i_total
        if len(expense) > i:
            html += "    <th>%s</th>\r\n" % (expense[i]['name'])
            html += "    <th>%s</th>\r\n" % (expense[i]['value'])
            e_total += float(expense[i]['value'])
        else:
            html += "    <th></th>\r\n"
            html += "    <th></th>\r\n"
        html += "    <th></th>\r\n"

        if len(income) > i:
            html += "    <th>%s</th>\r\n" % (income[i]['name'])
            html += "    <th>%s</th>\r\n" % (income[i]['value'])
            i_total += float(income[i]['value'])
        else:
            html += "    <th></th>\r\n"
            html += "    <th></th>\r\n"
        html += "    <th></th>\r\n"

        html += "  </tr>\r\n"

        return html

def gen_table(data):
    inc = data["inc"]
    exp = data["exp"]

    if len(inc) > len(exp):
        iter = len(inc)
    else:
        iter = len(exp)

    html = ''
    for i in xrange(0,iter):
        html+= gen_table_data(i,expense,income)

    html += gen_table_data(0,[{"name": "Total:","value": e_total}],[{"name": "Total:","value": i_total}]) #todo: clean this up

    return html

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

	if True:
            month = int(access[0:len(access) - 4])
            year = int(access[len(access) - 4:len(access)])
            if month in month_lookup:
                disp_month = month_lookup[month]
            else:
                return {"code": 200, "msg": "Invalid date.", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}

            info = {"exp": expense, "inc": income}

            return {"code": 200, "file": "eval.html", "template": { "gen.table": gen_table(info), "meta.year": str(year), "meta.month" : disp_month }, "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
        else:
            return {"code": 200, "msg": "no data exists for that date", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}

    else:
        return {"code": 200, "file": "index.html", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
