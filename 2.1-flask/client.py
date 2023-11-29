import requests

## Регистариция пользователя:

# response = requests.post('http://127.0.0.1:5000/register', json={'name': 'Vova', 'email_address': 'Vovan@yndex.ru',
#                                                                  'password': 'Vova!@1234'})
## Вход:

# response = requests.post('http://127.0.0.1:5000/login', json={'name': 'Vova', 'email_address': 'Vovan@yndex.ru',
#                                                               'password': 'Vova!@1234'})
## Получение пользователя и всех его обьявлений по id:

# response = requests.get('http://127.0.0.1:5000/user/1')

## Частичное изменение данных пользователя:

# response = requests.patch('http://127.0.0.1:5000/user/1', json={'email_address': 'vladimir@gmai.com'},
#                           headers={'token': '0e4c42c3-aca3-419b-8b55-68bd7f0031af'})
## Удаление пользователя:

# response = requests.delete('http://127.0.0.1:5000/user/5', headers={'token': '8170d15d-6c99-4873-90c7-2862a12a2180'})

## Создание обьявления:

# response = requests.post('http://127.0.0.1:5000/ads', json={'ad_header': 'Разработчик Python',
#                                                             'description': 'Крутое резюме', 'owner_id': 1},
#                          headers={'token': '0e4c42c3-aca3-419b-8b55-68bd7f0031af'})
## Получение обьявления по id:

# response = requests.get('http://127.0.0.1:5000/ads/3')

## Частичное изменение обьявления:

# response = requests.patch('http://127.0.0.1:5000/ads/1', json={'description': 'Крутейшее резюме'},
#                           headers={'token': '0e4c42c3-aca3-419b-8b55-68bd7f0031af'})
## Удаление обьявления:

# response = requests.delete('http://127.0.0.1:5000/ads/3', headers={'token': '0e4c42c3-aca3-419b-8b55-68bd7f0031af'})

print(response.status_code)
print(response.json())
