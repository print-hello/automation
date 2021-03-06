import time
import subprocess
import requests
from dbconnection import fetch_one_sql


def check_vpn():
    p = subprocess.Popen('.\\checkvpn.bat', shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while curline != b'':
        curlines = str(curline).replace('\\r\\n', '')
        curline = p.stdout.readline()
    p.wait()
    print(curlines)
    if curlines != "b'network is OK'":
        return 0
    else:
        return 1


def rasphone_vpn():
    p = subprocess.Popen('.\\rasphonevpn.bat', shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while curline != b'':
        # print(curline)
        curline1 = str(curline).replace("\\r\\n", "")
        curline = p.stdout.readline()
    p.wait()


def get_out_ip():
    url = "http://2019.ip138.com/ic.asp"
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print('ip:' + ip)
    return ip


def connect_vpn(conn, vpn):
    sql = 'SELECT account, pwd, server, ip from vpn where account=%s'
    result = fetch_one_sql(conn, sql, vpn)
    if result:
        vpn = result['account']
        vpn_pwd = result['pwd']
        vpn_ip = result['ip']
        vpn_server = result['server'].replace('.lianstone.net', '')
        with open(".\\vpn.txt", "w", encoding='utf-8') as fp:
            print(vpn_server + "," + vpn + "," + vpn_pwd)
            fp.write(vpn_server + "," + vpn + "," + vpn_pwd)
    else:
        print(
            'No corresponding VPN account has been detected and the system is being shut down...')
        time.sleep(600)
        os.system('Shutdown -s -t 0')
    print('Disconnect the original VPN connection')
    rasphone_vpn()
    print('Handling new VPN...')
    check_vpn()
    net_ip = get_out_ip()
    while True:
        if net_ip == vpn_ip:
            print('VPN connection IP is correct!')
            break
        else:
            check_vpn()
            time.sleep(10)
            net_ip = get_out_ip()
