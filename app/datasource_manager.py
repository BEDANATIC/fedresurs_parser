from app import models, parser, db, logging
from datetime import datetime

def get_companies_guid_by_keyword(keyword, **kwargs):
    logging.info(f'Получение guid компаний с сервера по ключевому слову -> {keyword}')
    companies_guid = parser.get_companies_guid_by_keyword(keyword, **kwargs)
    logging.info(f'Найдено {len(companies_guid)} компаний по ключевому слову -> {keyword}')
    return companies_guid

def get_company_info(company_guid):
    company_info = {}

    company_from_db = models.Companies.query.filter_by(guid=company_guid).first()
    logging.info(f'Попытка получить информацию о компании ({company_guid}) из базы данных')
    if company_from_db:
        company_info = company_from_db.asdict()
        logging.info(f'Информация о компании ({company_guid}) получена из базы данных')
    else:
        logging.info(f'Информации о компании ({company_guid}) НЕТ в базе данных')
        logging.info(f'Попытка получить информацию о компании ({company_guid}) от сервера')
        company_info_from_parser = parser.get_company_info(company_guid)
        if company_info_from_parser != {}:
            logging.info(f'Информация о компании ({company_guid}) получена от сервера')
            company_info = company_info_from_parser
            db.session.add(models.Companies(**company_info_from_parser))
            db.session.commit()
        else:
            logging.info(f'Компания ({company_guid}) не найдена ')

    return company_info

def get_company_messages(company_guid):
    messages_info = []

    messages_info_from_db = models.Messages.query.filter_by(owner_guid=company_guid).all()
    logging.info(f'Попытка получить сообщения компании ({company_guid}) из базы данных')
    if messages_info_from_db:
        logging.info(f'Сообщения компании ({company_guid}) получены из базы данных')
        for message_info_from_db in messages_info_from_db:
            messages_info.append(message_info_from_db.asdict())
    else:
        logging.info(f'Сообщения компании ({company_guid}) НЕТ в базе данных')
        logging.info(f'Попытка получить сообщения компании ({company_guid}) от сервера')
        messages_info_from_parser = parser.get_company_messages(company_guid)
        if len(messages_info_from_parser) > 0:
            logging.info(f'Сообщения компании ({company_guid}) получены от сервера')
            for message in messages_info_from_parser:
                if message == {}:
                    continue
                messages_info.append(message)
                message['owner_guid'] = company_guid
                db.session.add(models.Messages(**message))
            db.session.commit()

    if len(messages_info) == 0:
        logging.info(f'Сообщения компании ({company_guid}) НЕ найдены')
    else:
        logging.info(f'Найдено {len(messages_info)} сообщений компании ({company_guid})')

    return messages_info
