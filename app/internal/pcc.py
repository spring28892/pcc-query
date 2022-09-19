# -*- coding: utf-8 -*-

import requests, re
from urllib.parse import unquote
from bs4 import BeautifulSoup

sess = requests.session()
url = 'https://pe2sys.pcc.gov.tw/Public/EGR/Report1.aspx?progid=EGR_2_2_1'

def find_value(name, web):
    reg = 'name="' + name + '".+value="(.*)" />'
    pattern = re.compile(reg)
    result  = pattern.findall(web.text)
    try:
        return result[0]
    except:
        return ""

def convert_dic(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def get_viewstate():
  header = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      #"Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "zh-TW,zh;q=0.9",
      "Connection": "keep-alive",
      "Host": "pe2sys.pcc.gov.tw",
      "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
  }

  req = sess.get(url, headers = header)

  __VIEWSTATE = find_value('__VIEWSTATE', req)
  __VIEWSTATEGENERATOR = find_value('__VIEWSTATEGENERATOR', req)
  HiddenField = unquote(req.text.split('ctl00_ctl00_ToolkitScriptManager1_HiddenField&amp;_TSM_CombinedScripts_=')[1].split('"')[0])
  cookie = '; '.join([x+"="+req.cookies[x] for x in req.cookies.get_dict()])

  return __VIEWSTATE, __VIEWSTATEGENERATOR, HiddenField, cookie

def get_license_info(id_input):
    __VIEWSTATE, __VIEWSTATEGENERATOR, HiddenField, cookie = get_viewstate()
    data = {
        "ctl00$ctl00$ToolkitScriptManager1": "ctl00$ctl00$MainContent$MainContent$UpdatePanel_QueryCondition|ctl00$ctl00$MainContent$MainContent$btn_Query",
        "__LASTFOCUS": "",
        "ctl00_ctl00_ToolkitScriptManager1_HiddenField": HiddenField.replace("+"," "),
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": __VIEWSTATE,
        "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
        "ctl00$ctl00$MainContent$MainContent$DDL_Subject": "",
        "ctl00$ctl00$MainContent$MainContent$Qtxt_Engr_Name": "",
        "ctl00$ctl00$MainContent$MainContent$Qtxt_SerialNum": id_input,
        "ctl00$ctl00$MainContent$MainContent$Qtxt_CompSerialNum": "",
        "ctl00$ctl00$MainContent$MainContent$Qtxt_CompName": "",
        "__ASYNCPOST": True,
        "ctl00$ctl00$MainContent$MainContent$btn_Query":"查 詢"
    }
    header = {
        "Accept": "*/*",
        #"Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "4308",
        "Cookie": cookie,
        #"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "pe2sys.pcc.gov.tw",
        "Origin": "https://pe2sys.pcc.gov.tw",
        "Referer": "https://pe2sys.pcc.gov.tw/Public/EGR/Report1.aspx?progid=EGR_2_2_1",
        "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    req = sess.post(url, headers = header, data = data)
    soup = BeautifulSoup(req.text, 'lxml')
    table_list = soup.select('table.main tr td div')
    if len(table_list)>0:
        username = table_list[1].text.strip()
        prac_license_id = table_list[2].text.strip()
        status = table_list[3].text.strip()
        company = table_list[4].text.strip()
        license_id_list = table_list[5].text.strip().split()
        license_id = convert_dic(license_id_list)
        valid_time = table_list[6].text.strip().split("~")
        valid_time_start = valid_time[0].strip()
        valid_time_end = valid_time[1].strip()
        proof_time = table_list[7].text.strip()
        penalty = table_list[8].text.strip()
        return username, prac_license_id, status, company, license_id, valid_time_start, valid_time_end, proof_time, penalty
    else:
        return None

