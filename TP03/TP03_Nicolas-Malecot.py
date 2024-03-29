{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn import svm\n",
    "from sklearn.svm import SVC\n",
    "from sklearn.datasets import make_blobs, make_circles\n",
    "from sklearn.inspection import DecisionBoundaryDisplay\n",
    "from sklearn.utils import shuffle\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.model_selection import cross_validate, train_test_split, GridSearchCV\n",
    "from scipy.stats import multivariate_normal\n",
    "\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "\n",
    "%matplotlib inline\n",
    "plt.style.use('ggplot')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# TP: Support Vector Machine (SVM)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Preliminary questions"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**1)** Show that the primal problem solved by the SVM can be rewritten as follows :\n",
    "\n",
    "$$ \\text{argmin}_{\\mathbf{w} \\in \\mathcal{H}, w_0 \\in \\mathbb{R} } \\left( \\frac{1}{2}||\\mathbf{w}||^2 + C \\sum_{i=1}^n [ 1 - y_i ( \\langle \\mathbf{w}, \\Phi(\\mathbf{x_i}) \\rangle + w_0 )]_+ \\right) $$"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<div class='alert alert-block alert-warning'>\n",
    "            Answer:</div>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**2)** Explain the sentence : \"an SVM minimizes the classification error using a convex upper bound\". The function $x \\rightarrow [1 - x]_+ = \\text{max}(0, 1-x)$ is called *Hinge* (*charnière* en français). Explain the difference between the pivotal loss and the loss of binary classification."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<div class='alert alert-block alert-warning'>\n",
    "            Answer:</div>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Example of using the SVC class from scikit-learn"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#  Data Generation\n",
    "\n",
    "def rand_gauss(n=100, mu=[1, 1], sigmas=[0.1, 0.1]):\n",
    "    \"\"\" Sample n points from a Gaussian variable with center mu,\n",
    "    and std deviation sigma\n",
    "    \"\"\"\n",
    "    d = len(mu)\n",
    "    res = np.random.randn(n, d)\n",
    "    return np.array(res * sigmas + mu)\n",
    "\n",
    "\n",
    "def rand_bi_gauss(n1=100, n2=100, mu1=[1, 1], mu2=[-1, -1], sigmas1=[0.1, 0.1],\n",
    "                  sigmas2=[0.1, 0.1]):\n",
    "    \"\"\" Sample n1 and n2 points from two Gaussian variables centered in mu1,\n",
    "    mu2, with respective std deviations sigma1 and sigma2\n",
    "    \"\"\"\n",
    "    ex1 = rand_gauss(n1, mu1, sigmas1)\n",
    "    ex2 = rand_gauss(n2, mu2, sigmas2)\n",
    "    y = np.hstack([np.ones(n1), -1 * np.ones(n2)])\n",
    "    X = np.vstack([ex1, ex2])\n",
    "    ind = np.random.permutation(n1 + n2)\n",
    "    return X[ind, :], y[ind]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This is an example of using SVC for data generated with the above function\n",
    "n1 = 20\n",
    "n2 = 20\n",
    "mu1 = [1., 1.]\n",
    "mu2 = [-1., -1.]\n",
    "sigma1 = [0.9, 0.9]\n",
    "sigma2 = [0.9, 0.9]\n",
    "X1, y1 = rand_bi_gauss(n1, n2, mu1, mu2, sigma1, sigma2)\n",
    "\n",
    "X_train = X1[::2]\n",
    "Y_train = y1[::2].astype(int)\n",
    "X_test = X1[1::2]\n",
    "Y_test = y1[1::2].astype(int)\n",
    "\n",
    "# fit the model with linear kernel\n",
    "clf = SVC(kernel='linear')\n",
    "clf.fit(X_train, Y_train)\n",
    "\n",
    "# predict labels for the test data base\n",
    "y_pred = clf.predict(X_test)\n",
    "\n",
    "# check your score\n",
    "score_train = clf.score(X_train, Y_train)\n",
    "score_test = clf.score(X_test, Y_test)\n",
    "print('Training score : %s' % score_train)\n",
    "print('Testing score : %s' % score_test)\n",
    "\n",
    "# display the points\n",
    "plt.figure(1, figsize=(5, 5))\n",
    "ax = plt.gca()\n",
    "DecisionBoundaryDisplay.from_estimator(\n",
    "    clf,\n",
    "    X1,\n",
    "    plot_method=\"contour\",\n",
    "    colors=\"k\",\n",
    "    levels=[0],\n",
    "    alpha=0.5,\n",
    "    ax=ax,\n",
    ")\n",
    "ax.scatter(X_train[:, 0], X_train[:, 1], c=Y_train)\n",
    "ax.scatter(X_test[:, 0], X_test[:, 1], c=Y_test, cmap=plt.cm.Paired)\n",
    "plt.title('First data set')\n",
    "plt.axis('equal')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Linear SVM"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**3)** Draw a i.i.d. sample from a mixture of two Gaussian distributions : each class is a Gaussian with specific parameters. This time, use the function ```make_blobs``` available in ```sklearn.datasets``` library. Reserve 75% of the data for training and 25% for the test data.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create two centers for the two distributions \n",
    "centers = ...\n",
    "\n",
    "# Use make_blobs to generate the two dimensions points from the two centers\n",
    "X, y = make_blobs(...)\n",
    "\n",
    "# Plot the points \n",
    "pos = np.where(y == 1)[0]\n",
    "neg = np.where(y == 0)[0]\n",
    "plt.scatter(X[pos,0], X[pos,1], c='r')\n",
    "plt.scatter(X[neg,0], X[neg,1], c='b')\n",
    "plt.axis('equal')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use sklearn's train_test_split to divide up data\n",
    "X_train, X_test, y_train, y_test = ..."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**4)** Since the probability distributions are known, numerically estimate the Bayes risk. \n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from scipy.stats import multivariate_normal\n",
    "# Do a Monte-Carlo estimation of the Bayes Risk (given the gaussian distributions you used to generate data)\n",
    "# You need to use the imported class from scipy to generate a large number of samples which you will use \n",
    "# to approximate the integral of the Bayes risk\n",
    "n_mc = ... # Repeat this n_mc times - enough to approximate \n",
    "expectation = 0\n",
    "for i in range(n_mc):\n",
    "    rand = # Random binary choice: will the point be generated from the first or second gaussian ? \n",
    "    if ...:\n",
    "        # First case: y = 0\n",
    "        x = np.random.multivariate_normal(...)\n",
    "    else:\n",
    "        # Second case: y = 1\n",
    "        x = np.random.multivariate_normal(...)\n",
    "\n",
    "    # You have to compute the conditional posterior probability of x given the 2 gaussians \n",
    "    # Use the multivariate_normal.pdf() method !    \n",
    "    p1 = multivariate_normal.pdf(...)\n",
    "    p2 = multivariate_normal.pdf(...)\n",
    "    # Compute the risk from these and add it to the total\n",
    "    ...\n",
    "    expectation += ...\n",
    "\n",
    "expectation /= n_mc\n",
    "\n",
    "print(f'Estimated Bayes risk: {np.around(expectation, 3)}')\n",
    "print(f'Estimated Bayes accuracy: {1 - np.around(expectation, 3)}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**5)** Draw the decision boundary $H$ induced by SVM as well as the hyperplanes $H_1$ and $H_{−1}$. Vary the parameter C to see its impact on the number of support vectors. We can use the code in the following example: https://scikit-learn.org/stable/auto_examples/svm/plot_separating_hyperplane.html.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a linear SVM and train it on the training data\n",
    "clf = ...\n",
    "...\n",
    "print(f'Train/Test scores: {clf.score(X_train, y_train)}/{clf.score(X_test, y_test)}')\n",
    "\n",
    "# Plot the data\n",
    "plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=30, cmap=plt.cm.Paired)\n",
    "\n",
    "# plot the decision function\n",
    "ax = plt.gca()\n",
    "xlim = ax.get_xlim()\n",
    "ylim = ax.get_ylim()\n",
    "\n",
    "# create grid to evaluate model\n",
    "xx = np.linspace(xlim[0], xlim[1], 30)\n",
    "yy = np.linspace(ylim[0], ylim[1], 30)\n",
    "YY, XX = np.meshgrid(yy, xx)\n",
    "xy = np.vstack([XX.ravel(), YY.ravel()]).T\n",
    "Z = clf.decision_function(xy).reshape(XX.shape)\n",
    "\n",
    "# plot decision boundary and margins\n",
    "ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,\n",
    "           linestyles=['--', '-', '--'])\n",
    "# plot support vectors\n",
    "ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100,\n",
    "           linewidth=1, facecolors='none', edgecolors='k')\n",
    "\n",
    "plt.axis('equal')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**6)** Define the Gaussian classes such that the two distributions overlap. Draw an i.i.d. sample from the joint probability distribution. Apply a 5-fold Cross-Validation (for example, using the function ```GridSearchCV```) to find the optimal parameter $C∗$ to classify this new dataset using a linear kernel.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Generate data and verify graphically that the two classes overlap\n",
    "# Re-use the code from question 3 and 5\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find the best working C with a 5-fold cross-validation\n",
    "# Look into a bunch of values for C\n",
    "parameters = {'kernel': ['linear'], 'C': list(np.logspace(-3, 3, 5))}\n",
    "# Use these parameters + a SVM models with GridSearchCV (look at the documentation !)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**7)** Show how tuning SVM hyperparameters on training data, for example by taking a Gaussian kernel (the parameters are therefore $\\gamma$ and $C$), can lead to overfitting.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "gammas = [0.1, 1, 10, 100]\n",
    "# Create a gaussian svm and vary the parameter of the kernel, check the difference between training and testing scores\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Non linear SVM"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**8)** Define a new binary nonlinear classification problem : for instance, define one class as a Gaussian surrounded by the other chosen as a circle class, or choose the second class as a mixture of two Gaussian in such way that the separation problem is nonlinear. Generate a non-linearly separable dataset (we could for example use the function ```make_blobs``` available in ```sklearn.datasetslibrary``` ).\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use make blobs with three centers which are aligned, for example\n",
    "# Class 0 - Class 1 - Class 0 \n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**9)** Use an SVM with a linear kernel then a Gaussian (with well-adapted parameters, that you can obtain using, again, ```GridSearchCV```) then plot the decision boundaries of these algorithms on separate graphs.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the code of question 6 again\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Learning curve\n",
    "\n",
    "**10)** Draw the learning curve of the algorithm : with fixed hyper-parameters and a fixed test set, calculate the training and test errors by using training sub-sets of training data of various sizes (drawn randomly). For each size, repeat the experiment a large number of times to average the performance. \n",
    "Plot the train and test error based on the size of the train set subset. Estimate and display the accuracy of the Bayes predictor on the same graph. Comment.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Total number of training samples\n",
    "n_tr = len(X_train)\n",
    "\n",
    "# Repeat the experiment for all these training sizes\n",
    "sizes = np.arange(20, n_tr, 5)\n",
    "\n",
    "# Repeat each experiment this many times \n",
    "n_m = 20  \n",
    "\n",
    "# Store scores in these lists\n",
    "scores_train = []\n",
    "scores_test = []\n",
    "\n",
    "# Main loop: varying the training size\n",
    "for size in sizes:\n",
    "    score_train = 0\n",
    "    score_test = 0\n",
    "    # Second loop: repeating the experiment for each size\n",
    "    for i in range(n_m):\n",
    "        # Create a SVM, keeping the same parameters\n",
    "        ...\n",
    "        # For each experiment, draw a subset of the training data of the appropriate size\n",
    "        idx = np.random.choice(range(n_tr), size=size)\n",
    "        X_train_reduced = X_train[idx, :]\n",
    "        y_train_reduced = y_train[idx]\n",
    "        \n",
    "        # Fit the classifier and compute the scores on training and test data\n",
    "        ...\n",
    "    # Add the average of the scores to the lists\n",
    "    ...\n",
    "\n",
    "# Plot the results\n",
    "plt.plot(sizes, scores_train, label='Train')\n",
    "plt.plot(sizes, scores_test, label='Test')\n",
    "plt.xlabel('Quantity of training data')\n",
    "plt.ylabel('Accuracy')\n",
    "\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Do a Monte-Carlo estimation of the Bayes Risk (given the gaussian distributions you used to generate data)\n",
    "# This is the same computation than in question 4). \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add this estimation to the plot of train/test error\n",
    "# This is constant: you should add a horizontal line to your graph\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<div class='alert alert-block alert-warning'>\n",
    "            Answer:</div>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Error versus complexity\n",
    "\n",
    "**11)** Add noise to the dataset by randomly modifying the labels of some training data. Then, draw the complexity curves of the algorithm : with set train and test set, draw the train and test error as a function of the complexity (i.e. as a function of the value of the hyper-parameter controlling the complexity, or the number of support vector). Comment.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Modify the class of some data points randomly\n",
    "n_noise = 50\n",
    "n_tr = len(y_train)\n",
    "idx = np.random.choice(range(n_tr), n_noise)\n",
    "y_train[idx] = 1 - y_train[idx]\n",
    "\n",
    "pos = np.where(y_train == 1)[0]\n",
    "neg = np.where(y_train == 0)[0]\n",
    "\n",
    "# Visualise the data\n",
    "plt.scatter(X_train[pos,0], X_train[pos,1], c='r')\n",
    "plt.scatter(X_train[neg,0], X_train[neg,1], c='b')\n",
    "plt.axis('equal')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Vary the appropriate parameter and plot the training/testing results\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "scrolled": true
   },
   "source": [
    "<div class='alert alert-block alert-warning'>\n",
    "            Answer:</div>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Bonus : Application to face classification"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Code for downloading and organizing the data:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "###############################################################################\n",
    "#               Face Recognition Task\n",
    "###############################################################################\n",
    "\"\"\"\n",
    "The dataset used in this example is a preprocessed excerpt\n",
    "of the \"Labeled Faces in the Wild\", aka LFW_:\n",
    "\n",
    "  http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz (233MB)\n",
    "\n",
    "  _LFW: http://vis-www.cs.umass.edu/lfw/\n",
    "\n",
    "\"\"\"\n",
    "\n",
    "from time import time\n",
    "import pylab as pl\n",
    "from sklearn.datasets import fetch_lfw_people\n",
    "\n",
    "\n",
    "####################################################################\n",
    "# Download the data (if not already on disk); load it as numpy arrays\n",
    "lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4,\n",
    "                              color=True, funneled=False, slice_=None,\n",
    "                              download_if_missing=True)\n",
    "# data_home='.'\n",
    "\n",
    "# introspect the images arrays to find the shapes (for plotting)\n",
    "images = lfw_people.images\n",
    "n_samples, h, w, n_colors = images.shape\n",
    "\n",
    "# the label to predict is the id of the person\n",
    "target_names = lfw_people.target_names.tolist()\n",
    "\n",
    "####################################################################\n",
    "# Pick a pair to classify such as\n",
    "names = ['Tony Blair', 'Colin Powell']\n",
    "# names = ['Donald Rumsfeld', 'Colin Powell']\n",
    "\n",
    "idx0 = (lfw_people.target == target_names.index(names[0]))\n",
    "idx1 = (lfw_people.target == target_names.index(names[1]))\n",
    "images = np.r_[images[idx0], images[idx1]]\n",
    "n_samples = images.shape[0]\n",
    "y = np.r_[np.zeros(np.sum(idx0)), np.ones(np.sum(idx1))].astype(np.int)\n",
    "\n",
    "####################################################################\n",
    "# Extract features\n",
    "\n",
    "# features using only illuminations\n",
    "X = (np.mean(images, axis=3)).reshape(n_samples, -1)\n",
    "\n",
    "# # or compute features using colors (3 times more features)\n",
    "# X = images.copy().reshape(n_samples, -1)\n",
    "\n",
    "# Scale features\n",
    "X -= np.mean(X, axis=0)\n",
    "X /= np.std(X, axis=0)\n",
    "\n",
    "####################################################################\n",
    "# Split data into a half training and half test set\n",
    "# X_train, X_test, y_train, y_test, images_train, images_test = \\\n",
    "#    train_test_split(X, y, images, test_size=0.5, random_state=0)\n",
    "# X_train, X_test, y_train, y_test = \\\n",
    "#    train_test_split(X, y, test_size=0.5, random_state=0)\n",
    "\n",
    "indices = np.random.permutation(X.shape[0])\n",
    "train_idx, test_idx = indices[:int(X.shape[0] / 2)], indices[int(X.shape[0] / 2):]\n",
    "X_train, X_test = X[train_idx, :], X[test_idx, :]\n",
    "y_train, y_test = y[train_idx], y[test_idx]\n",
    "images_train, images_test = images[train_idx, :, :, :], images[test_idx, :, :, :]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**12)** By modifying the followind code, show the influence of the regularization parameter. For example, the prediction error can be displayed as a function of $C$ on a logarithmic scale between $1e5$ and $1e-5$.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "####################################################################\n",
    "# Quantitative evaluation of the model quality on the test set\n",
    "print(\"Fitting the classifier to the training set\")\n",
    "t0 = time()\n",
    "\n",
    "# Add the regularization parameter and test for a range of values\n",
    "# Plot the performances\n",
    "clf = svm.SVC(kernel=\"linear\")\n",
    "clf.fit(X_train, y_train)\n",
    "score = clf.score(X_test, y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"Predicting the people names on the testing set\")\n",
    "t0 = time()\n",
    "\n",
    "# Predict labels for the X_test images with the best regularization parameter you obtained\n",
    "y_pred = clf.predict(X_test)\n",
    "\n",
    "print(\"done in %0.3fs\" % (time() - t0))\n",
    "print(\"Chance level : %s\" % max(np.mean(y), 1. - np.mean(y)))\n",
    "print(\"Accuracy : %s\" % clf.score(X_test, y_test))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "####################################################################\n",
    "# Qualitative evaluation of the predictions using matplotlib\n",
    "\n",
    "def plot_gallery(images, titles, n_row=3, n_col=4):\n",
    "    \"\"\"Helper function to plot a gallery of portraits\"\"\"\n",
    "    pl.figure(figsize=(1.8 * n_col, 2.4 * n_row))\n",
    "    pl.subplots_adjust(bottom=0, left=.01, right=.99, top=.90,\n",
    "                       hspace=.35)\n",
    "    for i in range(n_row * n_col):\n",
    "        pl.subplot(n_row, n_col, i + 1)\n",
    "        pl.imshow(images[i])\n",
    "        pl.title(titles[i], size=12)\n",
    "        pl.xticks(())\n",
    "        pl.yticks(())\n",
    "\n",
    "\n",
    "def title(y_pred, y_test, names):\n",
    "    pred_name = names[int(y_pred)].rsplit(' ', 1)[-1]\n",
    "    true_name = names[int(y_test)].rsplit(' ', 1)[-1]\n",
    "    return 'predicted: %s\\ntrue:      %s' % (pred_name, true_name)\n",
    "\n",
    "# This will just show some examples with their associated prediction - nothing to change\n",
    "prediction_titles = [title(y_pred[i], y_test[i], names)\n",
    "                     for i in range(y_pred.shape[0])]\n",
    "\n",
    "plot_gallery(images_test, prediction_titles)\n",
    "pl.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**13)** By adding nuisance variables, thus increasing the number of variables to the number of learning\n",
    "points fixed, show that performance drops.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add a number of nuisance variable to the existing data points, by generating randomly their values\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**14)** What is the effect of choosing a non-linear RBF kernel on prediction ? You will be able to improve the prediction with a reduction of dimension based on the object ```sklearn.decomposition.RandomizedPCA```.\n",
    "\n",
    "<div class='alert alert-block alert-info'>\n",
    "            Code:</div>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Apply the SVM with the chosen kernel after dimension reduction by PCA\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}