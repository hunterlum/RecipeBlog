from flask import Flask,render_template,url_for
from RecipeManager import RecipeManager 
import json
#python3 -m flask run
app = Flask(__name__)

with open('./bucket_info.json','r') as bucket_info:
    bucket_info = json.load(bucket_info)
rm = RecipeManager(bucket = bucket_info['s3_bucket'],recipes_folder = bucket_info['s3_json_folder'])

@app.route('/')
def main():
    #rm.update_manager()
    print('hello world')
    return render_template('index.html',tags=rm.tags)

@app.route('/update')
def update_manager():
    rm.update_manager()
    return render_template('index.html',tags=rm.tags)

@app.route('/tag/<tag>')
def recipes_with_tag(tag):
    #rm.update_manager()
    recipes = rm.list_recipes_with_tag(tag)
    return render_template('list_recipes.html',tags=rm.tags,tag=tag,recipes=recipes)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    #rm.update_manager()
    recipe = rm.get_recipe_from_id(recipe_id)
    return render_template('recipe.html'
        ,title=recipe['Title']
        ,description=recipe['Description']
        ,ingredients=recipe['Ingredients']
        ,instructions=recipe['Instructions']
        ,photo=recipe['Photo']
        ,recipe_tags=recipe['Tags']
        ,tags=rm.tags
    )
if __name__ == '__main__':
    app.run()
