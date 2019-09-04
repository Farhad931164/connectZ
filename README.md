# Connect 4

This is connect 4 game, with the ability to have arbitrary game size.

# About

Game describtion, [Connect Four](https://en.wikipedia.org/wiki/Connect_Four)

## How to run

You can pass text files with that specifid format to the game. The engine will process the input file and print out the final result. 

## Input file structure

The input file should contain the game size in the first line. The rest of file should be player drops starting from player1.

## Input file sample

3, 3, 3  `This is the game size X, Y, Z. X=Columns, Y=Rows, Z=Number of connects(To win)`
1 `Player1`
2 `Player2`
3 `Player1`
1 `Player2`
2 `Player1`
3 `Player2`
1 `Player1`

|˅| ˅| ˅|
|:--:|:--:|:--:|
|X | | |
|X |O |X |
|X |O |X |

Player 1, won the game !!!
