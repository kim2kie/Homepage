# -*- coding: utf-8 -*-
from odbAccess import openOdb
import csv
from abaqusConstants import NODAL

# ABAQUS ODB
odb_path = 'C:/Users/KGW/Desktop/API test/fr-Kst-knn50kt10-full-without-nomal.odb'
odb = openOdb(odb_path)

# instance
instance_name = 'H-BEAM-1'
instance = odb.rootAssembly.instances[instance_name]

# node
node_labels = [1437, 2912, 2913, 2914, 2915]


# CSV
output_csv_path = 'C:/Users/KGW/Desktop/API test/Disp.csv'
with open(output_csv_path, 'wb') as csvfile: # 'wb'
    csvwriter = csv.writer(csvfile)

    # Header row
    header_row = ['Time'] + ['Node_{}_U{}'.format(label, dir) for label in node_labels for dir in ['1', '2', '3']]
    csvwriter.writerow(header_row)

    # Loop step
    for step_name in odb.steps.keys():
        step = odb.steps[step_name]
        # Loop frame step
        for frame_num, frame in enumerate(step.frames):
            row_data = []

            # Time
            time_data = frame.frameValue
            row_data.append(time_data)

            # displacement field output
            displacement_field = frame.fieldOutputs['U']
            displacement_subField = displacement_field.getSubset(region=instance, position=NODAL)

            # node labels data
            displacement_dict = {value.nodeLabel: value.data for value in displacement_subField.values}

            # Loop node label
            for label in node_labels:
                # Get data
                displacement = displacement_dict.get(label, [0.0, 0.0, 0.0])  # Default to zeros if not found
                row_data.extend(displacement)

            # Write CSV
            csvwriter.writerow(row_data)

# Close ODB
odb.close()