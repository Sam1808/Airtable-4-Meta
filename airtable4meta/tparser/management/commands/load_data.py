import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from environs import Env

from tparser.models import Rawdata, Psychotherapist, Method



class Command(BaseCommand):
    help = 'Add data to database.'

    def handle(self, *args, **options):

        env = Env()
        env.read_env()
        
        api_key = env.str("AIRTABLE_API_KEY")        
        base_id = env.str("AIRTABLE_BASE_ID")
        table_name = env.str("AIRTABLE_NAME", "Psychotherapists")

        url = f'https://api.airtable.com/v0/{base_id}/{table_name}'

        headers = {'Authorization': f'Bearer {api_key}'}

        response = requests.get(url, params=(), headers=headers)
        airtable_response = response.json()
        
        raw_data = Rawdata.objects.create(data=str(airtable_response))

        print(f'Create data dump with ID:{raw_data.id} at {raw_data.upload_datetime}')

        airtable_records = []

        for record in airtable_response['records']:

            psychotherapist, created = Psychotherapist.objects.get_or_create(
                airtable_id = record['id'],                
            )

            airtable_records.append(record['id'])

            if psychotherapist.name != record['fields']['Имя']:
                psychotherapist.name = record['fields']['Имя']
                psychotherapist.save()
                

            image_url = record['fields']['Фотография'][0]['url']
            image_air_name = image_url.split('/')[-1]
            image_name = f'{psychotherapist.airtable_id}-{image_air_name}'
            
            if psychotherapist.image.name != image_name:
                response = requests.get(image_url)
                psychotherapist.image.save(image_name, ContentFile(response.content))
                

            if not created: # I can do it more elegantly ;)
                psychotherapist.tag.all().delete()
                
            for method in record['fields']['Методы']:
                tag, created = Method.objects.get_or_create(method=method)
                psychotherapist.tag.add(tag)
            
            

        table_differences = set(Psychotherapist.objects.all().values_list('airtable_id', flat=True)) - set(airtable_records)
        
        if len(table_differences) > 0:
            for base_record in table_differences:
                Psychotherapist.objects.get(airtable_id = base_record).delete()
                print (f'Record ID: {base_record} was deleted!')

        return "Done!"
        