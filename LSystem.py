import turtle
import random
from math import cos, sqrt, radians


def normal_choice(lst, mean=None, stddev=None):
    if mean is None:
        # if mean is not specified, use center of list
        mean = (len(lst) - 1) / 2

    if stddev is None:
        # if stddev is not specified, let list be -3 .. +3 standard deviations
        stddev = len(lst) / 6

    while True:
        index = int(random.normalvariate(mean, stddev) + 0.5)
        if 0 <= index < len(lst):
            return lst[index]


def choose_rule(rules):
    """
    Function to choose a rule given a probability that changes
    :param rules: dictionary of rules
    :return: rule
    """
    stddev = None
    mean = None
    return normal_choice(rules, stddev, mean)


def extend_axiom(axiom, rules):
    """
    Function to create instructions given an axiom and a set of rules
    :param axiom: string
    :param rules: dictionary of strings
    :return: extended instructions as string
    """
    instructions = ""
    for x in axiom:
        if x in rules:
            instructions += choose_rule(rules[x])
        else:
            instructions += x
    return instructions


def create_instructions(axiom, rules, it):
    """
    Function to create instructions for given number of iterations
    :param axiom: string
    :param rules: dictionary of rules
    :param it: iteration
    :return: instruction string
    """
    a = axiom
    for i in range(it):
        instructions = extend_axiom(a, rules)
        a = instructions
    return instructions


def draw_branch(t, instructions, it):
    """
    Function to draw the turtle graphic given an instruction string and the current iteration
    :param t: Turtle object
    :param instructions: string of instructions to follow
    :param it: current iteration
    """
    d = 1/(it+1) * 50
    a = 60
    pos = []
    heading = []
    for x in instructions:
        if x == "F":
            t.forward(d)
        elif x == "G":
            t.forward(((it+1)**2)*d)
        elif x == "H":
            t.lt(10)
            t.forward((it+1)*d*0.8)
            t.rt(55)
            t.forward(sqrt(((d**2)/25)*cos(radians(10))))
            t.rt(90)
            t.forward(sqrt(((d**2)/25)*cos(radians(10))))
            t.rt(55)
            t.forward((it+1)*d*0.8)
        elif x == "C":
            r = d/4
            t.circle(r)
        elif x == "+":
            t.lt(a)
        elif x == "-":
            t.rt(a)
        elif x == "*":
            t.lt(90)
        elif x == "/":
            t.rt(90)
        elif x == "[":
            pos.append(t.pos())
            heading.append(t.heading())
        elif x == "]":
            t.setpos(pos.pop())
            t.seth(heading.pop())


def draw_snowflake(axiom, rules, it):
    """
    Function to draw the snowflake with 6 branches
    :param axiom: axiom string
    :param rules: rules dictionary
    :param it: iterations
    """
    t = turtle.Turtle()
    turtle.mode("logo")
    turtle.bgcolor("#123d5a")
    t.ht()
    t.pencolor("white")
    t.pendown()
    instructions = create_instructions(axiom, rules, it)
    print(instructions)
    for i in range(6):
        t.home()
        t.seth(i * 60)
        draw_branch(t, instructions, it)
    t.penup()
    turtle.done()

axiom = "XE"
P = {"X": ["F[--G][++G]X", "F[+GX][-GX]X", "F[+H][-H]X", "F[*GX][/GX]X", "F[--GX][++GX]X", "CX"], "E": ["C", "F", "H"]}
it = 2

draw_snowflake(axiom, P, it)
