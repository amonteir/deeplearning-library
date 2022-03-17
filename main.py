import numpy as np
import copy
import matplotlib.pyplot as plt
from testCases_v2 import *
from public_tests import *
import sklearn
import sklearn.datasets
import sklearn.linear_model
from planar_utils import plot_decision_boundary, sigmoid, load_planar_dataset, load_extra_datasets
from nn_1hl import NN1HiddenLayer


def layer_sizes(X, Y):
    """
    Arguments:
    X -- input dataset of shape (input size, number of examples)
    Y -- labels of shape (output size, number of examples)

    Returns:
    n_x -- the size of the input layer
    n_h -- the size of the hidden layer
    n_y -- the size of the output layer
    """
    n_x = X.shape[0]
    n_h = 4
    n_y = Y.shape[0]

    return n_x, n_h, n_y


def initialize_parameters(n_x, n_h, n_y):
    """
    Argument:
    n_x -- size of the input layer
    n_h -- size of the hidden layer
    n_y -- size of the output layer

    Returns:
    params -- python dictionary containing your parameters:
                    W1 -- weight matrix of shape (n_h, n_x)
                    b1 -- bias vector of shape (n_h, 1)
                    W2 -- weight matrix of shape (n_y, n_h)
                    b2 -- bias vector of shape (n_y, 1)
    """

    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters


def forward_propagation(X, parameters):
    """
    Argument:
    X -- input data of size (n_x, m)
    parameters -- python dictionary containing your parameters (output of initialization function)

    Returns:
    A2 -- The sigmoid output of the second activation
    cache -- a dictionary containing "Z1", "A1", "Z2" and "A2"
    """
    # Retrieve each parameter from the dictionary "parameters"
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    # YOUR CODE ENDS HERE

    # Implement Forward Propagation to calculate A2 (probabilities)
    Z1 = np.dot(W1, X) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)

    assert (A2.shape == (1, X.shape[1]))

    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}

    return A2, cache


def compute_cost(A2, Y):
    """
    Computes the cross-entropy cost given in equation (13)

    Arguments:
    A2 -- The sigmoid output of the second activation, of shape (1, number of examples)
    Y -- "true" labels vector of shape (1, number of examples)

    Returns:
    cost -- cross-entropy cost given equation (13)

    """

    m = Y.shape[1]  # number of examples

    # Compute the cross-entropy cost
    # (≈ 2 lines of code)
    # logprobs = ...
    # cost = ...
    # YOUR CODE STARTS HERE
    # logprobs =
    cost = (-1 / m) * np.sum(np.dot(np.log(A2), Y.T) + np.dot(np.log(1 - A2), (1 - Y.T)))
    # OR
    # logprobs = np.multiply(np.log(A2),Y) + np.multiply((1-Y),np.log(1-A2))
    # cost = (-1/m) * np.sum(logprobs)

    # YOUR CODE ENDS HERE

    cost = float(np.squeeze(cost))  # makes sure cost is the dimension we expect.
    # E.g., turns [[17]] into 17

    return cost


def backward_propagation(parameters, cache, X, Y):
    """
    Implement the backward propagation using the instructions above.

    Arguments:
    parameters -- python dictionary containing our parameters
    cache -- a dictionary containing "Z1", "A1", "Z2" and "A2".
    X -- input data of shape (2, number of examples)
    Y -- "true" labels vector of shape (1, number of examples)

    Returns:
    grads -- python dictionary containing your gradients with respect to different parameters
    """
    m = X.shape[1]

    # First, retrieve W1 and W2 from the dictionary "parameters".
    # (≈ 2 lines of code)
    # W1 = ...
    # W2 = ...
    # YOUR CODE STARTS HERE
    W1 = parameters["W1"]
    W2 = parameters["W2"]

    # YOUR CODE ENDS HERE

    # Retrieve also A1 and A2 from dictionary "cache".
    # (≈ 2 lines of code)
    # A1 = ...
    # A2 = ...
    # YOUR CODE STARTS HERE
    A1 = cache["A1"]
    A2 = cache["A2"]

    # YOUR CODE ENDS HERE

    # Backward propagation: calculate dW1, db1, dW2, db2.
    dZ2 = A2 - Y
    dW2 = (1 / m) * np.dot(dZ2, A1.T)
    db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = np.dot(W2.T, dZ2) * (1 - np.power(A1, 2))
    dW1 = (1 / m) * np.dot(dZ1, X.T)
    db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)

    # YOUR CODE ENDS HERE

    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}

    return grads


def update_parameters(parameters, grads, learning_rate=1.2):
    """
    Updates parameters using the gradient descent update rule given above

    Arguments:
    parameters -- python dictionary containing your parameters
    grads -- python dictionary containing your gradients

    Returns:
    parameters -- python dictionary containing your updated parameters
    """
    # Retrieve a copy of each parameter from the dictionary "parameters". Use copy.deepcopy(...) for W1 and W2
    # (≈ 4 lines of code)
    # W1 = ...
    # b1 = ...
    # W2 = ...
    # b2 = ...
    # YOUR CODE STARTS HERE
    W1 = copy.deepcopy(parameters["W1"])
    b1 = parameters["b1"]
    W2 = copy.deepcopy(parameters["W2"])
    b2 = parameters["b2"]

    # YOUR CODE ENDS HERE

    # Retrieve each gradient from the dictionary "grads"
    # (≈ 4 lines of code)
    # dW1 = ...
    # db1 = ...
    # dW2 = ...
    # db2 = ...
    # YOUR CODE STARTS HERE
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]

    # YOUR CODE ENDS HERE

    # Update rule for each parameter
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters


def nn_model(X, Y, n_h, num_iterations=10000, print_cost=False):
    """
    Arguments:
    X -- dataset of shape (2, number of examples)
    Y -- labels of shape (1, number of examples)
    n_h -- size of the hidden layer
    num_iterations -- Number of iterations in gradient descent loop
    print_cost -- if True, print the cost every 1000 iterations

    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    np.random.seed(3)
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[2]

    # Initialize parameters
    # (≈ 1 line of code)
    # parameters = ...
    # YOUR CODE STARTS HERE
    parameters = initialize_parameters(n_x, n_h, n_y)

    # YOUR CODE ENDS HERE

    # Loop (gradient descent)

    for i in range(0, num_iterations):

        # (≈ 4 lines of code)
        # Forward propagation. Inputs: "X, parameters". Outputs: "A2, cache".
        # A2, cache = ...
        A2, cache = forward_propagation(X, parameters)
        # Cost function. Inputs: "A2, Y". Outputs: "cost".
        # cost = ...
        cost = compute_cost(A2, Y)
        # Backpropagation. Inputs: "parameters, cache, X, Y". Outputs: "grads".
        # grads = ...
        grads = backward_propagation(parameters, cache, X, Y)
        # Gradient descent parameter update. Inputs: "parameters, grads". Outputs: "parameters".
        # parameters = ...
        parameters = update_parameters(parameters, grads, learning_rate=1.2)
        # YOUR CODE STARTS HERE

        # YOUR CODE ENDS HERE

        # Print the cost every 1000 iterations
        if print_cost and i % 1000 == 0:
            print("Cost after iteration %i: %f" % (i, cost))

    return parameters


def predict(parameters, X):
    """
    Using the learned parameters, predicts a class for each example in X

    Arguments:
    parameters -- python dictionary containing your parameters
    X -- input data of size (n_x, m)

    Returns
    predictions -- vector of predictions of our model (red: 0 / blue: 1)
    """

    # Computes probabilities using forward propagation, and classifies to 0/1 using 0.5 as the threshold.
    # (≈ 2 lines of code)
    # A2, cache = ...
    # predictions = ...
    # YOUR CODE STARTS HERE
    A2, cache = forward_propagation(X, parameters)
    predictions = (A2 > 0.5)

    # YOUR CODE ENDS HERE

    return predictions

def main():

    #  load the dataset
    X, Y = load_planar_dataset()
    plt.scatter(X[0, :], X[1, :], c=Y, s=40, cmap=plt.cm.Spectral)
    plt.show()

    """
    # Performance on other datasets
    # Datasets
    noisy_circles, noisy_moons, blobs, gaussian_quantiles, no_structure = load_extra_datasets()
    datasets = {"noisy_circles": noisy_circles,
                "noisy_moons": noisy_moons,
                "blobs": blobs,
                "gaussian_quantiles": gaussian_quantiles}
    ### START CODE HERE ### (choose your dataset)
    dataset = "gaussian_quantiles"
    ### END CODE HERE ###
    X, Y = datasets[dataset]
    X, Y = X.T, Y.reshape(1, Y.shape[0])
    # make blobs binary
    if dataset == "blobs":
        Y = Y % 2
    # Visualize the data
    plt.scatter(X[0, :], X[1, :], c=Y, s=40, cmap=plt.cm.Spectral)
    plt.show()
    """

    shape_X = X.shape
    shape_Y = Y.shape
    m = Y.size

    print('The shape of X is: ' + str(shape_X))
    print('The shape of Y is: ' + str(shape_Y))
    print(f'I have m = {m} training examples!')

    # Train the logistic regression classifier
    clf = sklearn.linear_model.LogisticRegressionCV()
    clf.fit(X.T, Y.T.ravel())

    # Plot the decision boundary for logistic regression
    plot_decision_boundary(lambda x: clf.predict(x), X, Y)
    plt.title("Logistic Regression")
    plt.show()

    # Print accuracy
    LR_predictions = clf.predict(X.T)
    print('Accuracy of logistic regression: %d ' % float(
        (np.dot(Y, LR_predictions) + np.dot(1 - Y, 1 - LR_predictions)) / float(Y.size) * 100) +
          '% ' + "(percentage of correctly labelled datapoints)")


    t_X, t_Y = layer_sizes_test_case()
    (n_x, n_h, n_y) = layer_sizes(t_X, t_Y)
    print("The size of the input layer is: n_x = " + str(n_x))
    print("The size of the hidden layer is: n_h = " + str(n_h))
    print("The size of the output layer is: n_y = " + str(n_y))
    # TEST
    # layer_sizes_test(layer_sizes)

    np.random.seed(2)
    n_x, n_h, n_y = initialize_parameters_test_case()
    parameters = initialize_parameters(n_x, n_h, n_y)

    print("W1 = " + str(parameters["W1"]))
    print("b1 = " + str(parameters["b1"]))
    print("W2 = " + str(parameters["W2"]))
    print("b2 = " + str(parameters["b2"]))
    # TEST
    # initialize_parameters_test(initialize_parameters)

    t_X, parameters = forward_propagation_test_case()
    A2, cache = forward_propagation(t_X, parameters)
    print("A2 = " + str(A2))
    # TEST
    # forward_propagation_test(forward_propagation)

    A2, t_Y = compute_cost_test_case()
    cost = compute_cost(A2, t_Y)
    print("cost = " + str(compute_cost(A2, t_Y)))
    # TEST
    #compute_cost_test(compute_cost)


    parameters, cache, t_X, t_Y = backward_propagation_test_case()
    grads = backward_propagation(parameters, cache, t_X, t_Y)
    print("dW1 = " + str(grads["dW1"]))
    print("db1 = " + str(grads["db1"]))
    print("dW2 = " + str(grads["dW2"]))
    print("db2 = " + str(grads["db2"]))
    # TEST
    #backward_propagation_test(backward_propagation)

    parameters, grads = update_parameters_test_case()
    parameters = update_parameters(parameters, grads)
    print("W1 = " + str(parameters["W1"]))
    print("b1 = " + str(parameters["b1"]))
    print("W2 = " + str(parameters["W2"]))
    print("b2 = " + str(parameters["b2"]))
    # TEST
    # update_parameters_test(update_parameters)

    t_X, t_Y = nn_model_test_case()
    parameters = nn_model(t_X, t_Y, 4, num_iterations=10000, print_cost=True)
    print("W1 = " + str(parameters["W1"]))
    print("b1 = " + str(parameters["b1"]))
    print("W2 = " + str(parameters["W2"]))
    print("b2 = " + str(parameters["b2"]))
    # TEST
    # nn_model_test(nn_model)

    parameters, t_X = predict_test_case()
    predictions = predict(parameters, t_X)
    print("Predictions: " + str(predictions))
    # TEST
    # predict_test(predict)

    # Build a model with a n_h-dimensional hidden layer
    parameters = nn_model(X, Y, n_h=4, num_iterations=10000, print_cost=True)
    # Plot the decision boundary
    plot_decision_boundary(lambda x: predict(parameters, x.T), X, Y)
    plt.title("Decision Boundary for hidden layer size " + str(4))
    # Print accuracy
    predictions = predict(parameters, X)
    print('Accuracy: %d' % float(
        (np.dot(Y, predictions.T) + np.dot(1 - Y, 1 - predictions.T)) / float(Y.size) * 100) + '%')
    plt.show()

    
    # Tuning hidden layer size
    plt.figure(figsize=(16, 32))
    hidden_layer_sizes = [1, 2, 3, 4, 5, 20, 50]
    for i, n_h in enumerate(hidden_layer_sizes):
        plt.subplot(5, 2, i + 1)
        plt.title('Hidden Layer of size %d' % n_h)
        parameters = nn_model(X, Y, n_h, num_iterations=5000)
        plot_decision_boundary(lambda x: predict(parameters, x.T), X, Y)
        predictions = predict(parameters, X)
        accuracy = float((np.dot(Y, predictions.T) + np.dot(1 - Y, 1 - predictions.T)) / float(Y.size) * 100)
        print("Accuracy for {} hidden units: {} %".format(n_h, accuracy))
    plt.show()



if __name__ == '__main__':
    main()
    print("\nProgram finished. Goodbye!")


