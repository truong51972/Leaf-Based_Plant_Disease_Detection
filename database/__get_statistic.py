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
                     'Hàng 1': {'Virus khảm cà chua ToMV': int = ..., 
                                'Bệnh bạc lá sớm': int = ..., 
                                'Virus TYLCV (Tomato yellow leaf curl virus)': int = ..., 
                                'Bệnh tàn rụi muộn': int = ..., 
                                'Đốm vi khuẩn': int = ..., 
                                'Nấm Corynespora': int = ..., 
                                'Nấm Septoria lycopersici': int = ..., 
                                'Cây tốt': int = ..., 
                                'Bệnh khuôn lá': int = ..., 
                                'Bệnh nhện đỏ': int = ...},
                    'Hàng 2': ...,
                    ...
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
                SELECT LOCATION.lineID, DISEASE.diseaseName, count(*) as count
                FROM PIC 
                JOIN DISEASE on DISEASE.diseaseID = PIC.diseaseID
                JOIN LOCATION on LOCATION.locationID = PIC.locationID
                JOIN GARDEN on LOCATION.gardenID = GARDEN.gardenID
                WHERE (PIC.picDate BETWEEN '{startDate}' AND '{endDate}') 
                    and (GARDEN.gardenID = {gardenID})
                GROUP BY DISEASE.diseaseID, GARDEN.gardenID, LOCATION.lineID
                ''')
        
    data = cur.fetchall()

    lineID_list = set(map(lambda x: str(x[0]), data))

    statistic = dict()

    for i in lineID_list:
        lineName = 'Hàng ' + i
        statistic.update({lineName: dict()})
  
    for data_batch in data:
        lineName = 'Hàng ' + str(data_batch[0])
        diseaseName, count = data_batch[1], data_batch[2]
        statistic[lineName].update({diseaseName: count})

    return statistic