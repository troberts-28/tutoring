class Human():
    name = ""
    size = 0
    age = 0
    
    def __init__(self, name, size, age, birthyear, month, day):
        self.name = name
    
    def rename(self, new_name):
        self.name = new_name

Conrad = Human(name="Conrad", size=1.33, age=9.06, birthyear=2013, month="March", day=9)
Nini = Human(name="Nini", size=1.25, age=8.06, birthyear=2014, month="March", day=9)

TotalSize = Conrad.size + Nini.size

print(Nini.name)
print(Conrad.name)

Nini.rename()
Conrad.rename("PanNNNNNNNNNNNNNNNty PISSSSSSSSSSSS")

print(Nini.name)
print(Conrad.name)
