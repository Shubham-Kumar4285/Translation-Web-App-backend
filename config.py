import google.generativeai as genai


def detect_language(text):
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # or Gemini LLM specialized for language tasks
    prompt = f"Detect the language of the following text: '{text}'. Return only the ISO 639-1 code."
    response = model.generate_content(prompt)
    lang_code = response.text.strip()
    return lang_code


def gemini_translate(text, source_lang, target_lang):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    prompt = (
        f"Translate '{text}' from {source_lang} to {target_lang}. "
        "Return ONLY the translated text, nothing else."
    )
    response = model.generate_content(prompt)
    return response.text.strip()
