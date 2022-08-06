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

hls_jsl_cluster = dbutils.secrets.get("solution-accelerator-cicd", "hls_jsl_cluster") # This cluster is available in Databricks' internal environment only. Reach out to Databricks and JSL sales engineering and get a cluster set up to run these accelerators in your own environment
job_json = {
        "timeout_seconds": 7200,
        "name": job_name,
        "max_concurrent_runs": 1,
        "tags": {
            "usage": "solacc_testing",
            "group": "HLS"
        },
        "tasks": [
            {
                "existing_cluster_id": hls_jsl_cluster,
                "notebook_task": {
                    "notebook_path": f"00-README"
                },
                "task_key": "oncology_01",
                "description": ""
            },
            {
                "existing_cluster_id": hls_jsl_cluster,
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
                "existing_cluster_id": hls_jsl_cluster,
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
                "existing_cluster_id": hls_jsl_cluster,
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
                "existing_cluster_id": hls_jsl_cluster,
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
NotebookSolutionCompanion().deploy_compute(job_json, run_job=run_job)

# COMMAND ----------



# COMMAND ----------


