from django.conf import settings
import json

class Facebbok():
	def __init__(self):
		self.__user_post_api = settings.FB_HOST + '/me/feed/'
		self.__me_id_api = settings.FB_HOST + '/me/'
		self.__page_api = settings.FB_HOST + '/me/accounts/'

	def get_me(self, id, access):
		me_api = settings.FB_HOST + id
		params = {
			'access_token':access
		}
		response = requests.post(me_api, params = params)



		pass
	def get_page(self):
		pass

	def fb_user_post(self, access, post_data):
		pass

		# # user = self.request.user
  #       # data = self.request.data
        
  #       # POST NLP-->data
  #       post_data = data 
  #       access =  str(SocialToken.objects.filter(account__user = user)[0])
  #       #self.fb_user_post(access, post_data)
  #       self.fb_page_post(access, post_data)


  #       user_post_api = settings.FB_HOST + '/me/feed/'
  #       message = post_data.get('content')
  #       params = {
  #           'message':message,
  #           'access_token':access
    
  #       }
  #       resp = requests.post(user_post_api, params = params)

