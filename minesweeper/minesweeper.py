import pyautogui
import time

pyautogui.PAUSE = 0
speed = 0
mode = ""

# Easy Mode = 10 x 8
easy_rows = 8
easy_cols = 10
# Medium Mode = 18 x 14
medium_rows = 14
medium_cols = 18
# Hard Mode = 24 x 20
hard_rows = 20
hard_cols = 24

# COLORS
rgb0a = (216, 184, 154)
rgb0b = (230, 194, 160)
rgb1 = (35, 124, 204)
rgb2 = (60, 146, 65)
rgb3 = (216, 61, 62)
rgb4 = (109, 17, 137)
rgb5 = (224, 184, 63)
rgb6 = (77, 173, 148)
rgb7 = (98, 80, 55)
rgb8 = (192, 184, 175)

# Optimizing scanning
mustScan = True

# Determine game difficulty
def determine_difficulty():
    try:
        if pyautogui.locateOnScreen("easy.png", confidence=0.8) != None:
            print("easy mode")
            return "easy"
    except:
        try:
            if pyautogui.locateOnScreen("medium.png", confidence=0.8) != None:
                print("medium mode")
                return "medium"
        except: 
            if pyautogui.locateOnScreen("hard.png", confidence=0.8) != None:
                print("hard mode")
                return "hard"
    
    print("error: no mode found")

# Locate game board
def locate_board(mode):
    if(mode == "easy"):
        board_location = pyautogui.locateOnScreen('easy_grid.png', confidence=0.8)
        print(board_location)
    elif(mode == "medium"):
        board_location = pyautogui.locateOnScreen('medium_grid.png', confidence=0.8)
        print(board_location)
    elif(mode == "hard"):
        board_location = pyautogui.locateOnScreen('hard_grid.png', confidence=0.8)
        print(board_location)
    else:
        print("no board found")
        return
    
    return board_location

# Create the board as an array
def create_board(mode):
    if(mode == "easy"):
        board = [[" " for i in range(easy_cols)] for j in range(easy_rows)]
    elif(mode == "medium"):
        board = [[" " for i in range(medium_cols)] for j in range(medium_rows)]
    else:
        board = [[" " for i in range(hard_cols)] for j in range(hard_rows)]
    
    return board

# Scan board for numbers/blanks
def scan_board(board, board_location, mode):
    time.sleep(1)
    rows = len(board)
    cols = len(board[0])

    tile_width = board_location.width / cols
    tile_height = board_location.height / rows
    
    # center of top-left tile
    x = board_location.left + (tile_width / 2)
    y = board_location.top + (tile_height / 2)

    for row in range(rows):
        for col in range(cols):
            # move on to next if already revealed
            if board[row][col] != " ":
                x += tile_width
                continue

            # screenshot small region, check for color inside
            pixels = 3
            region = pyautogui.screenshot(region=(int(x), int(y), pixels, pixels))
            colors = region.getcolors()

            for color in colors:
                # check for 0
                if color[0] == (pixels * pixels):
                    if match_colors(color[1], rgb0a, mode) or match_colors(color[1], rgb0b, mode):
                        board[row][col] = 0
                        break
                # check for 1
                if match_colors(color[1], rgb1, mode):
                    board[row][col] = 1
                    break
                # check for 2
                if match_colors(color[1], rgb2, mode):
                    board[row][col] = 2
                    break
                # check for 3
                if match_colors(color[1], rgb3, mode):
                    board[row][col] = 3
                    break
                # check for 4
                if match_colors(color[1], rgb4, mode):
                    board[row][col] = 4
                    break
                # check for 5
                if match_colors(color[1], rgb5, mode):
                    board[row][col] = 5
                    break
                # check for 6
                if match_colors(color[1], rgb6, mode):
                    board[row][col] = 6
                    break
                # check for 7
                if match_colors(color[1], rgb7, mode):
                    board[row][col] = 7
                    break
                # # check for 8
                # elif match_colors(color[1], rgb8, mode):
                #     board[row][col] = 8

            pyautogui.moveTo(x, y)
            # time.sleep(0.1)

            # move to next column
            x += tile_width
        # move to next row
        x = board_location.left + (tile_width / 2)
        y += tile_height

# Check if two colors are the same
def match_colors(color1, color2, mode):
    tolerance = 25
    if mode == "easy":
        tolerance = 35
    elif mode == "hard":
        tolerance = 35
    
    for i in range(3): # compares each r,g,b value
        if color1[i] < (color2[i]-tolerance) or color1[i] > (color2[i]+tolerance):
            return False
        
    return True

# Try to find mines
def locate_mines(board, board_location):
    # for every number, if # of surrounding unrevealed tiles == number, place flags
    for row in range(len(board)):
        for col in range(len(board[0])):
            tile = board[row][col]
            if(tile == " " or tile == 0 or tile == "F"):
                continue

            unrevealed_tiles = 0
            possible_flags = []
            # top-left
            if row > 0 and col > 0:
                if board[row-1][col-1] == " " or board[row-1][col-1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row-1, col-1))
            # top
            if row > 0:
                if board[row-1][col] == " " or board[row-1][col] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row-1, col))
            # top-right
            if row > 0 and col < len(board[0])-1:
                if board[row-1][col+1] == " " or board[row-1][col+1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row-1, col+1))
            # left
            if col > 0:
                if board[row][col-1] == " " or board[row][col-1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row, col-1))
            # right
            if col < len(board[0])-1:
                if board[row][col+1] == " " or board[row][col+1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row, col+1))
            # bottom-left
            if row < len(board)-1 and col > 0:
                if board[row+1][col-1] == " " or board[row+1][col-1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row+1, col-1))
            # bottom
            if row < len(board)-1:
                if board[row+1][col] == " " or board[row+1][col] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row+1, col))
            # bottom-right
            if row < len(board)-1 and col < len(board[0])-1:
                if board[row+1][col+1] == " " or board[row+1][col+1] == "F":
                    unrevealed_tiles += 1
                    possible_flags.append((row+1,col+1))

            if(tile == unrevealed_tiles):
                for (i, j) in possible_flags:
                     if board[i][j] != "F":
                        board[i][j] = "F"
                        place_flag(board, board_location, i, j)
    
# Places a flag at a specified tile
def place_flag(board, board_location, row, col):
    rows = len(board)
    cols = len(board[0])

    tile_width = board_location.width / cols
    tile_height = board_location.height / rows
    
    x = board_location.left + (tile_width * col)
    y = board_location.top + (tile_height * row)
    x += tile_width / 2
    y += tile_height / 2

    pyautogui.moveTo(x, y, speed)
    pyautogui.rightClick()

# Reveal tiles that are known to be safe 
def locate_safe_tiles(board, board_location):
    for row in range(len(board)):
        for col in range(len(board[0])):
            tile = board[row][col]
            if tile != "F":
                continue

            surrounding_nums = []
            # top-left
            if row > 0 and col > 0:
                if isinstance(board[row-1][col-1], int) and board[row-1][col-1] > 0:
                    surrounding_nums.append((row-1, col-1))
            # top
            if row > 0:
                if isinstance(board[row-1][col], int) and board[row-1][col] > 0:
                    surrounding_nums.append((row-1, col))
            # top-right
            if row > 0 and col < len(board[0])-1:
                if isinstance(board[row-1][col+1], int) and board[row-1][col+1] > 0:
                    surrounding_nums.append((row-1, col+1))
            # left
            if col > 0:
                if isinstance(board[row][col-1], int) and board[row][col-1] > 0:
                    surrounding_nums.append((row, col-1))
            # right
            if col < len(board[0])-1:
                if isinstance(board[row][col+1], int) and board[row][col+1] > 0:
                    surrounding_nums.append((row, col+1))
            # bottom-left
            if row < len(board)-1 and col > 0:
                if isinstance(board[row+1][col-1], int) and board[row+1][col-1] > 0:
                    surrounding_nums.append((row+1, col-1))
            # bottom
            if row < len(board)-1:
                if isinstance(board[row+1][col], int) and board[row+1][col] > 0:
                    surrounding_nums.append((row+1, col))
            # bottom-right
            if row < len(board)-1 and col < len(board[0])-1:
                if isinstance(board[row+1][col+1], int) and board[row+1][col+1] > 0:
                    surrounding_nums.append((row+1,col+1))

            for (i, j) in surrounding_nums:
                check_if_enough_flags(board, board_location, i, j)

# Check if this tile has enough flags around it, if so: reveal safe tiles
def check_if_enough_flags(board, board_location, row, col):
    flag_count = 0
    possible_safe = []

    # top-left
    if row > 0 and col > 0:
        if board[row-1][col-1] == " ":
            possible_safe.append((row-1, col-1))
        elif board[row-1][col-1] == "F":
            flag_count += 1
    # top
    if row > 0:
        if board[row-1][col] == " ":
            possible_safe.append((row-1, col))
        elif board[row-1][col] == "F":
            flag_count += 1
    # top-right
    if row > 0 and col < len(board[0])-1:
        if board[row-1][col+1] == " ":
            possible_safe.append((row-1, col+1))
        elif board[row-1][col+1] == "F":
            flag_count += 1
    # left
    if col > 0:
        if board[row][col-1] == " ":
            possible_safe.append((row, col-1))
        elif board[row][col-1] == "F":
            flag_count += 1     
    # right
    if col < len(board[0])-1:
        if board[row][col+1] == " ":
            possible_safe.append((row, col+1))
        elif board[row][col+1] == "F":
            flag_count += 1
    # bottom-left
    if row < len(board)-1 and col > 0:
        if board[row+1][col-1] == " ":
            possible_safe.append((row+1, col-1))
        elif board[row+1][col-1] == "F":
            flag_count += 1
    # bottom
    if row < len(board)-1:
        if board[row+1][col] == " ":
            possible_safe.append((row+1, col))
        elif board[row+1][col] == "F":
            flag_count += 1
    # bottom-right
    if row < len(board)-1 and col < len(board[0])-1:
        if board[row+1][col+1] == " ":
            possible_safe.append((row+1,col+1))
        elif board[row+1][col+1] == "F":
            flag_count += 1
    
    num = board[row][col]
    if num == flag_count:
        for (i, j) in possible_safe:
            reveal_tile(board, board_location, i, j)

# Reveal a specified tile
def reveal_tile(board, board_location, row, col):
    rows = len(board)
    cols = len(board[0])

    tile_width = board_location.width / cols
    tile_height = board_location.height / rows
    
    x = board_location.left + (tile_width * col)
    y = board_location.top + (tile_height * row)
    x += tile_width / 2
    y += tile_height / 2

    pyautogui.moveTo(x, y, speed)
    pyautogui.click()
    time.sleep(0.05)

    # look at the revealed tile, if not empty, then add to board
    # if none of the revealed tiles are empty, 
    # then we don't need to scan the entire board again
    pixels = 5
    region = pyautogui.screenshot(region=(int(x), int(y), pixels, pixels))
    colors = region.getcolors()

    for color in colors:
        # check for empty
        if color[0] == (pixels * pixels):
            if match_colors(color[1], rgb0a, mode) or match_colors(color[1], rgb0b, mode):
                board[row][col] = 0
                global mustScan
                mustScan = True
                break
        # check for 1
        if match_colors(color[1], rgb1, mode):
            board[row][col] = 1
            break
        # check for 2
        if match_colors(color[1], rgb2, mode):
            board[row][col] = 2
            break
        # check for 3
        if match_colors(color[1], rgb3, mode):
            board[row][col] = 3
            break
        # check for 4
        if match_colors(color[1], rgb4, mode):
            board[row][col] = 4
            break
        # check for 5
        if match_colors(color[1], rgb5, mode):
            board[row][col] = 5
            break
        # # check for 6
        # if match_colors(color[1], rgb6, mode):
        #     board[row][col] = 6
        #     break
        # check for 7
        if match_colors(color[1], rgb7, mode):
            board[row][col] = 7
            break
        # # check for 8
        # elif match_colors(color[1], rgb8, mode):
        #     board[row][col] = 8

def check_if_done(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == " ":
                return False
                
    return True

# Print the board state to the console
def print_board(board):
    print(" ", end=" ")
    for i in range(len(board[0])):
        print("-", end=" ")
    print("")

    for i in range(len(board)):
        print("|", end=" ")
        for j in range(len(board[0])):
            print(board[i][j], end=" ")
        print("|")

    print(" ", end=" ")
    for i in range(len(board[0])):
        print("-", end=" ")
    print("")


# Main method
def main():
    print("Minesweeper Bot")
    # time.sleep(1)

    global mode
    mode = determine_difficulty()
    board_location = locate_board(mode)

    board = create_board(mode)

    # reveal a tile in the middle
    x = board_location.left + (board_location.width / 2)
    y = board_location.top + (board_location.height / 2)
    pyautogui.click(x, y)

    global mustScan 
    for i in range(100):
        if(mustScan):
            scan_board(board, board_location, mode)
            print("Scanning...")
            print_board(board)
            mustScan = False

        locate_mines(board, board_location)
        print("Flagging...")
        print_board(board)

        locate_safe_tiles(board, board_location)
        print("Revealing...")

        if check_if_done(board):
            exit(0)
    
# main guard
if __name__ == '__main__':
    main()