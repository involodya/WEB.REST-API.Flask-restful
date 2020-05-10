import requests

# Получение всех работ
print(requests.get('http://127.0.0.1:8080/api/v2/jobs').json())
# Корректное получение одной работы
print(requests.get('http://127.0.0.1:8080/api/v2/jobs/1').json())
# Ошибочный запрос на получение одной работы — неверный id
print(requests.get('http://127.0.0.1:8080/api/v2/jobs/999').json())
# Ошибочный запрос на получение одной работы — строка
print(requests.get('http://127.0.0.1:8080/api/v2/jobs/test').json())
# Верный запрос
print(requests.post('http://127.0.0.1:8080/api/v2/jobs',
                    json={'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1',
                          'is_finished': False}
                    ).json())
# Не передан параметр is_finished
print(requests.post('http://127.0.0.1:8080/api/v2/jobs',
                    json={'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1'}
                    ).json())
# Передача неверного параметра
print(requests.post('http://127.0.0.1:8080/api/v2/jobs',
                    json={'job': '1',
                          'team_leader': 1,
                          'work_size': 'fhfsdh',
                          'collaborators': '1',
                          'is_finished': 123}
                    ).json())
# Убедимся, что работа добавлена
print(requests.get('http://127.0.0.1:8080/api/v2/jobs').json())
# Удалим работу
print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/100').json())
# Несуществующая работа
print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/999').json())
# Ошибочный запрос на удаление работы — строка
print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/test').json())
# Убедимся, что работа удалена
print(requests.get('http://127.0.0.1:8080/api/v2/jobs').json())
