# web-scraping-challenge
Create a new repository for this project called web-scraping-challenge. Do not add this homework to an existing repository.


Clone the new repository to your computer.


Inside your local git repository, create a directory for the web scraping challenge. Use a folder name to correspond to the challenge: Missions_to_Mars.


Add your notebook files to this folder as well as your flask app.


Push the above changes to GitHub or GitLab.



Step 1 - Scraping
Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.


NASA Mars News

Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
Step 2 - MongoDB and Flask Application
Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.


Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.


Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

Store the return value in Mongo as a Python dictionary.



Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.


Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.
Step 3 - Submission
To submit your work to BootCampSpot, create a new GitHub repository and upload the following:


The Jupyter Notebook containing the scraping code used.


Screenshots of your final application.


Submit the link to your new repository to BootCampSpot.


Ensure your repository has regular commits (i.e. 20+ commits) and a thorough README.md file



Hints


Use Splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.


Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the /scrape url is visited and new data is obtained.


Use Bootstrap to structure your HTML template.
