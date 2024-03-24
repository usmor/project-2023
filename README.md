# DreamFood

Веб-приложение [DreamFood](https://dreamfood.pythonanywhere.com/) реализует 2 режима работы:
- подбор рецептов по введенным ингредиентам;
- подбор сбалансированного питания по количеству калорий.

<details><summary>Полный список файлов DreamFood</summary>

- Реализация сайта: `main.py`
- HTML-страницы: `папка templates`
- Изображения: `папка static`
- Реализация краулера №1: `web_1.ipynb`
- Реализация краулера №2: `web_2.ipynb`
- Обработка данных:  `data_processing.ipynb`
- Данные по рецептам: `my_recipes_data.csv.zip`
- Данные по ингредиентам: `ingredients.csv`
- Модули и пакеты для работы: `requirements.txt` </details>
О реализации проекта можно также почитать в [презентации](https://docs.google.com/presentation/d/1KM5novblLMESZhoQBRFeagFNAQ1t5eJlPlQIX0izoFM/edit?usp=sharing).

## Установка и использование
Для работы с программным кодом сайта необходимо будет установить (см. [requirements.txt](requirements.txt)): 
- **pandas** для работы с данными;
- **flask** для работы с веб-приложением; 
- **tqdm**, **beautifulsoup4**, **requests**, **fake-useragent** для реализации краулера;
- **pymorphy2** для обработки текстовых данных;
- **matplotlib** для визуализации данных. 

Это можно осуществить с помощью введенной в терминал команды:

```python
pip install -r requirements.txt
```
или (только для python3)
```python
pip3 install -r requirements.txt
```

Также используются различные встроенные модули: 
- Модуль **re** для работы с регулярными выражениями;
- Модуль **random** для работы со случайными элементами списков;
- Модуль **itertools** для работы с итераторами;
- Модуль **zipfile** для распаковки архивов.

## Интерфейс 

<details><summary>Список страниц на сайте</summary>

- `dreamfood.pythonanywhere.com` — переход на главную страницу веб-приложения;
- `/fridge` позволяет перейти на страницу по поиску рецептов по ингредиентам; 
- `/nutrition` осуществляют вызов страницы с подбором сбалансированного питания.</details>

## Данные 
Данные были получены путем обкачки сайтов с рецептами: 
- [povar.ru](https://povar.ru/mostnew/all/)
- [1000.menu](https://1000.menu/catalog/bjstro-i-vkusno)

После обработки данных был получен датасет `my_recipes_data.csv.zip` длиной около 50к строк. 
Были собраны следующие данные: 
- название блюда;
- ссылка на оригинальный рецепт;
- калорийность на 100г блюда;
- количество белков, жиров и углеводов (в граммах) в расчете на 100г блюда;
- текст рецепта.
  
## Подробнее о режимах работы
**Холодильник**

Данная функция позволяет пользователю подобрать рецепт в зависимости от введенных ингредиентов. 

*Алгоритм работы*
1) Пользователь вводит от 1 до 3 ингредиентов (для удобства была реализована функция автозаполнения);
2) Программа находит в `ingredients.csv` нужный ингредиент и соотвествующий ему список рецептов (операция производится от 1 до 3 раз);
3) Если ингредиентов несколько, программа находит объединение полученных множеств рецептов;
4) В зависимости от результата пользователь получает либо список рецептов, соответствующих его запросу, либо сообщение об отсутствии результатов поиска.

**Сбалансированное питание**

Данная функция позволяет пользователю подобрать 3 варианта сбалансированного питания (3 блюда по 300г) с учетом суточной нормы калорий. 

*Режимы работы*
- Пользователь вводит свои личные данные (пол, возраст, вес, рост и тип образа жизни);
- Пользователь вводит самостоятельно целевое количество калорий.

NB: суточная норма калорий считается с помощью формулы Маффина – Джеора с учетом коэффициента физической активности Харриса – Бенедикта (информация взята с сайта [здоровое-питание.рф](https://clck.ru/39UBxA))

*Алгорит работы*
1) В зависимости от выбранного режима работы суточное количество калорий либо считается программой самостоятельно, либо используется из запроса пользователя;
2) Из `my_recipes_data.csv` выбираются рецепты, где калорийность в расчете на 300г отличается по модулю от 1/3 таргетного значения калорий  на 10% максимум;
3) Создаются комбинации из найденной раннее подгруппы рецептов и проверяются на условие;
   - общая калорийность отличается по модулю от таргета на 20% максимум;
   - белки составляют около 30% процентов калорийности;
   - жиры составляют около 40% процентов калорийности;
   - углеводы составляют около 30% процентов калорийности;
4) Процедура проверки комбинации повторяется до тех пор, пока не будет найдено 3 варианта различных комбинаций;
5) Пользователь получает 3 списка рецептов, каждый из которых сопровождается графиком с распределением белков, жиров и углеводов, а также информацией об общей калорийности.

## Перспективы развития проекта 
На данный момент DreamFood функционирует в рамках тех команд, что в него вложены, тем не менее в дальнейшем можно будет улучшить интерфейс и расширить список возможностей: 
- увеличить базу рецептов;
- уменьшить время обработки запроса;
- оптимизировать алгоритм по подбору сбалансированного питания, уменьшив погрешность расчета;
- обеспечить постоянный хостинг сайт. 

## Aвторы
Проект реализован студенткой ФИКЛа НИУ ВШЭ, 2024 год 
[Анна Луценко](https://t.me/usmor);



