# Data 

This folder is used for data generation. Most of the files are copied over from homework 1, but 
if you want to check out the code to generate data, it's in create_data.py. Also, checkout the 
dataset folders if you want to see the actual data.

- Vanilla_dataset: contains the same data (train_x, train_y) we used to train gaussian processes. 
I generated 11000 data points. I plan on using this to train and experiment with "vanilla" neural
networks.

- image_dataset: Will contain all the images we need for training data,
along with other information we need. Each folder contains 50 images (one epoch), and data.csv contains 
the image along with the corresponding delta state at that time step.
