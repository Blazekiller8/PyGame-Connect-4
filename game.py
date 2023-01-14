import pygame

# Initialize Pygame and create a window
pygame.init()
width = 800
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")

center_x = width / 2
center_y = height / 2
board_width = 700
board_height = 600
offset_x = center_x - (board_width / 2)
offset_y = center_y - (board_height / 2)

# Load the images for the game pieces
red_piece = pygame.image.load("assets/red_piece.png")
yellow_piece = pygame.image.load("assets/yellow_piece.png")

# Create a gradient background
background = pygame.Surface((width, height))
for x in range(width):
    for y in range(height):
        background.set_at((x, y), (x % 256, y % 256, (x+y) % 256))

# Create a large font for the title
title_font = pygame.font.Font(None, 48)
title_text = title_font.render("Connect 4", True, (255, 255, 255))

# Create a medium font for the score and player's turn
score_font = pygame.font.Font(None, 36)

# Create a button for starting the game
start_button = pygame.image.load("assets/start_button.png")
rectangle = pygame.Rect(x-500, y-500, 500, 500)
# add this line to check the button initialization
print("start button loaded")
# add this line to print the button size
print("Button size is", start_button.get_rect().size)

# Create a 2D array to represent the game board
board = [[0 for _ in range(6)] for _ in range(7)]
# Create a 1D array to represent the lowest empty space in each column
lowest_empty_space = [0 for _ in range(7)]


# Function to check for a win condition


def check_win(board):
    # Check for horizontal win
    for row in range(6):
        for col in range(4):
            if board[col][row] == board[col+1][row] == board[col+2][row] == board[col+3][row] != 0:
                return True

    # Check for vertical win
    for col in range(7):
        for row in range(3):
            if board[col][row] == board[col][row+1] == board[col][row+2] == board[col][row+3] != 0:
                return True

    # Check for diagonal win
    for col in range(4):
        for row in range(3):
            if board[col][row] == board[col+1][row+1] == board[col+2][row+2] == board[col+3][row+3] != 0:
                return True
    for col in range(4):
        for row in range(3):
            if board[col][row+3] == board[col+1][row+2] == board[col+2][row+1] == board[col+3][row] != 0:
                return True
    return False


# Initialize variables for the game loop
player1 = True
game_over = False
game_started = False

# Main game loop
while not game_over:
    print("game loop")  # add this line to check the game loop

    # Draw the background and title
    screen.blit(background, (0, 0))
    screen.blit(title_text, (width/2-100, 50))

    if not game_started:
        # Draw the start button
        # pygame.draw.rect(screen, (255, 0, 0), rectangle, 2)
        screen.blit(start_button, rectangle)
        for event in pygame.event.get():
            # add this line to check the events
            print("Event to start the game -", event)

            if event.type == pygame.QUIT:
                game_over = True

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if (event.pos[0] > x-500 and event.pos[0] < x and event.pos[1] > y-500 and event.pos[1] < y) or rectangle.collidepoint(event.pos):
                    print("Button clicked!")
                    # add this line to print the button coordinates
                    print(event.pos)
                    # add this line to check the event.pos values
                    print("Start button clicked")
                    game_started = True
    else:
        print("Drawing game board")
        # Draw the game board and pieces
        for col in range(1, 7):
            for row in range(1, 6):
                pygame.draw.rect(screen, (0, 0, 255),
                                 (col*100, row*100, 100, 100))
                if board[col][row] == 1:
                    screen.blit(red_piece, (col*100+50, row*100+50))
                elif board[col][row] == 2:
                    screen.blit(yellow_piece, (col*100+50, row*100+50))
                else:
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (col*100+50, row*100+50), 30)
        print("Game board drawn")
        # Draw the score and player's turn
        if player1:
            player_text = score_font.render(
                "Player 1's turn", True, (255, 0, 0))
        else:
            player_text = score_font.render(
                "Player 2's turn", True, (255, 255, 0))
        screen.blit(player_text, (width/2-50, height-50))

        for event in pygame.event.get():
            # add this line to check the events
            print("Event to place the piece -", event)

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                if click_x > 100 and click_x < 700 and click_y > 100 and click_y < 600:
                    cell_x = click_x // 100  # column position
                    cell_y = lowest_empty_space[cell_x]

                    if cell_y < 7:
                        # column is not full, place a piece
                        if board[cell_y][cell_x] == 0:
                            if player1:
                                board[cell_y][cell_x] = 1
                                screen.blit(
                                    red_piece, (cell_x*100+50, cell_y*100+50))
                            else:
                                board[cell_y][cell_x] = 2
                                screen.blit(
                                    yellow_piece, (cell_x*100+50, cell_y*100+50))
                        lowest_empty_space[cell_x] += 1
                        player1 = not player1

                    else:
                        end_text = score_font.render(
                            "Column Already full!", True, (255, 255, 0))
                        screen.blit(end_text, (width/2-50, height-100))

    # Check for game over
    if check_win(board):
        if player1:
            player_text = score_font.render(
                "Player 1 wins!", True, (255, 0, 0))
        else:
            player_text = score_font.render(
                "Player 2 wins!", True, (255, 255, 0))
        screen.blit(player_text, (width/2-50, height-50))
        end_text = score_font.render("Click to Exit!", True, (255, 255, 0))
        screen.blit(end_text, (width/2-50, height-100))
        for event in pygame.event.get():
            print(event)  # add this line to check the events
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                game_over = True

    print("update function")  # add this line to check the update function
    pygame.display.update()
