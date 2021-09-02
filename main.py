from math import floor, ceil
from tkinter import *
from tkinter.ttk import Combobox

from PIL import Image, ImageTk
import requests
import chess
from time import sleep
from stockfish import Stockfish

stockfish_ = Stockfish("stockfish.exe")
stockfish_.set_skill_level(20)
stockfish_.set_depth(13)
stockfish_.set_elo_rating(3500)

click = ''
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
codes_reversed = {
    '0': 'p',
    '1': 'P',
    '2': 'n',
    '3': 'N',
    '4': 'b',
    '5': 'B',
    '6': 'r',
    '7': 'R',
    '8': 'q',
    '9': 'Q',
    '10': 'k',
    '11': 'K',
}
positions = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
]
pieces_ordered = [
    'p_black',
    'p_white',
    'n_black',
    'n_white',
    'b_black',
    'b_white',
    'r_black',
    'r_white',
    'q_black',
    'q_white',
    'k_black',
    'k_white'
]
board_map = {
    'a1': 7,
    'a2': 1,
    'a3': False,
    'a4': False,
    'a5': False,
    'a6': False,
    'a7': 0,
    'a8': 6,
    'b1': 3,
    'b2': 1,
    'b3': False,
    'b4': False,
    'b5': False,
    'b6': False,
    'b7': 0,
    'b8': 2,
    'c1': 5,
    'c2': 1,
    'c3': False,
    'c4': False,
    'c5': False,
    'c6': False,
    'c7': 0,
    'c8': 4,
    'd1': 9,
    'd2': 1,
    'd3': False,
    'd4': False,
    'd5': False,
    'd6': False,
    'd7': 0,
    'd8': 8,
    'e1': 11,
    'e2': 1,
    'e3': False,
    'e4': False,
    'e5': False,
    'e6': False,
    'e7': 0,
    'e8': 10,
    'f1': 5,
    'f2': 1,
    'f3': False,
    'f4': False,
    'f5': False,
    'f6': False,
    'f7': 0,
    'f8': 4,
    'g1': 3,
    'g2': 1,
    'g3': False,
    'g4': False,
    'g5': False,
    'g6': False,
    'g7': 0,
    'g8': 2,
    'h1': 7,
    'h2': 1,
    'h3': False,
    'h4': False,
    'h5': False,
    'h6': False,
    'h7': 0,
    'h8': 6
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
    else:
        for pos in board_map.keys():
            if type(board_map[pos]) == type(8):
                pos_w = w*cols_list.index(pos[0])+w/2
                pos_h = h*(8-eval(pos[-1]))+h/2+3
                piece = pieces_ordered[board_map[pos]]
                canvas_analyze.create_image(pos_w, pos_h, image=eval(piece), tags=(piece,))


def canvas_clicked(event):
    global click, board_map
    square = str(cols_list[floor(event.x/w)])+str(rows[8-ceil(event.y/h)])
    if click == '':
        click = square
    else:
        board_map[square] = board_map[click]
        board_map[click] = False
        click = ''
        show_board(True)


def reset():
    global board_map, click
    click = ''
    board_map = {
        'a1': 7,
        'a2': 1,
        'a3': False,
        'a4': False,
        'a5': False,
        'a6': False,
        'a7': 0,
        'a8': 6,
        'b1': 3,
        'b2': 1,
        'b3': False,
        'b4': False,
        'b5': False,
        'b6': False,
        'b7': 0,
        'b8': 2,
        'c1': 5,
        'c2': 1,
        'c3': False,
        'c4': False,
        'c5': False,
        'c6': False,
        'c7': 0,
        'c8': 4,
        'd1': 9,
        'd2': 1,
        'd3': False,
        'd4': False,
        'd5': False,
        'd6': False,
        'd7': 0,
        'd8': 8,
        'e1': 11,
        'e2': 1,
        'e3': False,
        'e4': False,
        'e5': False,
        'e6': False,
        'e7': 0,
        'e8': 10,
        'f1': 5,
        'f2': 1,
        'f3': False,
        'f4': False,
        'f5': False,
        'f6': False,
        'f7': 0,
        'f8': 4,
        'g1': 3,
        'g2': 1,
        'g3': False,
        'g4': False,
        'g5': False,
        'g6': False,
        'g7': 0,
        'g8': 2,
        'h1': 7,
        'h2': 1,
        'h3': False,
        'h4': False,
        'h5': False,
        'h6': False,
        'h7': 0,
        'h8': 6
    }
    show_board()


def get_board_fen():
    fen = ''
    for pos in range(0, 8):
        row = positions[pos*8:pos*8+8]
        to_add = ''
        last_empty = False
        empty = 0
        for cas in row:
            if type(board_map[cas]) == type(False):
                empty += 1
                last_empty = True
            else:
                if last_empty:
                    to_add += str(empty)+str(codes_reversed[str(board_map[cas])])
                    last_empty = False
                    empty = 0
                else:
                    to_add += str(codes_reversed[str(board_map[cas])])
        if empty != 0:
            to_add += str(empty)
        fen += "/"+to_add
    fen = fen[1:]
    fen += " "
    if turn.get() == "Turno de Blancas":
        fen += "w"
    else:
        fen += "b"
    fen += " "
    if castle_w_on.get():
        fen += "KQ"
    if castle_b_on.get():
        fen += "kq"
    fen += " - 0 1"
    return fen


window = Tk()
window.title("TrampaChess")
window.iconbitmap("icon.ico")

menu = Menu(window, tearoff=False)
menu_file = Menu(menu, tearoff=False)
menu_file.add_command(label="Reset Board", command=lambda: reset())
menu_file.add_command(label="Try fen", command=lambda: print(get_board_fen()))
menu.add_cascade(label="File", menu=menu_file)
window.configure(menu=menu)

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
canvas_analyze.grid(row=2, column=0, columnspan=3)
canvas_analyze.bind('<Button-1>', canvas_clicked)
show_board()

castle_w_on = BooleanVar(value=True)
Checkbutton(window, text="Enroque blanco permitido", font="Helvetica 20", variable=castle_w_on).grid(row=0, column=0)
Label(window, text="|", font="Helvetica 20").grid(row=0, column=1)
castle_b_on = BooleanVar(value=True)
Checkbutton(window, text="Enroque negro permitido", font="Helvetica 20", variable=castle_b_on).grid(row=0, column=2)
turn = Combobox(window, font="Helvetica 20", state="readonly", width=44)
turn.grid(row=1, column=0, columnspan=3)
turn['values'] = ["Turno de Blancas", "Turno de Negras"]
turn.set("Turno de Blancas")

# module_moves = Scale(window, font="Helvetica 15", label="Profundidad del módulo", from_=3, to=100, orient=HORIZONTAL, command=stockfish_.set_depth)
# module_moves.place(rely=0.29, relx=0.305, relwidth=0.69)
# module_moves.set(15)

window.mainloop()
