# Databricks notebook source
# MAGIC %md This notebook sets up the companion cluster(s) to run the solution accelerator. It also creates the Workflow to create a Workflow DAG and illustrate the order of execution. Feel free to interactively run notebooks with the cluster or to run the Workflow to see how this solution accelerator executes. Happy exploring!
# MAGIC 
# MAGIC The pipelines, workflows and clusters created in this script are user-specific, so you can alter the workflow and cluster via UI without affecting other users. Running this script again after modification resets them.
# MAGIC 
# MAGIC **Note**: If the job execution fails, please confirm that you have set up other environment dependencies as specified in the accelerator notebooks. Accelerators sometimes require the user to set up additional cloud infra or data access, for instance. 

# COMMAND ----------

# DBTITLE 0,Install util packages
# MAGIC %pip install git+https://github.com/databricks-academy/dbacademy-rest git+https://github.com/databricks-academy/dbacademy-gems git+https://github.com/databricks-industry-solutions/notebook-solution-companion

# COMMAND ----------

from solacc.companion import NotebookSolutionCompanion

# COMMAND ----------

cluster_json = {
    "num_workers": 8,
    "cluster_name": "oncology_cluster",
    "spark_version": "9.1.x-cpu-ml-scala2.12", # TODO: This needs to be updated to match JSL 4.1
    "spark_conf": {
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.kryoserializer.buffer.max": "2000M",
        "spark.databricks.delta.formatCheck.enabled": "false"
    },
    "node_type_id": "i3.xlarge",
    "driver_node_type_id": "i3.xlarge",
    "autotermination_minutes": 120
}

# COMMAND ----------

nsc = NotebookSolutionCompanion()
cluster_id = nsc.create_or_update_cluster_by_name(nsc.customize_cluster_json(cluster_json))

# COMMAND ----------

task_json = {'tasks': [{
    'task_key': 'setup_cluster',
    'depends_on': [],
    'existing_cluster_id': cluster_id,
    "notebook_task": {
        "notebook_path": "/Shared/John Snow Labs/Install JohnSnowLabs NLP",
        "source": "WORKSPACE"
        },
    'timeout_seconds': 86400}]
            }
nsc.submit_run(task_json)

# COMMAND ----------

job_json = {
        "timeout_seconds": 7200,
        "max_concurrent_runs": 1,
        "tags": {
            "usage": "solacc_testing",
            "group": "HLS"
        },
        "tasks": [
            {
                "existing_cluster_id": cluster_id,
                "notebook_task": {
                    "notebook_path": f"00-README"
                },
                "task_key": "oncology_01",
                "description": ""
            },
            {
                "existing_cluster_id": cluster_id,
                "libraries": [],
                "notebook_task": {
                    "notebook_path": f"01-entity-extraction"
                },
                "task_key": "oncology_02",
                "description": "",
                "depends_on": [
                    {
                        "task_key": "oncology_01"
                    }
                ]
            },
            {
                "existing_cluster_id": cluster_id,
                "libraries": [],
                "notebook_task": {
                    "notebook_path": f"02-oncology-analytics"
                },
                "task_key": "oncology_03",
                "description": "",
                "depends_on": [
                    {
                        "task_key": "oncology_02"
                    }
                ]
            },
            {
                "existing_cluster_id": cluster_id,
                "libraries": [],
                "notebook_task": {
                    "notebook_path": f"03-create-db"
                },
                "task_key": "oncology_04",
                "description": "",
                "depends_on": [
                    {
                        "task_key": "oncology_03"
                    }
                ]
            },
            {
                "existing_cluster_id": cluster_id,
                "libraries": [],
                "notebook_task": {
                    "notebook_path": f"04-config"
                },
                "task_key": "oncology_05",
                "description": "",
                "depends_on": [
                    {
                        "task_key": "oncology_04"
                    }
                ]
            }
        ]
    }

# COMMAND ----------

dbutils.widgets.dropdown("run_job", "False", ["True", "False"])
run_job = dbutils.widgets.get("run_job") == "True"
nsc.deploy_compute(job_json, run_job=run_job)

# COMMAND ----------



# COMMAND ----------


