from robotics import Robot

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")


def introduce_yourself():
    robot.say_hello()

def retrieve_information():
    website="https://www.wikipedia.org"
    robot.run(website,SCIENTISTS)

def steps():
    robot.display_description(SCIENTISTS)

def farewell():
    robot.say_goodbye()

def main():
    introduce_yourself()
    steps()
    retrieve_information()
    farewell()

if __name__ == "__main__":
    main()
