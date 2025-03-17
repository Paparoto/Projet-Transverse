import random
# 3 DOORS









# CEMENTARY










# RIDDLES
riddles = {
    "You measure my life in hours and I serve you by expiring. I’m quick when I’m thin and slow when I’m fat. The wind is my enemy": "candle",
    "What is seen in the middle of March and April that can’t be seen at the beginning or end of either month":" r ",
    "The first two letters signify a male, the first three letters signify a female, the first four letters signify a great, while the entire word whispers promises but binds in chains.":"heroine"
}
def riddle_game():
    riddle_number = random.randint(0,2)
    print(list(riddles.keys())[riddle_number])
    answer = " " + input("Your answer : ") + " "
    if list(riddles.values())[riddle_number] in answer:
        print("Congrats!")

riddle_game()