{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "c6b3e8da",
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import pandas as pd\n",
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "fc48b404",
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_all():\n",
    "    # create an instance of a Splinter browser (prepping automated browser)\n",
    "    executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "    news_title, news_paragraph = mars_news(browser)\n",
    "\n",
    "    # run all scraping functions and store results in dictionary\n",
    "    data = {\n",
    "      \"news_title\": news_title,\n",
    "      \"news_paragraph\": news_paragraph,\n",
    "      \"featured_image\": featured_image(browser),\n",
    "      \"facts\": mars_facts(),\n",
    "      \"last_modified\": dt.datetime.now(),\n",
    "      \"hemispheric_data\": mars_hemispheres(browser)\n",
    "    }\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "20622e28",
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape titles and teasers from redplanetscience.com\n",
    "def mars_news(browser):\n",
    "    # give the url of the site being to scrape with splinter\n",
    "    url = 'https://redplanetscience.com/'\n",
    "    # visit the Mars NASA news site\n",
    "    browser.visit(url)\n",
    "\n",
    "    # delay loading of page\n",
    "    browser.is_element_present_by_css('div.list_text', wait_time=1)\n",
    "\n",
    "    # convert the browser html to a soup object\n",
    "    html = browser.html\n",
    "    news_soup = soup(html, 'html.parser')\n",
    "\n",
    "    try: \n",
    "        # search for elements with tag (div) using attribute (list_text)\n",
    "        slide_elem = news_soup.select_one('div.list_text')\n",
    "        \n",
    "        # use the parent element to find the first `a` tag and save it as `news_title`\n",
    "        # only RETURN title of the news article and not any of the HTML tags or elements\n",
    "        news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "\n",
    "        # use the parent element to find the paragraph text\n",
    "        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "    except AttributeError: \n",
    "        return None, None\n",
    "        \n",
    "    return news_title, news_paragraph"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "edb83891",
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape Mars Data: Featured Image (10.3.4)\n",
    "def featured_image(browser):\n",
    "    # give the url of the site being to scrape\n",
    "    url = 'https://spaceimages-mars.com'\n",
    "    # visit the site\n",
    "    browser.visit(url)\n",
    "\n",
    "    # find and click the full image button\n",
    "    full_image_elem = browser.find_by_tag('button')[1]\n",
    "    full_image_elem.click()\n",
    "\n",
    "    # parsing the 2nd window so that we can continue scraping\n",
    "    # parse the resulting html with soup\n",
    "    html = browser.html\n",
    "    img_soup = soup(html, 'html.parser')\n",
    "    \n",
    "    try:\n",
    "        # find the relative image url\n",
    "        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "\n",
    "    except AttributeError: \n",
    "        return None    \n",
    "    \n",
    "    # add base URL of image and include the img_url to name the absolute URL\n",
    "    img_url = f'https://spaceimages-mars.com/{img_url_rel}'\n",
    "    \n",
    "    return img_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "5f2c1b19",
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape Mars and Earth Facts Table\n",
    "def mars_facts():\n",
    "    try: \n",
    "        # more-less a copy-paste of the table we want\n",
    "        # create a dataframe of the table\n",
    "        df = pd.read_html('https://galaxyfacts-mars.com')[0]\n",
    "    except BaseException:\n",
    "        return None\n",
    " \n",
    "    # assign columns and set index of dataframe   \n",
    "    df.columns=['Description', 'Mars', 'Earth']\n",
    "    df.set_index('Description', inplace=True)\n",
    "    # convert it to HTML (more-less)\n",
    "    return df.to_html(classes=\"table table-striped\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "171d3f70",
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape Mars Hemispheric Image and Title\n",
    "def mars_hemispheres(browser):\n",
    "    \n",
    "    # initial page   \n",
    "    url = 'https://marshemispheres.com/'\n",
    "    browser.visit(url)\n",
    "        \n",
    "    hemisphere_image_urls = []\n",
    "    \n",
    "    for x in range(4, 12, 2):\n",
    "        # goto page you need scrap data from\n",
    "        to_click = browser.find_by_tag('a')[x] \n",
    "        to_click.click()\n",
    "    \n",
    "        # define an empty dictionary\n",
    "        a_dict = {}\n",
    "    \n",
    "        # parse resulting html\n",
    "        html = browser.html\n",
    "        products_soup = soup(html, 'html.parser')\n",
    "\n",
    "        try:\n",
    "            # get the image\n",
    "            product_jpeg = products_soup.find('div', class_='wide-image-wrapper')\n",
    "            jpeg = product_jpeg.find('a').get('href')\n",
    "            jpeg_with_parent = f'{url}{jpeg}'\n",
    "        \n",
    "            # get the title\n",
    "            product_title = products_soup.find('div', class_='cover')\n",
    "            title = product_title.find('h2',class_='title').text\n",
    "        \n",
    "            # put image and title into the dictionary \n",
    "            a_dict['img_url'] =  jpeg_with_parent\n",
    "            a_dict['title'] = title\n",
    "        \n",
    "            # append the dictionary to your list\n",
    "            hemisphere_image_urls.append(a_dict)\n",
    "        \n",
    "            #go back to initial page so that you can get next \n",
    "            browser.back()\n",
    "        except BaseException:\n",
    "            return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "4ba3ca8c",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Current google-chrome version is 98.0.4758\n",
      "Get LATEST chromedriver version for 98.0.4758 google-chrome\n",
      "Driver [/Users/leanna/.wdm/drivers/chromedriver/mac64/98.0.4758.102/chromedriver] found in cache\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'news_title': \"NASA's Mars Reconnaissance Orbiter Undergoes Memory Update\", 'news_paragraph': 'Other orbiters will continue relaying data from Mars surface missions for a two-week period.', 'featured_image': 'https://spaceimages-mars.com/image/featured/mars1.jpg', 'facts': '<table border=\"1\" class=\"dataframe table table-striped\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Mars</th>\\n      <th>Earth</th>\\n    </tr>\\n    <tr>\\n      <th>Description</th>\\n      <th></th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Mars - Earth Comparison</th>\\n      <td>Mars</td>\\n      <td>Earth</td>\\n    </tr>\\n    <tr>\\n      <th>Diameter:</th>\\n      <td>6,779 km</td>\\n      <td>12,742 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 ?? 10^23 kg</td>\\n      <td>5.97 ?? 10^24 kg</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2</td>\\n      <td>1</td>\\n    </tr>\\n    <tr>\\n      <th>Distance from Sun:</th>\\n      <td>227,943,824 km</td>\\n      <td>149,598,262 km</td>\\n    </tr>\\n    <tr>\\n      <th>Length of Year:</th>\\n      <td>687 Earth days</td>\\n      <td>365.24 days</td>\\n    </tr>\\n    <tr>\\n      <th>Temperature:</th>\\n      <td>-87 to -5 ??C</td>\\n      <td>-88 to 58??C</td>\\n    </tr>\\n  </tbody>\\n</table>', 'last_modified': datetime.datetime(2022, 2, 15, 20, 41, 15, 598277), 'hemispheric_data': None}\n"
     ]
    }
   ],
   "source": [
    "if __name__ == \"__main__\":\n",
    "    # scrape data\n",
    "    print(scrape_all())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "91dd5a2e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "PythonData",
   "language": "python",
   "name": "pythondata"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
