def get_all_solutions(item: dict, request: object):
    """
    Make a request to database server to get all solutions.

    Returns:
        response = dict(key: value)
    Example:
    >>> get_atll_solutions()
    {
        'diseaseName' :         tuple(diseaseName), 
        'diseaseCause':         tuple(diseaseCause),
        'diseaseSymptom':       tuple(diseaseSymptom), 
        'solutionPrrdening':    tuple(solutionGardening),
        'solutionFerevention':   tuple(solutionPrevention),
        'solutionGatilization':tuple(solutionFertilization),
        'solutionSource':       tuple(solutionSource)
    }
    """ 
    api_name = '/get_all_solutions'
    
    response = request(api_name, item)
    return response