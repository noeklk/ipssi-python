import secrets

from flask import Flask, redirect, render_template, request, session, url_for

from .static.config import hostname
from .static.helper.casino_helper import (check_best_hand,
                                                   deuxieme_tirage, get_deck,
                                                   loop_deck_removal,
                                                   serve_amount_from_deck)

SECRET_KEY = secrets.token_urlsafe(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def set_bankroll(bankroll: int):
    session['bankroll'] = bankroll
def get_bankroll():
    return session['bankroll']

def set_bet(bet: int):
    session['bet'] = bet
def get_bet():
    return session['bet']

def reset():
    set_bankroll(0)
    set_bet(0)

@app.route('/')
@app.route('/start/<error_message>')
def view_start(error_message = None):
    reset()

    return render_template('play.html', hostname = hostname, error_message = error_message)

@app.route('/try_again', defaults={'error_message': None}, methods=['POST', 'GET'])
@app.route('/try_again/<error_message>', methods=['POST', 'GET'])
def view_try_again(error_message = None):
    return render_template('try_again.html', hostname = hostname, error_message = error_message, bankroll = get_bankroll())

@app.route('/bank_handler', methods=['POST', 'GET'])
def bank_handler():
    bankroll = int(request.form['bankroll'])
    bet = int(request.form['bet'])

    print(bankroll, bet)

    if bet > bankroll:
        if not bankroll:
            bankroll = get_bankroll()
            return redirect(url_for('try_again', error_message = "Montant parié supérieur à votre banque, veuillez saisir un montant inférieur à votre banque"))
    
        return redirect(url_for('view_start', error_message = "Montant parié supérieur à votre banque, veuillez saisir un montant inférieur à votre banque"))
    
    set_bankroll(bankroll - bet)
    set_bet(bet)

    return redirect(url_for('show_starting_hand_page'))

@app.route('/try_again_bank_handler', methods=['POST', 'GET'])
def try_again_bank_handler():
    bankroll = get_bankroll()
    bet = int(request.form['bet'])

    print(bankroll, bet)

    if bet > bankroll:

        return redirect(url_for('view_try_again', error_message = "Montant parié supérieur à votre banque, veuillez saisir un montant inférieur à votre banque"))
       
    set_bankroll(bankroll - bet)
    set_bet(bet)

    return redirect(url_for('show_starting_hand_page'))

@app.route('/starting_hand')
def show_starting_hand_page():
    return render_template('starting_hand.html', hostname = hostname, starting_hand = serve_amount_from_deck(get_deck()), bet = get_bet(), bankroll = get_bankroll())

@app.route('/final_hand', methods=['POST', 'GET'])
def show_final_hand_page():
    starting_hand = request.form['cards']
    starting_hand_list = starting_hand.split(";")
    deck = loop_deck_removal(starting_hand_list)

    chosen_cards = []

    for i in starting_hand_list:
        card = request.form[f'decision_{i}']
        if "keep_" in card:
            chosen_cards.append(card.split("keep_")[1])

    final_hand = deuxieme_tirage(chosen_cards, deck)

    mult, result = check_best_hand(final_hand)

    bet_result = mult * get_bet()
    set_bankroll(get_bankroll() + bet_result)

    return render_template('final_hand.html', final_hand = final_hand, mult = mult, result = result, bankroll = get_bankroll(), bet_result = bet_result)

@app.route('/reset', methods=['POST', 'GET'])
def redirect_start():
    reset()
    return redirect(url_for('view_start'))
