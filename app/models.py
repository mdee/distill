from django.db import models
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    """
    A review of a location
    """
    text = models.CharField(max_length=5000)
    author = models.CharField(max_length=1000, default="Unknown")
    grade = models.IntegerField(null=True)
    created_date = models.DateTimeField(default=timezone.now(), null=False)

    def get_ember_dict(self):
        return {"text": self.text, "grade": self.grade, "id": self.id}


class Topic(models.Model):
    """
    A topic denoting a cluster or grouping of reviews.
        -'category' can be NGRAM, NOUNPHRASE, or ENTITY, defaults to NGRAM
    """
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=False, default='NGRAM')
    reviews = models.ManyToManyField(Review, null=True)

    def get_ember_dict(self):
        return {"name": self.name, "id": self.id, "reviews": [r.id for r in self.reviews.all()]}


class Property(models.Model):
    """
    A physical location belonging to a Customer organization, stores its reviews
    """
    #  Instance fields
    name = models.CharField(max_length=100)
    reviews = models.ManyToManyField(Review, null=True)
    topics = models.ManyToManyField(Topic, null=True)
  
    def get_ember_dict(self):
        return {"name": self.name, "id": self.id, "reviews": [r.id for r in self.reviews.all()], "topics": [t.id for t in self.topics.all()]}

    def get_all_review_dicts_for_ember(self):
        return [r.get_ember_dict() for r in self.reviews.all()]

    def get_all_topic_dicts_for_ember(self):
        return [t.get_ember_dict() for t in self.topics.all()]

