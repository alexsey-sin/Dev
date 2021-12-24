def reverse(text):
    return text[::-1]
    
def is_palindrome(text):
    forbidden = (' ', '/', '.', ',', '!', ':', ';', '&', '?')
    # char_list = []
    # for s in text:
        # if s not in forbidden:
            # char_list.append(s)
    # s_text = ''.join(char_list).lower()
    
    s_text = ''.join(c for c in text if c not in forbidden).lower()
    print(s_text)
    return s_text == reverse(s_text)
    
something = input('Введите текст: ')
if is_palindrome(something):
    print("Да, это палиндром")
else:
    print("Нет, это не палиндром")