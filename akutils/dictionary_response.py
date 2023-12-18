# Define function to return response from dictionary
def get_response(test, dictionary, type):
    """
    Description: retrieves either a key or value from a dictionary
    Inputs: 'test' -- a variable to test against the dictionary keys or values
            'dictionary' -- a dictionary that stores keys and values to test and retrieve
            'type' -- either 'key' to return a key or 'value' to return a value
    Returned Value: returns a key or value
    Preconditions: requires a predefined dictionary
    """
    for key, value in dictionary.items():
        if type == 'key':
            if test == value:
                return key
        elif type=='value':
            if test == key:
                return value
        else:
            print('ERROR: Type must be either "key" or "value".')
            quit()

# Define function to return value from dictionary
def get_attribute_code_block():
    '''
    Description: provides the dictionary response function as a code block for arcpy
    Inputs: none
    Returned Value: returns a code block
    Preconditions: none
    '''
    code_block = '''def get_response(test, dictionary, type):
    for key, value in dictionary.items():
        if type == 'key':
            if test == value:
                return key
        elif type=='value':
            if test == key:
                return value
        else:
            print('ERROR: Type must be either "key" or "value".')
            quit()'''
    return code_block
