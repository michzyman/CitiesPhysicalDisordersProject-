import pandas as pd

COL_NAMES = ['MINIMUM LATITUDE', 'MAXIMUM LATITUDE', 'MINIMUM LONGITUDE', 'MAXIMUM LONGITUDE']

def generate_predictions(input_filename):
  parcels = pd.read_csv('user_files/uploads/{}'.format(input_filename), usecols=COL_NAMES)

  parcels['PREDICTION'] = 0

  parcels.to_csv('user_files/outputs/{}-output.csv'.format(input_filename), index=False)
