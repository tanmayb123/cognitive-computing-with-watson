import json
import sys
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, CategoriesOptions, ConceptsOptions, EmotionOptions, EntitiesOptions, KeywordsOptions, MetadataOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions

API_key = 'w02JlNpjSbT6OBJSjT1dd3Fe4ebXETJz4yp0etEEFmrU'
Model_key = ' '

print("API_key = " + API_key)
print("Model_key = " + Model_key)

if len(sys.argv) > 1:
    resource_link = sys.argv[1]
else:
    resource_link = 'https://electrek.co/2019/02/18/tesla-model-3-aftermarket-bumper/'

print("Understanding document at: " + resource_link)

natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey=API_key,
        url='https://gateway.watsonplatform.net/natural-language-understanding/api')

response = natural_language_understanding.analyze(
        url=resource_link,
        features=Features(
            categories=CategoriesOptions(limit=10),
            concepts=ConceptsOptions(limit=50),
            emotion=EmotionOptions(document=True, targets=['Elon Musk', 'SpaceX', 'NASA']),
            entities=EntitiesOptions(limit=100, mentions=True, sentiment=True, emotion=True),
            keywords=KeywordsOptions(limit=100, sentiment=True, emotion=True),
            metadata=MetadataOptions(),
            relations=RelationsOptions(),
            semantic_roles=SemanticRolesOptions(limit=50, keywords=True, entities=True),
            sentiment=SentimentOptions(['Rockets', 'Space', 'Mars'])),
        return_analyzed_text=True).get_result()

print()
print("=======================================================================")
print()

if response.get("warnings") != None:
    for i in range(len(response["warnings"])):
        print("Warnings: " + response["warnings"][i].encode('utf-8'))

if response.get("language") != None:
    print("Text is written in " + response["language"])

if response.get("analyzed_text") != None:
    width = 200
    print("The text that was analyzed is:")
    for i in range(len(response.get("analyzed_text"))/width):
        print("    " + response.get("analyzed_text")[i*width:i*width+width].replace('\n',' ').encode('utf-8'))

if response.get("retrieved_url") != None:
    print("This text can be found at: " + response["retrieved_url"].encode('utf-8'))

if response.get("usage") != None:
    print("This request returned " + str(response["usage"]["features"]) + " features; processed " + str(response["usage"]["text_characters"]) + " charaters; in " + str(response["usage"]["text_units"]) + " units.")

if response.get("concepts") != None:
    print("The following concepts were discussed:")
    for i in range(len(response["concepts"])):
        print("    [" + response["concepts"][i]["text"].encode('utf-8') + "] with " + str(int(response["concepts"][i]["relevance"]*100)) + "% confidence, as identified in " + response["concepts"][i]["dbpedia_resource"].encode('utf-8'))

if response.get("entities") != None:
    print("The following entities were found:")
    for i in range(len(response["entities"])):
        relevance=response["entities"][i].get("relevance")
        if relevance == None:
            relevance=0
        print("    [" + response["entities"][i]["text"].replace(u'\xa0', u' ').encode('utf-8') + "] of type <" + response["entities"][i]["type"].replace(u'\xa0', u' ').encode('utf-8') + "> was found " + str(response["entities"][i]["count"]).replace(u'\xa0', u' ') + " times, with " + str(int(relevance*100)) + "% confidence.")
        print("        The entity was found in:")
        for j in range(len(response["entities"][i]["mentions"])):
            print("            \"" + response["entities"][i]["mentions"][j]["text"].replace(u'\xa0', u' ').encode('utf-8') + "\", at index " + str(response["entities"][i]["mentions"][j]["location"][0]).replace(u'\xa0', u' '))
        if (response["entities"][i].get("emotion")) != None:
            target_emotion=response["entities"][i]["emotion"]
            print("        The emotional scores for this entity are: " + str(int(target_emotion["anger"]*100)) + "% Anger; " + str(int(target_emotion["disgust"]*100)) + "% Disgust; " + str(int(target_emotion["fear"]*100)) + "% Fear; " + str(int(target_emotion["joy"]*100)) + "% Joy; and " + str(int(target_emotion["sadness"]*100)) + "% Sadness.")
        if (response["entities"][i].get("sentiment")) != None:
            print("        The sentiment score for this entity is: " + str(response["entities"][i]["sentiment"]["score"]))

if response.get("relations") != None:
    print("The following relationships were found:")
    for i in range(len(response["relations"])):
        print("    A <" + response["relations"][i]["type"].encode('utf-8') + "> relationship was found, with " + str(int(response["relations"][i]["score"]*100)) + "% confidence, in \"" + response["relations"][i]["sentence"].encode('utf-8') + "\", between the following entities:")
        for j in range(len(response["relations"][i]["arguments"])):
            print("        within \"" + response["relations"][i]["arguments"][j]["text"].encode('utf-8') + "\" at index " + str(response["relations"][i]["arguments"][j]["location"]) + ": ")
            for k in range(len(response["relations"][i]["arguments"][j]["entities"])):
                print("            [" + response["relations"][i]["arguments"][j]["entities"][k]["text"].encode('utf-8') + "] of type <" + response["relations"][i]["arguments"][j]["entities"][k]["type"].encode('utf-8') + ">")

if response.get("keywords") != None:
    print("The following keywords were found:")
    for i in range(len(response["keywords"])):
        print("    [" + response["keywords"][i]["text"].encode('utf-8') + "] was found " + str(response["keywords"][i]["count"]) + " times, with " + str(int(response["keywords"][i]["relevance"]*100)) + "% confidence.")
        if (response["keywords"][i].get("emotion")) != None:
            target_emotion=response["keywords"][i]["emotion"]
            print("        The emotional scores for this keyword are: " + str(int(target_emotion["anger"]*100)) + "% Anger; " + str(int(target_emotion["disgust"]*100)) + "% Disgust; " + str(int(target_emotion["fear"]*100)) + "% Fear; " + str(int(target_emotion["joy"]*100)) + "% Joy; and " + str(int(target_emotion["sadness"]*100)) + "% Sadness.")
        if (response["keywords"][i].get("sentiment")) != None:
                print("        The sentiment score for this keyword is: " + str(response["keywords"][i]["sentiment"]["score"]))

if response.get("categories") != None:
    print("The following categories of information were found:")
    for i in range(len(response["categories"])):
        print("    [" + response["categories"][i]["label"].encode('utf-8') + "] was found, with " + str(int(response["categories"][i]["score"]*100)) + "% confidence.")

if response.get("emotion") != None:
    document_emotion=response["emotion"]["document"]["emotion"]
    print("The overall document had an emotional score of: " + str(int(document_emotion["anger"]*100)) + "% Anger; " + str(int(document_emotion["disgust"]*100)) + "% Disgust; " + str(int(document_emotion["fear"]*100)) + "% Fear; " + str(int(document_emotion["joy"]*100)) + "% Joy; and " + str(int(document_emotion["sadness"]*100)) + "% Sadness.")
    if (response["emotion"].get("targets")) != None:
        print("Emotions were assessed for the following target entities:")
        for i in range(len(response["emotion"].get("targets"))):
            target_emotion=response["emotion"]["targets"][i]["emotion"]
            print("    [" + response["emotion"]["targets"][i]["text"].encode('utf-8') + "] was assessed with an emotional score of: " + str(int(target_emotion["anger"]*100)) + "% Anger; " + str(int(target_emotion["disgust"]*100)) + "% Disgust; " + str(int(target_emotion["fear"]*100)) + "% Fear; " + str(int(target_emotion["joy"]*100)) + "% Joy; and " + str(int(target_emotion["sadness"]*100)) + "% Sadness.")

if response.get("metadata") != None:
    print("The document meta data included:")
    for i in range(len(response["metadata"]["authors"])):
        print("    Authored by: " + response["metadata"]["authors"][i]["name"].encode('utf-8'))
    print("    It was published on:" + response["metadata"]["publication_date"].encode('utf-8') + " with a title of \"" + response["metadata"]["title"].encode('utf-8') + "\", and links to:")
    for i in range(len(response["metadata"]["feeds"])):
        print("        " + response["metadata"]["feeds"][i]["link"].encode('utf-8'))
    print("    And an image of: " + response["metadata"]["image"].encode('utf-8'))


if response.get("semantic_roles") != None:
    print("Semantic roles were found in the following sentances:")
    for i in range(len(response["semantic_roles"])):
        print(("    \"" + response["semantic_roles"][i]["sentence"] + "\"").encode('utf-8'))
        if (response["semantic_roles"][i].get("subject") != None):
            print("        Subject: \"" + response["semantic_roles"][i]["subject"]["text"].encode('utf-8') + "\".")
        if (response["semantic_roles"][i].get("action") != None):
            print("         Action: \"" + response["semantic_roles"][i]["action"]["text"].encode('utf-8') + "\".")
        if (response["semantic_roles"][i].get("object") != None):
            print("         Object: \"" + response["semantic_roles"][i]["object"]["text"].encode('utf-8') + "\".")

if response.get("sentiment") != None:
    if (response["sentiment"].get("document") != None):
        print("The overall tone of the document is " + response["sentiment"]["document"]["label"].encode('utf-8'))
# Need to add sentiment assessment for each targeted entity.

