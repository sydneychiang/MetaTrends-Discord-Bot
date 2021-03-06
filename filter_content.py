
def format_tweet(tweet):
  return f"[{tweet['type'].capitalize()}] {tweet['user_name']} (@{tweet['screen_name']})\n{tweet['text']}"

def format_tv_movie(tvMovie):
  string = f"[{tvMovie['type'].capitalize()}] {tvMovie['original_title']}\n{tvMovie['overview']}"
  return string

def format_youtube(youtube):
  string = f"[{youtube['type'].capitalize()}] {youtube['channelTitle']}\n{youtube['title']}"
  return string

def format_twitch(twitch):
  string = f"[{twitch['type'].capitalize()}] {twitch['user_name']}\n{twitch['title']} ({twitch['game']})"
  return string

def format_reddit(reddit):
  string = f"[{reddit['type'].capitalize()}] {reddit['subreddit']}\n{reddit['title']}"
  return string

def format_spotify(spotify):
  artistNames = [artist['name'] for artist in spotify['artists']]
  string = f"[{spotify['type'].capitalize()}] {spotify['name']} by {' & '.join(artistNames)}"
  return string


def format_content(content):
  newstr = ""
  if content["type"] == "tweet":
    newstr += format_tweet(content)
  elif content["type"] == "tv" or content["type"] == "movie":
    newstr += format_tv_movie(content)
  elif content["type"] == "youtube":
    newstr += format_youtube(content)
  elif content["type"] == "twitch":
    newstr += format_twitch(content)
  elif content["type"] == "reddit":
    newstr += format_reddit(content)
  elif content["type"] == "spotify":
    newstr += format_spotify(content)

  newstr += "\n"
  return newstr


def get_titles(content):
  if content["type"] == "tv" or content["type"] == "movie":
    return content["type"], content["original_title"]
  elif content["type"] == "spotify":
    return content["type"], content["name"]
  elif content["type"] == "tweet":
    return content["type"], content["text"]
  else:
    return content["type"], content["title"]

