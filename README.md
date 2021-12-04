# Garbage-Detection-Service
Решение представлено в рамках хакатона "Цифровой прорыв. Финал 2021"  

Инструкция по развёртыванью и запуску решения

1. установить docker и docker-compose;
2. в папке 'ml' выполнить pip install requirements.txt;
3. в папке с решением выполнить следующие команды:  
   docker-compose pull  
   docker-compose build  
   docker-compose up -d  
после чего на http://localhost:3000/dashboard/ будет доступен сервис по определению заполненности мусорных контейнеров в реальном времени.
4. в папке 'backend\Tester' выполнить python tester.py;
5. для обработки изображений нужно в папке 'ml' выполнить python main.py (предобученные модели https://drive.google.com/drive/folders/1g4ZJm_-37nIbu5IJfG24H_bxpLK0bJoH?usp=sharing предворительно нужно так же поместить в папку 'ml'). Изображения нужно помещать в папку 'ml/image_source'.
