# Garbage Detection Service
Решение представлено в рамках хакатона "Цифровой прорыв. Финал 2021"
Кейс от Минцифры и республики Татарстан по созданию сервиса использования данных с видеокамер
(в том числе детекция мусора на дорогах и заполненности мусорных баков)


### Адрес реализованного демо-решения:

http://3.17.12.94/dashboard/


### Инструкция по локальному развёртыванию и запуску решения

1. установить docker и docker-compose;
2. в папке 'ml' выполнить pip install -r requirements.txt;
3. содержимое файла `env.example` переместить в файл `.env`;
4. в папке с решением выполнить следующие команды:  
   docker-compose pull  
   docker-compose build  
   docker-compose up -d  
после чего на http://localhost:3000/dashboard/ откроется страница по определению заполненности мусорных контейнеров в реальном времени.
5. в папке 'backend\Tester' выполнить python tester.py;
6. для обработки изображений нужно в папке 'ml' выполнить python main.py (предобученные модели https://drive.google.com/drive/folders/1g4ZJm_-37nIbu5IJfG24H_bxpLK0bJoH?usp=sharing предварительно нужно так же поместить в папку 'ml'). Изображения нужно помещать в папку 'ml/image_source'.


### Содержимое репозитория
- Сервис:
	- backend/
	- frontend/
	- grafana/
	- heatmap/
	- ml/
	- nginx/
- R&D:
	- model_faster-rcnn/
	- notebooks/
- presentation.pdf

### Решение команды NoName
