# API Сервис поиска ближайших машин для перевозки грузов.

## Стек и требования:
- Django Rest Framework;
- PostgreSQL;
- Приложение должно запускаться в docker compose без дополнительных доработок;
- БД должна заполняется начальными данными. Локации загружаются из csv-файла. Локация машин заполняется случайным образом;
- Расчет и отображение расстояний в милях;
- Расчет расстояний с помощью библиотеки geopy, без учета маршрута, только от точки до точки.
- Поля Груза:
    - локация pick-up;
    - локация delivery;
    - вес (1-1000);
    - описание.
- Поля Машины:
    - уникальный номер (цифра от 1000 до 9999 + случайная заглавная латинская буква);
    - текущая локация;
    - грузоподъемность (1-1000).
- Поля Локации:
    - город;
    - штат;
    - почтовый индекс (zip);
    - широта;
    - долгота.

## Базовые функции сервиса:
- Создание груза (локации pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
- Получение груза по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.
- Фильтр списка грузов по весу;
- Автоматическое обновление локаций всех машин раз в 15 секунд (локация меняется на другую случайную).
