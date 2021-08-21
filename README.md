
Setup an run:

    Localy on django dev server:
        1. Use python 3.8 or above, recommended to use virtual env.
        2. pip install -r requirements.txt
        3. python manage.py setup --input_data <path to json data>
        4. python manage.py runserver 0.0.0.0:80
    
    Using docker-compose (django and nginx):
        1. docker-compose up -d --buld
        2. docker-compose exec django python3 manage.py setup --input_data <path to json data>
    
    Using docker:
        1. docker build . -t exercise
        2. docker run --rm -d -p 80:8000 -v <input data folder relative path>:/home/app/web/data exercise python manage.py runserver 0.0.0.0:8000
        4. docker ps (to get container id)
        3. docker exec <container id> python3 manage.py setup --input_data <relative path to json data>
