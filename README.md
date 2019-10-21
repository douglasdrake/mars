# mars

# Description and Methods
* A Flask app is provided that scrapes five sites for information and images about Mars:
1. [NASA's Mars Exploration Program](https://mars.nasa.gov/news)
2. [Jet Propulsion Laboaratory Mars Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
3. [Mars Weather Twitter Feed](https://twitter.com/MarsWxReport?lang=en)
4. [Mars Facts](https://space-facts.com/mars/)
5.  [USGS Astrogeology Center](https://astrogeology.usgs.gov)

* `splinter` is used to visit the sites.
* Beautiful Soup, `bs4`, is used to parse and scrape the sites.
* The results of the scraping are saved in a MongoDB.
* Finally, the results are rendered in an HTML template.

`app.py` provides the Flask app and `scrape_mars.py` contains the functions used for scraping.

# Results
* [Jupyter notebook with results from 10-21-2019 scrape](https://nbviewer.jupyter.org/github/douglasdrake/mars/blob/master/scrape_mars.ipynb).




