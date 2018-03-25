# VimRev

It is simple reversi software.  

![gui](https://github.com/Vimmer-Yamagen/VimRev/blob/images/gui.png)

## Environment

+ Python 3.6.4  

## How to use  

If you want to play "Player vs Player", please execute below command.
> python src/main.py -f player -p player

In addition, the following commands are prepared.  
> python src/main.py -f player -p ai <-"Player vs AI"(first move is player)  
> python src/main.py -f ai -p player <-"AI vs Player"(first move is ai)  
> python src/main.py -f ai -p ai <-"AI vs AI"  

--first / -f -> set first move(Player or AI)  
--passive / -p -> set passive move(Player or AI)  

## Memo  
+ If you rewrite draw function in GameManager class, you are able to display various information in the right side.  

+ And I implement AI which move randomly. If you rewrite placeDisc function in AI class, you are able to make more powerful AI.  

+ Enjoy  