#!bin/bash

i=0;

while [ $i -le 20 ]
do
    echo "Game" $i
    java bobby.RandomPlayer 5000 > tr1.txt & java bobby.RandomPlayer 5000 > tr2.txt & java bobby.RandomPlayer 5000 > tr3.txt & java bobby.RandomPlayer 5000 > tr4.txt & java bobby.RandomPlayer 5000 > tr5.txt & java bobby.RandomPlayer 5000 > tr6.txt
    i=$(($i+1));
    python3 autograder.py -t tr*;
    sleep 5s;
done