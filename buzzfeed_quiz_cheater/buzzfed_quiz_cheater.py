import json
import os
import urllib.request
import collections

DEBUG = True

def downloadJsonData(url):
    print ("Fazendo o download dos dados do quiz...")
    try:
        response = urllib.request.urlopen(url)
    except:
        return None

    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

    title = text[text.index('<title>') + 7:]
    title = title[:title.index('</title>')]

    scriptStart = text.index('{"subbuzz":{')
    script = text[scriptStart:]
    scriptEnd = script.index('</script>')
    script = script[:scriptEnd]
    data = json.loads(script)

    if DEBUG:
        with open('data.json', 'w') as f:
            f.write(script)
    print("Pronto!\n")

    data['alex_title'] = title

    return data

def main(url):
    if not DEBUG:
        with open("data.json") as fp:
            data = json.load(fp)
    else:
        data = downloadJsonData(url)

    if data is None:
        print ("Erro: Não foi possivel baixar os dados do link que você passou:")
        print(url)
        return

    #if data['subbuzz']['type'] != 'personality':
    #    print("Desculpe. Esse programa só funciona com testes BuzzFeed do tipo 'Personalidade'")
        #return

    try:
        hasPersonality = data['subbuzz']['questions'][0]['answers'][0]['personality_index']
        print("Perguntas ordenadas pela note decrescente:")
    except:
        hasPersonality = False
        print("Perguntas sem ordem. Quizz não tem personality index:")

    highScore = []
    questionIdx = 1
    for question in data['subbuzz']['questions']:
        questionTitle = question['header'].strip()
        if questionTitle == '':
            questionTitle = question['tile_text']
        if questionTitle == '':
            questionTitle = 'Pergunta %d' % (questionIdx)
            questionIdx += 1
        print("%s" % (questionTitle))
        answers = {}
        count = 0

        highScore.append([questionTitle, -1, ''])

        # Monta a lista de respostas e depois as ordena em ordem decrescente de pontos
        for answer in question['answers']:
            answerTitle = answer['header'].strip()
            if answerTitle == '':
                answerTitle = answer['tile_text'].strip()
            if answerTitle == '':
                answerTitle = "Resposta %d" % (count + 1)

            if hasPersonality:
                personalityIndex = answer['personality_index']
                answers[personalityIndex] = answerTitle
                points = personalityIndex
            else:
                answers[count] = answerTitle
                try:
                  isCorrect = answer['correct'] == 1
                except:
                  isCorrect = False

                if isCorrect:
                    points = 1
                else:
                    points = 0
            count += 1

            if highScore[-1][1] < points:
                highScore[-1] = [questionTitle, points, answerTitle]

        answers = collections.OrderedDict(sorted(answers.items(), reverse=True))
        #first = True
        for answer in answers:
            print("\tResposta (%d pontos): %s " % (answer, answers[answer]))
            #if first:
            #    highScore.append([questionTitle, answers[answer]])
            #    first = False

    print("\nResultados, ordenados por nota decrescente:")
    count = len(data['subbuzz']['results'])
    for idx in range(count):
        v=count-idx-1
        title = data['subbuzz']['results'][v]['header']
        print ("\t%d: %s" % (v, title))

    print("\n===============================================================")
    print (data['alex_title'])

    print("Para tirar a maior nota, responda da seguinte forma:")
    for question, points, answer in highScore:
        print("\t%s %s" % (question, answer))

print ("Copie e cole o endeço do teste BuzFeed na linha abaixo:")
print ("(Use o botão direito e selecione 'Colar' no menu que vai se abrir)")

if DEBUG:
    #url = 'https://www.buzzfeed.com/br/victornascimento/biscoito-corpo-delicia-biscoiteiro-nudes?origin=btm-fd'
    #url = 'https://www.buzzfeed.com/br/rafaelcapanema/quantos-por-cento-sem-vergonha-voce-e?utm_source=dynamic&fbclid=IwAR28S5CPoAvhuT-T3JEbdHJQ1c47058pn3dGQMVahTYf_AWnZCOoSYJAkOk'
    #url = 'https://www.buzzfeed.com/br/farrahpenn/duvido-voco-gabaritar-este-quiz-sobre-orgasmo?origin=btm-fd'
    url = 'https://www.buzzfeed.com/br/jasminnahar/teste-comidas-salgadas-pessoa-doce?origin=btm-fd'
    url = 'https://www.buzzfeed.com/portinari/qual-presidente-do-brasil-do-saculo-xx-voca-seri-2cft1xnlr9?utm_source=dynamic&utm_campaign=bfsharefacebook&quiz_result=124577124_4&fbclid=IwAR0stXjVNRNX2OBS8viYscUL3WLP16-DVjU1KfBJ9aBAEUMCqTniByjlX6E#124577124'
else:
    url = input('>>')

main(url)

#print("")
#print(url)
#url = 'https://www.buzzfeed.com/br/rafaelcapanema/quantos-por-cento-sem-vergonha-voce-e?utm_source=dynamic&fbclid=IwAR28S5CPoAvhuT-T3JEbdHJQ1c47058pn3dGQMVahTYf_AWnZCOoSYJAkOk'

#url = 'https://www.buzzfeed.com/br/christianzamora/monte-a-piroca-ideal-e-revelaremos-um-segredo-profundo?origin=btm-fd'



#with open("data.json") as fp:
#    data = json.load(fp)




