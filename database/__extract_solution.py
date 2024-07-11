import sqlite3

def get_solution_tomato(con):
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
    where diseaseID between 1 and 10
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
        'Tên Bệnh' :         diseaseName, 
        'Nguyên Nhân':         diseaseCause,
        'Triệu Chứng':       diseaseSymptom, 
        'Phòng Ngừa':   solutionPrevention,
        'Làm Vườn':    solutionGardening,
        'Phân Bón':solutionFertilization,
        'Nguồn':       solutionSource
    }

def get_solution_potato(con):
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
    where diseaseID between 11 and 17
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
        'Tên Bệnh' :         diseaseName, 
        'Nguyên Nhân':         diseaseCause,
        'Triệu Chứng':       diseaseSymptom, 
        'Phòng Ngừa':   solutionPrevention,
        'Làm Vườn':    solutionGardening,
        'Phân Bón':solutionFertilization,
        'Nguồn':       solutionSource
    }