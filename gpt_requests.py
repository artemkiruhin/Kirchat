import g4f
def get_gpt_response(message):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        if isinstance(response, dict) and 'choices' in response:
            return response['choices'][0]['message']['content']
        elif isinstance(response, str):
            return response
        else:
            return "Неизвестный формат ответа от GPT-4."
    except Exception as e:
        return f"Извините, произошла ошибка: {str(e)}"