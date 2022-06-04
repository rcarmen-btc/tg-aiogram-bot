from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag


cl = Client()
cl.login('uchkuchh', 'riser12345')

#
media_pk = cl.media_pk_from_url('https://www.instagram.com/p/CeYNTs8MHbg/')
media_path = cl.video_download(media_pk)
adw0rd = cl.user_info_by_username('dualipa')
hashtag = cl.hashtag_info('dhbastards')
#
cl.video_upload_to_story(
      media_path,
     "Credits @adw0rd",
    mentions=[StoryMention(user=adw0rd, x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
     links=[StoryLink(webUri='https://github.com/adw0rd/instagrapi')],
     # hashtags=[StoryHashtag(hashtag=hashtag, x=0.23, y=0.32, width=0.5, height=0.22)],
     medias=[StoryMedia(media_pk=media_pk, x=0.5, y=0.5, width=0.6, height=0.8)]
)
