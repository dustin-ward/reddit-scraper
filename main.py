import redditdata as reddit

# Top 200 posts + comments
data = reddit.get_data(2)

# Data for https://www.reddit.com/r/mainframe/comments/lrzigv/the_y2k_experience/
post = data[17]
print("POST================================")
print(post['title'])
print(f"Author: {post['author']} at {post['created']}")
print(f"Upvotes: {post['upvotes']} ({post['ratio']*100}%)")
print(post['body'],"\n")

print("COMMENTS============================")
for comment in post['comments']:
    print(f"Author: {comment['author']} at {comment['created']}")
    print(f"Upvotes: {comment['upvotes']}")
    print(comment['body'],"\n")
