''' 

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
    

LICENSE:
    
    - This project is licensed under the MIT License. See the LICENSE file for details.
    
'''
