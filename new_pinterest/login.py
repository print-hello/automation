from selenium import webdriver
import time
import requests
import json
from dbconnection import commit_sql
import pymysql


def login(driver, email, pwd, account_id, cookie, conn):
    login_url = 'https://www.pinterest.com/login/?referrer=home_page'
    login_flag = ''
    # if cookie:
    #     login_state = cookieLogin(driver, cookie)
    # else:
    #     login_state = 0

    # if login_state == 0:
    driver.get(login_url)
    if driver.page_source.find('This site can’t be reached') > -1:
        login_state = 2
        print('Net error!')
        return login_state
    elif driver.page_source.find("This page isn’t working") > -1:
        login_state = 2
        print('Net error!')
        return login_state
    else:
        driver.find_element_by_name("id").send_keys(email)
        driver.find_element_by_name("password").send_keys(pwd)
        driver.find_element_by_xpath("//form//button").click()
        time.sleep(5)
    # Determine if the login was successful
    try:
        login_flag = driver.find_element_by_xpath('//form//button/div').text
    except:
        pass
    if login_flag == 'Log in':
        login_state = 0
    else:
        login_state = 1
        cookies = driver.get_cookies()
        cookies = json.dumps(cookies)
        cookies = cookies.replace('\\', '\\\\')
        cookies = cookies.replace('\"', '\\"')
        sql = "UPDATE account set cookie=%s where id=%s"
        commit_sql(conn, sql, (cookies, account_id))
    return login_state
    

def cookieLogin(driver, cookie):
    login_url = 'https://www.pinterest.com/login/?referrer=home_page'
    login_flag = ''
    driver.get(login_url)
    print('cookieLogin...')
    # clear cookies, To prevent the automatic login to other accounts 
    driver.delete_all_cookies()
    time.sleep(2)
    try:
        cookies = json.loads(cookie)
        for coo in cookies:
            coo.pop('domain')
            driver.add_cookie(coo)
        driver.refresh()
    except Exception as e:
        print('The cookies is invalid. You are trying to login')
        login_state = 0
        return login_state
    time.sleep(5)
    try:
        login_flag = driver.find_element_by_xpath('//form//button/div').text
    except:
        pass
    if login_flag == 'Log in':
        login_state = 0
    else:
        login_state = 1
    return login_state
