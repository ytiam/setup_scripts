from pandas import read_csv
import logging
from pandas.plotting import scatter_matrix
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split


# Load dataset(t1)
def read_data(**kwargs):
    '''
    Do your data reading stuffs here
    '''
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = read_csv(url, names=names)
    logging.info('Data Reading Successfully DOne')
    return dataset


# Data Report(t2)
def data_report(**kwargs):
    '''
    Generate some data reports here
    '''
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='read_table')
    data_shape = (df.shape[0], df.shape[1])
    logging.info('Number of rows: %s, Number of coulums: %s' % data_shape)
    class_dist = df.groupby('class').size()
    logging.info('Target Distribution: %s' % (str(class_dist)))
    number_of_nulls = df.isnull().sum()
    logging.info('Number of nulls per columns: %s' % (str(number_of_nulls)))
    return df


# Plot Variable Distributions(t3)
def plot_var_distributions(**kwargs):
    '''
    Plot some variable distributions here
    '''
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='data_report')
    ax = df.hist()
    fig = ax[0][0].get_figure()
    fig_path = kwargs['fig_path']
    fig.savefig(fig_path + '/df_all_var_hist.jpg')
    logging.info('Data Variable Histograms Saved Under %s' % fig_path)
    ax1 = scatter_matrix(df)
    fig1 = ax1[0][0].get_figure()
    fig1.savefig(fig_path + '/df_scatter_plot.jpg')
    logging.info('Data Variable Scatterplots Saved Under %s' % fig_path)
    return df


# Make train_test data(t4)
def make_train_test(**kwargs):
    '''
    Do train test related data steps here
    '''
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='data_report')
    array = df.values
    X = array[:, 0:4]
    y = array[:, 4]
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)
    logging.info('train_shape: %d , validation_shape: %d' % (len(X_train), len(X_validation)))
    return [X_train, X_validation, Y_train, Y_validation]
