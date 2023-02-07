# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

_Реализованные возможности при помощи API запросов:_
+ Регистрация нового юзера
+ Авторизация при помощи email и JWT токенов
+ Оставлять отзывы к тем или иным произведениям
+ Писать комментарри к отзывам
+ Выставлять оценки к произведениям
+ Просматривать чужие комментарии и отзывы

_Для пользователя со статусом admin и moderator реализованы следующие возможности_:
+ Добавлять, удалять и изменять данные о пользователях (admin only)
+ Добавлять, удалять и изменять комментарии
+ Добавлять, удалять и изменять данные о произведениях (admin only)
+ Добавлять, удалять и изменять отзывы

_Используемые инструменты_
1. Python ^3.7
2. djangorestframework==3.12.4
3. requests==2.26.0
4. Django==3.2
5. PyJWT==2.1.0
6. pytest==6.2.4

## Setup
```
$ git clone https://github.com/RBekr/api_yamdb.git
$ cd api_yamdb
$ python -m venv venv
$ source venv/Scripts/activate
$ pip install -r requirements.txt
$ cd api_yamdb
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
## Examples

__ДОКУМЕНТАЦИЯ__
`http://127.0.0.1:8000/redoc/`

Регистрация: 
`POST /api/v1/signup/`

Получение токена: 
`POST v1/auth/token/`

`GET /api/v1/titles/`

`GET /api/v1/titles/{title_id}/`

`POST /api/v1/titles/{title_id}/reviews`

__Авторы__: [__Руслан__](https://github.com/RBekr) 
[__Никита__](https://github.com/Irena-bun)
[__Ирена__](https://github.com/Mr-Green-N)