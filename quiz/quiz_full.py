score=0
total_questions=5

print("Welcome to Tim's Quiz")
answer=input("Are you ready to play the Quiz ? (yes/no) :")

if answer.lower() == "yes" or answer.lower() == "y":
    answer=input("\nQuestion 1: What is Tim's favourite food?\nA) Pizza\nB) Soup\nC) Cheerios\nD) Curry\n")
    if answer.lower() == "a":
        score += 1
        print("Correct! Tim loves pizza :)")
    else:
        print("Wrong answer :(")

    answer=input("\nQuestion 2: Where is Tim from?\nA) France\nB) London\nC) Norway\nD) Brazil\n")
    if answer.lower() == "c":
        score += 1
        print("Correct! Tim is from Norway :)")
    else:
        print("Wrong answer :(")
    
    answer=input("\nQuestion 3: How old is Tim?\nA) 102\nB) 16\nC) 35\nD) 25\n")
    if answer.lower() == "d":
        score += 1
        print("Correct! Tim is 25 :)")
    else:
        print("Wrong answer :(")
    
    answer=input("\nQuestion 4: Who is the oldest?\nA) Tim\nB) Python\nC) Google\nD) Justin Bieber\n")
    if answer.lower() == "b":
        score += 1
        print("Correct! Python was first released in 1991 :)")
    else:
        print("Wrong answer :(")

    answer=input("\nQuestion 5: Who is the youngest?\nA) Tim\nB) Python\nC) Google\nD) Justin Bieber\n")
    if answer.lower() == "c":
        score += 1
        print("Correct! Google was founded in 1998. That's right, Tim lived in a world without Google...")
    else:
        print("Wrong answer :( Google was founded in 1998. That's right, Tim lived in a world without Google...")
    
    print("\nThankyou for playing my quiz! You got", score, "questions correct!")
    mark=(score/total_questions)*100
    print("Score:", round(mark, 2), "%")
else:
    print("What a shame! You just missed out on a great quiz - come and play next time!")

