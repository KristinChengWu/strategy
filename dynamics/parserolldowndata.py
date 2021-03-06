import pandas as pd


def clean(file, windspeed=0):
    """
    :param file: Csv as generated by the test data
    
    :return: Cleaned DataFrame for usage in rolldownconverter.py
    """
    data = pd.read_csv(file)
    if "test.csv" in file or 'canlog' in file:
        # Calculate the average measured velocity
        data['average_velocity'] = data['Velocity']
    elif 'RollDown' in file:
        data = data.dropna(subset=['vehicle_velocity_right'])
        # We divide by 200 to take the average of two values multiplied by 100
        data['average_velocity'] = (data['vehicle_velocity_right']
                                    + data['vehicle_velocity_left']) / 200
        data['Time'] = data['Time Offset [ms]'] / 100
    # The first ~50 data points will always be useless
    data = data.truncate(before=50)
    data['time'] = (data['Time'] - data['Time'].iloc[0])
    # Convert to seconds
    data['time'] = data['time']
    # Adjust and convert to ms
    # Drop unnecessary data
    data = data[['time', 'average_velocity']]
    return data
