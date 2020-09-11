import json
import re
from flask import request
from app import app, logging, datasource_manager as ds


@app.route('/')
def greeting():
    return {
            'Instruction': 'SEE README.md'
        }

@app.route('/company/<company_guid>')
def company(company_guid):
    return {
        'company': ds.get_company_info(company_guid)
    }


@app.route('/search/company/<keyword>')
def companies(keyword):
    companies_guid = ds.get_companies_guid_by_keyword(keyword, **request.args)

    return {
        'count': len(companies_guid),
        'guid': companies_guid
    }


@app.route('/company/<company_guid>/messages')
def messages(company_guid):
    regex_filter = request.args.get('regex_filter') or r'банкрот'

    messages_info = []
    messages = ds.get_company_messages(company_guid, **request.args)
    for message in messages:
        if re.search(regex_filter, message.get('text').lower() or ' '):
            messages_info.append(message)

    logging.info(f'Найдено {len(messages_info)} релевантных сообщений компании ({company_guid}) (текст-фильтр: "{regex_filter}")')

    return {
        'count': len(messages_info),
        'messages': messages_info
    }
