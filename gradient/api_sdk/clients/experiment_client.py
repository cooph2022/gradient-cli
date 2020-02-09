from .base_client import BaseClient
from .. import repositories, models, constants, utils
from ..sdk_exceptions import ResourceCreatingDataError


class ExperimentsClient(utils.ExperimentsClientHelpersMixin, BaseClient):
    def create_single_node(
            self,
            project_id,
            machine_type,
            command,
            ports=None,
            name=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
            registry_url=None,
            use_vpc=False,
    ):
        """
        Create single node experiment

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str machine_type: Machine type [required]
        :param str command: Container entrypoint command  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str container: Container (dockerfile) [required]
        :param str container_user: Container user for running the specified command in the container. If no containerUser is specified, the user will default to 'root' in the container.
        :param str registry_username: Registry username for accessing private docker registry container if necessary
        :param str registry_password: Registry password for accessing private docker registry container if necessary
        :param str registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
            registry_url=registry_url,
        )

        repository = repositories.CreateSingleNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def create_multi_node(
            self,
            project_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            name=None,
            experiment_type_id=constants.ExperimentType.GRPC_MULTI_NODE,
            ports=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            parameter_server_container_user=None,
            parameter_server_registry_username=None,
            parameter_server_registry_password=None,
            parameter_server_registry_url=None,
            use_vpc=False,
    ):
        """
        Create multinode experiment

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str parameter_server_container: Parameter server container  [required]
        :param str parameter_server_machine_type: Parameter server machine type  [required]
        :param str parameter_server_command: Parameter server command  [required]
        :param int parameter_server_count: Parameter server count  [required]
        :param int|str experiment_type_id: Experiment Type ID
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if necessary
        :param str worker_registry_password: Registry password for accessing private docker registry container if necessary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param str parameter_server_container_user: Parameter server container user
        :param str parameter_server_registry_username: Registry username for accessing private docker registry container if necessary
        :param str parameter_server_registry_password: Registry password for accessing private docker registry container if necessary
        :param str parameter_server_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        experiment_type_id = self._get_experiment_type_id(experiment_type_id)

        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)

        experiment = models.MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_username=parameter_server_registry_username,
            parameter_server_registry_password=parameter_server_registry_password,
            parameter_server_registry_url=parameter_server_registry_url,
        )

        repository = repositories.CreateMultiNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def create_mpi_multi_node(
            self,
            project_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            name=None,
            master_container=None,
            master_machine_type=None,
            master_command=None,
            master_count=None,
            ports=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            master_container_user=None,
            master_registry_username=None,
            master_registry_password=None,
            master_registry_url=None,
            use_vpc=False,
    ):
        """
        Create multinode experiment using MPI

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str master_container: Master container  [required]
        :param str master_machine_type: Master machine type  [required]
        :param str master_command: Master command  [required]
        :param int master_count: Master count  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if necessary
        :param str worker_registry_password: Registry password for accessing private docker registry container if necessary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param str master_container_user: Master container user
        :param str master_registry_username: Registry username for accessing private docker registry container if necessary
        :param str master_registry_password: Registry password for accessing private docker registry container if necessary
        :param str master_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)
        experiment_type_id = constants.ExperimentType.MPI_MULTI_NODE

        experiment = models.MpiMultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            master_container=master_container,
            master_machine_type=master_machine_type,
            master_command=master_command,
            master_count=master_count,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            master_container_user=master_container_user,
            master_registry_username=master_registry_username,
            master_registry_password=master_registry_password,
            master_registry_url=master_registry_url,
        )

        repository = repositories.CreateMpiMultiNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def run_single_node(
            self,
            project_id,
            machine_type,
            command,
            name=None,
            ports=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
            registry_url=None,
            use_vpc=False,
    ):
        """Create and start single node experiment

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str machine_type: Machine type [required]
        :param str command: Container entrypoint command  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str container: Container (dockerfile) [required]
        :param str container_user: Container user for running the specified command in the container. If no containerUser is specified, the user will default to 'root' in the container.
        :param str registry_username: Registry username for accessing private docker registry container if necessary
        :param str registry_password: Registry password for accessing private docker registry container if necessary
        :param str registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
            registry_url=registry_url,
        )

        repository = repositories.RunSingleNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def run_multi_node(
            self,
            project_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            name=None,
            experiment_type_id=constants.ExperimentType.GRPC_MULTI_NODE,
            ports=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            parameter_server_container_user=None,
            parameter_server_registry_username=None,
            parameter_server_registry_password=None,
            parameter_server_registry_url=None,
            use_vpc=False,
    ):
        """Create and start multinode experiment

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str parameter_server_container: Parameter server container  [required]
        :param str parameter_server_machine_type: Parameter server machine type  [required]
        :param str parameter_server_command: Parameter server command  [required]
        :param int parameter_server_count: Parameter server count  [required]
        :param int|str experiment_type_id: Experiment Type ID [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if necessary
        :param str worker_registry_password: Registry password for accessing private docker registry container if necessary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param str parameter_server_container_user: Parameter server container user
        :param str parameter_server_registry_username: Registry username for accessing private docker registry container if necessary
        :param str parameter_server_registry_password: Registry password for accessing private docker registry container if necessary
        :param str parameter_server_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        experiment_type_id = self._get_experiment_type_id(experiment_type_id)

        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)

        experiment = models.MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_username=parameter_server_registry_username,
            parameter_server_registry_password=parameter_server_registry_password,
            parameter_server_registry_url=parameter_server_registry_url,
        )

        repository = repositories.RunMultiNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def run_mpi_multi_node(
            self,
            project_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            master_container,
            master_machine_type,
            master_command,
            master_count,
            name=None,
            ports=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            datasets=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            is_preemptible=False,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            master_container_user=None,
            master_registry_username=None,
            master_registry_password=None,
            master_registry_url=None,
            use_vpc=False,
    ):
        """Create and start multinode experiment using MPI

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str master_container: Master container  [required]
        :param str master_machine_type: Master machine type  [required]
        :param str master_command: Master command  [required]
        :param int master_count: Master count  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict|list[dict]|tuple[dict] datasets: Dict or list of dicts describing dataset(s) used in experiment.
                                                     Required keys: "url"
                                                     Optional keys: "tag" for S3 tag and "auth" for S3 token
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param bool is_preemptible: Is preemptible
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if necessary
        :param str worker_registry_password: Registry password for accessing private docker registry container if necessary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param str master_container_user: Master container user
        :param str master_registry_username: Registry username for accessing private docker registry container if necessary
        :param str master_registry_password: Registry password for accessing private docker registry container if necessary
        :param str master_registry_url: Registry server URL for accessing private docker registry container if necessary
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :returns: experiment handle
        :rtype: str
        """
        self.validate_cluster_id_need_vpc(cluster_id, use_vpc)
        if not is_preemptible:
            is_preemptible = None

        datasets = self._dataset_dicts_to_instances(datasets)

        experiment_type_id = constants.ExperimentType.MPI_MULTI_NODE

        experiment = models.MpiMultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            master_container=master_container,
            master_machine_type=master_machine_type,
            master_command=master_command,
            master_count=master_count,
            ports=ports,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            datasets=datasets,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            is_preemptible=is_preemptible,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            master_container_user=master_container_user,
            master_registry_username=master_registry_username,
            master_registry_password=master_registry_password,
            master_registry_url=master_registry_url,
        )

        repository = repositories.RunMpiMultiNodeExperiment(api_key=self.api_key, logger=self.logger)
        handle = repository.create(experiment, use_vpc=use_vpc)
        return handle

    def start(self, experiment_id, use_vpc=False):
        """Start existing experiment that has not run

        :param str experiment_id: Experiment ID
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :raises: exceptions.GradientSdkError
        """

        repository = repositories.StartExperiment(api_key=self.api_key, logger=self.logger)
        repository.start(experiment_id, use_vpc=use_vpc)

    def stop(self, experiment_id, use_vpc=False):
        """Stop running experiment

        :param str experiment_id: Experiment ID
        :param bool use_vpc: Set to True when using Virtual Private Cloud

        :raises: exceptions.GradientSdkError
        """

        repository = repositories.StopExperiment(api_key=self.api_key, logger=self.logger)
        repository.stop(experiment_id, use_vpc=use_vpc)

    def list(self, project_id=None, offset=None, limit=None, get_meta=False, tags=None):
        """Get a list of experiments. Optionally filter by project ID

        :param str|list|None project_id:
        :param int offset:
        :param int limit:
        :param bool get_meta: get dict of metadata like number of total items, etc. Setting to True changes rtype
        :param list[str]|tuple[str] tags: tags to filter with OR

        :return: experiments
        :rtype: list[models.SingleNodeExperiment|models.MultiNodeExperiment]|tuple[list[models.SingleNodeExperiment|models.MultiNodeExperiment],dict]
        """

        repository = repositories.ListExperiments(api_key=self.api_key, logger=self.logger)
        experiments = repository.list(project_id=project_id, limit=limit, offset=offset, get_meta=get_meta, tags=tags)
        return experiments

    def get(self, experiment_id):
        """Get experiment instance

        :param str experiment_id: Experiment ID
        :rtype: models.SingleNodeExperiment|models.MultiNodeExperiment|MpiMultiNodeExperiment
        """
        repository = repositories.GetExperiment(api_key=self.api_key, logger=self.logger)
        experiment = repository.get(experiment_id=experiment_id)
        return experiment

    def logs(self, experiment_id, line=0, limit=10000):
        """Show list of latest logs from the specified experiment.

        :param str experiment_id: Experiment ID
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: list of LogRows
        :rtype: list[models.LogRow]
        """

        repository = repositories.ListExperimentLogs(api_key=self.api_key, logger=self.logger)
        logs = repository.list(experiment_id, line, limit)
        return logs

    def yield_logs(self, experiment_id, line=0, limit=10000):
        """Get log generator. Polls the API for new logs

        :param str experiment_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        repository = repositories.ListExperimentLogs(api_key=self.api_key, logger=self.logger)
        logs_generator = repository.yield_logs(experiment_id, line, limit)
        return logs_generator

    def delete(self, experiment_id):
        repository = repositories.DeleteExperiment(api_key=self.api_key, logger=self.logger)
        repository.delete(experiment_id)

    def _dataset_dicts_to_instances(self, datasets):
        if not datasets:
            return None

        if isinstance(datasets, dict):
            datasets = [datasets]

        for ds in datasets:
            if not ds.get("uri"):
                raise ResourceCreatingDataError("Error while creating experiment with dataset: "
                                                "\"uri\" key is required and it's value must be a valid S3 URI")

        datasets = [models.Dataset(**ds) for ds in datasets]
        return datasets
