from tkinter import *
from PIL import Image, ImageTk
import requests
import chess
from time import sleep
from stockfish import Stockfish

stockfish_ = Stockfish("stockfish.exe")
stockfish_.set_skill_level(20)
stockfish_.set_depth(13)
stockfish_.set_elo_rating(3500)

cols_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = ['1', '2', '3', '4', '5', '6', '7', '8']
w = 41
h = 42
codes = {
    'p': 0,
    'P': 1,
    'n': 2,
    'N': 3,
    'b': 4,
    'B': 5,
    'r': 6,
    'R': 7,
    'q': 8,
    'Q': 9,
    'k': 10,
    'K': 11
}


def getbookmoves(stockfish, porcentaje=0.1, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", moves=50, profundidad=50):
    if profundidad <= 0:
        print("fin linea")
    else:
        params = (
            ('variant', 'standard'),
            ('recentGames', 0),
            ('topGames', 0),
            ('moves', moves),
            ('speeds[]', ['blitz', 'rapid', 'classical']),
            ('ratings[]', ['2200', '2500']),
            ('fen', fen),
        )
        response = requests.get('https://explorer.lichess.ovh/lichess', params=params)
        parsed = response.json()
        for i in range(0, moves):
            try:
                if parsed["moves"][i]["white"] + parsed["moves"][i]["black"] + parsed["moves"][i]["draws"] / parsed["moves"][0]["white"] + parsed["moves"][0]["black"] + parsed["moves"][0]["draws"] >= porcentaje:
                    stockfish.set_fen_position(fen)
                    val_ant = stockfish.get_evaluation()['value']/100
                    stockfish.make_moves_from_current_position([parsed["moves"][i]["uci"]])
                    val_act = stockfish.get_evaluation()['value']/100
                    is_incorrect = abs(val_act - val_ant) >= 1
                    if is_incorrect:
                        board = chess.Board(fen)
                        board.push_san(parsed["moves"][i]["san"])
                        stockfish.set_fen_position(board.fen())
                        a = stockfish.get_best_move_time(5000)
                        print({
                            'cmove': a,
                            'var': "{} - {}".format(val_ant, val_act),
                            'fen': fen,
                            'san': parsed["moves"][i]["san"]
                        })
                        profundidad -= 1
                        getbookmoves(board.fen(), moves, profundidad)
                    else:
                        board = chess.Board(fen)
                        board.push_san(parsed["moves"][i]["san"])
                        stockfish.set_fen_position(board.fen())
                        print(parsed["moves"][i]["san"], " - ", val_act, " - ", val_ant)
                        getbookmoves(board.fen(), moves, profundidad)
            except:
                pass
            sleep(0.1)


def show_board(moved=False):
    canvas_analyze.create_image(int(board_img.width / 2), int(board_img.height / 2), image=board, tags=("board",))
    if not moved:
        canvas_analyze.create_image(w*2+w/2, h*7+h/2+3, image=b_white, tags=("bwhite", ))
        canvas_analyze.create_image(w*5+w/2, h*7+h/2+3, image=b_white, tags=("bwhite", ))
        canvas_analyze.create_image(w+w/2, h*7+h/2+3, image=n_white, tags=("nwhite", ))
        canvas_analyze.create_image(w*6+w/2, h*7+h/2+3, image=n_white, tags=("nwhite", ))
        canvas_analyze.create_image(w/2, h*7+h/2+3, image=r_white, tags=("rwhite", ))
        canvas_analyze.create_image(w*7+w/2, h*7+h/2+3, image=r_white, tags=("rwhite", ))
        canvas_analyze.create_image(w*3+w/2, h*7+h/2+3, image=q_white, tags=("qwhite", ))
        canvas_analyze.create_image(w*4+w/2, h*7+h/2+3, image=k_white, tags=("kwhite", ))
        canvas_analyze.create_image(w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*2+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*3+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*4+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*5+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*6+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))
        canvas_analyze.create_image(w*7+w/2, h*6+h/2+3, image=p_white, tags=("pwhite", ))

        canvas_analyze.create_image(w*2+w/2, h/2+3, image=b_black, tags=("bblack", ))
        canvas_analyze.create_image(w*5+w/2, h/2+3, image=b_black, tags=("bblack", ))
        canvas_analyze.create_image(w+w/2, h/2+3, image=n_black, tags=("nblack", ))
        canvas_analyze.create_image(w*6+w/2, h/2+3, image=n_black, tags=("nblack", ))
        canvas_analyze.create_image(w/2, h/2+3, image=r_black, tags=("rblack", ))
        canvas_analyze.create_image(w*7+w/2, h/2+3, image=r_black, tags=("rblack", ))
        canvas_analyze.create_image(w*3+w/2, h/2+3, image=q_black, tags=("qblack", ))
        canvas_analyze.create_image(w*4+w/2, h/2+3, image=k_black, tags=("kblack", ))
        canvas_analyze.create_image(w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*2+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*3+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*4+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*5+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*6+w/2, h+h/2+3, image=p_black, tags=("pblack", ))
        canvas_analyze.create_image(w*7+w/2, h+h/2+3, image=p_black, tags=("pblack", ))


def canvas_clicked(event):
    print(event.x, " - ", event.y)


window = Tk()
window.title("TrampaChess")
window.iconbitmap("icon.ico")

board_img = Image.open("board.png")
board = ImageTk.PhotoImage(file="board.png")
b_black = ImageTk.PhotoImage(file="pieces_image/bblack.png")
b_white = ImageTk.PhotoImage(file="pieces_image/bwhite.png")
n_black = ImageTk.PhotoImage(file="pieces_image/nblack.png")
n_white = ImageTk.PhotoImage(file="pieces_image/nwhite.png")
r_black = ImageTk.PhotoImage(file="pieces_image/rblack.png")
r_white = ImageTk.PhotoImage(file="pieces_image/rwhite.png")
p_black = ImageTk.PhotoImage(file="pieces_image/pblack.png")
p_white = ImageTk.PhotoImage(file="pieces_image/pwhite.png")
q_black = ImageTk.PhotoImage(file="pieces_image/qblack.png")
q_white = ImageTk.PhotoImage(file="pieces_image/qwhite.png")
k_black = ImageTk.PhotoImage(file="pieces_image/kblack.png")
k_white = ImageTk.PhotoImage(file="pieces_image/kwhite.png")

canvas_analyze = Canvas(window, width=board_img.width, height=board_img.height)
canvas_analyze.grid(row=0, column=0, rowspan=40, columnspan=3)
canvas_analyze.bind('<Button-1>', canvas_clicked)
show_board()

window.mainloop()
