def translit_ru_to_en(text):
    "Russian translit: converts 'привет'->'privet'"

    table = {u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'e', u'з': 'z',
             u'и': 'i', u'й': 'j', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p',
             u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ъ': "'", u'ы': 'y',
             u'ь': "'", u'э': 'e', u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E',
             u'Ё': 'E', u'З': 'Z', u'И': 'I', u'Й': 'J', u'К': 'K', 'Л': 'L', u'М': 'M', u'Н': 'N',
             u'О': 'O', u'П': 'P', u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H',
             u'Ъ': "'", 'Ы': 'Y', u'Ь': "'", u'Э': 'E', u'ж': 'zh', u'ц': 'ts',u'ч': 'ch',u'ш': 'sh',
             u'щ': 'sch',u'ю': 'ju',u'я': 'ja', u'Ж': 'Zh', u'Ц': 'Ts', u'Ч': 'Ch'}

    translit = u''
    for i, item in enumerate(text):
        if item in table:
            item = table[item]
        translit += item
    return translit
