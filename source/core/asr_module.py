#####
# This module will create the model
# We will train model on "minispeechcommands" dataset (1 second or less audio files - [yes, no, up, down, go, stop, left, and right])
# Therefore, to use this model -> audio clips must be 1 second
# The model can then be exported and used without having to train each time
#####

import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
import tensorflow_io as tfio

from keras import layers
from keras import models
from IPython import display

# Set the seed value for experiment reproducibility.
seed = 42
tf.random.set_seed(seed)
np.random.seed(seed)

# Import the mini speech commands dataset
DATASET_PATH = 'data/mini_speech_commands'      

data_dir = pathlib.Path(DATASET_PATH)   # We create a directory to store the audio clips as (directory where project exists)/data/mini_speech_commands
if not data_dir.exists():               # Only download the dataset if it doesn't already exist
  tf.keras.utils.get_file(              # This dataset is offered by Google under a CC BY license
      'mini_speech_commands.zip',
      origin="http://storage.googleapis.com/download.tensorflow.org/data/mini_speech_commands.zip",
      extract=True,
      cache_dir='.', cache_subdir='data')
  
# The audio clips are stored in 8 folders corresponding to each keyword
# We can grab the labels from the folder names
commands = np.array(tf.io.gfile.listdir(str(data_dir)))
commands = commands[(commands != 'README.md') & (commands != '.DS_Store')]
print()
print('Commands:', commands)

###
# Now that we have our dataset, we split into a training dataset and a validation data set
# The batch_size is a a number of samples processed before the model is updated
#       for more info on batch size: <https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/>
# The validation_split creates a validation data set that is 1/5 the size of the whole dataset
#       Our whole dataset = 8000 files -> 8000 * 0.2 = 1600 files for validation
# The seed is an optional random seed for shuffling and transformations
# The output_sequence_length pads the short ones to exactly 1 second (and would trim longer ones) so that they can be easily batched
#       The dataset consists of audio clips of 1 second or less at 16kHz
###     
train_ds, val_ds = tf.keras.utils.audio_dataset_from_directory(
    directory=data_dir,
    batch_size=64,
    validation_split=0.2,
    seed=0,
    output_sequence_length=16000,
    subset='both')

label_names = np.array(train_ds.class_names)
print()
print("label names:", label_names)

# The dataset now contains batches of audio clips and integer labels. The audio clips have a shape of (batch, samples, channels)
print()
print(train_ds.element_spec)

# This dataset only contains single channel audio, so use the tf.squeeze function to drop the extra axis
def squeeze(audio, labels):
  audio = tf.squeeze(audio, axis=-1)
  return audio, labels

train_ds = train_ds.map(squeeze, tf.data.AUTOTUNE) 
val_ds = val_ds.map(squeeze, tf.data.AUTOTUNE)

# The utils.audio_dataset_from_directory function only returns up to two splits
# It's a good idea to keep a test set separate from your validation set
# Ideally you'd keep it in a separate directory, but in this case you can use Dataset.shard to split the validation set into two halves
# Note that iterating over any shard will load all the data, and only keep its fraction.

# Split the validation dataset into two halves (800 files each)
# Test -> first half
# Validation -> second half
test_ds = val_ds.shard(num_shards=2, index=0)
val_ds = val_ds.shard(num_shards=2, index=1)
print()
for example_audio, example_labels in train_ds.take(1):  
  print(example_audio.shape)
  print(example_labels.shape)

# Plot some audio waveforms
label_names[[1, 1, 3, 0]]

plt.figure(figsize=(16, 10))            # Use matplotlib to plot audio waveforms
rows = 2                                # Create a figure with 4 plots
cols = 2
n = rows * cols
for i in range(n):
  plt.subplot(rows, cols, i+1)
  audio_signal = example_audio[i]
  plt.plot(audio_signal)
  plt.title(label_names[example_labels[i]])
  plt.yticks(np.arange(-1.2, 1.2, 0.2))
  plt.ylim([-1.1, 1.1])
#plt.show()

###
# Convert waveforms to spectrograms
# Transform the waveforms from the time-domain signals into the time-frequency-domain signals
#       by computing the short-time Fourier transform (STFT) to convert the waveforms to spectrograms
#       show frequency changes over time and can be represented as 2D images
# These spectrogram images will be fed into your neural network to train the model
###
# The waveforms need to be of the same length, so that when you convert them to spectrograms, the results have similar dimensions
#  This can be done by simply zero-padding the audio clips that are shorter than one second (using tf.zeros)
###
# When calling tf.signal.stft, choose the frame_length and frame_step parameters such that the generated spectrogram "image" is almost square
#       for more information on the STFT parameters choice, refer to this Coursera video on audio signal processing and STFT <https://www.coursera.org/lecture/audio-signal-processing/stft-2-tjEQe>
###
# The STFT produces an array of complex numbers representing magnitude and phase
#       However, we only use the magnitude, which you can derive by applying tf.abs on the output of tf.signal.stft
###
def get_spectrogram(waveform):
  # Convert the waveform to a spectrogram via a STFT.
  spectrogram = tf.signal.stft(
      waveform, frame_length=255, frame_step=128)
  # Obtain the magnitude of the STFT.
  spectrogram = tf.abs(spectrogram)
  # Add a `channels` dimension, so that the spectrogram can be used
  # as image-like input data with convolution layers (which expect
  # shape (`batch_size`, `height`, `width`, `channels`).
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

# Next, print the shapes of one example's tensorized waveform and the corresponding spectrogram
for i in range(4):
  label = label_names[example_labels[i]]
  waveform = example_audio[i]
  spectrogram = get_spectrogram(waveform)

  print()
  print('Label:', label)
  print('Waveform shape:', waveform.shape)
  print('Spectrogram shape:', spectrogram.shape)

# A function for displaying a spectrogram
def plot_spectrogram(spectrogram, ax):
  if len(spectrogram.shape) > 2:
    assert len(spectrogram.shape) == 3
    spectrogram = np.squeeze(spectrogram, axis=-1)
  # Convert the frequencies to log scale and transpose, so that the time is
  # represented on the x-axis (columns).
  # Add an epsilon to avoid taking a log of zero.
  log_spec = np.log(spectrogram.T + np.finfo(float).eps)
  height = log_spec.shape[0]
  width = log_spec.shape[1]
  X = np.linspace(0, np.size(spectrogram), num=width, dtype=int)
  Y = range(height)
  ax.pcolormesh(X, Y, log_spec)

# Plot the example's waveform over time and the corresponding spectrogram (frequencies over time):
fig, axes = plt.subplots(2, figsize=(12, 8))
timescale = np.arange(waveform.shape[0])
axes[0].plot(timescale, waveform.numpy())
axes[0].set_title('Waveform')
axes[0].set_xlim([0, 16000])

plot_spectrogram(spectrogram.numpy(), axes[1])
axes[1].set_title('Spectrogram')
plt.suptitle(label.title())
#plt.show()

# Now, create spectrogram datasets from the audio datasets
# a function to create spectrogram datasets
def make_spec_ds(ds):
  return ds.map(
      map_func=lambda audio,label: (get_spectrogram(audio), label),
      num_parallel_calls=tf.data.AUTOTUNE)

# Run the function on our datasets (training, validation, and test)
train_spectrogram_ds = make_spec_ds(train_ds)
val_spectrogram_ds = make_spec_ds(val_ds)
test_spectrogram_ds = make_spec_ds(test_ds)

# Examine the spectrograms for different examples of the dataset
for example_spectrograms, example_spect_labels in train_spectrogram_ds.take(1):
  break
rows = 3
cols = 3
n = rows*cols
fig, axes = plt.subplots(rows, cols, figsize=(16, 9))

for i in range(n):
    r = i // cols
    c = i % cols
    ax = axes[r][c]
    plot_spectrogram(example_spectrograms[i].numpy(), ax)
    ax.set_title(label_names[example_spect_labels[i].numpy()])

#plt.show()


# Now its time to build and train the model
# Add Dataset.cache and Dataset.prefetch operations to reduce read latency while training the model
train_spectrogram_ds = train_spectrogram_ds.cache().shuffle(10000).prefetch(tf.data.AUTOTUNE)
val_spectrogram_ds = val_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)
test_spectrogram_ds = test_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)

# Use a simple convolutional neural network (CNN), since you have transformed the audio files into spectrogram images
# The tf.keras.Sequential model will use the following Keras preprocessing layers
#       tf.keras.layers.Resizing: to downsample the input to enable the model to train faster
#       tf.keras.layers.Normalization: to normalize each pixel in the image based on its mean and standard deviation
# For the Normalization layer, its adapt method would first need to be called on the training data in order to compute aggregate statistics (the mean and the standard deviation)
input_shape = example_spectrograms.shape[1:]
print()
print('Input shape:', input_shape)      # The shape of the spectrograms which the model is trained on
num_labels = len(label_names)

# Instantiate the `tf.keras.layers.Normalization` layer.
norm_layer = layers.Normalization()
# Fit the state of the layer to the spectrograms
# with `Normalization.adapt`.
norm_layer.adapt(data=train_spectrogram_ds.map(map_func=lambda spec, label: spec))

model = models.Sequential([
    layers.Input(shape=input_shape),
    # Downsample the input.
    layers.Resizing(32, 32),
    # Normalize.
    norm_layer,
    layers.Conv2D(32, 3, activation='relu'),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_labels),
])

print()
print("Model Summary")
model.summary()

# Configure the Keras model with the Adam optimizer and the cross-entropy loss
# Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments
#       For more info on Adam optimizer: <https://keras.io/api/optimizers/adam/>
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'],
)

# Train the model over 7 epochs
EPOCHS = 7
history = model.fit(
    train_spectrogram_ds,
    validation_data=val_spectrogram_ds,
    epochs=EPOCHS,
    callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
)

# Plot the training and validation loss curves to check how the model has improved during training
metrics = history.history
plt.figure(figsize=(16,6))
plt.subplot(1,2,1)
plt.plot(history.epoch, metrics['loss'], metrics['val_loss'])
plt.legend(['loss', 'val_loss'])
plt.ylim([0, max(plt.ylim())])
plt.xlabel('Epoch')
plt.ylabel('Loss [CrossEntropy]')

plt.subplot(1,2,2)
plt.plot(history.epoch, 100*np.array(metrics['accuracy']), 100*np.array(metrics['val_accuracy']))
plt.legend(['accuracy', 'val_accuracy'])
plt.ylim([0, 100])
plt.xlabel('Epoch')
plt.ylabel('Accuracy [%]')

plt.show()

# Evaluate the model performance - Run the model on the test set and check the model's performance
model.evaluate(test_spectrogram_ds, return_dict=True)

# Display a confusion matrix
#       Use a confusion matrix to check how well the model did classifying each of the commands in the test set
# For more info on confusion matrix: <https://developers.google.com/machine-learning/glossary#confusion-matrix>
y_pred = model.predict(test_spectrogram_ds)
y_pred = tf.argmax(y_pred, axis=1)
y_true = tf.concat(list(test_spectrogram_ds.map(lambda s,lab: lab)), axis=0)
confusion_mtx = tf.math.confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx,
            xticklabels=label_names,
            yticklabels=label_names,
            annot=True, fmt='g')
plt.xlabel('Prediction')
plt.ylabel('Label')
plt.show()

# Run inference on an audio file
# Finally, verify the model's prediction output using an input audio file of someone saying "no"
x = data_dir/'no/01bb6a2a_nohash_0.wav'
x = tf.io.read_file(str(x))
x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
x = tf.squeeze(x, axis=-1)
waveform = x
x = get_spectrogram(x)
x = x[tf.newaxis,...]

prediction = model(x)
x_labels = ['down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']
plt.bar(x_labels, tf.nn.softmax(prediction[0]))
plt.title('No')
plt.show()

# Export the model with preprocessing
# The model's not very easy to use if you have to apply those preprocessing steps before passing data to the model for inference
# So build an end-to-end version
class ExportModel(tf.Module):
  def __init__(self, model):
    self.model = model

    # Accept either a string-filename or a batch of waveforms.
    # YOu could add additional signatures for a single wave, or a ragged-batch. 
    self.__call__.get_concrete_function(
        x=tf.TensorSpec(shape=(), dtype=tf.string))
    self.__call__.get_concrete_function(
       x=tf.TensorSpec(shape=[None, 16000], dtype=tf.float32))


  @tf.function
  def __call__(self, x):
    # If they pass a string, load the file and decode it. 
    if x.dtype == tf.string:
      x = tf.io.read_file(x)
      x, _ = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
      x = tf.squeeze(x, axis=-1)
      x = x[tf.newaxis, :]
    
    x = get_spectrogram(x)  
    result = self.model(x, training=False)
    
    class_ids = tf.argmax(result, axis=-1)
    class_names = tf.gather(label_names, class_ids)
    return {'predictions':result,
            'class_ids': class_ids,
            'class_names': class_names}
  
# Test run the "export" model
export = ExportModel(model)
export(tf.constant(str(data_dir/'no/01bb6a2a_nohash_0.wav')))

# Save and reload the model, the reloaded model gives identical output
tf.saved_model.save(export, "saved")
imported = tf.saved_model.load("saved")
imported(waveform[tf.newaxis, :])