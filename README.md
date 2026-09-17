# Self-Driving Car — Behavioral Cloning

A deep learning based autonomous driving system that learns to steer a car from human driving data using behavioral cloning.

The project uses a convolutional neural network inspired by NVIDIA's end-to-end self-driving architecture. The model learns the relationship between road images and steering angles and then uses the trained network to control the car inside a driving simulator.

## Demo

The project is demonstrated using a driving simulator where the trained neural network receives live camera frames and continuously predicts steering and throttle values.


## Features

* End-to-end behavioral cloning
* CNN-based steering prediction
* Center, left and right camera training
* Steering correction for side cameras
* Steering distribution balancing
* Image preprocessing
* Random horizontal flipping
* Brightness augmentation
* Translation augmentation
* Automatic learning-rate reduction
* Early stopping
* Best-model checkpointing
* Real-time simulator control
* Dynamic throttle based on steering angle and vehicle speed

## Project Pipeline

```text
Driving Simulator
        ↓
Driving Images + Steering Angles
        ↓
Data Preprocessing
        ↓
Data Augmentation
        ↓
Steering Distribution Balancing
        ↓
CNN Training
        ↓
Trained Model
        ↓
Real-Time Camera Input
        ↓
Steering Prediction
        ↓
Throttle Control
        ↓
Autonomous Driving
```

## Model Architecture

The model is a PilotNet-inspired convolutional neural network.

```text
Input Image
66 × 200 × 3
      ↓
Conv2D 24
      ↓
Conv2D 36
      ↓
Conv2D 48
      ↓
Conv2D 64
      ↓
Conv2D 64
      ↓
Dropout
      ↓
Flatten
      ↓
Dense 100
      ↓
Dense 50
      ↓
Dense 10
      ↓
Steering Angle
```

The model is trained using Mean Squared Error loss and the Adam optimizer.

## Image Preprocessing

The input images are processed before being passed to the neural network.

The preprocessing pipeline includes:

* Cropping irrelevant sky and car regions
* RGB to YUV conversion
* Gaussian blur
* Resizing to 200 × 66
* Pixel normalization

## Data Augmentation

To improve generalization, the training pipeline applies random augmentation.

### Horizontal Flip

Images can be horizontally flipped and the steering angle is inverted accordingly.

### Translation

Images can be shifted horizontally while adjusting the steering angle.

### Brightness

Random brightness changes are applied to simulate different lighting conditions.

### Camera Selection

During training, images are sampled from:

* Center camera
* Left camera
* Right camera

Side-camera steering correction is applied to compensate for the camera position.

## Steering Distribution Balancing

Driving datasets usually contain a large number of frames where the vehicle is travelling almost straight.

Without balancing, the model can become biased toward predicting steering values close to zero.

This project uses steering-angle bins and inverse-frequency weighting to give more importance to less frequent steering situations.

## Training

The model is trained using batches generated dynamically from the dataset.

Training includes:

* 80/20 training-validation split
* Random augmentation
* Balanced steering sampling
* Batch size of 32
* Adam optimizer
* MSE loss
* Learning-rate reduction
* Early stopping
* Best model checkpointing

The trained model is saved as:

```text
self_driving_model.keras
```

## Running the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Create the environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the trained model

Place the trained model in the project root:

```text
self_driving_model.keras
```

The trained model is intentionally excluded from the Git repository because of its size.

### 5. Start the driving server

```bash
python drive.py
```

The server will listen on:

```text
localhost:4567
```

### 6. Start the simulator

Launch the simulator and connect it to the running server.

Once connected, the simulator sends camera frames to the Python server.

The neural network predicts the steering angle and the control system calculates an appropriate throttle value.

## Project Structure

```text
self-driving-car/
│
├── drive.py
├── train.ipynb
├── requirements.txt
├── README.md
├── .gitignore
│
└── self_driving_model.keras
```

The following directories are intentionally excluded from Git:

```text
beta_simulator_windows/
IMG/
```

The `IMG` directory contains the collected training images and can become very large.

## Results

The trained model successfully controls the simulated vehicle using real-time camera input.

The model was evaluated primarily through simulator driving performance in addition to validation loss.

The best validation performance should not be considered the only measure of success because autonomous driving quality depends heavily on sequential behavior, steering stability, recovery ability, and dataset quality.

## Technologies

* Python
* TensorFlow
* Keras
* OpenCV
* NumPy
* Pandas
* Scikit-learn
* Flask
* Python Socket.IO
* Eventlet
* Driving Simulator

## Key Learning Outcomes

This project demonstrates practical experience with:

* Computer vision
* Convolutional neural networks
* Behavioral cloning
* Data augmentation
* Dataset balancing
* Regression
* Deep learning training pipelines
* Real-time inference
* Model deployment
* Simulator integration

## Future Improvements

Potential improvements include:

* More diverse driving data
* Additional recovery scenarios
* Better steering smoothing
* More advanced speed control
* Temporal models such as CNN-LSTM
* Road segmentation
* Lane detection
* Reinforcement learning based control
* Real-world camera testing

## Author

**Burhan Arshad**

BS Computer Science
Pakistan
