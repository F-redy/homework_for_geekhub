# task 4.
# Створіть функцію <morse_code>, яка приймає на вхід рядок у вигляді
# коду Морзе та виводить декодоване значення (латинськими літерами).
#    Особливості:
#     - використовуються лише крапки, тире і пробіли (.- )
#     - один пробіл означає нову літеру
#     - три пробіли означають нове слово
#     - результат може бути case-insensetive (на ваш розсуд - велики чи маленькими літерами).
#     - для простоти реалізації - цифри, знаки пунктуацїї, дужки, лапки тощо використовуватися не будуть.
#     Лише латинські літери.
#     - додайте можливість декодування сервісного сигналу SOS (...---...)
#     Приклад:
#     --. . . -.- .... ..-- -...   .. ...   .... . .-. .
#     результат: GEEKHUB IS HERE


MORSE_DECODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I',
    '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '-----': '0',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'", '-.-.--': '!', '-..-.': '/', '-.--.': '(',
    '-.--.-': ')', '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+',
    '-....-': '-', '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@',
}

MORSE_ENCODE = {value: key for key, value in MORSE_DECODE.items()}


def morse_code(morse_string: str) -> str:
    decoded_words = []

    for word in morse_string.split('   '):
        decoded_word = ''
        for letter in word.split():
            decoded_word += MORSE_DECODE.get(letter, letter)
        decoded_words.append(decoded_word)

    print(' '.join(decoded_words))

    return ' '.join(decoded_words)


def encode_morse(string: str) -> str:
    morse_words = []

    for word in string.split():
        encoded_word = ''
        for letter in word:
            encoded_word += MORSE_ENCODE.get(letter, letter) + ' '
        morse_words.append(encoded_word.strip())

    print('   '.join(morse_words))

    return '   '.join(morse_words)


if __name__ == '__main__':
    morse_code('--. . . -.- .... ..- -...   .. ...   .... . .-. .')  # GEEKHUB IS HERE
    morse_code('... --- ...   .- .-')  # SOS AA
    morse_code('.... . .-.. .-.. --- -.-.--   .... --- .--   .- .-. .   -.-- --- ..- -.-.--')  # HELLO! HOW ARE YOU!
    morse_code('-.-. .- .-.. .-..   ----. .---- .---- -.-.--   .-- .   -. . . -..   .--. .. --.. --.. .-   ..- .-.'
               ' --. . -. - .-.. -.-- -.-.--')  # CALL 911! WE NEED PIZZA URGENTLY!
