class Angel:
    color = "white"
    feature = "wings"
    home = "Heaven"


class Demon:
    color = "red"
    feature = "horns"
    home = "Hell"


creatures = [Angel(), Demon()]

for creature in creatures:
    print(creature.color)
    print(creature.feature)
    print(creature.home)