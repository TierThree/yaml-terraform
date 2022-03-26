from custom_exceptions import *

class KeyCheck:

    def __init__(self):
        pass

    def top_level_keys(self, key_list):
       if "provider" not in key_list \
         or "metadata" not in key_list \
         or "spec" not in key_list:
             raise TopLevelKeysMissing()

    def metadata_keys(self, key_list):
        if "name" not in key_list:
            raise MetadataKeysMissing()

    def spec_keys(self, key_list):
        if "cpu" not in key_list \
         or "memory" not in key_list \
         or "network" not in key_list \
         or "disks" not in key_list:
            raise SpecKeysMissing()

    def provider_keys(self, key_list):
        if "name" not in key_list:
            raise ProviderKeysMissing()