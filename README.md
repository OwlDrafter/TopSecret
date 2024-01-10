curl -X POST -H "Content-Type: application/json" -d '{"date": "2024-01-10", "title": "Встреча", "text": "Обсуждение проекта"}' http://127.0.0.1:5000/api/v1/calendar/add


curl http://127.0.0.1:5000/api/v1/calendar/list


curl http://127.0.0.1:5000/api/v1/calendar/read/1


curl -X PUT -H "Content-Type: application/json" -d '{"date": "2024-01-11", "title": "Обновленная встреча", "text": "Новое описание"}' http://127.0.0.1:5000/api/v1/calendar/update/1


curl -X DELETE http://127.0.0.1:5000/api/v1/calendar/delete/1


