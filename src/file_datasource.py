from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from typing import List

#
class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        pass

    def file_data_reader(self, path: str):
        while True:
            file = open(path)
            data_reader = reader(file)
            header = next(data_reader)

            for row in data_reader:
                yield row

            file.close()

    def read(self) -> List[AggregatedData]:
        """Метод повертає дані отримані з датчиків"""
        dataList = []
        for i in range(5):
            dataList.append(
                AggregatedData(
                    Accelerometer(*next(self.accelerometer_data_reader)),
                    Gps(*next(self.gps_data_reader)),
                    Parking(*next(self.gps_data_reader)),
                    datetime.now()
                )
            )

        return dataList

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_data_reader = self.file_data_reader(self.accelerometer_filename)
        self.gps_data_reader = self.file_data_reader(self.gps_filename)
        self.parking_data_reader = self.file_data_reader(self.parking_filename)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        pass