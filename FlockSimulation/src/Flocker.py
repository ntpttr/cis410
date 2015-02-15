__author__ = 'Nate'

import math

class Flocker:

    """
    Class for members of the flock

    Attributes:
        xPos - the position on the x axis of the flocker
        zPos - the position on the z axis of the flocker
        xVel - the velocity of the flocker in the x direction
        zVel - the velocity of the flocker in the y direction
        name - the string for the name of the flocker
    """

    # variables shared by all members of the flock
    flockerArray = []
    alignmentWeight = 0
    cohesionWeight = 0
    separationWeight = 0

    def __init__(self, _xPos, _yPos, _zPos, _xVel, _yVel, _zVel, _name):
        self.xPos = _xPos
        self.yPos = _yPos
        self.zPos = _zPos
        self.xVel = _xVel
        self.yVel = _yVel
        self.zVel = _zVel
        self.name = _name
        self.flockerArray.append(self)

    def updatePostion(self):
        """
        Updates the position of the flocker based on its velocity
        :return: Nothing
        """
        self.xPos += self.xVel
        self.yPos += self.yVel
        self.zPos += self.zVel

    def updateVelocity(self):
        """
        Updates the velocity of the flocker based on the algorithms of alignment, cohesion and separation
        :return: Nothing
        """
        alignment = self.computeAlignment()
        cohesion = self.computeCohesion()
        separation = self.computeSeparation()

        self.xVel += alignment[0] * self.alignmentWeight + cohesion[0] * self.cohesionWeight + separation[0] * self.separationWeight
        self.yVel += alignment[1] * self.alignmentWeight + cohesion[1] * self.cohesionWeight + separation[1] * self.separationWeight
        self.zVel += alignment[2] * self.alignmentWeight + cohesion[2] * self.cohesionWeight + separation[2] * self.separationWeight

        # normalize the vector
        length = math.sqrt((self.xVel * self.xVel) + (self.yVel * self.yVel) + (self.zVel * self.zVel))
        self.xVel /= length
        self.yVel /= length
        self.zVel /= length

    def distanceFrom(self, other):
        """
        Computes the distance between two flockers
        :param other: other flocker
        :return: distance between self and other
        """
        distance = math.sqrt((self.xPos - other.xPos) ** 2 + (self.yPos - other.yPos) ** 2 + (self.zPos - other.zPos) ** 2)
        return distance

    def computeAlignment(self):
        """
        Compute a vector whose velocity aligns with that of neighboring flockers
        :return: vector v
        """

        v = [0, 0, 0]
        numNeighbors = 0

        for other in self.flockerArray:
            if other != self:
                if self.distanceFrom(other) < 0.5:
                    v[0] += other.xVel
                    v[1] += other.yVel
                    v[2] += other.zVel
                    numNeighbors += 1

        if numNeighbors == 0:
            return v

        v[0] /= numNeighbors
        v[1] /= numNeighbors
        v[2] /= numNeighbors
        # normalize the vector
        length = math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))
        v[0] /= length
        v[1] /= length
        v[2] /= length

        return v

    def computeCohesion(self):
        """
        Compute a vector that points towards the center of mass of neighboring flockers
        :return: vector v
        """

        v = [0, 0, 0]
        numNeighbors = 0

        for other in self.flockerArray:
            if other != self:
                if self.distanceFrom(other) < 0.5:
                    v[0] += other.xPos
                    v[1] += other.yPos
                    v[2] += other.zPos
                    numNeighbors += 1

        if numNeighbors == 0:
            return v

        v[0] /= numNeighbors
        v[1] /= numNeighbors
        v[2] /= numNeighbors
        v[0] -= self.xPos
        v[1] -= self.yPos
        v[2] -= self.zPos

        # normalize the vector
        length = math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))
        v[0] /= length
        v[1] /= length
        v[2] /= length

        return v

    def computeSeparation(self):
        """
        Compute a vector that points away from neighboring flockers
        :return: vector v
        """

        v = [0, 0, 0]
        numNeighbors = 0

        for other in self.flockerArray:
            if other != self:
                if self.distanceFrom(other) < 0.5:
                    v[0] += other.xPos - self.xPos
                    v[1] += other.yPos - self.yPos
                    v[2] += other.zPos - self.zPos
                    numNeighbors += 1

        if numNeighbors == 0:
            return v

        v[0] /= numNeighbors
        v[1] /= numNeighbors
        v[2] /= numNeighbors
        v[0] *= -1
        v[1] *= -1
        v[2] *= -1

        # normalize the vector
        length = math.sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]))
        v[0] /= length
        v[1] /= length
        v[2] /= length

        return v