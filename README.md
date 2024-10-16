# logparse
 Парсер Nginx логов на Django.

```bash
git clone https://github.com/avgalaida/logparse.git
cd logparse
docker-compose up --build    
docker-compose exec web python manage.py migrate   
```

### Тесты
```
docker-compose exec web python manage.py test   
``` 

### Команда
```
docker-compose exec web python manage.py parse_log 'https://drive.google.com/file/d/18Ss9afYL8xTeyVd0ZTfFX9dqja4pBGVp/view?usp=sharing'
```

### Админ
```
docker-compose exec web python manage.py createsuperuser
```

### Ендпоинты

http://localhost:8000/api/ \
http://localhost:8000/swagger/ \
http://localhost:8000/admin/ 
