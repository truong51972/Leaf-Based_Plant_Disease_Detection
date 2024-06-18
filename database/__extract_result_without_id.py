import sqlite3

def extract_result_without_id(class_name:str,
                                con):
    
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
                from DISEASE where class_name = {class_name}
                ''')
    
    data_list = cur.fetchall()[0]
    (
    diseaseName, 
    diseaseCause,
    diseaseSymptom, 
    solutionPrevention,
    solutionGardening,
    solutionFertilization,
    solutionSource
    ) = (
        data_list[0],
        data_list[1],
        data_list[2],
        data_list[3],
        data_list[4],
        data_list[5],
        data_list[6]
                 ) 

    description = {
        'cause':diseaseCause,
        'symptom':diseaseSymptom                
    }
    solution = {
        'prevention':solutionPrevention,
        'gardening':solutionGardening,
        'fertilization':solutionFertilization,
        'source':solutionSource
    }

    con.commit()
    
    return diseaseName, description, solution