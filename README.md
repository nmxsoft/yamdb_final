![finaltask](https://github.com/nmxsoft/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## REST API YamDB - база отзывов о фильмах, музыке и книгах

### Стек

- Python 3.7.0
- Django 2.2.16
- DRF 3.12.4
- Nginx
- docker-compose

### Описание

Это практическое задание, выполненное в ходе подготовки к командной работе.

### Результат 

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Ресурсы API YaMDb

- Ресурс ***auth***: аутентификация.
- Ресурс ***users***: пользователи.
- Ресурс ***titles***: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс ***categories***: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс ***genres***: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс ***reviews***: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс ***comments***: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.
***Путь к документации (redoc) в блоке описания запуска проекта***.

### Самостоятельная регистрация пользователя

1. Пользователь отправляет POST-запрос с параметрами "email" и "username" на эндпоинт:
```
/api/v1/auth/signup/
```
2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами "username" и "confirmation_code" на эндпоинт:
```
/api/v1/auth/token/
```
4. В ответе на запрос ему приходит token (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт:
```
/api/v1/users/me/
```
и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт:
```
/api/v1/users/
```
Описание полей запроса для этого случая — в документации. После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт (письмо с кодом подтверждения пользователю не отправляется):
```
/api/v1/auth/signup/
```
В ответ должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами "username" и "confirmation_code" на эндпоинт:
```
/api/v1/auth/token/
```
В ответе на запрос приходит token (JWT-токен), как и при самостоятельной регистрации.

### Как запустить проект:

1. Клонировать репозиторий:

```
git clone https://github.com/nmxsoft/yamdb_final.git
```

2. Добавить в клонированный репозиторий секреты (Settings/Secrets):

```
Переменная: USER, значение: <имя пользователя для подключения к серверу>
```
```
Переменная: HOST, значение: <публичный ip-адрес сервера>
```
```
Переменная: SSH_KEY, значение: <закрытый ssh-ключ для подключения к серверу>
```
```
Переменная: PASSPHRASE, значение: <пароль, если ssh-ключ защищён паролем>
```
```
Переменная: DOCKER_USERNAME, значение: <имя пользователя для поключения к DockerHub>
```
```
Переменная: DOCKER_PASSWORD, значение: <пароль для поключения к DockerHub>
```
```
Переменная: DB_ENGINE, значение: django.db.backends.postgresql
```
```
Переменная: DB_HOST, значение: db
```
```
Переменная: DB_NAME, значение: postgres
```
```
Переменная: DB_PORT, значение: 5432
```
```
Переменная: POSTGRES_USER, значение: postgres
```
```
Переменная: POSTGRES_PASSWORD, значение: postgres
```
```
Переменная: TELEGRAM_TO, значение: <токен Вашего телеграм-аккаунта>
```
```
Переменная: TELEGRAM_TOKEN, значение: <токен Вашего телеграм-бота>
```

3. В файле 
```
/infra/nginx/default.conf
```
в строке 'server_name <ip-адрес>' указать публичный ip-адрес сервера

4. Скопировать на сервер файлы:

```
cd infra
```
```
scp docker-compose.yaml <пользователь_сервера>@<ip-адрес сервера>:/home/<домашняя папка>
```
```
scp -r /nginx <пользователь_сервера>@<ip-адрес сервера>:/home/<домашняя папка>
```
5. На сервере установить пакеты docker.io и docker-compose v2.6.1

6. Запушить проект на удалённый репозиторий:

```
git add .
```
```
git commit -m '<comment>'
```
```
git push
```

7. Подключиться к серверу и создать суперпользователя в контейнере web:

```
ssh <пользователь>@<ip-адрес сервера>
```
```
sudo docker-compose exec -T web python manage.py createsuperuser
```

Примеры на рабочем сервере:

	1) http://51.250.21.86/api/v1/
	2) http://51.250.21.86/admin
	3) http://51.250.21.86/redoc


Разработчики:
	Айрат Бакиев, Виталий Яремчук, Макс Никулин
	
Лицензия:
		I like Linus Torvalds, GNU/GPL
		