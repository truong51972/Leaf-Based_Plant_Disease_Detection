import sqlite3

def get_solution(con):
    cur = con.cursor()
    cur.execute(f'''
    select                   
    diseaseName, 
    diseaseCause, 
    diseaseSymptom, 
    solutionPrevention,
    solutionGardening,
    solutionFertilization,
    solutionSource
    from DISEASE
''')
    solution = cur.fetchall()
    
    (
    diseaseName, 
    diseaseCause,
    diseaseSymptom, 
    solutionPrevention,
    solutionGardening,
    solutionFertilization,
    solutionSource
    ) = (
        list(map(lambda x: x[0], solution)),
        list(map(lambda x: x[1], solution)),
        list(map(lambda x: x[2], solution)),
        list(map(lambda x: x[3], solution)),
        list(map(lambda x: x[4], solution)),
        list(map(lambda x: x[5], solution)),
        list(map(lambda x: x[6], solution))
                 )
    
    return {
        'diseaseName' :         diseaseName, 
        'diseaseCause':         diseaseCause,
        'diseaseSymptom':       diseaseSymptom, 
        'solutionPrevention':   solutionPrevention,
        'solutionGardening':    solutionGardening,
        'solutionFertilization':solutionFertilization,
        'solutionSource':       solutionSource
    }
    
if __name__ == '__main__':
    con = sqlite3.connect('data.db')
    print(len(get_solution(con)))