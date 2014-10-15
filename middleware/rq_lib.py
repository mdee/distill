from middleware.ner_lib import *
from app.models import *
import django_rq


def analyze_reviews_for_topics(property_id):
    prop = Property.objects.get(id=property_id)
    prop.topics_processing = True
    prop.save()
    docs = []
    for r in prop.reviews.all():
        docs.append({"text": r.text, "id": r.id})
    noun_phrase_list = pos_tag_text_documents(docs)
    new_phrases = []
    # Bucket noun phrases with same subject together.
    for n in noun_phrase_list:
        if len(new_phrases):
            found = False
            for np in new_phrases:
                if n["noun_phrase"].split(' ')[1] == np["noun_phrase"]:
                    found = True
                    for i in n["ids"]:
                        np["ids"].append(i)
                if len(np["noun_phrase"].split(' ')) == 2 and n["noun_phrase"].split(' ')[1] == np["noun_phrase"].split(' ')[1]:
                    np["noun_phrase"] = n["noun_phrase"].split(' ')[1]
                    found = True
                    for i in n["ids"]:
                        np["ids"].append(i)
            if not found:
                new_phrases.append(n)
        else:
            new_phrases.append(n)
    if len(new_phrases) > 10:
        new_phrases = new_phrases[:10]

    for n in new_phrases:
        if n["noun_phrase"] != "this place" and n["noun_phrase"] != "place" and n["noun_phrase"] != "this restaurant":
            new_topic = Topic(name=n["noun_phrase"], category='NOUNPHRASE')
            new_topic.save()
            for rid in n["ids"]:
                new_topic.reviews.add(Review.objects.get(id=rid))
            new_topic.save()
            prop.topics.add(new_topic)
            prop.save()
    prop.topics_analyzed = True
    prop.save()
