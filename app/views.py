from django.shortcuts import render
import json
import os
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from app.models import *

# Create your views here.

class AppLandingView(View):

    def get(self, request):
        return render_to_response("app/ember_main.html", {}, context_instance=RequestContext(request))

    def post(self, request):
        prop = Property.objects.get(name="Ian's Pizza on State (fake)")
        return HttpResponse(json.dumps({"property_id": prop.id}), content_type="application/json")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(AppLandingView, self).dispatch(*args, **kwargs)


class PropertiesView(View):

    def get(self, request, property_id):
        """
        Returns ember-friendly dicts for a property and its associated reviews
        """
        prop = Property.objects.get(id=property_id)
        return HttpResponse(json.dumps({"properties": [prop.get_ember_dict()], "reviews": prop.get_all_review_dicts_for_ember(), "topics": prop.get_all_topic_dicts_for_ember()}), content_type="application/json")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(PropertiesView, self).dispatch(*args, **kwargs)


class ReviewsView(View):

    def get(self, request, review_id):
        """
        Returns ember-friendly dicts for a review
        """
        
