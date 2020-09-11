import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Referer': 'https://fedresurs.ru/'
}


def get_companies_guid_by_keyword(keyword, **kwargs):
    company_search_url = 'https://fedresurs.ru/backend/companies/search'
    # параметры для фильтрации поиска
    data = {
        'entitySearchFilter': {
            'regionNumber': None,
            'startRowIndex': '0',
            'pageSize': '10000',
            'name': keyword,
            'legalCase': None,
            'onlyActive': True
        }
    }

    if kwargs != {}:
        data.update(kwargs)

    companies_guid = []
    try:
        response = session.post(company_search_url, data=json.dumps(data))
        page_data = json.loads(response.text)['pageData']
        companies_guid = [company_info['guid'] for company_info in page_data]

    except Exception:
        pass

    return companies_guid


def get_company_info(company_guid):
    url = f'https://fedresurs.ru/backend/companies/{company_guid}'
    company_info = {}
    try:
        company_info_json = json.loads(session.get(url).text)

        company_info['guid'] = company_guid
        company_info['address'] = company_info_json['companyInfo']['egrulAddress']
        company_info['fullName'] = company_info_json['companyInfo']['fullName']
        company_info['inn'] = company_info_json['companyInfo']['inn']
        company_info['kpp'] = company_info_json['companyInfo']['kpp']
        company_info['ogrn'] = company_info_json['companyInfo']['ogrn']
        
    except Exception:
        pass

    return company_info


def _get_company_messages_guid(company_guid, **kwargs):
    url = 'https://fedresurs.ru/backend/companies/publications'
    data = {
        'guid': company_guid,
        'pageSize': '10000',
        'startRowIndex': '0',
        'startDate': None,
        'endDate': None,
        'messageNumber': None,
        'bankruptMessageTypeGroupId': None,
        'legalCaseId': None,
        'searchAmReport': True,
        'searchFirmBankruptMessage': True,
        'searchFirmBankruptMessageWithoutLegalCase': False,
        'searchSfactsMessage': True,
        'searchSroAmMessage': True,
        'searchTradeOrgMessage': True,
        'sfactMessageType': None,
        'sfactsMessageTypeGroupId': None
    }

    if kwargs != {}:
        data.update(kwargs)

    messages_guid = []
    try:
        messages_json = session.post(url, data=json.dumps(data))
        messages_guid = [message['guid']
                                 for message in json.loads(messages_json.text)['pageData']]

    except Exception:
        pass

    return messages_guid


def _get_message_info(message_guid):
    message_info = {}
    try:
        url = f'https://bankrot.fedresurs.ru/MessageWindow.aspx?ID={message_guid}'
        message_html = session.post(url).text

        bs = BeautifulSoup(message_html, 'html.parser')

        raw_date = bs.find(['td', 'tr'], string=re.compile(r'\d{2}\.\d{2}\.\d{4}')).text
        raw_text = bs.find(class_='msg').text
        message_info['text'] = re.sub(r'Текст:', '', raw_text)
        message_info['url'] = url
        # Формат даты в ответе -> '      03.03.20        '
        message_info['date'] = datetime.strptime(re.sub(r'\s', '', raw_date), '%d.%m.%Y')
        message_info['guid'] = message_guid
    except:
        try:
            url = f'https://fedresurs.ru/backend/sfactmessages/{message_guid}'
            massage_json = json.loads(session.get(url).text)
            message_info['text'] = massage_json['content']['text']
            message_info['url'] = url
            # Формат даты в ответе -> '2020-08-28T09:58:15.89'
            raw_date = massage_json['datePublish']
            message_info['date'] = datetime.strptime(raw_date[:10], '%Y-%m-%d')
            message_info['guid'] = message_guid

        except Exception:
            message_info = {}

    return message_info


def get_company_messages(company_guid, **kwargs):
    company_messages_guid = _get_company_messages_guid(company_guid, **kwargs)
    company_messages_info = [_get_message_info(message_guid) for message_guid in company_messages_guid]
    return company_messages_info