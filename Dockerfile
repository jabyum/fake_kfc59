# язык программирования в контейнере
FROM python:3.12
# создаем папку в контейнере для нашего проекта
WORKDIR /app
# какие файлы и куда мы копируем
COPY . /app
# скачивание зависимостей/библиотек
RUN pip install --no-cache-dir -r requirements.txt
# указываем команду для запуска проекта
CMD ["python", "bot.py"]

