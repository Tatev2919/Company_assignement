def get_value(data, key, default, lookup=None, mapper=None):
    """
    Finds the value from data associated with key, or default if the
    key isn't present.
    If a lookup enum is provided, this value is then transformed to its
    enum value.
    If a mapper function is provided, this value is then transformed
    by applying mapper to it.
    """
    # Check if the key is present in the data dictionary
    if key in data:
        return_value = data[key]
    else:
        return_value = default  # Return default if key is missing
    
    # Handle cases where the value is None or an empty string
    if return_value is None or return_value == "":
        return_value = default
    
    # Transform value if lookup is provided
    if lookup:
        return_value = lookup.get(return_value, return_value)  # Use get() to avoid KeyError
    
    # Transform value if mapper function is provided
    if mapper:
        return_value = mapper(return_value)
    
    return return_value

def ftp_file_prefix(namespace):
    """
    Given a namespace string with dot-separated tokens, returns the
    string with the final token replaced by 'ftp'.
    Example: a.b.c => a.b.ftp
    """
    # Assume that namespace is a string and contains at least one '.'
    if not isinstance(namespace, str) or '.' not in namespace:
        raise ValueError("Namespace should be a dot-separated string")
    return ".".join(namespace.split(".")[:-1]) + '.ftp'

def string_to_bool(string):
    """
    Returns True if the given string is 'true' case-insensitive,
    False if it is 'false' case-insensitive.
    Raises ValueError for any other input.
    """
    if string.strip().lower() == 'true':  # Added strip() to address leading and/or trailing spaces
        return True
    if string.strip().lower() == 'false':
        return False
    raise ValueError(f'String {string} is neither true nor false')

def config_from_dict(dict):
    """
    Given a dict representing a row from a namespaces csv file,
    returns a DAG configuration as a pair whose first element is the
    DAG name and whose second element is a dict describing the DAG's properties.
    """
    # Assume that 'Namespace' and 'Airflow DAG' keys are in the dict
    if 'Namespace' not in dict or 'Airflow DAG' not in dict:
        raise KeyError("Dict must contain 'Namespace' and 'Airflow DAG' keys")
    
    namespace = dict['Namespace']
    return (dict['Airflow DAG'],
            {
                "earliest_available_delta_days": 0,
                "lif_encoding": 'json',
                "earliest_available_time":
                get_value(dict, 'Available Start Time', '07:00'),
                "latest_available_time":
                get_value(dict, 'Available End Time', '08:00'),
                "require_schema_match":
                get_value(dict, 'Requires Schema Match', 'True',
                         mapper=string_to_bool),
                "schedule_interval":
                get_value(dict, 'Schedule', '1 7 * * * '),
                "delta_days":
                get_value(dict, 'Delta Days', 'DAY_BEFORE',
                         lookup=DeltaDays),
                "ftp_file_wildcard":
                get_value(dict, 'File Naming Pattern', None),
                "ftp_file_prefix":
                get_value(dict, 'FTP File Prefix',
                         ftp_file_prefix(namespace)),
                "namespace": namespace
            }
           )

