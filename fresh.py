"""Alfred workflow to get Rotten Tomatoes scores"""

from __future__ import print_function
import sys
from workflow import Workflow, web, ICON_INFO
import json


API_KEY = 'zt4v6a9fvnjeb5396ewbhdz9'

def main(wf):
    
    # Check for workflow update
    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)
                    
    # Get query from Alfred
    if len(wf.args):
        qtype = wf.args[0]
        query = wf.args[1]
    else:
        qtype = None
        query = None
    
    # Query Rotten Tomatoes for matching movies
    if qtype == 'movie':
        rturl = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json'
    elif qtype == 'tv':
        # Currently the RottenTomatoes API doesnt support TV shows
        pass
    params = dict(q=query, page_limit=10, page=1, apikey=API_KEY)
    response = web.get(rturl, params)
    
    # throw an error if request failed
    response.raise_for_status()
    
    # encode json formatted response into a dict
    movies = response.json()
    moviesStr = json.dumps(movies, indent=4)

    # Get necessary data and add to Alfred items
    for movie in movies['movies']:
        rtTitle = movie['title']
        rtYear = movie['year']
        rtScore = movie['ratings']['critics_score']
        rtLink = movie['links']['alternate']
        if rtScore != -1:
            rtIsFresh = movie['ratings']['critics_rating']
            rtData = '{0:4d}%\t{1} ({2})'.format(rtScore, rtTitle, rtYear)
        else:
            rtIsFresh = None
            rtData = '\t\t{0} ({1})'.format(rtTitle, rtYear)
        if rtIsFresh == 'Fresh':
            rtIcon = 'icons/freshtomato.png'
        elif rtIsFresh == 'Certified Fresh':
            rtIcon = 'icons/certifiedtomato.png'
        elif rtIsFresh == 'Rotten':
            rtIcon = 'icons/splattomato.png'
        elif rtIsFresh == None:
            rtIcon = 'icons/noscore.png'
        
        wf.add_item(title = rtData,
                    arg = rtLink,
                    valid = True,
                    icon = rtIcon)
        
    # Send XML formatted result to Alred
    wf.send_feedback()
    
if __name__ == u"__main__":
    wf = Workflow(update_settings={
        'github_slug': 'dalimatt/tomatometer',
        'frequency': 1
    })
    sys.exit(wf.run(main))
