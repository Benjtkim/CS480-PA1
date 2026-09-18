"""
This is the main entry of your program. Almost all things you need to implement is in this file.
The main class Sketch inherit from CanvasBase. For the parts you need to implement, they all marked TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

"""
from __future__ import annotations

import os

import wx
import math
import random
import numpy as np

from Buff import Buff
from Point2D import Point2D as Point
from ColorType import ColorType
from CanvasBase2D import CanvasBase2D as CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Please don't forget to override interrupt methods, otherwise NotImplementedError will be thrown

    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will perform a bounds check

    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising super sampling level

    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with key board press interruption. Use this to add new keys or new methods
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing

    List of methods to override the ones in CanvasBase:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard

    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer

    """

    debug: int = 0
    texture_file_path: str = "./pattern.jpg"
    texture: Buff | None = None

    # control flags
    randomColor: bool = False
    doTexture: bool = False
    doSmooth: bool = False
    doAA: bool = False
    doAAlevel: int = 4

    # test case status
    MIN_N_STEPS: int = 6
    MAX_N_STEPS: int = 192
    n_steps: int = 12  # For test case only
    test_case_index: int = 0
    test_case_list: list = []  # If you need more test cases, write as a method and add to list

    def __init__(self, parent: wx.Frame) -> None:
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist: list[Point], x: int, y: int) -> None:
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x: int, y: int) -> None:
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point is provided or a line when two points are provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.buff.setPoint(self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            # TODO 1: uncomment this and comment out setPoint when you have finished the drawLine function
            self.drawLine(self.buff, self.points_l[-2], self.points_l[-1], self.doSmooth, self.doAA, self.doAAlevel)
            # self.drawRectangle(self.buff, self.points_l[-2], self.points_l[-1])
            # self.buff.setPoint(self.points_l[-1])
            # self.points_l.clear()

    def drawRectangle(self, buff: Buff, p1: Point, p2: Point) -> None:

        delta_x = abs(p1.x - p2.x)
        min_x = min(p1.x, p2.x)
        for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
            for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                brightness = (x - min_x) / delta_x
                p = Point(x, y, ColorType(brightness, brightness, brightness))
                buff.setPoint(p)


    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x: int, y: int) -> None:
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.buff.setPoint(self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            # TODO 1: uncomment this and comment out setPoint when you have finished the drawLine function
            self.drawLine(self.buff, self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel)
            # self.buff.setPoint(self.points_r[-1])
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            # TODO 2: uncomment drawTriangle and comment out setPoint when you have finished the drawTriangle function
            self.drawTriangle(self.buff, self.points_r[-3], self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel, self.doTexture)
            # self.buff.setPoint(self.points_r[-1])
            # self.points_r.clear()

    def Interrupt_Keyboard(self, keycode: int) -> None:
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if x != min(max(0, int(x)), texture.width - 1):
            print("Warning: Texture query x coordinate is out of bounds")
        if y != min(max(0, int(y)), texture.height - 1):
            print("Warning: Texture query y coordinate is out of bounds")
        return texture.getPointFromPointArray(x, y)

    def drawLine(self, buff: Buff, p1: Point, p2: Point,
                    doSmooth: bool = True, doAA: bool = False, doAAlevel: int = 4) -> list[Point]:
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """

        # The list should start with p1.
        pts_drawn = [p1]

        # Required for simulating linear transformations.
        minusD_x = 1
        yStep = 1

        # Calculate delta_x and y.
        delta_x = p2.x - p1.x
        delta_y = p2.y - p1.y

        # Make copies of delta_x and y in case we take the absolute value of either or
        # flip them.
        orig_dx = delta_x
        orig_dy = delta_y

        # Boolean for whether the slope is shallow or steep. Use abs on delta_x and y
        # because both can be negative.
        shallowSlope = abs(delta_x) >= abs(delta_y)

        # Booleans for whether delta_x or y are negative.
        posDelta_x = delta_x >= 0
        posDelta_y = delta_y >= 0

        # For this implementation of Bresenham's, for steep slopes, the goal is to 
        # calculate the points that would make up the line for the reciprocal slope, 
        # but plot them with their coordinates flipped.

        # Iterate from (p1.x + 1, p1.y/p1.y+1) to (p2.x, p2.y). Y_0 would start at p1.y.
        if (shallowSlope and posDelta_x and posDelta_y):
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            Y_curr = p1.y
            range_x = range(min_x + 1, max_x + 1)

        # Iterate from (p1.y + 1, p1.x/p1.x + 1) to (p2.y, p2.x). So, delta_x and y would be 
        # flipped, and Y_0 would start at p1.x.
        elif (not shallowSlope and posDelta_x and posDelta_y):
            hold = delta_x
            delta_x = delta_y
            delta_y = hold
            min_x = min(p1.y, p2.y)
            max_x = max(p1.y, p2.y)
            Y_curr = p1.x
            range_x = range(min_x + 1, max_x + 1)

        # Iterate from (p1.x - 1, p1.y/p1.y + 1) to (p2.x, p2.y). Y_curr would start at 
        # p1.y.
        elif (shallowSlope and not posDelta_x and posDelta_y):
            delta_x = abs(delta_x)
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            Y_curr = p1.y
            range_x = range(max_x - 1, min_x - 1, -1)

        # Iterate from (p1.y + 1, p1.x/p1.x - 1) to (p2.y, p1.x + delta_x). The variable yStep 
        # is -1 because we want to simulate iterating backwards on x, which is represented by y 
        # for this slope since we plot the points with their coordinates flipped. 
        elif (not shallowSlope and not posDelta_x and posDelta_y):
            hold = abs(delta_x)
            delta_x = delta_y
            delta_y = hold
            min_x = min(p1.y, p2.y)
            max_x = max(p1.y, p2.y)
            Y_curr = p1.x
            yStep = -1
            range_x = range(min_x + 1, max_x + 1)

        # Iterate from (p1.x + 1, p1.y/p1.y - 1) to (p2.x, p2.y). Y_0 would start at p1.y, and 
        # yStep would be -1 to simulate the choice between the current or lower pixel as opposed 
        # to the current or upper pixel.
        elif (shallowSlope and posDelta_x and not posDelta_y):
            delta_y = abs(delta_y)
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            Y_curr = p1.y
            yStep = -1
            range_x = range(min_x + 1, max_x + 1)

        # Iterate from (p1.y - 1, p1.x/p1.x + 1) to (p2.y, p2.x). Y_0 would start at p1.x.
        elif (not shallowSlope and posDelta_x and not posDelta_y):
            delta_y = abs(delta_y)
            hold = delta_x
            delta_x = delta_y
            delta_y = hold
            min_x = min(p1.y, p2.y)
            max_x = max(p1.y, p2.y)
            Y_curr = p1.x
            range_x = range(max_x - 1, min_x - 1, -1)

        # Iterate from (p1.x - 1, p1.y/p1.y - 1) to (p2.x, p2.y). Y_0 would start at p1.y, 
        # and yStep would be -1.
        elif (shallowSlope and not posDelta_x and not posDelta_y):
            delta_x = abs(delta_x)
            delta_y = abs(delta_y)
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            Y_curr = p1.y
            range_x = range(max_x - 1, min_x - 1, -1)
            yStep = -1

        # Iterate from (p1.y - 1, p1.x/p1.x - 1) to (p2.y, p2.x). Y_0 would start at p1.x, and 
        #yStep would be -1.
        elif (not shallowSlope and not posDelta_x and not posDelta_y):
            delta_x = abs(delta_x)
            delta_y = abs(delta_y)
            hold = delta_x
            delta_x = delta_y
            delta_y = hold
            min_x = min(p1.y, p2.y)
            max_x = max(p1.y, p2.y)
            Y_curr = p1.x
            range_x = range(max_x - 1, min_x - 1, -1)
            yStep = -1

        # This is how you calculate D_0, and D_curr would obviously start at D_0.
        D_curr = 2 * delta_y - delta_x

        # Each case has a range associated with it.
        for x in range_x:

            minusD_x += 1

            # If the decision parameter is positive, apply Bresenham's by choosing
            # the corresponding pixel and by adding 2 * delta_y - 2 * delta_x.
            if D_curr > 0:
                Y_curr += yStep
                D_curr = D_curr + 2 *delta_y - 2 * delta_x

            # If the decision parameter is negative, apply Bresenham's by simply
            # adding 2 * delta_y.
            else :
                D_curr = D_curr + 2 * delta_y

            # If doSmooth is on, we need to do color interpolation.
            if (doSmooth):
                # Calculating t:
                # (1 - t)(p1.x) + tp2.x = x
                # p1.x - tp1.x + tp2.x = x
                # tp2.x - tp1.x = x - p1.x
                # t = (x - p1.x) / (p2.x - p1.x)
                # t = (x - p1.x) / delta_x
                # If using y, follow the same steps as above but replace x with y. The 
                # choice of using one over the other will depend on which delta is 
                # greater, or in other words, whether the line is shallow or steep.
                if shallowSlope:
                    t = (x - p1.x) / orig_dx
                else:
                    # Remember that for a steep slope, the current x represents the y coordinate 
                    # of the point that will be plotted, hence x - p1.y.
                    t = (x - p1.y) / orig_dy

                # Interpolation for the rgb values follows the same process as for coordinates.
                red = (1 - t) * p1.color.r + t * p2.color.r
                green = (1 - t) * p1.color.g + t * p2.color.g
                blue = (1 - t) * p1.color.b + t * p2.color.b

                # Need to use the interpolated values to create a ColorType object.
                color = ColorType(red, green, blue)

                # Coordinates would be normal for a shallow and positive slope.
                if (shallowSlope and posDelta_x and posDelta_y):
                    p = Point(x, Y_curr, color)

                # For a steep slope, the coordinates should be flipped.    
                elif (not shallowSlope and posDelta_x and posDelta_y):
                    p = Point(Y_curr, x, color)

                # For a shallow and negative slope, simulate iterating backwards using minusD_x.
                elif (shallowSlope and not posDelta_x and posDelta_y):
                    p = Point(p1.x - minusD_x, Y_curr, color)

                elif (not shallowSlope and not posDelta_x and posDelta_y):
                    p = Point(Y_curr, x, color)

                elif (shallowSlope and posDelta_x and not posDelta_y):
                    p = Point(x, Y_curr, color)

                elif (not shallowSlope and posDelta_x and not posDelta_y):
                    p = Point(Y_curr, x, color)

                elif (shallowSlope and not posDelta_x and not posDelta_y):
                    p = Point(x, Y_curr, color)

                elif (not shallowSlope and not posDelta_x and not posDelta_y):
                    p = Point(Y_curr, x, color)

                pts_drawn.append(p)
                buff.setPoint(p)

            # If doSmooth is off, the color of the point should be p1's color.
            else:
                if (shallowSlope and posDelta_x and posDelta_y):
                    p = Point(x, Y_curr, p1.color)
                elif (not shallowSlope and posDelta_x and posDelta_y):
                    p = Point(Y_curr, x, p1.color)
                elif (shallowSlope and not posDelta_x and posDelta_y):
                    p = Point(x, Y_curr, p1.color)
                elif (not shallowSlope and not posDelta_x and posDelta_y):
                    p = Point(Y_curr, x, p1.color)
                elif (shallowSlope and posDelta_x and not posDelta_y):
                    p = Point(x, Y_curr, p1.color)
                elif (not shallowSlope and posDelta_x and not posDelta_y):
                    p = Point(Y_curr, x, p1.color)
                elif (shallowSlope and not posDelta_x and not posDelta_y):
                    p = Point(x, Y_curr, p1.color)
                elif (not shallowSlope and not posDelta_x and not posDelta_y):
                    p = Point(Y_curr, x, p1.color)

                pts_drawn.append(p)
                buff.setPoint(p)
        
        return pts_drawn

    def drawTriangle(self, buff: Buff, p1: Point, p2: Point, p3: Point,
                     doSmooth: bool = True, doAA: bool = False, doAAlevel: int = 4,
                     doTexture: bool = False) -> None:
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color
        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Use of barycentric coordinates is not allowed in this function.
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. Texture-mapped fill of triangles should be controlled by doTexture.

        # Draw the 3 edges and save the lists each call to drawLine generates. Note that the points in each list
        # are sorted in increasing y-coord order.
        list1 = self.drawLine(buff, p1, p2, doSmooth, doAA, doAAlevel)
        list2 = self.drawLine(buff, p2, p3, doSmooth, doAA, doAAlevel)
        list3 = self.drawLine(buff, p1, p3, doSmooth, doAA, doAAlevel)

        # Add the 3 verticies into a list and sort them by their y-coords to find the upper, middle, and lower y-coords.
        pointsList = [p1, p2, p3]
        pointsList = sorted(pointsList, key=lambda point: point.y)
        upperY = pointsList[2].y
        middleY = pointsList[1].y
        lowerY = pointsList[0].y

        # Find the delta_y for the upper triangle, and the delta_y for the lower triangle.
        delta_y1 = upperY - middleY
        delta_y2 = middleY - lowerY

        # for y in range(upperY, middleY, -1):
        #     print("hello")
        
        return

    # test for lines lines in all directions
    def testCaseLine01(self, n_steps: int) -> None:
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal
    def testCaseLine02(self, n_steps: int) -> None:
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127) / 255,
                                          (128 + math.cos(d_theta * i * 5) * 127) / 255)),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127) / 255,
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127) / 255)),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps: int) -> None:
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps: int) -> None:
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps: int) -> None:
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()

    main()