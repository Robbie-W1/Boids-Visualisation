from math import sqrt

class Vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.calculate_magnitude()
        self.magnitude

    def __add__(self, other):
        if other is None:
            return self
        if type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other, self.y + other)
        

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def __sub__(self, other):
        if type(other) == Vector:
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return Vector(self.x - other, self.y - other)
        
    def __truediv__(self, other):
        if type(other) != Vector:
            return Vector(self.x / other, self.y / other)

        if other.x != 0 and other.y != 0:
            return Vector(self.x / other.x, self.y / other.y)
        else:
            return Vector(self.x, self.y)

    def __str__(self):
        return " ".join([f"x={self.x :.3f},", f"y={self.y :.3f}"])

    def set_magnitude(self, magnitude):
        self.calculate_magnitude()
        if self.magnitude != 0:
            return  self * (magnitude / self.magnitude)
        else:
            return Vector(0, 0)

    def calculate_magnitude(self):
        self.magnitude = sqrt(self.x **2 + self.y **2)
    
        
def main():
    a = Vector(3,4)
    print(a.magnitude)
    print(a)
    a = a.set_magnitude(100)
    print(a)
    print(a.magnitude)
    
    

if __name__ == "__main__":
    main()
