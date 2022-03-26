import yaml
import json
import argparse
from key_check import KeyCheck
from tf_gen import TerraformGeneration

def key_validation(configuration):
    key_val = KeyCheck()

    # Check the top level keys
    key_val.top_level_keys(configuration.keys())

    # Check the second level keys
    key_val.provider_keys(configuration["provider"].keys())
    key_val.metadata_keys(configuration["metadata"].keys())
    key_val.spec_keys(configuration["spec"].keys())   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse the yaml configuration into a terraform file")
    parser.add_argument('-y', '--yaml', type=str, help='Specify the yaml file')
    args = parser.parse_args()

    with open(args.yaml, 'r') as f:
        configuration = yaml.safe_load(f)
    
    key_validation(configuration)

    #print(json.dumps(configuration, indent=4, sort_keys=False))

    tf = TerraformGeneration(configuration)
    tf.terraform_gen()

    