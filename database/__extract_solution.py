import sqlite3

def _get_solution(con):
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
        tuple(i[0] for i in solution),
        tuple(i[1] for i in solution),
        tuple(i[2] for i in solution),
        tuple(i[3] for i in solution),
        tuple(i[4] for i in solution),
        tuple(i[5] for i in solution),
        tuple(i[6] for i in solution)
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