#!/usr/bin/env python
import NeuronPlotLib.parse_csv as csv
import NeuronPlotLib.modality_plot as plt
import os

if __name__ == '__main__':

    # input files in the demo folder:
    files = [
        'modality_data.csv',
    ]

    for file in files:

        # Get full path of input files
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, 'demo_data', file)

        # Parse data from csv file
        new_csv = csv.LoadCsv(file_path)
        data, binarization = new_csv.ParseCsv()

        # Make figure:
        plot = plt.ModalityPlot(data,
                                binarization,
                                modalities=[
                                    'Set 1', 'Set 2', 'Set 3'],
                                angles=[90, 210, 330],
                                labels=False,
                                scalecircle=0.3,   # Scale circle radius
                                marker='',         # vector endpoints marker
                                linestyle='-',
                                linewidth=0.7,
                                alpha=0.5,
                                same_scale=False,  # Draw all the subplots in the same scale
                                figsize=(10, 10),
                                title='Modality Diagram Example',
                                colors=(
                                    'tab:green',   # Set 1 color
                                    'navy',        # Set 2 color
                                    'tab:red',     # Set 3 color
                                    'tab:cyan',    # Sets 1 & 2 intersection color
                                    'darkorange',  # Sets 1 & 3 intersection color
                                    'tab:purple',  # Sets 2 & 3 intersection color
                                    'black'),      # All sets   intersection color
                                )

        plot.save(file_path, type='svg', transparent=True)
        plot.show()