from flask import Flask, render_template, request

app = Flask(__name__)

def avaliar_jogada(minhas_cartas):
    valor1, naipe1 = minhas_cartas[0]
    valor2, naipe2 = minhas_cartas[1]

    # Simulação da lógica da IA para avaliação de jogadas
    if valor1 == valor2:
        return f"A IA apostaria/agiria de forma agressiva com um par ({valor1} {naipe1})."
    elif naipe1 == naipe2:
        return f"A IA consideraria um possível flush ({valor1} {naipe1} e {valor2} {naipe2})."
    else:
        return f"A IA talvez adotasse uma abordagem mais cautelosa com estas cartas ({valor1} {naipe1} e {valor2} {naipe2})."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        carta1 = request.form['carta1']
        naipe1 = request.form['naipe1']
        carta2 = request.form['carta2']
        naipe2 = request.form['naipe2']

        minhas_cartas = [(carta1, naipe1), (carta2, naipe2)]
        resultado = avaliar_jogada(minhas_cartas)

        return render_template('index.html', resultado=resultado)
    return render_template('index.html', resultado=None)

if __name__ == '__main__':
    app.run(debug=True)
