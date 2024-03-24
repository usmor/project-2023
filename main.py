from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
from itertools import chain
import random
import matplotlib
import matplotlib.pyplot as plt
import zipfile

with zipfile.ZipFile('my_recipes_data.csv.zip', 'r') as zip_ref:
    zip_ref.extractall()

app = Flask(__name__)


# при вызове функции main() переходим на главную страницу

@app.route('/')
def main():
    return render_template('index.html')


# при вызове функции fridge() переходим на страницу с анкетой для поиска рецептов

@app.route('/fridge')
def fridge():
    return render_template('fridge.html')


# при вызове функции your_fridge() переходим на страницу с полученным списком рецептов

@app.route('/your_recipes')
def your_fridge(name=None):
    file = pd.read_csv('ingredients.csv')

    # получаем ингредиенты от пользователя
    ingredient_1 = request.args.get('ingredient_1')
    ingredient_2 = request.args.get('ingredient_2')
    ingredient_3 = request.args.get('ingredient_3')
    if ingredient_1 == '' and ingredient_2 == '' and ingredient_3 == '':
        return render_template('error.html')
    recipes = None
    result = {'all_ingr': [], 'all_rec': None}

    # реализация алгоритма поиска подходящих рецептов
    if ingredient_1 != '':
        if ingredient_1 in file['name'].tolist():
            result['all_ingr'].append(ingredient_1)
            recipes = find_recipes(ingredient_1)
        else:
            return render_template('error.html')
    if ingredient_2 != '':
        if ingredient_2 in file['name'].tolist():
            result['all_ingr'].append(ingredient_2)
            if recipes is not None:
                recipes &= find_recipes(ingredient_2)
            else:
                recipes = find_recipes(ingredient_2)
        else:
            return render_template('error.html')
    if ingredient_3 != '':
        if ingredient_3 in file['name'].tolist():
            result['all_ingr'].append(ingredient_3)
            if recipes is not None:
                recipes &= find_recipes(ingredient_3)
            else:
                recipes = find_recipes(ingredient_3)
        else:
            return render_template('error.html')

    # получение данных найденных рецептов
    data = pd.read_csv('my_recipes_data.csv')

    result['all_ingr'] = ', '.join(result['all_ingr'])
    if len(recipes) != 0:

        result['all_rec'] = []
        for i in list(recipes):
            result['all_rec'].append([' '.join(list(data.loc[data['id'] == int(i)]['title'])),
                                      ' '.join(list(data.loc[data['id'] == int(i)]['link']))])
    else:
        result['all_rec'] = 'К сожалению, по Вашему запросу не было найдено подходящих рецептов.'
        return render_template('no_result.html', name=name, result=result)

    return render_template('your_recipes.html', name=name, result=result)


# при вызове функции nutrition() переходим на страницу с анкетой для поиска сбалансированного питания

def find_recipes(name):
    file = pd.read_csv('ingredients.csv')
    return set(str(list(file.loc[file['name'] == name]['all recipes'])).replace(
        '[[', '').replace(']]', '').replace("['[", '').replace("]']", '').split(', '))


@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')


# при вызове функции nutrition_result() переходим на страницу с результатами поиска сбалансированного питания

@app.route('/nutrition_result')
def nutrition_result(name=None):
    styles = {'Минимальная активность/сидячий образ жизни': 1.2,
              'Легкая нагрузка 1–3 раза в неделю': 1.375,
              'Тренировки 3–5 раз в неделю': 1.55,
              'Тренировки ежедневно': 1.7,
              'Тяжелая физическая работа/тренировки 2 раза в день': 1.9
              }

    # получение данных пользователя
    sex = request.args.get('sex')
    age = request.args.get('age')
    weight = request.args.get('weight')
    height = request.args.get('height')
    style = request.args.get('style')
    cal = request.args.get('cal')

    result = dict()

    # формула для подсчета суточной нормы калорий
    formula = [9.99, None, 6.25, None, -4.92, None, None, None]

    # проверка данных на формат
    # если данные введены верны, вызывается функция count() для поиска подходящих рецептов
    if cal != '' and all([sex, age, weight, height, style]):
        return render_template('error.html')
    if cal == "":
        if not all([sex, age, weight, height,
                    style]) or not age.isdigit() or not weight.isdigit() or not height.isdigit() or style == 'None' \
                or sex == 'None':
            return render_template('error.html')
        elif all([sex, age, weight, height,
                  style]) and age.isdigit() and weight.isdigit() and height.isdigit() and sex != 'None' \
                and style != 'None':
            formula[1] = int(weight)
            formula[3] = int(height)
            formula[5] = int(age)
            if sex == 'Женский':
                formula[6] = -161
            elif sex == 'Мужской':
                formula[6] = 5
            formula[7] = styles[style]
            calories = round(
                (formula[0] * formula[1] + formula[2] * formula[3] - formula[4] * formula[5] + formula[6]) * formula[7],
                2)
            result['calories'] = calories
            result['params'] = [f'Пол: {sex.lower()}',
                                f'Возраст: {age}',
                                f'Вес: {weight} кг',
                                f'Рост: {height} см',
                                f'Образ жизни: {style.lower()}']

            if 500 <= float(cal) <= 6500:
                result['data'] = count(calories)
            else:
                return render_template('error.html')

    elif cal.isdigit() and 500 <= float(cal) <= 5000:
        result['data'] = count(float(cal))
        result['calories'] = cal
        result['params'] = ['нет данных']
    else:
        return render_template('error.html')

    return render_template('nutrition_result.html', name=name, result=result)


# подсчет общего числа калорий в комбинации

def calculate_total_calories(comb):
    return sum([inner_list[1] * 3 for inner_list in comb])


# подсчет общего числа белков в комбинации

def calculate_total_proteins(comb):
    return sum([inner_list[2] * 3 * 4.1 for inner_list in comb])


# подсчет общего числа жиров в комбинации

def calculate_total_fats(comb):
    return sum([inner_list[3] * 3 * 9.3 for inner_list in comb])


# подсчет общего числа углеводов в комбинации

def calculate_total_carbs(comb):
    return sum([inner_list[4] * 3 * 4.1 for inner_list in comb])


# поиск комбинации и проверка на условие
# получение нужных данных для подходящей комбинации

def count(calories):
    df = pd.read_csv('my_recipes_data.csv')
    final_combinations = []
    inter = df[abs(df['calorie content'] * 3 - calories / 3) <= calories * 0.1]

    while len(final_combinations) < 3:
        trial = random.sample(list(inter['id']), 3)
        trial = [list(df.loc[df['id'] == item][['id',
                                                'calorie content',
                                                'proteins',
                                                'fats',
                                                'carbohydrates']].values.tolist()[0]) for item in trial]
        total_calories = calculate_total_calories(trial)
        total_proteins = calculate_total_proteins(trial)
        total_fats = calculate_total_fats(trial)
        total_carbs = calculate_total_carbs(trial)

        if all([
            abs(total_calories - calories) / calories <= 0.2,
            abs(total_proteins - total_calories * 0.3) / (total_calories * 0.3) <= 0.2,
            abs(total_fats - total_calories * 0.3) / (total_calories * 0.3) <= 0.2,
            abs(total_carbs - total_calories * 0.4) / (total_calories * 0.4) <= 0.2
        ]):
            final_combinations.append([
                [item[0] for item in trial],
                total_calories,
                round(total_proteins, 2),
                round(total_fats, 2),
                round(total_carbs, 2)
            ])

    for comb in range(len(final_combinations)):
        final_combinations[comb].append(f'static/photos/visualisation/{comb}.jpg')
        for i in range(3):
            final_combinations[comb][0][i] = list(chain.from_iterable(
                df.loc[df['id'] == final_combinations[comb][0][i]][['title', 'link']].values.tolist()))

    return visualisation(final_combinations)


# создание диаграмм с характеристиками комбинации (белки, жиры и углеводы)

def visualisation(final_combinations):
    # палитра цветов для графиков
    colors = ['#FFE787', '#E85D75', '#94C5CC']
    labels = ['белки', 'жиры', 'углеводы']

    # построение графиков
    matplotlib.use('agg')
    matplotlib.rcParams['font.family'] = 'georgia'

    for comb in range(len(final_combinations)):
        values = [final_combinations[comb][2], final_combinations[comb][3], final_combinations[comb][4]]
        plt.rc('font', size=30)
        plt.figure(figsize=(8, 8), facecolor='#FBEEDA')
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.savefig(f'static/photos/visualisation/{comb}.jpg', dpi=300, bbox_inches='tight')
        plt.close()
    return final_combinations


if __name__ == '__main__':
    app.run(debug=False, port=5000)
