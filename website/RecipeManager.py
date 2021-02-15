import boto3
import json

class RecipeManager():
    def __init__(self,bucket,recipes_folder):
        self.session = boto3.session.Session()
        self.bucket = bucket
        self.recipes_folder = recipes_folder+'/'
        self.recipes = self.get_recipes()
        self.tags = self.list_tags()
        return None

    def update_manager(self):
        try:
            self.recipes = self.get_recipes()
            self.tags = self.list_tags()
        except Exception as e:
            return {'update_status':'failure','info':e}
        return {'update_status':'success','info':'Update completed successfully.'}

    def list_recipes(self):
        """
        List all recipes in s3 
        """
        s3 = self.session.client('s3')
        recipe_objects = []

        paginator = s3.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self.bucket,Prefix=self.recipes_folder)
        for page in page_iterator:
            recipe_objects += list(filter(lambda key:key!=self.recipes_folder,map(lambda obj:obj['Key'],page['Contents'])))
        return recipe_objects
    
    def get_recipe_from_id(self,recipe_id):
        """
        Retrieve a recipe given a recipe id
        """
        recipe = list(filter(lambda recipe:recipe['ID']==int(recipe_id),self.recipes))
        assert(len(recipe)==1)
        return recipe[0]

    def get_recipe_from_s3(self,key):
        """
        Retrieve a recipe object from s3 and load as json
        """
        s3 = self.session.client('s3')
        recipe_object = s3.get_object(
            Bucket = self.bucket,
            Key = key
        )
        recipe_object = recipe_object['Body'].read().decode('utf-8')
        return json.loads(recipe_object)

    def get_recipes(self): 
        """
        loads all recipes in s3 as dictionary object to self.recipes attribute
        """
        recipes = self.list_recipes()
        return list(map(self.get_recipe_from_s3,recipes))

    def list_tags(self):
        """
        Gathers a unique set of tags from all available recipes
        """
        recipe_tags = list(map(lambda recipe:recipe['Tags'],self.recipes))
        tags = set([tag for recipe in recipe_tags for tag in recipe])
        tags = list(tags)
        tags.sort()
        return tags

    def list_recipes_with_tag(self,tag):
        if tag in self.tags:
            return list(filter(lambda recipe:tag in recipe['Tags'],self.recipes))
        else:
            return None

if __name__=='__main__':
    with open('./bucket_info.json','r') as bucket_info:
        bucket_info = json.load(bucket_info)
    rm = RecipeManager(bucket = bucket_info['s3_bucket'],recipes_folder = bucket_info['s3_json_folder'])
    print(rm.tags)
