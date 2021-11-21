score=0
total_questions=3

print("Welcome to Tim's Quiz")
answer=input("Are you ready to play the Quiz ? (yes/no) :")

if answer.lower() == "yes" or answer.lower() == "y":
    answer=input("\nQuestion 1: What is Tim's favourite food?\nA) Pizza\nB) Soup\nC) Cheerios\nD) Curry\n")
    if answer.lower() == "a":
        score += 1
        print("Correct! Tim loves pizza :)")
    else:
        print("Wrong answer :(")

    answer=input("\nQuestion 2: How old is Tim?\nA) 102\nB) 16\nC) 35\nD) 24\n")
    if answer.lower() == "d":
        score += 1
        print("Correct! Tim is 24 :)")
    else:
        print("Wrong answer :(")

    answer=input("\nQuestion 3: Where is Tim from?\nA) France\nB) London\nC) America\nD) Brazil\n")
    if answer.lower() == "b":
        score += 1
        print("Correct! Tim is from London :)")
    else:
        print("Wrong answer :(")
    
    print("\nThankyou for playing my quiz! You got", score, "questions correct!")
    mark=(score/total_questions)*100
    print("Score:", round(mark, 2), "%")
else:
    print("What a shame! You just missed out on a great quiz - come and play next time!")

