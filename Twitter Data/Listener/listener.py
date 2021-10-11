import settings
import private
import tweepy as tw
import dataset
from textblob import TextBlob #package to sentimental analysis from text
from sqlalchemy.exc import ProgrammingError
import json
import re

db = dataset.connect(settings.CONNECTION_STRING)

class StreamListener(tw.StreamListener):

    def on_status(self, status):
        """ if status.retweeted_status:
            return
         """
        if not re.search("RT @",status.text):
            description = status.user.description
            loc = status.user.location
            text = status.text
            coords = status.coordinates
            geo = status.geo
            name = status.user.screen_name
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count
            bg_color = status.user.profile_background_color
            source = status.source
            blob = TextBlob(text)
            sent = blob.sentiment
            print(status.text)      
            if geo is not None:
                geo = json.dumps(geo)

            if coords is not None:
                coords = json.dumps(coords)

            table = db[settings.TABLE_NAME]
            try:
                table.insert(dict(
                    user_description=description,
                    user_location=loc,
                    coordinates=coords,
                    text=text,
                    geo=geo,
                    user_name=name,
                    user_created=user_created,
                    user_followers=followers,
                    id_str=id_str,
                    created=created,
                    retweet_count=retweets,
                    user_bg_color=bg_color,
                    source=source,
                    polarity=sent.polarity,
                    subjectivity=sent.subjectivity,
                ))
            except ProgrammingError as err:
                print(err)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tw.OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
auth.set_access_token(private.TWITTER_KEY, private.TWITTER_SECRET)
api = tw.API(auth)

stream_listener = StreamListener()
stream = tw.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS, languages=["pt"])