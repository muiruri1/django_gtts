from django.test import TestCase, Client
from json import loads
from os import path
from .models import Speech
from .templatetags.gTTS import say, temp_path
from .cache import remove_cache

class TranslationStorage_TestCase(TestCase):
    """ requires makemigration and migrate before testing """
    language = 'en'
    text = 'something to say'

    def test_speech_stored_and_returned(self):
        resp = say(self.language, self.text)
        self.assertEquals(
            Speech.objects.get(
                language=language,
                text=text)
                , resp)

    def test_dynamic_route(self):
        resp = loads(
            Client().get('/gtts/%s/%s' %(
                self.language, self.text
            )).content
        )['mp3']
        self.assertEqual(
            resp,
            say(self.language, self.text)
        )
    
    def test_dynamic_auth_route(self):
        resp = Client().get('/gtts_auth/%s/%s' %(
            self.language, self.text
        )).status_code
        self.assertEqual(resp, 302)

    def test_remove_cache(self):
        self.assertTrue(
            path.isdir(temp_path)
        )
        remove_cache()
        self.assertFalse(
            path.isdir(temp_path)
        )
    
    def test_say_false_input(self):
        try:
            say(False, False)
        except Exception as e:
            self.assertEquals(
                type(e),
                TypeError
            )