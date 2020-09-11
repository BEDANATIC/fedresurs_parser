# Fedresurs_parser
Веб-сервис для получения данных компании и их сообщений с сайта fedresurs.ru
# Установка
1. Установите [Docker](https://www.docker.com/get-started)
2. Клонируйте текущий репозиторий
3. В корне проекта выполните: `sudo docker build -t fedresurs .`, тем самым создав контейнер
4. Запустите контейнер командой: `sudo docker run -p 5000:5000 fedresurs`
# Использованте веб-сервиса
* Для получения идентификаторов компаний отправте запрос на [`http://127.0.0.1:5000/search/company/KEYWORD`](http://127.0.0.1:5000/search/company/KEYWORD), где KEYWORD - ключевое слово для поиска
* Для получения данных о компании отправте запрос на `http://127.0.0.1:5000/company/GUID`[`http://127.0.0.1:5000/company/GUID`](http://127.0.0.1:5000/company/GUID), где GUID - идентификатор компании
* Для сообщений компании отправте запрос на `http://127.0.0.1:5000/company/GUID/messages`[`http://127.0.0.1:5000/company/GUID/messages`](http://127.0.0.1:5000/company/GUID/messages), где GUID - идентификатор компании
