from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'hangman-secret-key-2024'

WORDS = ['python', 'programming', 'computer', 'hangman', 'developer',
         'keyboard', 'algorithm', 'function', 'variable', 'internet',
         'database', 'software', 'hardware', 'network', 'security',
         'javascript', 'framework', 'coding', 'debugging', 'terminal']


def initialize_game():
    word = random.choice(WORDS).lower()
    session['word'] = word
    session['guessed_letters'] = []
    session['attempts'] = 6
    session['word_completion'] = ['_'] * len(word)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    initialize_game()
    return jsonify({
        'word_display': ' '.join(session['word_completion']),
        'attempts': session['attempts'],
        'guessed_letters': session['guessed_letters'],
        'game_over': False
    })


@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    letter = data.get('letter', '').lower()

    if not letter or len(letter) != 1 or not letter.isalpha():
        return jsonify({'error': 'Invalid input'}), 400

    word = session.get('word')
    guessed_letters = session.get('guessed_letters', [])
    attempts = session.get('attempts', 6)
    word_completion = session.get('word_completion', [])

    if letter in guessed_letters:
        return jsonify({
            'word_display': ' '.join(word_completion),
            'attempts': attempts,
            'guessed_letters': guessed_letters,
            'message': 'You already guessed that letter!',
            'game_over': False,
            'correct': False
        })

    guessed_letters.append(letter)
    session['guessed_letters'] = guessed_letters

    correct = False
    if letter in word:
        correct = True
        for i, char in enumerate(word):
            if char == letter:
                word_completion[i] = letter
        session['word_completion'] = word_completion
        message = f"Good job! '{letter}' is in the word."
    else:
        attempts -= 1
        session['attempts'] = attempts
        message = f"Sorry, '{letter}' is not in the word."

    game_over = False
    if '_' not in word_completion:
        game_over = True
        message = f"🎉 Congratulations! You won! The word was '{word}'."
    elif attempts == 0:
        game_over = True
        message = f"💀 Game Over! The word was '{word}'."
        word_completion = list(word)

    return jsonify({
        'word_display': ' '.join(word_completion),
        'attempts': attempts,
        'guessed_letters': sorted(guessed_letters),
        'message': message,
        'game_over': game_over,
        'correct': correct
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)