# Define function to read geodatabase table to pandas dataframe
def geodatabase_to_dataframe(table):
    """
    Description: creates a pandas dataframe from a geodatabase table
    Inputs: 'table' -- a table contained within a file geodatabase
    Returned Value: returns a pandas dataframe
    Preconditions: requires a pre-existing table in a file geodatabase
    """

    # Import packages
    import arcpy
    import pandas as pd

    # Convert table to pandas dataframe
    columns = [field.name for field in arcpy.ListFields(table) if field.type != 'Geometry']
    output_data = pd.DataFrame(data=arcpy.da.SearchCursor(table, columns), columns=columns)

    # Return dataframe
    return output_data
