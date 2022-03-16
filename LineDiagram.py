import math
import os
import matplotlib.pyplot as plt
from cycler import cycler


'''
Errors for if the multiplier, modulus, or color pallette is not set.
'''

class MultiplierNoneError(Exception):
    pass


class ModulusNoneError(Exception):
    pass


class ColorsNoneError(Exception):
    pass


class LineDiagram:
    FIGSIZES = [4, 6, 8, 11] # matplotlib image sizes
    # If the image directory doesn't exist, create it.
    IMAGE_DIR = os.path.dirname(os.path.realpath(__file__))
    IMAGE_DIR = os.path.join(IMAGE_DIR, 'PNG')
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)


    '''
    Generates line diagrams like those in the Mathologer video
    "Tesla's 3-6-9 and Vortex Math: Is this really the key to the universe?"
    https://www.youtube.com/watch?v=6ZrO90AI0c8
    '''


    def __init__(self):
        pass

    def new_diagram(self,
                    multiplier=None,
                    modulus=None,
                    colors=None,
                    line_width=0.01,
                    draw_circle=False):
        if multiplier is None:
            raise MultiplierNoneError

        if modulus is None:
            raise ModulusNoneError

        if colors is None:
            raise ColorsNoneError

        self.LINE_WIDTH = line_width

        # Find the cycle of remainders under repeated multiplication of some
        # number modulus some other number.
        remainders_sets = []
        for x in range(1, modulus):
            if not any(x in rs for rs in remainders_sets):
                remainders = [x]
                while True:
                    remainder = (remainders[-1] * multiplier)%modulus
                    if remainder in remainders:
                        break
                    else:
                        remainders.append(remainder)
                remainders_sets.append(remainders)

        self.image(multiplier, modulus, remainders_sets, draw_circle, colors)


    def image(self, multiplier, modulus, remainders_sets, draw_circle, colors):

        '''
        Create the line diagram.
        '''

        # Initiate the plot.
        fig, ax = plt.subplots(dpi=300)
        color_cycler = (cycler(color=colors))
        ax.set_aspect(1)

        # Hide text for matplotlib.
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(bottom=False, labelbottom=False, left=False,
                       labelleft=False)

        # Sometimes the lines suggest the circle enough so it is plain to see
        # what it is without literally drawing the circle.
        if draw_circle:
            circle = plt.Circle((0, 0),
                                1,
                                fill=False,
                                linewidth=self.LINE_WIDTH,
                                color=colors[-1])
            ax.add_artist(circle)

        # The minimum and maximum for the range of the image.
        plt.xlim((-1.01, 1.01))
        plt.ylim((-1.01, 1.01))

        ax.set_facecolor('#000000')

        # Draw lines connecting the cycle of remainders as they appear in the
        # sequence.
        xs = []
        ys = []
        for remainders in remainders_sets:
            for remainder in remainders + [remainders[0]]:
                angle = (remainder / modulus) * 2*math.pi + 0.5*math.pi
                xs.append(math.cos(angle))
                ys.append(math.sin(angle))

        # Color each line in accordance with the magnitude. If there are four
        # colors in the pallette, color the lines in quartiles of magnitude.
        min_magnitude = 0
        max_magnitude = 2
        magnitudes = []
        for i in range(1, len(xs)):
            magnitude = self.line_magnitude(xs[i-1], xs[i], ys[i-1], ys[i])
            magnitudes.append(magnitude)
        magnitudes.sort()
        step = len(magnitudes) / len(colors)
        cutoff_magnitudes = [min_magnitude]
        for i in range(1, len(colors)):
            magnitude = magnitudes[int(step*i)]
            cutoff_magnitudes.append(magnitude)

        for i in range(1, len(xs)):
            magnitude = self.line_magnitude(xs[i-1], xs[i], ys[i-1], ys[i])
            step = (max_magnitude-min_magnitude)/len(colors)
            c_i = 0
            for j, cutoff_magnitude in enumerate(cutoff_magnitudes):
                if magnitude >= cutoff_magnitude:
                    c_i = j
            ax.plot([xs[i-1], xs[i]],
                    [ys[i-1], ys[i]],
                    linewidth=self.LINE_WIDTH,
                    color=colors[c_i])

        # Write images for each matplotlib figure size.
        for i, figsize in enumerate(self.FIGSIZES):
            IMAGE_F = 'multiplier={:,}'.format(multiplier) + \
                      ' modulus={:,}'.format(modulus) + ' ' + str(i+1) + '.png'
            IMAGE_PATH = os.path.join(self.IMAGE_DIR, IMAGE_F)

            gcf = plt.gcf()
            gcf.set_figwidth(figsize)
            gcf.set_figheight(figsize)
            plt.savefig(IMAGE_PATH, bbox_inches='tight', pad_inches=0)


    def line_magnitude(self, x1, x2, y1, y2):

        '''
        Return the magnitude of a line given the endpoints.
        '''

        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def digital_sum(self, x):

        '''
        Return the digital sum of x.
        '''

        if x < 10:
            return x
        else:
            return x%10 + self.digital_sum(x//10)


    def digital_root(self, x):

        '''
        Return the digital root of x.
        '''

        while True:
            x = self.digital_sum(x)
            if x < 10:
                return x


if __name__ == '__main__':
    pass
