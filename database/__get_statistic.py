import sqlite3
from copy import deepcopy

def get_statistic(startDate:str,
                  endDate:str,
                  gardenName:str,
                  con):
    '''
    :input:
    startDate:str,
    endDate:str,
    gardenName:str,
    con = sqlite3.connect(<database directory>)

    :output:
    statistic = {
                        'overall_data' : dict(key, value),
                        'per_line' : {
                            'Hàng 1' : {
                                'Khoẻ' : int,
                                'Bệnh' : int,
                                'Chi tiết' : {
                                    dict('Tên bệnh' : số lượng)
                                }
                            },
                            'Hàng 2' : {
                                'Khoẻ' : int,
                                'Bệnh' : int,
                                'Chi tiết' : {
                                    dict('Tên bệnh' : số lượng)
                                }               
                            }
                        }
                    }
    '''

    cur = con.cursor()

    cur.execute(f'''
                SELECT gardenID 
                FROM GARDEN
                WHERE gardenName = '{gardenName}'
                ''')
    gardenID = cur.fetchall()[0][0]

    cur.execute(f'''
                SELECT * FROM
                (SELECT LOCATION.lineID, DISEASE.diseaseName, count(*) as count
                FROM PIC 
                JOIN DISEASE on DISEASE.diseaseID = PIC.diseaseID
                JOIN LOCATION on LOCATION.locationID = PIC.locationID
                JOIN GARDEN on LOCATION.gardenID = GARDEN.gardenID
                WHERE (PIC.picDate BETWEEN '{startDate}' AND '{endDate}') 
                    and (GARDEN.gardenID = {gardenID})
                GROUP BY DISEASE.diseaseID, GARDEN.gardenID, LOCATION.lineID)
                ORDER BY lineID asc
                ''')
        
    data = cur.fetchall()

    lineID_list = list(map(lambda x: 'Hàng ' + str(x[0]), data))

    statistic = dict()
    final_stat = dict()

    for i in lineID_list:
        statistic.update({i: dict()})
  
    for data_batch in data:
        lineName = 'Hàng ' + str(data_batch[0])
        diseaseName, count = data_batch[1], data_batch[2]
        statistic[lineName].update({diseaseName: count})

    final_stat = {
        'overall_data': statistic,
        'per_line': dict()
    }

    for i in lineID_list:
        healthy = 0
        unhealthy = 0
        for disease in statistic[i].keys():
            if disease == 'Cây tốt':
                healthy = statistic[i][disease]
            else:
                unhealthy += statistic[i][disease]
        final_stat['per_line'].update({
                i : {
                    'Khỏe': healthy,
                    'Bệnh': unhealthy,
                    'Chi tiết': deepcopy(statistic[i])
                }})

    return final_stat