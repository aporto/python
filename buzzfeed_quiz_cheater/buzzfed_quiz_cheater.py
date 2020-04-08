import json
import os
import urllib.request
import collections

url = 'https://www.buzzfeed.com/br/rafaelcapanema/quantos-por-cento-sem-vergonha-voce-e?utm_source=dynamic&fbclid=IwAR28S5CPoAvhuT-T3JEbdHJQ1c47058pn3dGQMVahTYf_AWnZCOoSYJAkOk'

#url = 'https://www.buzzfeed.com/br/christianzamora/monte-a-piroca-ideal-e-revelaremos-um-segredo-profundo?origin=btm-fd'

def downloadJsonData(url):
    print ("Fazendo o download dos dados do quiz...")
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary

    scriptStart = text.index('{"subbuzz":{')
    script = text[scriptStart:]
    scriptEnd = script.index('</script>')
    script = script[:scriptEnd]
    data = json.loads(script)

    with open('data.json', 'w') as f:
        f.write(script)

    return data

#with open("data.json") as fp:
#    data = json.load(fp)
data = downloadJsonData(url)

try:
    hasPersonality = data['subbuzz']['questions'][0]['answers'][0]['personality_index']
    print("Perguntas ordenadas pela note decrescente:")
except:
    hasPersonality = False
    print("Perguntas sem ordem. Quizz não tem personality index:")

for question in data['subbuzz']['questions']:
    questionTitle = question['tile_text']
    print("%s" % (questionTitle))
    answers = {}
    count = 0

    # Monta a lista de respostas e depois as ordena em ordem decrescente de pontos
    for answer in question['answers']:
        answerTitle = answer['tile_text']
        if hasPersonality:
            personalityIndex = answer['personality_index']
            answers[personalityIndex] = answerTitle
        else:
            answers[count] = answerTitle
            count += 1

    answers = collections.OrderedDict(sorted(answers.items(), reverse=True))
    for answer in answers:
        print("\tResposta (%d pontos): %s " % (answer, answers[answer]))

print("\nResultados, ordenados por nota decrescente:")
count = len(data['subbuzz']['results'])
for idx in range(count):
    v=count-idx-1
    title = data['subbuzz']['results'][v]['header']
    print ("\t%d: %s" % (v, title))




