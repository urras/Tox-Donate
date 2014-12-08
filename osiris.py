import time
import os

month_lookup = {1: "January", 2: "Febuary", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

expense = [{"name": "Server 1","net": "10.00","gross":"10.00"},{"name": "botnet+", "net": "50.00","gross":"10.00"},{"name": "DNS", "net": "5.00","gross":"10.00"},{"name": "SJW donations", "net": "1.00","gross":"10.00"}]
income = [{"name": "paypal","net": "10.00","gross":"10.00"},{"name": "NSA bribes","net": "500.00","gross":"11.00"}]

enet_total = 0.0 #shameful in production
inet_total = 0.0
egross_total = 0.0
igross_total = 0.0

def gen_table_data(i,x,expense,income):
        html = '<tr class="g">'
        global egross_total
        global enet_total
        global igross_total
        global inet_total
        i2 = i - x
        if i >= x:
            html += '<tr class="r">'
            html += "<td>%s</td>" % (expense[i]['name'])
            html += "<td></td>"
            html += "<td></td>"
            html += "<td>%s</td>" % (expense[i]['gross'])
            html += "<td>%s</td>" % (expense[i]['net'])
            egross_total += float(expense[i]['gross'])
            enet_total += float(expense[i]['net'])
            html += "</tr>"

        else:
            html += '<tr class="g">'
            html += "<td>%s</td>" % (income[i2]['name'])
            html += "<td>%s</td>" % (income[i2]['gross'])
            html += "<td>%s</td>" % (income[i2]['net'])
            html += "<td></td>"
            html += "<td></td>"
            html += "</tr>"
            igross_total += float(income[i2]['gross'])
            inet_total += float(income[i2]['net'])


        html += "</tr>"

        return html

def gen_table(data):
    global egross_total
    global enet_total
    global igross_total
    global inet_total
    inc = data["inc"]
    exp = data["exp"]

    iter = len(inc) + len(exp)

    html = ''
    for i in xrange(0,iter - 2):
        html+= gen_table_data(i,len(inc),expense,income)

    html += '<tr class="g t">'
    html += "<td>Total:</td>"
    html += "<td>%s</td>" % (igross_total)
    html += "<td>%s</td>" % (inet_total)
    html += "<td>%s</td>" % (egross_total)
    html += "<td>%s</td>" % (enet_total)
    html += "</tr>"

    enet_total = 0.0
    inet_total = 0.0
    egross_total = 0.0
    igross_total = 0.0

    return html

def reply(msg):
    table_cache = msg['persist']
    if table_cache == 0:
        table_cache = {}

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

            info_hash = str(month) + str(year)
            if info_hash in table_cache:
                table = table_cache[info_hash]
                print "cached lookup"
            else:
                table = gen_table(info)
                table_cache[info_hash] = table
                print "real work happened"

            return {"code": 200, "file": "eval.html", "template": { "gen.table": table, "meta.year": str(year), "meta.month" : disp_month }, "persist": table_cache, "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
        else:
            return {"code": 200, "msg": "no data exists for that date", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}

    else:
        return {"code": 200, "file": "index.html", "header": {"Content-Type": 'text/html', "X-Powered-By": 'OSIRIS Mach/4'}}
