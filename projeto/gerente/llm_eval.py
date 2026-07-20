import requests
import mytokens

def llm_responde(pergunta):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={mytokens.GEMINI_TOKEN}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "systemInstruction": {
            "parts": [{"text": "Faça uma análise das especificações de hardware passado, responda sempre em português, evitando emojis ou detalhar o texto de qualquer forma e de forma resumida."}]
        },

        "contents": [
            {
                "parts": [
                    {"text": ""}
                ]
            }
        ],

        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 10000
        }
    }


    data['contents'][0]['parts'][0]['text'] = pergunta

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        resposta = response.json()
        resposta = resposta['candidates'][0]['content']['parts'][0]['text']
        return resposta
    else:
        return f'Não foi possível conectar com a llm:  {response.status_code}'

    #para consultar os modelos válidos
    #curl -X GET \ "https://generativelanguage.googleapis.com/v1beta/models?key=[TOKEN]"
