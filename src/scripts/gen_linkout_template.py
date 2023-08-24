import json
from ruamel.yaml import YAML
from string import Template
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filepath',
                    help='Path to json version of ontology for input')
args = parser.parse_args()

f = open(args.filepath, 'r')
j = json.loads(f.read())
g = j['graphs'][0]
conf = open('../config/db_graph_atlas.yaml', 'r')
yaml = YAML(typ='safe')
mapping = yaml.load(conf.read())
link = Template("http://atlas.brain-map.org/atlas?atlas="
                "$atlas_id#structure=$structure_id")

seed = {'ID': 'ID',
        'xref': 'A OboInOwl:hasDbXref',
        'prefLabel': 'A skos:prefLabel'}

tab = [seed]

for n in g['nodes']:
    if 'type' in n.keys() and n['type'] == 'CLASS':
        lstat = True
        for k, v in mapping.items():
            if str(n['id']).lower().startswith('https://purl.brain-bican.org/ontology/%s' % k) and 'lbl' in n and not str(n['id']).endswith('_ENTITY'):
                for a in v['atlases']:
                    try:
                        tab.append({'ID': n['id'],
                                    'xref': link.substitute(atlas_id=a['id'],
                                                            structure_id=str(n['id']).rsplit('_', 1)[-1]),
                                    'prefLabel': ' '.join([n['lbl'],
                                                           ' (',
                                                           v['species'],
                                                           ')'])})
                    except Exception as e:
                        print("ERROR: Exception occurred while processing: " + n['id'])
                        raise e
                lstat = False
        if lstat and 'lbl' in n.keys():
            tab.append({'ID': n['id'], 'xref': '', 'prefLabel': n['lbl']})


r_temp = pd.DataFrame.from_records(tab)
r_temp.to_csv('../templates/linkouts.tsv', sep='\t', index=False)

