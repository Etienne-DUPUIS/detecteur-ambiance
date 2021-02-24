from IO import LCD
import dataset_creation as ds
import sensor

if __name__ == "__main__":
    print("Start recording data for 300s")
    LCD.lcd_text("Start recording data for 300s", LCD.LCD_LINE_1)
    data = ds.record_data(300, sensor.read_all_sensor, ["Humidity", "Temperature", "Motion"])
    print("Stop recording")
    print(data)
    print(ds.write_data(data))

    while True:
        timestamp, values = sensor.read_all_sensor()
        LCD.lcd_text(str(timestamp), LCD.LCD_LINE_1)
        LCD.lcd_text(str(values), LCD.LCD_LINE_2)