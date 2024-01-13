from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Import namespaces


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            # whatIsThis = ai_client.detect_language(documents=[text])
            # Output
            # [DetectLanguageResult(id=0, primary_language=DetectedLanguage(name=English, iso6391_name=en, confidence_score=1.0), warnings=[], statistics=None, is_error=False, kind=LanguageDetection)]

            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
            
            # Get sentiment
            # whatIsThis = ai_client.analyze_sentiment(documents=[text])
            # Output
            # [AnalyzeSentimentResult(id=0, sentiment=negative, warnings=[], statistics=None, confidence_scores=SentimentConfidenceScores(positive=0.0, neutral=0.01, negative=0.99), sentences=[SentenceSentiment(text=Very noisy and rooms are tiny The Lombard Hotel, San Francisco, USA 9/5/2018 बहुत बेकार है ये होटल , sentiment=negative, confidence_scores=SentimentConfidenceScores(positive=0.0, neutral=0.01, negative=0.99), length=99, offset=0, mined_opinions=[])], is_error=False, kind=SentimentAnalysis)]

            sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
            print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
            
            # Get key phrases
            # whatIsThis = ai_client.extract_key_phrases(documents=[text])
            # Output
            # [ExtractKeyPhrasesResult(id=0, key_phrases=['hôtel agréable', "L'Hotel Buckingham", 'Londres', 'UK', 'personnel', 'chambres'], warnings=[], statistics=None, is_error=False, kind=KeyPhraseExtraction)]
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if(len(phrases) > 0):
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))
            
            # Get entities
            # whatIsThis = ai_client.recognize_entities(documents=[text])
            # Output
            # [RecognizeEntitiesResult(id=0, entities=[CategorizedEntity(text=hôtel, category=Location, subcategory=None, length=5, offset=3, confidence_score=0.87), CategorizedEntity(text=Hotel Buckingham, category=Location, subcategory=None, length=16, offset=20, confidence_score=0.73), CategorizedEntity(text=Londres, category=Location, subcategory=City, length=7, offset=38, confidence_score=0.99), CategorizedEntity(text=Londres, category=Location, subcategory=None, length=7, offset=38, confidence_score=0.99), CategorizedEntity(text=Londres, category=Location, subcategory=GPE, length=7, offset=38, confidence_score=0.99), CategorizedEntity(text=UK, category=Location, subcategory=CountryRegion, length=2, offset=47, confidence_score=0.97), CategorizedEntity(text=hôtel, category=Location, subcategory=None, length=5, offset=62, confidence_score=0.96), CategorizedEntity(text=personnel, category=PersonType, subcategory=None, length=9, offset=72, confidence_score=0.68), CategorizedEntity(text=amical, category=Skill, subcategory=N]

            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if(len(entities) > 0):
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get linked entities
            # whatIsThis = ai_client.recognize_linked_entities(documents=[text])
            # Output
            # [RecognizeLinkedEntitiesResult(id=0, entities=[LinkedEntity(name=United Nations, matches=[LinkedEntityMatch(confidence_score=0.15, text=Un, length=2, offset=0)], language=en, data_source_entity_id=United Nations, url=https://en.wikipedia.org/wiki/United_Nations, data_source=Wikipedia, bing_entity_search_api_id=745078b6-bda9-6c9c-3967-aeda6bb10099), LinkedEntity(name=L'Hôtel, matches=[LinkedEntityMatch(confidence_score=0.42, text=L'Hotel, length=7, offset=18)], language=en, data_source_entity_id=L'Hôtel, url=https://en.wikipedia.org/wiki/L'Hôtel, data_source=Wikipedia, bing_entity_search_api_id=03fab396-5939-54d5-502c-7692fe637b7b), LinkedEntity(name=Buckingham, matches=[LinkedEntityMatch(confidence_score=0.02, text=Buckingham, length=10, offset=26)], language=en, data_source_entity_id=Buckingham, url=https://en.wikipedia.org/wiki/Buckingham, data_source=Wikipedia, bing_entity_search_api_id=c1c2979f-a8dc-9042-8fa4-d0fc332e2170), LinkedEntity(name=London, matches=[LinkedEntityMatch(confidence_score=0.49, text=Lo]
            
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()