import regex as re
import os
def clean_text(text):
    text=re.sub(r'\*(\w+)\*',  r' \1 ', text)

#   remove caracters at the end of a line
    text=re.sub(r'\'+\n', '\n', text)
    text=re.sub(r'\*+\n', '\n', text)

    #     remove the last line return
    #todo : trim and lowercase in refine
    text = text.rstrip('\n')
    text = text.lstrip(',')
    text = text.lstrip('/')
    text = text.lstrip(' ')

#         remove successive spaces
    text=re.sub(r'(\s)+', r'\1', text)


#         change all tab to one tab
    text=re.sub(r'\\+t',  r'\\t', text)

#         remove the following occurence from the text
    text=re.sub(r'\'\?',  r'', text)
#         successive remove occurences of \t
    text=re.sub(r'(\\t)+',  r'\\t', text)
    text=re.sub(r'(\' *)+',  '\'', text)



#         replace '\t' with space
    text=re.sub(r'\\t',  r' ', text)
    text = text.replace('\t', ' ')
#         remove sucessive spaces
    text=re.sub(r'(\s)+',  r'\1', text)


#         fix les puces - sans espace
    text=re.sub(r'^-([a-zA-Z\S])',  r'\1', text)
    text=re.sub(r'\n-([a-zA-Z\S])',  r'\n\1', text)

#         fix problems in the start of paragraph
    list_caracters = ['\*','\?','\.','>','[1-9]\.','[1-9]', '¤']
    for character in list_caracters:
        text=re.sub(r'^(?:'+character+'|'+character+' )([a-zA-Z\S])',  r'- \1', text)
    text=re.sub(r'^(?:\*|\* )([a-zA-Z\S])',  r'\n- \1', text)
    text=re.sub(r'^ *: *',  r'', text)

#         fix the problem des puces other than -
    list_caracters = ['\*','\·','\.','>', '¤', 'o', '\?']
    for character in list_caracters:
        text=re.sub(r'\n(?:'+character+'|'+character+' )([a-zA-Z\S])',  r'\n- \1', text)
#         the numbering puces
    text=re.sub(r'\n(?:[1-9][0-9]|[1-9])\.? ?([a-zA-Z\S])', r'\n- \1', text)


#         fix problem in the middle of the text
    list_caracters = ['\*','\?']
    for character in list_caracters:
        text=re.sub(r'([a-zA-Z\S\.])(?: '+character+' |'+character+' | '+character+')([a-zA-Z\S])',  r'\1\n- \2', text)

#     remove empty cells and the ones starting with '
    text=re.sub(r' ?\n-\s+\n',  r'\n', text)
    text=re.sub(r'\n- \'+', r'\n- ', text)
    text=re.sub(r'\n.\n', r'\n', text)
    text=re.sub(r'- *[0-9]+-[0-9]+', r'', text)
    text=re.sub(r'\n+', r'\n', text)
    text=re.sub(r'- [0-9]+\s', r'', text)
    text=re.sub(r'- [A-Za-z]+$', r'', text)
    text=re.sub(r'- *$', r'', text)
    text=re.sub(r'- ~*\n', r'', text)

    #clean all puces
    text=re.sub(r'^[\.>\?\-\:]', r'', text)
    text=re.sub(r'[\*\·¤\=]', '.', text)
    # temporary replace -
    text=re.sub('-',' ',text)
    text = os.linesep.join([s for s in text.splitlines() if s])
    return text
