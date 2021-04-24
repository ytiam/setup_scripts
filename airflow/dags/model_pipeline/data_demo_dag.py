# Building the DAG using the functions from data_process and model module
import datetime as dt
from airflow import DAG
from airflow.operators import PythonOperator
from model_pipeline.data_process import *
from model_pipeline.model import run_model

fig_path = '_give_the_path_where_you_want_to_save_the_images_'

# Declare Default arguments for the DAG
default_args = {
    'owner': 'atanu',
    'depends_on_past': False,
    'start_date': dt.datetime.strptime('2020-03-24T00:00:00', '%Y-%m-%dT%H:%M:%S'),
    'provide_context': True
}

# creating a new dag
dag = DAG('dataflow_process_dag', default_args=default_args, schedule_interval='0 0 * * 2', max_active_runs=1)

# Integrating different operatortasks in airflow dag
# Integrating read_data operator in airflow dag
read_table = PythonOperator(task_id='read_table', python_callable=read_data,
                            op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating data_report operator in airflow dag
data_report = PythonOperator(task_id='data_report', python_callable=data_report,
                             op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating plots operator in airflow dag
plots = PythonOperator(task_id='var_dist_plots', python_callable=plot_var_distributions,
                       op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating train_test operator in airflow dag
train_test = PythonOperator(task_id='train_test', python_callable=make_train_test,
                            op_kwargs={'fig_path': fig_path}, dag=dag)
# Integrating model_run operator in airflow dag
model_run = PythonOperator(task_id='model_run', python_callable=run_model,
                           op_kwargs={'fig_path': fig_path}, dag=dag)

# Set the task sequence
read_table.set_downstream(data_report)
data_report.set_downstream([plots, train_test])
train_test.set_downstream(model_run)
