#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import numpy as np

# Only use for plot layout adjustment
DEBUG = False


class ModalityPlot:
    '''
        Input fotmat:

        data: list of points, each point should be represented as a
              list or touple containing three floats, one per modality.

    '''

    def __init__(self,
                 data: list,
                 binarization: list,
                 modalities=('A', 'B', 'C'),
                 angles=[90, 210, 330],
                 labels=True,
                 scalecircle=1,
                 marker='',
                 linestyle='-',
                 linewidth=0.5,
                 alpha=0.8,
                 same_scale=False,
                 figsize=(10, 10),
                 title='',
                 colors=(
                     'tab:green',
                     'tab:blue',
                     'tab:red',
                     'tab:cyan',
                     'tab:olive',
                     'tab:purple',
                     'black'),
                 normalization_func='sigmoid',
                 ) -> None:

        self.data = data
        self.binarization = binarization
        self.modalities = modalities
        self.angles = np.deg2rad(angles)
        self.labels = labels
        self.scalecircle = scalecircle
        self.marker = marker
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.alpha = alpha
        self.same_scale = same_scale
        self.figsize = figsize
        self.title = title
        self.colors = colors
        self.normalization_func = normalization_func
        self.modality_patterns = (
            (True, False, False),
            (False, True, False),
            (False, False, True),
            (True, True, False),
            (True, False, True),
            (False, True, True),
            (True, True, True),
        )
        self.modalities = (
            (self.modalities[0], None, None),
            (None, self.modalities[1], None),
            (None, None, self.modalities[2]),
            (self.modalities[0], self.modalities[1], None),
            (self.modalities[0], None, self.modalities[2]),
            (None, self.modalities[1], self.modalities[2]),
            (None, None, None),
        )

        # check input:
        assert self.data, 'data array must not be empty'
        assert self.binarization, 'binarization array must not be empty'
        assert len(self.data) == len(
            self.binarization), 'data and binarization arrays must have exact length'
        assert len(self.data[0]) == len(self.binarization[0]
                                        ) == 3, 'data and binarization arrays must have three columns each'

        # Prepare figure:
        self.make_fig()

    def normalization(self, input) -> list:
        '''
            Define function to normalize coordinates
            to values in range of 0 to 1 for HSV color model.
            input: np.array
        '''

        match self.normalization_func:

            case 'linear':
                def func(x): return (x - np.min(input)) / \
                    (np.max(input) - np.min(input))

            case 'sigmoid':
                def func(x): return 1 / (1 + np.exp(-x))

            # case 'log':
            #     log_input = np.log1p(input)
            #     func = lambda x: (x - np.min(log_input)) / (np.max(log_input) - np.min(log_input))

        return [func(x) for x in input]

    def vector_addition(self, data) -> list:

        resultants = []
        for point in data:

            # ignore empty lines
            if not all(x == 0 for x in point):

                # Calculate resultant vector
                resultants.append(
                    np.sum([point[i] * np.exp(1j * self.angles[i]) for i in range(len(point))]))
            else:
                resultants.append((0))

        return resultants

    def find_match_modality(self, sample, list) -> int:
        for i, item in enumerate(list):
            if item == sample:
                return i
        return 0

    def draw_scalecircle(self, ax) -> None:

        # Plot the single-unit circle
        r = self.scalecircle
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(theta, [r]*len(theta), color='black',
                linestyle=':', linewidth=1, zorder=10)

    def initiate_subplot(self, ax) -> None:

        # Set custom design
        ax.set_yticklabels([])
        ax.set_xticks(self.angles if self.labels else [])
        ax.grid(False)
        ax.spines['polar'].set_visible(
            False) if not DEBUG else ax.spines['polar'].set_visible(True)
        ax.patch.set_facecolor('none')

    # Draw coordinate grid on the top of figure
    # to make easier subplots alignment on devtime
    def debug_grid(self, fig, y, x) -> None:

        for i in range(1, y*x+1):

            ax = fig.add_subplot(y, x, i)

            # Set the facecolor of the axes
            ax.patch.set_facecolor('none')
            ax.set_xticks([])
            ax.set_yticks([])

            for spine in ax.spines.values():
                spine.set_edgecolor('black')

    def draw_subplot(self, ax, modality_pattern, modalities) -> None:

        resultants = self.vector_addition(self.data)

        # for future sets calculation
        sets_counter = [0] * 8

        # Color measurement in HSV format (temporarry abandoned future)
        # hue_array = self.normalization(np.angle(resultants))
        # sat_array = np.ones_like(hue_array)
        # val_array = self.normalization(np.abs(resultants))
        # color = mcolors.hsv_to_rgb((hue, sat, val))

        for resultant, data_row, bin_row in zip(resultants, self.data, self.binarization):

            if resultant and (bin_row == modality_pattern) or modality_pattern == (True, True, True):
                # defining the modality of responce to apply color and z-order
                modality_pattern_number = self.find_match_modality(
                    bin_row, self.modality_patterns)
                sets_counter[modality_pattern_number] += 1
                color = self.colors[modality_pattern_number]
                zorder = modality_pattern_number

                ax.plot(
                    [0, np.angle(resultant)],
                    [0, np.abs(resultant)],
                    zorder=zorder,
                    marker=self.marker,
                    linestyle=self.linestyle,
                    linewidth=self.linewidth,
                    color=color,
                    alpha=self.alpha)
                if self.labels:
                    ax.set_xticklabels(modalities)

        if self.scalecircle:
            self.draw_scalecircle(ax)

    # Make figure layout,
    # starting point of plotting
    def make_fig(self) -> None:

        # Create figure
        fig = plt.figure(figsize=self.figsize)

        # Defining layout
        gs = gridspec.GridSpec(20, 20, figure=fig)
        ax1 = fig.add_subplot(gs[1:11, 5:15], polar=True)
        ax2 = fig.add_subplot(gs[7:17, 1:11], polar=True)
        ax3 = fig.add_subplot(gs[7:17, 9:19], polar=True)
        ax12 = fig.add_subplot(gs[4:14, 3:13], polar=True)
        ax13 = fig.add_subplot(gs[4:14, 7:17], polar=True)
        ax23 = fig.add_subplot(gs[7:17, 5:15], polar=True)
        ax0 = fig.add_subplot(gs[5:15, 5:15], polar=True)
        subplots = (ax1, ax2, ax3, ax12, ax13, ax23, ax0)

        for ax, modality_pattern, modalities in zip(subplots, self.modality_patterns, self.modalities):
            self.initiate_subplot(ax)
            self.draw_subplot(ax, modality_pattern, modalities)

        if self.same_scale:
            rlim = ax0.get_xlim()
            for ax in subplots:
                ax.set_rlim(rlim)

        # Draw coordinate grid on the top of figure
        # to make easier subplots alignment on devtime
        if DEBUG:
            self.debug_grid(fig, 20, 20)

        plt.subplots_adjust(wspace=0.0, hspace=0.0)
        plt.tight_layout()
        plt.suptitle(self.title)

    def show(self):
        plt.show()

    def save(self, filename, type='svg', transparent=False):
        plt.savefig('{}.{}'.format(filename, type), transparent=transparent)


if __name__ == '__main__':
    print('\nThis script can be used as an imported module only\n')
