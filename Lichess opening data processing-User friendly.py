''' 
README

Welcome to my script for analysing data on chess openings!

This script provides useful tools for dissecting opening data, finding specific
statistics for an opening, and so on.

This introduction section is meant as a useful guide to what each input does
and what each output means. You can keep this to the side as you work with the
script and data in the console log. The script is set up in a way that all
inputs are given through the console log, allowing for a clearer UI.

NB: The measurement for determining how good an opening is will be defined as 
'weighted win rate'. This win rate is simply White's win percentage minus
Black's win percentage (draws do not count), leaving a single percentage value. 
If this value is positive, the opening is favourable for White. A negative
value shows that the opening is, naturally, favourable for Black.


CAPABILITIES:
    
    This script can ...
    1. select openings that are within user-implemented boundaries.
    2. plot histograms covering the win-rate of openings.
    3. find and plot the best openings for White or Black.
    4. compare White's and Black's best openings with each other.
    5. fetch statistics of any opening, such as its moves, win rate, etc.
    
    
PRE-USAGE:
    
    - The document 'stats-all.txt' is required for this script to work, check
      if this document is also in the same path as the script is.
      
    - Make sure to install any modules that aren't yet installed on your
      computer. You can do this by typing, for example, !pip install mplcursors
      into the console on the bottom right. A list of all imported modules is 
      provided below the copyright info, in the preamble of the code.
      
    - Once all the required modules are installed, simply run the script once
      to load all the data and its functionalities.
      
    - That's all! A prompt should show up in the console, allowing user-inputs.
      Again, every input can be made in the console log; you shouldn't need to 
      make any changes to the script itself.
    

USAGE:
    
    - The program will first ask for some boundaries of your choice. An
      overview of the boundaries is as follows:
          
          minimum number of players:
              This allows you to filter out openings that are rarely played.
              e.g. typing '1000000' will only select openings that have been
              played over 1 million times.
              
          maximum move count:
              This is meant to filter out openings that are too 'deep' (they 
              contian too many moves). e.g. typing '4' will select openings 
              that are themselves 4 moves long (from BOTH sides) or less.
              
          starting moves:
              This refers to the 'root'-position of your desired selection of
              openings. e.g. typing '1 e4' will only select openings that start
              with the King's Pawn.
              NB: this input MUST be in short algebraic chess notation, without
              periods after the digits (like: 1 e4 e5 2 Nf3 Nc6 3 Bb5)
              
          NB: If you don't wish to implement a boundary, simply skip that section
          by hitting return/enter. The script will put a placeholder boundary in
          place that acts no different from having no boundary at all.
              
          
    - After implementing the boundaries, you will see the number of openings
      that fall within your selection, as well as a menu that allows you choose 
      what action to perform on your selection. An overview of these action is
      as follows:
          
          Histogram:
              This will display a histogram which contains how often a certain
              weighted win rate of your selection of openings appears. 
              Depending on your boundaries, the value that appears most often
              will be around 0. 
                  Furthermore, the script will use the mean and standard 
              deviation σ of the data to plot a model normal curve. 
        
          Best 50 openings for White/Black:
              Depending on the side you choose, this will display a plot 
              containing the best openings for that side within your selected
              boundaries. The x-axis will have the name of the opening and the
              y-axis will have the weighted win rate. 
                  Before plotting, you will get to choose to enable mplcursors. 
              Enabling this allows you to see the full name of any opening by
              hovering over the point. This is only recommended for fast PCs
              and will not work if your graphic backend is set to 'inline'.
                  The script will also print the name of the very best opening.
                  
          Z-factor:
              This will show the Z-factor and the name of the best opening for
              both White and Black within your selection. The Z-factor
              shows 'how many standard deviations away from the mean' that
              opening is, allowing you to compare the two openings. A higher 
              Z-factor means that that opening is statistically better.
              
          Fetch statistics for a specific opening:
              Choosing this will allow you to input the name, PGN or FEN of any
              opening (still within your selection!) and the script will fetch
              its stats. If you don't know either the name or the PGN/FEN of
              the opening, you can hit return/enter to skip that section. If
              you input both the name and the PGN/FEN, the script will ask you
              to choose what to search by.
                  The stats it will fetch are:
                      Name, FEN, PGN, Total games, White wins, Draws, 
                      Black wins, Weighted win rate, side (who's opening it is)
                      and a visual board of the current position
                      
          Fetch a random opening:
              This will simply give you the name and moves of a random opening
              within your boundaries.
                      
                      
    - Once you have chosen your action, you will be able to choose between:
        Choosing another action with the same boundaries
        Choosing different boundaries
        Closing the console
        
        
    - An example of how to use this script is finding the best response for
      Black against White's most common first move: 1. e4. 
          To find this, all you need to do is set the root position to '1 e4', 
      set the max amount of moves to 1, and then run the 3rd action (best 50 
      openings for Black). You will see a graph with all of Black's responses 
      ranked from worst to best (the Sicilian and the Caro-Kann are on top).
                          

SOURCES AND COPYRIGHT INFORMATION:
    
    - Opening names taken from jimmyvermeer.com
    - Opening data taken from the Lichess.org API database on February 6th 2024
    - Data has all blitz, rapid and classical games from ratings above 1000
    
    - You are free to publish any images or statistics from this script with
      proper credit. You are also free to make any changes to the script to
      fit your needs better.
      
    - You are not allowed to claim any images, statistics or (altered versions
      of) this script as your own. Even if the images have been created with a
      script that has been altered, proper credit is still required.
      
    - You are also not allowed to publish tampered images in a way that it
      displays the data incorrectly or is misleading. All graph titles, axes
      and points must correctly display your selection of openings.
      
    - If you have any question, suggestions or improvements for this script, 
      let me know at berendvanhapert@gmail.com!
      
    - Script written and published by Berend van Hapert, February 2024  
     
'''


# NECESSARY MODULES HERE FOR THIS SCRIPT TO WORK, INSTALL ANY THAT AREN'T YET 
# INSTALLED. YOU CAN RUN THE SCRIPT ONCE TO SEE WHAT MODULES YOU STILL NEED TO
# INSTALL (TYPE !pip install <module> IN THE CONSOLE)
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors as mpl
import chess.pgn
import time
import sys
import re
import io
from scipy.stats import norm
from difflib import get_close_matches


# creating start values of the global variables 
player_bound = None
move_bound = None
starting_moves = None

# function for converting PGNs to FENs, allowing for user-inputs in the form of PGNs
def pgn_to_fen(pgn):
    
    # function for removing variations from the PGN
    def remove_var(line):
        return re.sub(r'\([^)]*\)', '', line)
    
    # fetching the mainline of the PGN
    pgn_clean = io.StringIO(remove_var(pgn))
    
    # using the 'chess' module to read the PGN
    game = chess.pgn.read_game(pgn_clean)

    # setting up the board 
    board = game.board()
    
    # playing out the PGN on the board
    for move in game.mainline_moves():
        board.push(move)

    # returning the FEN of the position after the PGN has been implemented
    return(board.fen())


# function for creating the visual board for each opening
def Board_position(FEN):
    
    # creating the position using the FEN of the opening
    board = chess.Board(FEN)
    
    # returning the visual state of the board 
    return board


# FUNCTION FOR FETCHING THE STATS OF THE CHOSEN OPENING
# =============================================================================

# function depending its search based on name, FEN, and search request
def Opening_stats(Opening_name=False, FEN=False, search="Name"):
    
    # ignoring search request if only 'Opening_name' is given
    if Opening_name is not False and FEN is False:
        
        # fetching the right opening using the name
        selected_data = opening_data[opening_data['Opening Name'] == Opening_name]
        
        # fetching the needed statistics once the opening is found
        stats = selected_data[['Opening Name', 'FEN', 'PGN', 'White Wins', 'Draws', 'Black Wins', 'Win % Difference']]
        
        # determining for what side the opening is based on what list it is also in
        if Opening_name in white_openings['Opening Name'].values:
            side = 'It is black to move; the opening is for white'
        elif Opening_name in black_openings['Opening Name'].values:
            side = 'It is white to move; the opening is for black'
            
        # failsafe for bugged FENs or faulty/not-updated list-entries
        else:
            side = 'Error'
        
        # returning all the required stats
        return  stats, side

    # ignoring search request if only 'FEN_or_PGN' is given
    elif FEN is not False and Opening_name is False:
        
        # using slashes (only present in FENs) to determine if the input is PGN or FEN
        if '/' in FEN: 
            # keeping the FEN variable as is
            True
            
        # using the fact that the input has to be PGN if not FEN    
        else:
            # using the coverter function to transform the PGN into an FEN
            FEN = pgn_to_fen(FEN)
            
        # fetching the right opening using the FEN    
        selected_data = opening_data[opening_data['FEN'] == FEN]
        
        # fetching the needed statistics once the opening is found
        stats = selected_data[['Opening Name', 'FEN', 'PGN', 'White Wins', 'Draws', 'Black Wins', 'Win % Difference']]
        
        # determining for what side the opening is based on what list it is also in
        if FEN in white_openings['FEN'].values:
            side = 'It is black to move; the opening is for white'
        elif FEN in black_openings['FEN'].values:
            side = 'It is white to move; the opening is for black'
            
        # failsafe for bugged FENs or faulty/not-updated list-entries
        else:
            side = 'Error'
            
        # returning all the required stats
        return  stats, side
    
    # using the name of the opening for fetching the data
    # search is 'Name'  
    elif Opening_name is not False and FEN is not False and search == 'Name':
        
        # clarifying the search direction
        print("Two inputs given, searching by name (<search='FEN' or 'PGN'> to search by FEN or PGN instead)", '\n')
        
        # fetching the right opening using the name
        selected_data = opening_data[opening_data['Opening Name'] == Opening_name]
        
        # fetching the needed statistics once the opening is found
        stats = selected_data[['Opening Name', 'FEN', 'PGN', 'White Wins', 'Draws', 'Black Wins', 'Win % Difference']]
        
        # determining for what side the opening is based on what list it is also in
        if Opening_name in white_openings['Opening Name'].values:
            side = 'It is black to move; the opening is for white'
        elif Opening_name in black_openings['Opening Name'].values:
            side = 'It is white to move; the opening is for black'
            
        # failsafe for bugged FENs or faulty/not-updated list-entries
        else:
            side = 'Error'
        
        # returning all the required stats
        return  stats, side

    # using the FEN or converted PGN of the opening for fetching the data
    # search is anything but 'Name' 
    elif Opening_name is not False and FEN is not False and search != 'Name':
        
        # clarifying the search direction
        print("Two inputs given, searching by FEN or PGN (<search='Name'> to search by name instead)", '\n')
        
        # using slashes (only present in FENs) to determine if the input is PGN or FEN
        if '/' in FEN: 
            # keeping the FEN variable as is
            True
            
        # using the fact that the input has to be PGN if not FEN    
        else:
            # using the coverter function to transform the PGN into an FEN
            FEN = pgn_to_fen(FEN)
            
        # fetching the right opening using the FEN    
        selected_data = opening_data[opening_data['FEN'] == FEN]
        
        # fetching the needed statistics once the opening is found
        stats = selected_data[['Opening Name', 'FEN', 'PGN', 'White Wins', 'Draws', 'Black Wins', 'Win % Difference']]
        
        # determining for what side the opening is based on what list it is also in
        if FEN in white_openings['FEN'].values:
            side = 'It is black to move; the opening is for white'
        elif FEN in black_openings['FEN'].values:
            side = 'It is white to move; the opening is for black'
            
        # failsafe for bugged FENs or faulty/not-updated list-entries
        else:
            side = 'Error'
            
        # returning all the required stats 
        return  stats, side
    
    # failsafe to prevent misinputs from crashing the cell
    else:
        return None

# selection screen for the user to choose what to do
def select_sections():
    print("Select which section to run for selected openings:")
    print("1. Histogram of succes rate for both White and Black combined")
    print("2. Best 50 openings for White")
    print("3. Best 50 openings for Black")
    print("4. Z-factor for comparing the best opening for White with the best opening for Black")
    print("5. Fetch statistics for a specific opening")
    print("6. Fetch a random opening")

    choice = input("Enter your choice (1-6): ")
    print('\n')
    return choice


# loading global bounds
player_bound_input = input("Enter the minimum number of players (optional): ")
move_bound_input = input("Enter the maximum move count (optional): ")
starting_moves_input = input("Enter starting moves (optional): ")

# implementing make-shift bounds for blank inputs
try:
    player_bound = int(player_bound_input) if player_bound_input else 0
    move_bound = int(move_bound_input) if move_bound_input else 100
    starting_moves = starting_moves_input if starting_moves_input else False
except (ValueError, TypeError):
    print("\nCouldn't interpret the input, make sure to use integers and short algebraic chess notation for the boundaries")
    print('Try running the script again')
    sys.exit()

# importing data
opening_data = pd.read_csv('stats-all.txt', delimiter='\t')

# selecting data
opening_data = opening_data[(opening_data['White Wins'] + opening_data['Draws'] + opening_data['Black Wins']) >= player_bound]
opening_data = opening_data[(opening_data['FEN'].str.split().str[1] == 'b') & (pd.to_numeric(opening_data['FEN'].str.split().str[-1]) <= move_bound) | 
                            (opening_data['FEN'].str.split().str[1] == 'w') & (pd.to_numeric(opening_data['FEN'].str.split().str[-1]) <= (move_bound + 1))]
if starting_moves:
    opening_data = opening_data[opening_data['PGN'].fillna('').str.startswith(starting_moves)]

# implementing failsafe for when no opening falls within the boundaries
if len(opening_data) == 0:
    print('\nNo openings match the boundaries')
    print('Try running the script again with different boundaries')
    sys.exit()
    
# creating new colummns for the win rates of each color
opening_data['White Win %'] = opening_data['White Wins'] / (opening_data['White Wins'] + opening_data['Black Wins'] + opening_data['Draws']) * 100
opening_data['Black Win %'] = opening_data['Black Wins'] / (opening_data['White Wins'] + opening_data['Black Wins'] + opening_data['Draws']) * 100

# creating a new column for the 'weighted win rate'
# 'weighted win rate' is defined as <wite win rate> - <black win rate>
# a positive value indicates an advantage for white, a negative value for black
opening_data['Win % Difference'] = (opening_data['White Win %'] - opening_data['Black Win %']).round().astype(int)

# printing the number of openings within the boundaries
print('\n','=' * 60)
print('', "Number of openings within the boundaries:", len(opening_data))
print( '', "=" * 60, '\n')

# splitting the list of total openings into lists of openings for black and white
# sorting the lists in advance by weighted win rate
white_openings = opening_data[opening_data['FEN'].str.split().str[1] == 'b'].sort_values(by='Win % Difference') 
black_openings = opening_data[opening_data['FEN'].str.split().str[1] == 'w'].sort_values(by='Win % Difference') 

# creating variables for the columns required for graphing
white_names = white_openings['Opening Name']
white_percentages = white_openings['Win % Difference']
black_names = black_openings['Opening Name']
black_percentages = black_openings['Win % Difference']



# FUNCTION FOR RUNNING THE SELECTED SECTION
# =============================================================================

def run_section(section_choice):
    # loading the global variables
    global player_bound, move_bound, starting_moves, opening_data

    # 'if' statements to split the script into the correct sections
    if section_choice == "1":
        
        # arranging the size of the bins of the histogram
        # using the line to determine if there are any openings left within boundaries
        # force exiting if no openings remain
        try:
            bin_edges = np.arange(opening_data['Win % Difference'].min(), opening_data['Win % Difference'].max() + 2, 2)
        except ValueError:
            print('No openings match the boundaries')
            sys.exit()

        # starting the figure and plotting the values for the histogram
        plt.figure(figsize=(10,6))
        plt.hist(opening_data['Win % Difference'], bins=bin_edges, alpha=0.7, color='blue', edgecolor='black', density=True, label='Win % Difference')

        # calculating the mean and the standard deviation of the data
        mu, std = norm.fit(opening_data['Win % Difference'])

        # creating a model normal distribution using the mean and the standard deviation
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 1000)
        p = norm.pdf(x, mu, std)

        # plotting the normal distribution
        plt.plot(x, p, 'k', linewidth=2, label='Normal Distribution')

        # plotting all lines with σ values from -3σ to 3σ
        for i in range(1, 4):
            plt.axvline(mu - i * std, color='r', linestyle='--', linewidth=1)
            plt.text(mu - i * std, plt.ylim()[1]*0.9, '{}$\sigma$'.format(i), color='r', rotation=90, verticalalignment='top')
            plt.axvline(mu + i * std, color='r', linestyle='--', linewidth=1)
            plt.text(mu + i * std, plt.ylim()[1]*0.9, '{}$\sigma$'.format(i), color='r', rotation=90, verticalalignment='top')

        # labelling the axes and creating the title
        # turning the grid on
        plt.xlabel('Weighted win percentage (%)')
        plt.ylabel('Probability')
        plt.title('Histogram of weighted win percentage of every named chess opening (+ white, - black) within the selected boundaries')
        plt.grid(True)

        # creating the legend
        plt.legend()

        # showing the histogram
        plt.show()

        # printing the mean and the standard deviation, rounded to the nearest integer
        print('\n', '\t', 'Rounded mean =', int(mu))
        print('\t', 'Rounded standard deviation =', int(std))
        
    elif section_choice == "2":
        
        # allowing the user to choose whether or not they want mplcursors
        hover = input('Enable mplcursors (Y/N)?: ')
        
        # only start the plotting once the choice has been made
        if hover is not None:
            # selecting the best openings for white within the sample size
            top_white_names = white_names[-50:]
            top_white_percentages = white_percentages[-50:]
    
            # abbreviating the names of the openings on the x-axis for better readability
            top_abbreviated_white_names = [name[:15] + '...' if len(name) > 8 else name for name in top_white_names]
    
            # starting the figure and plotting the values for the scatter plot
            plt.figure(figsize=(10,6))
            plt.scatter(top_white_names, top_white_percentages)
    
            # plotting the abbreviated names on the x-axis
            plt.xticks(top_white_names, top_abbreviated_white_names, rotation=45, ha='right', fontsize=8)
    
            # separating overlapping elements
            plt.tight_layout()
    
            # labelling the axes and creating the title
            plt.xlabel('(Abbreviated) opening names')
            plt.ylabel('Weighted win rate (%)')
            plt.title('Top 50 openings for white based on weighted win rate within the selected boundaries')
    
            # implementing mplcursor to show the full names of the points when the cursor hovers over them
            # NB: DOESN'T WORK WHEN THE GRAPHICS BACKEND IS SET TO 'INLINE'
            if hover == 'Y' or hover == 'y':
                cursor = mpl.cursor(hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(top_white_names.iloc[sel.index]))
    
            # showing the scatter plot
            plt.show()
            
            # printing the name of the very best opening for white
            print('\n Best opening for White:', list(white_names)[-1])
        
    elif section_choice == "3":
        
        # allowing the user to choose whether or not they want mplcursors
        hover = input('Enable mplcursors (Y/N)?: ')
        
        # only start the plotting once the choice has been made
        if hover is not None:
            # selecting the best openings for black within the sample size
            top_black_names = black_names[:50][::-1]
            top_black_percentages = black_percentages[:50][::-1]
    
            # abbreviating the names of the openings on the x-axis for better readability
            top_abbreviated_black_names = [name[:15] + '...' if len(name) > 8 else name for name in top_black_names]
    
            # starting the figure and plotting the values for the scatter plot
            plt.figure(figsize=(10,6))
            plt.scatter(top_black_names, top_black_percentages)
    
            # plotting the abbreviated names on the x-axis
            plt.xticks(top_black_names, top_abbreviated_black_names, rotation=45, ha='right', fontsize=8)
    
            # inverting the y-axis to show the most negative weighted win rate at the top
            plt.gca().invert_yaxis()
    
            # separating overlapping elements
            plt.tight_layout()
    
            # labelling the axes and creating the title
            plt.xlabel('(Abbreviated) opening names')
            plt.ylabel('Weighted win rate (%)')
            plt.title('Top 50 openings for black based on weighted win rate within the selected boundaries')
    
            # implementing mplcursor to show the full names of the points when the cursor hovers over them
            # NB: DOESN'T WORK WHEN THE GRAPHICS BACKEND IS SET TO 'INLINE'
            if hover == 'Y' or hover == 'y':
                cursor = mpl.cursor(hover=True)
                cursor.connect("add", lambda sel: sel.annotation.set_text(top_black_names.iloc[sel.index]))
    
            # showing the scatter plot
            plt.show()
            
            # printing the name of the very best opening for black
            print('\n Best opening for Black:', list(black_names)[0])
        
    elif section_choice == "4":
        
        # calculating the mean and the standard deviation of the data
        mu, std = norm.fit(opening_data['Win % Difference'])
        
        # # calculating the Z-factor of the individual points
        z_factor_white = (float(white_percentages[-1:].iloc[0]) - mu)/std
        z_factor_black = abs(float((black_percentages[:1].iloc[0]) - mu)/std)

        # printing the Z-factor; higher Z-factor means better overall opening
        print('Z-factor of the best opening for white:', z_factor_white)
        print('Opening name: ',list(white_names)[-1], '\n')
        print('Z-factor of the best opening for black:', z_factor_black)
        print('Opening name: ',list(black_names)[0])
        
    elif section_choice == "5":
        
        # asking name and moves from the user
        Opening_Name = input("Enter the opening name (optional): ")
        FEN_or_PGN = input("Enter the FEN or PGN (optional): ")

        # reformatting the variables based on which ones were filled in
        # search_choice only required when two inputs were given
        if Opening_Name and FEN_or_PGN:
            search_choice = input("Enter 'Name' to search by opening name, 'FEN' to search by FEN and 'PGN' to search by PGN: ")
        elif Opening_Name and FEN_or_PGN is not True:
            search_choice = "Name"
            FEN_or_PGN = False
        elif Opening_Name is not True and FEN_or_PGN:
            search_choice = "FEN"
            Opening_Name = False
        
        # failsafe for unexpected errors
        else:
            print('An error occured')
            sys.exit()
            
        # skipping the spellchecker when searching by moves    
        if not Opening_Name or search_choice != 'Name':
            True
        
        # implementing 2 different types of user-assistance based on their input
        else:
            
            # assuming the user meant to type the full name of the opening
            if '-' in Opening_Name or '/' in Opening_Name:
                
                # selecting the names that are closest to the input 
                # this method is insensitive to spelling errors or dialects
                similar_names = get_close_matches(Opening_Name, opening_data['Opening Name'])
                
                # only selecting the best match if any matches have been found
                if similar_names:
                    Opening_Name = similar_names[0]
                else:
                    Opening_Name = None
            
            # assuming the user meant to type part of the opening
            else:
                
                # fetching all openings that contain the input
                # this method is not case-sensitive but sensitive to spelling error
                matching_names = [name for name in opening_data['Opening Name'] if Opening_Name.lower() in name.lower()]
                
                # only showing the openings if any have been found
                if not matching_names:
                    Opening_Name = None
                    
                # listing and indexing all the openings that contain the input 
                else:
                    print('\n','=' * 60)
                    print('', "Found one or multiple openings matching the inputted name:")
                    print( '', "=" * 60, '\n')
                    for idx, name in enumerate(matching_names):
                        print(f"{idx+1}. {name}")
                        
                    # allowing the user to choose the opening they want    
                    print('\n')
                    choice_idx = input("Enter the number of the opening you want to choose: ")
                    print('\n')
                    
                    # fetching the data of the desired opening
                    # failsafe for when the input is out of bounds
                    try:
                        choice_idx = int(choice_idx)
                        Opening_Name = matching_names[choice_idx - 1]
                    except (ValueError, IndexError):
                        print("Invalid choice.")
                        Opening_Name=None
        
        try:
            # assigning all the fetched stats from the function to variables
            Stats, WBtM = Opening_stats(Opening_Name, FEN_or_PGN, search_choice)
            
            # catching expected errors / misinputs
            try:
                
                # printing all the packaged opening statistics
                print('Name:', Stats['Opening Name'].iloc[0])
                print('FEN:', Stats['FEN'].iloc[0])
                print('PGN:', Stats['PGN'].iloc[0])
                print('Total games:', Stats['White Wins'].iloc[0] + Stats['Draws'].iloc[0] + Stats['Black Wins'].iloc[0])
                print('White wins:', Stats['White Wins'].iloc[0])
                print('Draws:', Stats['Draws'].iloc[0])
                print('Black Wins:', Stats['Black Wins'].iloc[0])
                print('Weighted win percentage:', Stats['Win % Difference'].iloc[0])
                
                # printing what side the opening is for
                print('Side:', WBtM)
                
                # printing the visual board state using the FEN of the opening
                print('---------------------------------------------------------------')
                print(Board_position(Stats['FEN'].iloc[0]))
                print('---------------------------------------------------------------')
                
            # expected error failsafe
            except IndexError:
                
                # printing status quo and suggestions to fix common mistakes
                print('No openings found')
                print('Try removing the boundaries of the processed openings?')
                
        # unexpected error failsafe
        except TypeError:
            
            # printing status quo
            print("Couldn't interpret the input, make sure to search by full name or FEN/PGN")
     
    elif section_choice == '6':
        
        # create a random index within the bounds of the selecting openings
        rand_num = np.random.randint(0, len(opening_data['FEN']))
        
        # fetching and printing the name and moves of the opening with the index
        opening_data_rand = opening_data.iloc[rand_num,:]
        print(f"\n Opening name: {opening_data_rand['Opening Name']}")
        print(f"\n Opening moves: {opening_data_rand['PGN']}")
    
    # retrying if the input is not an integer between 1 and 6
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
    
# main function for directing the user 
# control panel for executing the right parts of the code  
def main():
    
    # loading and storing the global variables
    global player_bound, move_bound, starting_moves, opening_data, white_openings, black_openings, white_names, white_percentages, black_names, black_percentages

    # performing the desired action
    while True:
        section_choice = select_sections()
        run_section(section_choice)

        # implementing some waiting time
        time.sleep(3)
    
        # asking the user for the next action
        print('\n')
        next_action = input("Choose next action: "
                             "\n1. Choose between sections 1-6 again with the same boundaries "
                             "\n2. Input new boundaries "
                             "\n3. Close kernel "
                             "\nEnter your choice (1-3): ")
        
        # simply running the run_section function again
        if next_action == "1":
            print('\n')
            continue
        
        
        # redifing the global variables and reselecting the data
        elif next_action == "2":
            print('\n')
            print("Please input new boundaries:")
            
            # returning to boundaries input section
            player_bound_input = input("Enter the minimum number of players (optional): ")
            move_bound_input = input("Enter the maximum move count (optional): ")
            starting_moves_input = input("Enter starting moves (optional): ")

            # updating global boundaries
            player_bound = int(player_bound_input) if player_bound_input else 0
            move_bound = int(move_bound_input) if move_bound_input else 100
            starting_moves = starting_moves_input if starting_moves_input else False

            # reloading data based on updated boundaries
            opening_data = pd.read_csv('stats-all.txt', delimiter='\t')
            opening_data = opening_data[(opening_data['White Wins'] + opening_data['Draws'] + opening_data['Black Wins']) >= player_bound]
            opening_data = opening_data[(opening_data['FEN'].str.split().str[1] == 'b') & (pd.to_numeric(opening_data['FEN'].str.split().str[-1]) <= move_bound) |
                                        (opening_data['FEN'].str.split().str[1] == 'w') & (pd.to_numeric(opening_data['FEN'].str.split().str[-1]) <= (move_bound + 1))]
            if starting_moves:
                opening_data = opening_data[opening_data['PGN'].fillna('').str.startswith(starting_moves)]
                
            # recreating the extra columns
            opening_data['White Win %'] = opening_data['White Wins'] / (opening_data['White Wins'] + opening_data['Black Wins'] + opening_data['Draws']) * 100
            opening_data['Black Win %'] = opening_data['Black Wins'] / (opening_data['White Wins'] + opening_data['Black Wins'] + opening_data['Draws']) * 100
            opening_data['Win % Difference'] = (opening_data['White Win %'] - opening_data['Black Win %']).round().astype(int)

            # printing the new number of openings within the boundaries
            print('\n','=' * 60)
            print('', "Number of openings within the boundaries:", len(opening_data))
            print( '', "=" * 60, '\n')

            # splitting and sorting the new openings
            white_openings = opening_data[opening_data['FEN'].str.split().str[1] == 'b'].sort_values(by='Win % Difference') 
            black_openings = opening_data[opening_data['FEN'].str.split().str[1] == 'w'].sort_values(by='Win % Difference') 

            # redifining variables for the columns required for graphing
            white_names = white_openings['Opening Name']
            white_percentages = white_openings['Win % Difference']
            black_names = black_openings['Opening Name']
            black_percentages = black_openings['Win % Difference']


        # closing the kernel
        elif next_action == "3":
            print("Closing kernel...")
            break  
        
        # failsafe for out of bounds inputs
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            sys.exit()

# only running the main function if the script is executed directly
if __name__ == "__main__":
    main()
