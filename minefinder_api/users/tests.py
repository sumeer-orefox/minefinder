from rest_framework.test import APITestCase
from users.api.views import get_random, get_access_token, get_refresh_token
from .models import User,UserProfile
from message_control.tests import create_image, SimpleUploadedFile


class TestGenericFunctions(APITestCase):

    def test_get_random(self):

        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # check that we are getting a result
        self.assertTrue(rand1)

        # check that rand1 is not equal to rand2
        self.assertNotEqual(rand1, rand2)

        # check that the length of result is what is expected
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1
        }

        token = get_access_token(payload)

        # check that we obtained a result
        self.assertTrue(token)

    def test_get_refresh_token(self):

        token = get_refresh_token()

        # check that we obtained a result
        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
           # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            "first_name":"Sam",
            "last_name" :"Garg",
            "re_password" : "Sam@12345",
            "is_seller" : False,
            "is_buyer" : True,
        }

        response = self.client.post(self.register_url, data=payload)

        # check that we obtain a status of 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload1 = {
           # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            "first_name":"Sam",
            "last_name" :"Garg",
            "re_password" : "Sam@12345",
            "is_seller" : False,
            "is_buyer" : True,
        }
        payload2 = {
           # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            
        }
        # register
        response1 = self.client.post(self.register_url, data=payload1)
        
        self.assertEqual(response1.status_code, 201)

        # login
        response = self.client.post(self.login_url, data=payload2)
        result = response.json()
          # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)
        
        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload1 = {
           # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            "first_name":"Sam",
            "last_name" :"Garg",
            "re_password" : "Sam@12345",
            "is_seller" : False,
            "is_buyer" : True,
        }
        payload2 = {
           # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            
        }

        # register
        self.client.post(self.register_url, data=payload1)

        # login
        response = self.client.post(self.login_url, data=payload2)
        refresh = response.json()["refresh"]

        # get refresh
        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()
        

        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"
    login_url = "/user/login"

    def setUp(self):
        payload1 = {
        # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            "first_name":"Sam",
            "last_name" :"Garg",
            #"re_password" : "Sam@12345",
            "is_seller" : False,
            "is_buyer" : True,
        }
        payload2 = {
        # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "samgarg@gmail.com",
            
        }
        
        self.user = User.objects.create_user(**payload1)

        # login
        response = self.client.post(self.login_url, data=payload2)
        result = response.json()
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name":"Sam",
            "last_name" :"Garg",
            "caption": "Being alive is different from living",
            "bio": "I am a passionation lover of ART, graphics and creation"
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Sam")
        self.assertEqual(result["last_name"], "Garg")
        self.assertEqual(result["user"]["email"], "samgarg@gmail.com")


    def test_post_user_profile_with_profile_picture(self):

        # upload image
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(
            self.file_upload_url, data=data, **self.bearer)
        result = response.json()

        payload = {
            "user_id": self.user.id,
            "first_name":"Sam",
            "last_name" :"Garg",
            "caption": "Being alive is different from living",
            "bio": "I am a passionation lover of ART, graphics and creation",
        
            "profile_picture_id": result["id"]
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()
        print("pp",result) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Sam")
        self.assertEqual(result["last_name"], "Garg")
        self.assertEqual(result["user"]["email"], "samgarg@gmail.com")
        self.assertEqual(result["profile_picture"]["id"], 1)

    def test_update_user_profile(self):
        # create profile

        payload = {
            "user_id": self.user.id,
            "first_name":"Sam",
            "last_name" :"Garg",
            "caption": "Being alive is different from living",
            "bio": "I am a passionation lover of ART, graphics and creation"
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()

        # --- created profile

        payload = {
            "first_name": "Sam_update",
            "last_name": "Garg_update",
        }

        response = self.client.patch(
            self.profile_url + f"/{result['id']}", data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "Sam_update")
        self.assertEqual(result["last_name"], "Garg_update")
        self.assertEqual(result["user"]["email"], "samgarg@gmail.com")

    def test_user_search(self):

        UserProfile.objects.create(user=self.user, first_name="Sam", last_name="Garg",
                                   caption="live is all about living", bio="I'm a youtuber")

        payload_user2 = {
        # "username": "adefemigreat",
            "password": "Neha@12345",
            "email": "nehagarg@gmail.com",
            "first_name":"Neha",
            "last_name" :"Garg",
            #"re_password" : "Sam@12345",
            "is_seller" : True,
            "is_buyer" : False,
        }
        user2 = User.objects.create_seller(**payload_user2)
        UserProfile.objects.create(user=user2, caption="it's all about testing", bio="I'm a youtuber")

        payload_user3 = {
        # "username": "adefemigreat",
            "password": "Manvi@12345",
            "email": "manvigarg@gmail.com",
            "first_name":"Manvi",
            "last_name" :"Garg",
            #"re_password" : "Sam@12345",
            "is_seller" : True,
            "is_buyer" : True,
        }
        user3 = User.objects.create_seller_buyer(**payload_user3)
        UserProfile.objects.create(user=user3, caption="it's all about testing", bio="I'm a youtuber")
        payload_user4 = {
        # "username": "adefemigreat",
            "password": "Sam@12345",
            "email": "manvi_g@gmail.com",
            "first_name":"Manvi",
            "last_name" :"Garg",
            #"re_password" : "Sam@12345",
            "is_seller" : False,
            "is_buyer" : True,
        }
        user4 = User.objects.create_seller_buyer(**payload_user4)
        UserProfile.objects.create(user=user4, caption="it's all about testing same first name", bio="I'm a tester")
         # test keyword = Manvi
        url = self.profile_url + "?keyword=Manvi"
        print("all users", UserProfile.objects.all()) 
        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)

        # test keyword = ade
        url = self.profile_url + "?keyword=Sam"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]
     
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 0)
       # self.assertEqual(result[0]["user"]["email"], "sam@gmail.com")

        # test keyword = vester
        url = self.profile_url + "?keyword=neha"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]


        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"]["email"], "nehagarg@gmail.com")    
        self.assertEqual(result[0]["message_count"],0)  
    
