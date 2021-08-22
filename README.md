
# Setup an run:

Add names to **mask_names.csv** if needed

    Localy on django dev server:
        1. Use python 3.8 or above, recommended to use virtual env.
        2. pip install -r requirements.txt
        4. python manage.py runserver 0.0.0.0:80
    
    Using docker-compose (django and nginx):
        1. docker-compose up -d --buld
    
    Using docker:
        1. docker build . -t exercise
        2. docker run --rm -d -p 80:8000 -v <input data folder relative path>:/home/app/web/data exercise python manage.py runserver 0.0.0.0:8000

# Notes
  The server passes requests to https://postman-echo.com in this way:
  https://<server_p>/<endpoint> => https://postman-echo.com/<endpoint>
  so actually https://<server_p>/post will work. But this allows quiqlly to change routing to any othe server. Just update this code in **engine/views.py**:
```python
    
    PATH_TO_SERVER = {
        r'.+': 'https://postman-echo.com'
    }
```
