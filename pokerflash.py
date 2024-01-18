from flask import Flask, render_template, request
from pypokerengine.api.game import setup_config, start_poker

app = Flask(__name__)

def open_range(posicao):
    if posicao == 'UTG':  # Under the Gun (primeira posição)
        return {'AA', 'KK', 'QQ', 'JJ', 'AKs', 'AQs'}
    elif posicao == 'MP':  # Middle Position (posição intermediária)
        return open_range('UTG').union({'TT', '99', 'AK', 'AQ', 'AJs', 'KQs'})
    elif posicao == 'CO':  # Cutoff (posição tardia)
        return open_range('MP').union({'88', '77', '66', 'ATs', 'KTs', 'QTs', 'JTs', 'KQ'})
    elif posicao == 'BTN':  # Button (botão)
        return open_range('CO').union({'55', '44', '33', '22', 'A9s', 'K9s', 'Q9s', 'J9s', 'T9s', '98s'})
    elif posicao == 'SB':  # Small Blind (pequeno blind)
        return open_range('BTN').union({'A8s', 'K8s', 'Q8s', 'J8s', 'T8s', '87s', 'A9', 'K9', 'Q9', 'J9', 'T9'})
    elif posicao == 'BB':  # Big Blind (grande blind)
        return open_range('SB').union({'A7s', 'K7s', 'Q7s', 'J7s', 'T7s', '98', '87', '76', '65'})

def calcular_equidade(minhas_cartas, posicao):
    # Aqui você pode implementar a lógica para calcular a equidade com base nas cartas e posição.
    # Este é um exemplo simples, você pode precisar de uma abordagem mais avançada.
    # Retorne um valor de equidade, por exemplo, entre 0 e 1.

    # Simulação simples para ilustrar o conceito
    if posicao == 'early':
        return 0.8
    elif posicao == 'late':
        return 0.9
    else:
        return 0.7

def analise_open_range_preflop(minhas_cartas, posicao):
    valor1, naipe1 = minhas_cartas[0]
    valor2, naipe2 = minhas_cartas[1]

    # Lógica de análise de open range no pré-flop
    if valor1 == valor2:
        return f"Avaliação Open Range Pré-Flop: Abordagem agressiva com um par de {valor1}s ({naipe1})."
    elif naipe1 == naipe2:
        return f"Avaliação Open Range Pré-Flop: Considerando um possível flush com {valor1} {naipe1} e {valor2} {naipe2}."
    else:
        # Aqui incorporamos o cálculo de equidade na mensagem de retorno
        equidade = calcular_equidade(minhas_cartas, posicao)
        return f"Avaliação Open Range Pré-Flop: Abordagem cautelosa com cartas não relacionadas ({valor1} {naipe1} e {valor2} {naipe2}). Equidade: {equidade * 100}%."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        carta1 = request.form['carta1']
        naipe1 = request.form['naipe1']
        carta2 = request.form['carta2']
        naipe2 = request.form['naipe2']
        posicao = request.form['posicao']

        minhas_cartas = [(carta1, naipe1), (carta2, naipe2)]
        resultado = analise_open_range_preflop(minhas_cartas, posicao)

        # Adicionando a avaliação do open range ao resultado
        resultado_open_range = open_range(posicao)
        resultado += f"\nOpen Range para {posicao}: {resultado_open_range}"

        return render_template('index.html', resultado=resultado)
    return render_template('index.html', resultado=None)

if __name__ == '__main__':
    app.run(debug=True)
