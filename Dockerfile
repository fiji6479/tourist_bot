# Используйте официальный образ Python
FROM python:3.8

# Установите зависимости вашего проект
#рабочая директория внутри контейнера
WORKDIR /tourist_bot
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируйте все файлы проекта в контейнер
COPY . /tourist_bot

ARG OC=my_default_value

# Определите команду для запуска вашего бота
CMD ["python", "./bot/bot_app.py", "OC"]
