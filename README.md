Добавление события:curl -X POST -H "Content-Type: application/json" -d '{"date": "2024-01-10", "title": "Встреча", "text": "Обсуждение проекта"}' http://127.0.0.1:5000/api/v1/calendar/add


Получение списка всех событий
:curl http://127.0.0.1:5000/api/v1/calendar/list


Чтение деталей события по ID:
curl http://127.0.0.1:5000/api/v1/calendar/read/1


Обновление события по ID:

curl -X PUT -H "Content-Type: application/json" -d '{"date": "2024-01-11", "title": "Обновленная встреча", "text": "Новое описание"}' http://127.0.0.1:5000/api/v1/calendar/update/1


Удаление события по ID:
curl -X DELETE http://127.0.0.1:5000/api/v1/calendar/delete/1


