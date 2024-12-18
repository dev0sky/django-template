import json
from langdetect import detect
from textblob import TextBlob
from googletrans import Translator
from rest_framework import viewsets
from django.shortcuts import render
from django.core.cache import cache
from core.models import Category, Phone
from rest_framework.response import Response
from core.serializers import CategorySerializer
from django.utils.translation import gettext_lazy as _

class PublicCachedListViewSet(viewsets.ModelViewSet):

    def get_cache_key(self, prefix, request, obj_id=None):
        """Genera una clave de caché única en el formato especificado."""
        key = f"{self.app_name}:{self.model_name}:{prefix}"
        if obj_id:
            key += f":{obj_id}"
        return key

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key("list", request)
        cached_data = cache.get(cache_key)
        if cached_data:
            print(_("Returning cached response with key: "), cache_key)
            return Response(json.loads(cached_data))
        
        response = super().list(request, *args, **kwargs)
        if response.data:
            try:
                json_data = json.dumps(response.data, ensure_ascii=False)
                cache.set(cache_key, json_data, timeout=60*15)
                print(_("Cached response with key:"), cache_key)
            except Exception as e:
                print(f"Error caching response: {e}")
        
        return response

    def retrieve(self, request, *args, **kwargs):
        obj_id = kwargs.get('pk')
        cache_key = self.get_cache_key("retrieve", request, obj_id)
        cached_data = cache.get(cache_key)
        if cached_data:
            print(_("Returning cached response with key: "), cache_key)
            return Response(json.loads(cached_data))

        response = super().retrieve(request, *args, **kwargs)
        try:
            json_data = json.dumps(response.data, ensure_ascii=False)
            cache.set(cache_key, json_data, timeout=60*15)
            print(_("Cached response with key: "), cache_key)
        except Exception as e:
            print(_("Error caching response: "), e)

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache_key = self.get_cache_key("list", request)
            cache.delete(cache_key)
            print(_("Invalidated cache with key: "), cache_key)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code in [200, 204]:
            obj_id = kwargs.get('pk')
            list_cache_key = self.get_cache_key("list", request)
            retrieve_cache_key = self.get_cache_key("retrieve", request, obj_id)
            cache.delete(list_cache_key)
            cache.delete(retrieve_cache_key)
            print(_("Invalidated cache with keys: "), list_cache_key, " and ",  retrieve_cache_key)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            obj_id = kwargs.get('pk')
            list_cache_key = self.get_cache_key("list", request)
            retrieve_cache_key = self.get_cache_key("retrieve", request, obj_id)
            cache.delete(list_cache_key)
            cache.delete(retrieve_cache_key)
            print(_("Invalidated cache with keys: "), list_cache_key, " and ", retrieve_cache_key)
        return response

class UserCachedListViewSet(viewsets.ModelViewSet):

    def get_cache_key(self, prefix, request, obj_id=None):
        """Genera una clave de caché única en el formato especificado."""
        key = f"{self.app_name}:{self.model_name}:{prefix}:{request.user.id}"
        if obj_id:
            key += f":{obj_id}"
        return key

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key("list", request)
        cached_data = cache.get(cache_key)
        if cached_data:
            print(_("Returning cached response with key: "), cache_key)
            return Response(json.loads(cached_data))
        
        response = super().list(request, *args, **kwargs)
        if response.data:
            try:
                json_data = json.dumps(response.data, ensure_ascii=False)
                cache.set(cache_key, json_data, timeout=60*15)
                print(_("Cached response with key:"), cache_key)
            except Exception as e:
                print(f"Error caching response: {e}")
        
        return response

    def retrieve(self, request, *args, **kwargs):
        obj_id = kwargs.get('pk')
        cache_key = self.get_cache_key("retrieve", request, obj_id)
        cached_data = cache.get(cache_key)
        if cached_data:
            print(_("Returning cached response with key: "), cache_key)
            return Response(json.loads(cached_data))

        response = super().retrieve(request, *args, **kwargs)
        try:
            json_data = json.dumps(response.data, ensure_ascii=False)
            cache.set(cache_key, json_data, timeout=60*15)
            print(_("Cached response with key: "), cache_key)
        except Exception as e:
            print(_("Error caching response: "), e)

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache_key = self.get_cache_key("list", request)
            cache.delete(cache_key)
            print(_("Invalidated cache with key: "), cache_key)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code in [200, 204]:
            obj_id = kwargs.get('pk')
            list_cache_key = self.get_cache_key("list", request)
            retrieve_cache_key = self.get_cache_key("retrieve", request, obj_id)
            cache.delete(list_cache_key)
            cache.delete(retrieve_cache_key)
            print(_("Invalidated cache with keys: "), list_cache_key, " and ",  retrieve_cache_key)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            obj_id = kwargs.get('pk')
            list_cache_key = self.get_cache_key("list", request)
            retrieve_cache_key = self.get_cache_key("retrieve", request, obj_id)
            cache.delete(list_cache_key)
            cache.delete(retrieve_cache_key)
            print(_("Invalidated cache with keys: "), list_cache_key, " and ", retrieve_cache_key)
        return response

def has_no_hate_content(text, umbral):
    # Detectar el idioma del texto
    language = detect(text)

    if language != 'en':
        # Traducir el texto a inglés si no está en inglés
        translator = Translator()
        translation = translator.translate(text, src=language, dest='en')
        text_en = translation.text
    else:
        # Si el texto está en inglés, utilizarlo directamente
        text_en = text

    # Realizar la validación en el texto en inglés
    blob_en = TextBlob(text_en)
    for sentence in blob_en.sentences:
        if sentence.polarity < umbral:  
            return False

    return True
#

# Create your views here.
