"""
В цепочках ДНК символы «A» и «T» дополняют друг друга, как «C» и «G».
У вас есть функция с одной стороной ДНК (строка, кроме Haskell);
вам нужно получить другую дополнительную сторону.
Нить ДНК никогда не бывает пустой или ДНК вообще не бывает
(опять же, за исключением Haskell).

Например:
>>> spin_words( "Hey fellow warriors" )
'Hey wollef sroirraw'
>>> spin_words( "This is a test")
'This is a test'
>>> spin_words( "This is another test" )
'This is rehtona test'

"""

def DNA_strand(dna):
    out = ''
    for ch in dna:
        if ch == 'A':
            out += 'T'
        elif ch == 'T':
            out += 'A'
        elif ch == 'G':
            out += 'C'
        elif ch == 'C':
            out += 'G'
    
    return out

# if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
print(DNA_strand("AAAA"), "TTTT")
print(DNA_strand("ATTGC"), "TAACG")
print(DNA_strand("GTAT"), "CATA")

# или
# import string
# def DNA_strand(dna):
    # return dna.translate(string.maketrans("ATCG","TAGC"))        
        
        