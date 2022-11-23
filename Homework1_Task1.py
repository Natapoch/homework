try:
    a = float(input('Оцените силу вашей душевной боли по шкале от 0 до 10: '))
    if 0 < a < 0.7:
        print('Кажется, вы испытываете легкое огорчение. Как человек в короткой поездке в метро, забывший дома наушники')
    elif 0.7 <= a < 2:
        print('Вы огорчены, будто на вашу одежду пролили утренний кофе. Но учтите, что кофейные пятна легко отстирываются')
    elif 2 <= a <= 4.2:
        print('Вы встревожены - почти как человек, которому придется звонить по телефону, и это в эпоху мессенджеров!')
    elif 4.2 < a < 5:
        print('Вы огорчены, будто прямо перед Вашим носом ушёл автобус, а следующий приедет через двадцать минут (и то, если только звезды сойдутся). Не расстраивайтесь, в таких ситуациях рано или поздно всё равно приезжает следующий автобус. А маленькая трудность - повод для размышления о чём-то большем')
    elif 5 <= a <= 6.9:
        print('Вы встревожены, как студент во время сессии. Но не забывайте, что сессия - это всего лишь небольшой период жизни')
    elif 6.9 < a <= 8:
        print('Вы слишком огорчены. Так огорчены, как программист, у которого не работает git. Помните, что поломки чинятся, жизнь становится лучше')
    elif 8 < a <= 9.9:
        print('Вы расстроены и подавлены так сильно, будто вам пришлось ехать в час пик от Выхино до другого конца Москвы с тремя пересадками на самых людных станциях. Поправьте одежду и причёску, протрите оттоптанные ботинки, разомните ту ногу, на которой пришлось стоять всю дорогу,  и идите вперёд. Трудности должны делать нас только сильнее')
    elif 9.9 < a <= 10:
        print('Вы слишком растроены и подавлены. Так сильно, как будто мир рушится вокруг Васю Но это не так. Всё будет хорошо')
    elif a <= 0:
        print('Поздравляем! У Вас всё хорошо. Сохраняйте свой оптимизм и жизнелюбие - это важные качества')
    else:
        print('Ваша душевная боль превашает заданный диапазон границ. Всё будет хорошо. Обратитесь к специалисту в области психологии, если хотите узнать детали')
except ValueError:
    print('Попробуйте ещё раз. Введите цифровое значение от 0 до 10')




