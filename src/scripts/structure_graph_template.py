import argparse
import pandas as pd
import csv

from structure_graph_utils import read_structure_graph


def generate_template(graph_json, output):
    data_list = read_structure_graph(graph_json)

    data_template = pd.DataFrame.from_records(data_list)
    data_template.to_csv(output, sep="\t", index=False, quoting=csv.QUOTE_NONE)


parser = argparse.ArgumentParser(description='Cli interface structure graph linkml template generation.')

parser.add_argument('-i', '--input', help="Path to input JSON file")
parser.add_argument('-o', '--output', help="Path to output TSV file")

args = parser.parse_args()

generate_template(args.input, args.output)
