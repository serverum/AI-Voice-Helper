import random
import nltk
import speech_recognition as sr
import playsound
import gtts
import os

BOT_CONFIG = {
    'intents': {
        'hello': {'examples': ['Привет', 'Здравствуйте', 'Добрый день'],
                  'responses': ['Прувет', 'Здравствуйте!', 'Доброго времени суток!']
                  },
        'buy': {
            'examples': ['До свидания', 'Пока', 'До новых встреч'],
            'responses': ['Пока пока', 'Чао', 'Hasta La Vista']
        },

        'howdy': {
            'examples': ['Как дела？', 'Как поживаешь?', 'Как ты'],
            'responses': ['отлично', 'как сам', 'лучше только в валхале']

        },

        'city': {
            'examples': ['Ты откуда', 'С какого ты города', 'Ты где живешь'],
            'responses': ['Москва', 'Столичный бот я', 'Питерский я бобот']
        },

        'mood': {
            'examples': ['Как настроение', 'Ты чего грустный', 'Че по настроению'],
            'responses': ['Все супер', 'Отличняк', 'Зашибись']
        },

        'doings': {
            'examples': ['Что делаешь', 'Чем занимаешься', 'Чем занят'],
            'responses': ['Жарю зефир', 'Строчу со скоростью света тебе', 'Писаю буквами']
        },

        'sports': {
            'examples': ['Любишь футбол', 'Занимаешься спортом', 'спорт любишь'],
            'responses': ['Обожаю', 'Гамаю в это сутками', 'Даааааа']
        }
    }
}


def voice_recognizer():
    print("Скажите что-нибудь >>>")
    # We will transform this function later to get voice
    try:
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)  # убираем посторонние шумы
        with m as source:
            audio = r.listen(source)  # Микрофон захвачен

        # Микрофон снова доступен другим программам

        voice_text = r.recognize_google(audio, language="ru")

        # Упражнение: добавить вывод текста
        print("Вы сказали:", voice_text)

        return voice_text
    except sr.UnknownValueError as err:
        print('Молчать нельзя, иначе выход', err)
        return 'пока'

def voice_reply(text):
    # Упражнение: добавить вывод текста
    print("Ассистент:", text)

    voice = gtts.gTTS(text, lang="ru")
    file_path = os.getcwd()
    audio_file = os.path.join(file_path, "audio.mp3")  # сохраняем в текущей директории наш аудио
    voice.save(audio_file)

    playsound.playsound(audio_file)
    os.remove(audio_file)

    return text


def preproccesor(text):
    output_text = ""
    for char in text.lower():
        if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            output_text += char
    return output_text


def get_intent(text):
    for intent in BOT_CONFIG['intents'].keys():
        # print(BOT_CONFIG['intents'].keys())
        for example in BOT_CONFIG['intents'][intent]['examples']:
            text1 = preproccesor(example)
            text2 = preproccesor(text)
            if len(text1) and len(text2) != 0:
                if nltk.edit_distance(text1, text2) / max(len(text1), len(text2)) < 0.4:
                    return intent
    return "Не удалось определить интент"


def bot(input_text):
    intent = get_intent(input_text)
    if intent != "Не удалось определить интент":
        rec = random.choice(BOT_CONFIG['intents'][intent]['responses'])
        voice_reply(rec)
    else:
        return 'Не пойму я еще твой интент'


def main():
    print('Начните со мной общение с первого слова>>>')
    input_text = ''
    while input_text != 'Завершить работу':
        input_text = voice_recognizer()
        print(bot(input_text))


if __name__ == '__main__':
    main()
