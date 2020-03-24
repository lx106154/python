import numpy as np
import matplotlib.pyplot as plt


# Define the Function class
class Function:
    """This class will act as a wrapper for a generic lambda function."""

    # Define the method when class Function is instantiated
    def __init__(self, f):
        self.f = f

    # Define the method when class Function is called
    def __call__(self, x):
        return self.f(x)

    # Define the four handling methods with another Function class
    # or with a float number
    def __add__(self, other):
        if type(other).__name__ == 'Function':
            return Function(lambda x: self.f(x) + other.f(x))
        elif type(other).__name__ == 'float':
            return Function(lambda x: self.f(x) + other)

    def __sub__(self, other):
        if type(other).__name__ == 'Function':
            return Function(lambda x: self.f(x) - other.f(x))
        elif type(other).__name__ == 'float':
            return Function(lambda x: self.f(x) - other)

    def __mul__(self, other):
        if type(other).__name__ == 'Function':
            return Function(lambda x: self.f(x) * other.f(x))
        elif type(other).__name__ == 'float':
            return Function(lambda x: self.f(x) * other)

    def __truediv__(self, other):
        if type(other).__name__ == 'Function':
            return Function(lambda x: self.f(x) / other.f(x))
        elif type(other).__name__ == 'float':
            return Function(lambda x: self.f(x) / other)


# Define the Plotter class
class Plotter:
    """This class will act as a wrapper for Matplotlib's plotting function.   When initialized, the domain of the function and the step size will needs to be specified. """

    # Assign the arguments to an np array of x values when class
    # Function is instantiated
    def __init__(self, low, high, stepsize):
        self.xvalues = np.arange(low, high, stepsize)

    # Define the add_func method
    def add_func(self, name, func):
        """This method will be used to add one function to the plot."""
        yvalues = [func(x) for x in self.xvalues]
        plt.plot(self.xvalues, yvalues, label=name)

    # Define the plot method
    def plot(self):
        """This method will show the final plot."""
        plt.legend(loc='upper left')
        plt.show()


if __name__ == "__main__":
    f1 = Function(lambda x: x ** 2)
    f2 = Function(lambda x: x + 3)
    f3 = Function(lambda x: np.sin(x))
    f4 = (f1 + f2) * f3 / 2.0
    plot = Plotter(0, 20, 0.1)
    plot.add_func("Function 1", f1)
    plot.add_func("Function 2", f2)
    plot.add_func("Function 3", f3)
    plot.add_func("Function 4", f4)
    plot.plot()
