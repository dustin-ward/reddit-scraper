import time
import requests
from requests.exceptions import HTTPError

PAGES = 5
RETRY_ATTEMPTS = 100
REDDIT_URL = 'https://www.reddit.com'
TOP_ALLTIME_URL = REDDIT_URL + '/r/mainframe/top.json?limit=100&t=all'

def get_data(num_pages):

    # Top (num_pages * 100) posts all-time on r/mainframe
    i = 0
    after = ""
    top_posts_links = []
    while i < num_pages:
        success = False
        for attempt in range(RETRY_ATTEMPTS):
            try:
                url = TOP_ALLTIME_URL

                # 'after' field can be supplied to request to get the next set of posts.
                # Is is set at the end of this try-catch
                if after != "":
                    url += "&after="+after

                request = requests.get(url, headers = {'User-agent': 'zos-assistant'})
                request.raise_for_status()

            # Bad status codes
            except HTTPError as err:
                print('Request error:', err)

                # Rate limited
                if request.status_code == 429:
                    print("Rate limit exceeded. Sleeping...")
                    time.sleep(180)
                    continue

            # Other errors
            except Exception as err:
                print('Error:', err)

            else:
                success = True
                data = request.json()['data']
                after = data['after']
                num_posts = len(data['children'])
                print(f'Found {num_posts} posts on page {i+1}...')

                # Store urls of each post
                for post in data['children']:
                    top_posts_links.append(post['data']['permalink'])
                break

        if not success:
            print("Unable to complete request, stopping...")

        i += 1


    # Get comments for each post
    reddit_data = []
    for url in top_posts_links:
        success = False
        for attempt in range(RETRY_ATTEMPTS):
            try:
                request = requests.get(REDDIT_URL+url+".json", headers = {'User-agent': 'zos-assistant'})
                request.raise_for_status()

            # Bad status codes
            except HTTPError as err:
                print('Request error:', err)

                # Rate limited
                if request.status_code == 429:
                    print("Rate limit exceeded. Sleeping...")
                    time.sleep(180)
                    continue

            # Other errors
            except Exception as err:
                print('Error:', err)

            else:
                success = True
                print(request.url, "STATUS:", request.status_code, request.reason)
                data = request.json()
                post = data[0]['data']['children'][0]
                comments = data[1]['data']['children']

                # Sanity. t3 = post, t1 = comment
                assert(post['kind'] == "t3")
                if len(comments) > 0:
                    #TODO: Ignore posts with no comments?
                    assert(comments[0]['kind'] == "t1")
                
                obj = {
                    'title': post['data']['title'],
                    'body': post['data']['selftext'],
                    'upvotes': post['data']['ups'],
                    'ratio': post['data']['upvote_ratio'],
                    'created': post['data']['created'],
                    'author': post['data']['author'],
                    'comments': get_comments(comments)
                }
                
                reddit_data.append(obj)
                time.sleep(2)
                break

        if not success:
            print("Unable to complete request, stopping...")
            break
    
    return reddit_data


#TODO: Replies are unwinded to a sequential format. Maybe the context is needed?
def get_comments(comments_json):
    comments = []
    for comment in comments_json:
        data = comment['data']
        if data['depth'] >= 10:
            continue
        
        comments.append({
            'body': data['body'],
            'created': data['created'],
            'author': data['author'],
            'upvotes': data['ups']
        })
        
        if data['replies'] != "":
            comments += get_comments(data['replies']['data']['children'])

    return comments
