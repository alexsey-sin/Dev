"""
Например:
>>> spin_words( "Hey fellow warriors" )
'Hey wollef sroirraw'
>>> spin_words( "This is a test")
'This is a test'
>>> spin_words( "This is another test" )
'This is rehtona test'

"""

def spin_words(row):
    # r_list = []
    # for world in row.split():
        # if len(world) >= 5:
            # world = world[::-1]
        # r_list.append(world)
    # return ' '.join(r_list)
    #или
    # return ' '.join((lambda w: w[::-1] if (len(w) >= 5) else w)(w) for w in row.split())
    #или
    return " ".join([w[::-1] if len(w) >= 5 else w for w in row.split()])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
# print(spin_words("Hey fellow warriors"))
# print(spin_words("This is a test"))
# print(spin_words("This is another test"))
