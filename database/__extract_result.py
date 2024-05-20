import sqlite3

def extract_result(picID:int, database='data.db'):  
    '''
            This private function is used for extract result with known picID

            :input:
            picID: int

            :return:
            tuple(class_name: str, description: dict, solution: dict)

            NOTE:
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
            '''  
    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute(f"""
            select picID,                   
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionPrevention,
                   solutionGardening,
                   solutionFertilization,
                   solutionSource
            from
            (
            select * from 
            (
                PIC join DISEASE on PIC.class_name=DISEASE.class_name
            )
                join SOLUTION on SOLUTION.class_name=PIC.class_name
            )
            where picID = {picID}
            """)

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
        data_list[1],
        data_list[2],
        data_list[3],
        data_list[4],
        data_list[5],
        data_list[6],
        data_list[7]
                 ) 

    class_name = diseaseName
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
    con.close()

    return class_name, description, solution