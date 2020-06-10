"""Probabilistic L-System to draw snowflakes using Turtle graphics"""
import turtle
import random
from math import cos, sqrt, radians
import os
from PIL import Image
import numpy as np


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
    d = 1 / (it + 1) * 200
    a = 60
    pos = []
    heading = []
    for x in instructions:
        if x == "F":
            t.forward(d)
        elif x == "G":
            t.forward(((it + 1) * d))
        elif x == "H":
            t.lt(10)
            t.forward(d * 0.8)
            t.rt(55)
            t.forward(sqrt(((d ** 2) / 25) * cos(radians(10))))
            t.rt(90)
            t.forward(sqrt(((d ** 2) / 25) * cos(radians(10))))
            t.rt(55)
            t.forward(d * 0.8)
        elif x == "C":
            r = d / 4
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


def draw_snowflake(axiom, rules, fileName):
    """
    Function to draw the snowflake with 6 branches and saves it
    :param axiom: axiom string
    :param rules: rules dictionary
    :param fileName: string
    """
    t = turtle.Turtle()
    turtle.mode("logo")
    t.ht()
    t.speed("fastest")
    t.pendown()
    t.width(3)
    it = random.choice([1, 2, 3])
    instructions = create_instructions(axiom, rules, it)
    for i in range(6):
        t.home()
        t.seth(i * 60)
        draw_branch(t, instructions, it)
    save_snowflake(fileName)


def save_snowflake(name):
    """
    Function to save the created snowflake in white as png
    :param name: string of name
    """
    turtle.Screen().getcanvas().postscript(file=name + '.eps')
    turtle.Screen().clear()
    command = "mogrify -resize ""400x400"" -transparent white -format png *.eps"
    os.system(command)

    im = Image.open(name + '.png')
    im = im.convert('RGBA')

    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][black_areas.T] = (255, 255, 255)
    image_data_bw = data.take(3, axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    image_data_new = data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1, :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(name + ".png", "PNG")


def create_snowflake(index):
    """
    Function to create one snowflake and save it and return the image
    :param index: index of the snowflake
    """
    axiom = "XE"
    P = {"X": ["F[--F][++F]X", "F[+FX][-FX]X", "F[+H][-H]X", "F[*FX][/FX]X", "F[--FX][++FX]X", "CX"],
         "E": ["C", "F", "H"]}
    fileName = "snowflake" + str(index)
    draw_snowflake(axiom, P, fileName)
    return fileName + '.png'
