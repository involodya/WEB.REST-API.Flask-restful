import requests

# Получение всех работ
print(requests.get('http://127.0.0.1:8080/api/v2/users').json())
# Корректное получение одной работы
print(requests.get('http://127.0.0.1:8080/api/v2/users/1').json())
# Ошибочный запрос на получение одной работы — неверный id
print(requests.get('http://127.0.0.1:8080/api/v2/users/9999').json())
# Ошибочный запрос на получение одной работы — строка
print(requests.get('http://127.0.0.1:8080/api/v2/users/test').json())
# Верный запрос
print(requests.post('http://127.0.0.1:8080/api/v2/users',
                    json={'surname': '1',
                          'name': '2',
                          'age': 21,
                          'position': 'astronaut',
                          'speciality': 'scientist',
                          'address': 'module_2',
                          'email': 'test239@mars.org'}
                    ).json())
# Не передан параметр age
print(requests.post('http://127.0.0.1:8080/api/v2/users',
                    json={'surname': '1',
                          'name': '2',
                          'position': 'astronaut',
                          'speciality': 'scientist',
                          'address': 'module_2',
                          'email': 'test239@mars.org'}
                    ).json())
# Передача неверного параметра
print(requests.post('http://127.0.0.1:8080/api/v2/users',
                    json={'surname': '1',
                          'name': '2',
                          'age': 'grssg',
                          'position': 'astronaut',
                          'speciality': 'scientist',
                          'address': 'module_2',
                          'email': 'test238@mars.org'}
                    ).json())
# Убедимся, что работа добавлена
print(requests.get('http://127.0.0.1:8080/api/v2/users').json())
# Удалим работу
print(requests.delete('http://127.0.0.1:8080/api/v2/users/100').json())
# Несуществующая работа
print(requests.delete('http://127.0.0.1:8080/api/v2/users/999').json())
# Ошибочный запрос на удаление работы — строка
print(requests.delete('http://127.0.0.1:8080/api/v2/users/test').json())
# Убедимся, что работа удалена
print(requests.get('http://127.0.0.1:8080/api/v2/users').json())
