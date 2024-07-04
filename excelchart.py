import os
import pandas as pd
import matplotlib.pyplot as plt

with open('expenses', 'rw') as file:
    df = pd.read_excel(file)
    
