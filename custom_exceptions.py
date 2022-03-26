"""
class (Exception):

    def __init__(self, message=""):
        super().__init__(message)

    def __str__(self):
        return f''
"""

class TopLevelKeysMissing(Exception):

    def __init__(self, message="Top Level Keys are missing."):
        super().__init__(message)

    def __str__(self):
        return f'Top Level Keys are missing. -> Required Keys Are: [provider, metadata, spec]'

class MetadataKeysMissing(Exception):

    def __init__(self, message="Metadata Keys are missing."):
        super().__init__(message)

    def __str__(self):
        return f'Metadata keys are missing. -> Required Keys Are: [name]'

class SpecKeysMissing(Exception):

    def __init__(self, message="Spec Keys are missing."):
        super().__init__(message)

    def __str__(self):
        return f'Spec keys are missing. -> Required Keys Are: [cpu, memory, network, disk]'

class ProviderKeysMissing(Exception):

    def __init__(self, message="Provider Keys are missing"):
        super().__init__(message)

    def __str__(self):
        return f'Provider keys are missing. -> Required Keys Are: [name]'