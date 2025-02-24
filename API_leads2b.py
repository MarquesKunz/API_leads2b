import requests
import json
import csv
import os

url = '---------------'
token = '--------------'

headers = {
    'Authorization': f'Bearer {token}'
}
params = {
    'updated_from': '2022-01-01 00:00:00',
    'limit': 120
}
response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    try:
        data = response.json()

        oportunidade_2 = data.get('result', [])
        if not oportunidade_2:
            print("Nenhuma oportunidade encontrada. Verifique os parâmetros da requisição.")
            exit()

        with open('oportunidade_2.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow([
                'opportunity_id', 'lead_id', 'pipeline', 'pipeline_step', 'contact_name', 'contact_email',
                'contact_state', 'contact_city', 'customer_address', 'customer_neighborhood', 'customer_number',
                'customer_complement', 'customer_city', 'customer_state', 'opportunity_status', 'total_value', 'tags', 'items'
            ])

            for opportunity in oportunidade_2:
                tags = ', '.join(tag['name'] for tag in opportunity.get('tags', []))
                items = ', '.join(item['name'] + ': ' + item['description'] for item in opportunity.get('items', []))

                total_value = float(opportunity.get('opportunity_total_value', '0') or '0')

                writer.writerow([
                    opportunity.get('opportunity_id', ''),
                    opportunity.get('lead_id', ''),
                    opportunity.get('pipeline', ''),
                    opportunity.get('pipeline_step', ''),
                    opportunity.get('contact_name', ''),
                    opportunity.get('contact_email', ''),
                    opportunity.get('contact_state', ''),
                    opportunity.get('contact_city', ''),
                    opportunity.get('customer_address', ''),
                    opportunity.get('customer_neighborhood', ''),
                    opportunity.get('customer_number', ''),
                    opportunity.get('customer_complement', ''),
                    opportunity.get('customer_city', ''),
                    opportunity.get('customer_state', ''),
                    opportunity.get('opportunity_status', ''),
                    total_value,  # Agora está correto!
                    tags,
                    items
                ])

        if os.path.exists("oportunidade_2.csv"):
            print("Arquivo 'oportunidade_2.csv' criado com sucesso!")
        else:
            print("Erro ao criar o arquivo CSV.")

    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON")
        print("Conteúdo da resposta:", response.text)
else:
    print(f"Erro na requisição: {response.status_code}")
    print("Conteúdo da resposta:", response.text)
