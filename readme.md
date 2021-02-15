# Food Blog 

## Introduction
Food blog using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/download/). This was a project I created so that I can document my favorite recipes and recreate them in the future. These recipes are organized by "genres" that describe the dish so that recipes and be explored depending on a certain mood.

## Overview
The Recipe Blog is a flask web app hosted serverlessly using AWS. The web app uses a custom class called RecipeManager which interacts with an S3 bucket. This bucket acts as the database and contains all the recipe data. Using RecipeManager, the web app retrieves the information it needs to populate web pages and list the genres in the nav bar dropdown menu by parsing the recipes in S3. Below is a quick architecure overview of the app as well as configuration instructions.

## Architecture
This site can be hosted serverlessly using the following AWS Services:
1. Route53
2. Lambda
3. S3
4. API Gateway
    * REST API
    * Custom Domain Name

![RecipeBlog](RecipeBlog.png)<br>

Route53 and Custom Domain Name are optional. Their only purpose is to point a custom domain to the REST API for an easier reference. The flask site is hosted in S3 which is invoked by the API Gateway. S3 is used to store recipes.
## Setup/Deployment
1. Setup S3
    * Create a public S3 bucket
    * The bucket should contain two folders
        * Recipe folder containing your recipe data
        * Photo folder containing your recipe photos
2. Deploy Web App using [Zappa](https://github.com/Miserlou/Zappa)<br>
Zappa is used to deploy a Lambda and REST API 
    * Install Zappa<br>
    `pip install zappa`
    * Create a virtual environment <br>
    `python3 -m venv venv`<br>
    `source venv/bin/activate`<br>
    `pip install zappa flask`
    * Initialize Zappa<br>
    `zappa init`
        * Follow the on screen instructions to initialize zappa
    * Deploy using Zappa<br>
    `zappa deploy`
    * A makefile has been created to facilitate updates
3. Create a Custom Domain<br>
This is an optional step to host the website using a user friendly name
    * Create a new domain using Route53
    * Create a Custom Domain Name in API Gateway 
        * Reference your desired domain/sub domain
        * Map your custom domain name to your REST API
    * Under your Hosted Zone in Route53 create an aliased A record
        * This A record should point to the API Gateway supplied after creating your Custom Domain Name in the previous step