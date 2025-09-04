# main.py
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist

os.makedirs("../outputs", exist_ok=True)

# ----------------------- CNN -----------------------

def preprocess_cnn_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    X_train = np.expand_dims(X_train, -1)
    X_test = np.expand_dims(X_test, -1)
    return X_train, X_test, y_train, y_test

def create_cnn(kernel_size):
    model = Sequential([
        Input(shape=(28, 28, 1)),
        Conv2D(32, kernel_size=kernel_size, activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def run_cnn_analysis():
    X_train, X_test, y_train, y_test = preprocess_cnn_data()
    kernel_sizes = [(3, 3), (5, 5), (7, 7)]
    for kernel in kernel_sizes:
        train_scores, val_scores = [], []
        for i in range(5):
            model = create_cnn(kernel)
            history = model.fit(X_train, y_train, epochs=10, batch_size=64, 
                                validation_data=(X_test, y_test), verbose=0)
            train_acc = history.history['accuracy'][-1]
            val_acc = history.history['val_accuracy'][-1]
            train_scores.append(train_acc)
            val_scores.append(val_acc)

            # 判断是否过拟合
            if train_acc - val_acc > 0.1:
                plt.figure()
                plt.plot(history.history['accuracy'], label='Train')
                plt.plot(history.history['val_accuracy'], label='Validation')
                plt.title(f'Overfitting Detected - CNN Kernel {kernel}')
                plt.xlabel('Epoch')
                plt.ylabel('Accuracy')
                plt.legend()
                plt.savefig(f'../outputs/cnn_kernel_{kernel}_run_{i}.png')
                plt.close()

        print(f"CNN Kernel {kernel}:")
        print(f"  Train Accuracy Mean: {np.mean(train_scores):.4f}, Std: {np.std(train_scores):.4f}")
        print(f"  Val Accuracy Mean:   {np.mean(val_scores):.4f}, Std: {np.std(val_scores):.4f}")
        print()

# ----------------------- Neural Network -----------------------

def preprocess_nn_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.reshape(-1, 784).astype('float32') / 255.0
    X_test = X_test.reshape(-1, 784).astype('float32') / 255.0
    return X_train, X_test, y_train, y_test

def create_nn(learning_rate):
    model = Sequential([
        Input(shape=(784,)),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=learning_rate), 
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def run_nn_analysis():
    X_train, X_test, y_train, y_test = preprocess_nn_data()
    learning_rates = [0.001, 0.01, 0.1]
    for lr in learning_rates:
        train_scores, val_scores = [], []
        for i in range(5):
            model = create_nn(lr)
            history = model.fit(X_train, y_train, epochs=10, batch_size=64,
                                validation_data=(X_test, y_test), verbose=0)
            train_acc = history.history['accuracy'][-1]
            val_acc = history.history['val_accuracy'][-1]
            train_scores.append(train_acc)
            val_scores.append(val_acc)

            if train_acc - val_acc > 0.1:
                plt.figure()
                plt.plot(history.history['accuracy'], label='Train')
                plt.plot(history.history['val_accuracy'], label='Validation')
                plt.title(f'Overfitting Detected - NN LR {lr}')
                plt.xlabel('Epoch')
                plt.ylabel('Accuracy')
                plt.legend()
                plt.savefig(f'../outputs/nn_lr_{lr}_run_{i}.png')
                plt.close()

        print(f"NN Learning Rate {lr}:")
        print(f"  Train Accuracy Mean: {np.mean(train_scores):.4f}, Std: {np.std(train_scores):.4f}")
        print(f"  Val Accuracy Mean:   {np.mean(val_scores):.4f}, Std: {np.std(val_scores):.4f}")
        print()

# ----------------------- SVM -----------------------

def run_svm_analysis():
    digits = datasets.load_digits()
    X = StandardScaler().fit_transform(digits.data)
    y = digits.target
    kernels = ['linear', 'rbf', 'poly']

    for kernel in kernels:
        train_scores, val_scores = [], []
        for i in range(5):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
            clf = svm.SVC(kernel=kernel)
            clf.fit(X_train, y_train)
            train_acc = accuracy_score(y_train, clf.predict(X_train))
            val_acc = accuracy_score(y_test, clf.predict(X_test))
            train_scores.append(train_acc)
            val_scores.append(val_acc)

            if train_acc - val_acc > 0.1:
                plt.figure()
                plt.bar(['Train', 'Validation'], [train_acc, val_acc])
                plt.title(f'Overfitting Detected - SVM Kernel {kernel}')
                plt.ylabel('Accuracy')
                plt.savefig(f'../outputs/svm_kernel_{kernel}_run_{i}.png')
                plt.close()

        print(f"SVM Kernel {kernel}:")
        print(f"  Train Accuracy Mean: {np.mean(train_scores):.4f}, Std: {np.std(train_scores):.4f}")
        print(f"  Val Accuracy Mean:   {np.mean(val_scores):.4f}, Std: {np.std(val_scores):.4f}")
        print()

# ----------------------- MAIN ENTRY -----------------------

if __name__ == "__main__":
    print("Running CNN Analysis...")
    run_cnn_analysis()
    print("\nRunning Neural Network Analysis...")
    run_nn_analysis()
    print("\nRunning SVM Analysis...")
    run_svm_analysis()
