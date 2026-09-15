"""
A Point class is defined here, which might store point coordinates, color and corresponding texture position.
First version Created on 09/23/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""
from __future__ import annotations

import copy
import time
from collections.abc import Sequence
from typing import overload
from ColorType import ColorType


class Point2D:
    """
    Properties:
        coords: List<Integer>
        color: ColorType
        texture: List<Float>
    Desciption:
        Invisible Variables:
        coords is used to describe coordinates of a point, only integers allowed
        color is used to describe color of a point, must be ColorType Object
        texture is used to describe corresponding coordinates in texture, can be float or double
        """

    # Enforce type checking for all variables, set them invisible
    __slots__ = ["coords", "color", "texture"]

    @property
    def x(self) -> int:
        return self.coords[0]

    @property
    def y(self) -> int:
        return self.coords[1]

    @overload
    def __init__(self, coords: Sequence[int] | None = None,
                 color: ColorType | None = None,
                 textureCoords: Sequence[float] | None = None) -> None: ...

    @overload
    def __init__(self, x: int, y: int,
                 color: ColorType | None = None,
                 textureCoords: Sequence[float] | None = None) -> None: ...

    def __init__(self, coords_or_x=None, y_or_color=None,
                 color_or_texture=None, textureCoords=None):
        """
        init Point by using coords, color, textureCoords or an existing point
        if point given, ignore other input arguments
        if point not given, any missing argument will be set to all zero

        Supports two calling conventions:
            Point2D((x, y), color, textureCoords)
            Point2D(x, y, color, textureCoords)

        :param coords: The coordinates of current Point. Only integer coordinates are allowed here.
        :type coords: list[int] or tuple[int]
        :param color: Point color defined in ColorType.
        :type color: ColorType
        :param textureCoords: Corresponding position in texture
        :type textureCoords: list[float] or tuple[float]
        :rtype: None
        """
        if isinstance(coords_or_x, (int, float)):
            # Point2D(x, y, ...) form
            coords = (int(coords_or_x), int(y_or_color))
            color = color_or_texture
            texture = textureCoords
        else:
            # Point2D([x, y], ...) form
            coords = coords_or_x
            color = y_or_color
            texture = color_or_texture

        # Set point coords
        self.coords = coords
        # Set color
        self.color = color
        # Set texture coords
        self.texture = texture

    def __repr__(self) -> str:
        print(self.coords, self.color)
        return "p:" + str(self.coords) + \
               " c:" + str(self.color) + \
               " t:" + str(self.texture)

    def __hash__(self) -> int:
        if self.texture is not None:
            tuple_texture = tuple(self.texture)
        else:
            tuple_texture = self.texture
        if self.coords is not None:
            tuple_coords = tuple(self.coords)
        else:
            tuple_coords = self.coords
        return hash((tuple_coords, self.color, tuple_texture))

    def __eq__(self, other: object) -> bool:
        try:
            result = self.coords == other.coords and \
                     self.texture == other.texture and \
                     self.color == other.color
        except AttributeError:
            return False
        return result

    def setColor(self, c: ColorType) -> None:
        """
        c should be ColorType, use c to set up color of this point
        This method will deep copy the input argument.
        If you only want to shallow copy the input argument to point color, access that variable directly.

        :param c: the color which you want to set this point to
        :type c: ColorType
        :rtype: None
        """
        self.color = c.copy()

    def setColor_r(self, r: float) -> None:
        self.color.r = r

    def setColor_g(self, g: float) -> None:
        self.color.g = g

    def setColor_b(self, b: float) -> None:
        self.color.b = b

    def getCoords(self) -> Sequence[int] | None:
        """
        Get point coordinates

        :rtype: tuple[int]
        """
        return self.coords

    def getTextureCoords(self) -> Sequence[float] | None:
        """
        Get corresponding texture coordinates

        :rtype: tuple[float]
        """
        return self.texture

    def getColor(self) -> ColorType | None:
        return self.color

    @overload
    def setCoords(self, coords: Sequence[int | float]) -> None: ...

    @overload
    def setCoords(self, x: int | float, y: int | float) -> None: ...

    def setCoords(self, coords_or_x, y=None):
        """
        Use a tuple/list or individual x, y values to set point coords

        :param coords: the point coordinates you want to set to
        :type coords: tuple[int] or list[int]
        """
        if y is not None:
            self.coords = (int(coords_or_x), int(y))
        else:
            self.coords = tuple(int(i) for i in coords_or_x)

    def setTextureCoords(self, textureCoords: Sequence[float]) -> None:
        """
        Use a tuple/list of coords to set point textureCoords

        :param textureCoords: the texture coordinates you want to set to
        :type textureCoords: tuple[float] or list[float]
        """
        self.texture = tuple(i for i in textureCoords)

    def copy(self) -> Point2D:
        """
        A deep copy of current point

        :rtype: Point
        """
        return Point2D(copy.deepcopy(self.coords), self.color.copy(), copy.deepcopy(self.texture))


if __name__ == "__main__":
    a = Point2D((1, 2))
    print(a)
    a.setColor(ColorType(0.5*255, 0.2*255, 0.3*255))
    print(a)
    a.setCoords([3, 4])
    print(a)
    a.setTextureCoords((2.22, 3.33))
    print("Point a: ", a)
    b = a.copy()
    print("Point copied from point a: ", b)

    print("Test for illegal input")
    c = Point2D((1.5, 4))
    print(c)

    # Test for list<Point>
    pl = [Point2D((1, 3)), Point2D((2, 3)), Point2D((3, 5))]
    print(pl)

    # Test for set<Point>
    ps = set(pl)
    print(ps)
    ps.add(Point2D((1, 3), ColorType(1, 0, 1)))
    print(ps)
    ps.add(Point2D((1, 3), ColorType(0, 0, 0)))
    print(ps)

    cds = (1, 2, 3)
    clr = ColorType(0.2, 0.3, 0.4)
    t1 = time.time()
    [Point2D() for _ in range(500 * 500)]
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = Point2D(cds, clr)
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = ColorType()
    print(time.time() - t1)
