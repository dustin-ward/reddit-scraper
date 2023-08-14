# Reddit Scraper

Python function to scrape top posts and comments from r/Mainframe

The entry point is `redditdata.get_data()`

Can scrape 100 posts roughly every 10 minutes/

Needs `pip install requests`

### Params

Pass the number of pages to scrape. The API request maxes out at 100 posts, so each page will add an additional 100 entries to the gathered data.

### Return

Returns a (json-like) array of dictionaries that looks like the following:

```
[
  . . .
  {
    'title'
    'body'
    'upvotes'
    'ratio'
    'created'
    'author'
    'comments': [
      . . .
       {
         'author'
         'created'
         'upvotes'
         'body'
       }
      . . .
    ]
  }
  . . .
]
```
