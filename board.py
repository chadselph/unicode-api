import itertools

start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
pieces = {k: chr(v) for k, v in zip("KQRBNPkqrbnp", range(0x2654, 0x2660))}


def fen_to_unicode(fen=start_fen, optimize=True, light=0x2003, dark=0x2630):
    # dark candidates: 0x2593
    # light candidates: 0x3000, 0x205F, 0x2001, 0x2003
    board_colors = itertools.cycle((chr(light), chr(dark)))
    def render_rank(fen_line):
        for char in fen_line:
            if char.isdigit():
                for i in range(int(char)):
                    yield next(board_colors)
            elif char in pieces: 
                next(board_colors)
                yield pieces[char]
            else:
                raise ValueError("Invalid FEN")
    ranks = []
    for rank in fen.split("/"):
        ranks.append("".join(render_rank(rank)).rstrip())
        next(board_colors)  # alternate starting color
    return "\n".join(ranks)

if __name__ == "__main__":
    print(fen_to_unicode())
