import numpy as np
import pandas as pd

# Generating synthetic dataset
num_samples = 1000

temperature_data = np.random.uniform(30, 41, num_samples)
headache_data = np.random.randint(0, 10, num_samples)
age_data = np.random.randint(0, 130, num_samples)

# Creating a Pandas DataFrame
dataset = pd.DataFrame({
    'Temperature': temperature_data,
    'Headache': headache_data,
    'Age': age_data
})

# Adding a column for emergency referral decision based on the fuzzy inference system
def fuzzy_inference(temperature, headache, age):
    if age > 70:
        return 'High'
    else:
        if temperature < 35 or headache < 4:
            return 'Low'
        else:
            return 'High'

dataset['Emergency'] = dataset.apply(lambda row: fuzzy_inference(row['Temperature'], row['Headache'], row['Age']), axis=1)

# Displaying the synthetic dataset
print(dataset.head(100))
dataset.to_csv('emergency_dataset.csv', index=False)

print("Dataset saved successfully as 'emergency_dataset.csv'")