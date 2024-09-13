from base64 import b64encode
from copy import deepcopy
from enum import Enum

import yaml


class AgRole(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class AgMode(Enum):
    SYNC = "synchronousCommit"
    ASYNC = "asynchronousCommit"
    CONFIG = "configurationOnly"


# TODO: Use jinja2 for the templates
class SqlSecretsYaml:
    def __init__(self, data):
        self.data = data

    def set_namespace(self, namespace):
        yaml_set(self.data, ("metadata", "namespace"), namespace)

    def set_sapassword(self, pwd, b64_encode=True):
        if b64_encode:
            pwd = b64encode(pwd.encode("utf-8")).decode("utf-8")
        yaml_set(self.data, ("data", "sapassword"), pwd)

    def validate(self):
        return yaml_get(self.data, ["data", "sapassword"]) is not None


class PersistentVolumeYaml:
    NAME_KEY = ["metadata", "name"]
    PATH_KEY = ["spec", "hostPath", "path"]

    def __init__(self, data):
        self.data = data

    def set_storage(self, storage):
        yaml_set(self.data, ["metadata", "labels", "storage"], storage)

    def set_name(self, name):
        yaml_set(self.data, PersistentVolumeYaml.NAME_KEY, name)

    def get_name(self):
        return yaml_get(self.data, PersistentVolumeYaml.NAME_KEY)

    def set_path(self, path):
        yaml_set(self.data, PersistentVolumeYaml.PATH_KEY, path)

    def get_path(self):
        return yaml_get(self.data, PersistentVolumeYaml.PATH_KEY)

    def copy(self):
        return PersistentVolumeYaml(deepcopy(self.data))


class PersistentVolumeClaimYaml:

    def __init__(self, data):
        self.data = data

    def set_name(self, name):
        yaml_set(self.data, ["metadata", "name"], name)

    def set_namespace(self, namespace):
        yaml_set(self.data, ["metadata", "namespace"], namespace)

    def set_storage_class_name(self, name):
        yaml_set(self.data, ["spec", "storageClassName"], name)


class SqlServerYaml:
    """Represents a single SQL Server YAML spec"""
    AG_SPEC_KEY = ("spec", "availabilityGroups")
    SQL_SERVER_SPEC_IDX = 0
    SERVICE_SPEC_IDX = 1

    def __init__(self, data):
        self.data = list(data)

    def __repr__(self):
        return repr(self.data)

    @property
    def sql_server_spec(self):
        return self.data[SqlServerYaml.SQL_SERVER_SPEC_IDX]

    @property
    def service_spec(self):
        return self.data[SqlServerYaml.SERVICE_SPEC_IDX]

    def remove_service_spec(self):
        return self.data.pop(SqlServerYaml.SERVICE_SPEC_IDX)

    def set_name(self, name):
        yaml_multi_set(self.sql_server_spec, name,
                       [("metadata", "name"), ("metadata", "labels", "name")])
        yaml_multi_set(self.service_spec, name, [("metadata", "name"),
                                                 ("spec", "selector", "name")])

    def set_namespace(self, namespace):
        for data in self.data:
            yaml_set(data, ("metadata", "namespace"), namespace)

    def set_volume_claim_template_with_selector(self, selector, storage="2Gi"):
        self.set_instance_root_volume_claim_template({
            "accessModes": ["ReadWriteOnce"],
            "selector": {
                "matchLabels": {
                    "storage": selector
                }
            },
            "resources": {
                "requests": {
                    "storage": storage
                }
            }
        })

    def set_volume_claim_template_with_storage_class(
            self, storage_class="default", storage="5Gi"):
        self.set_instance_root_volume_claim_template({
            "accessModes": ["ReadWriteOnce"],
            "storageClass": storage_class,
            "resources": {
                "requests": {
                    "storage": storage
                }
            }
        })

    def set_volume_mounts(self, mounts):
        yaml_set(self.sql_server_spec, ["spec", "sqlServerContainer", "volumeMounts"], mounts)

    def set_volumes(self, volumes):
        yaml_set(self.sql_server_spec, ["spec", "volumes"], volumes)

    def set_availability_groups(self, ags):
        yaml_set(self.sql_server_spec, SqlServerYaml.AG_SPEC_KEY, ags)

    def set_agent_image(self, image):
        yaml_set(self.sql_server_spec, ["spec", "agentsContainerImage"], image)


    def set_instance_root_volume_claim_template(self, data):
        yaml_set(self.sql_server_spec,
                 ["spec", "instanceRootVolumeClaimTemplate"], data)

    def set_service_type(self, service_type):
        yaml_set(self.service_spec, ["spec", "type"], service_type)

    def dump(self):
        return yaml.dump(self.data)

    def copy(self):
        return SqlServerYaml(deepcopy(self.data))


class OperatorYaml:
    def __init__(self, data):
        self.data = list(data)

    def set_namespace(self, namespace):
        ns_operator = "mssql-operator-{}".format(namespace)
        for doc in self.data:
            if doc["kind"] == "ClusterRole":
                yaml_set(doc, ("metadata", "name"), ns_operator)
            elif doc["kind"] == "ClusterRoleBinding":
                yaml_set(doc, ("metadata", "name"), ns_operator)
                yaml_set(doc, ("roleRef", "name"), ns_operator)
                doc["subjects"][0]["namespace"] = namespace
            else:
                doc["metadata"]["namespace"] = namespace

    @property
    def deployment_spec(self):
        for doc in self.data:
            if doc["kind"] == "Deployment":
                return doc
        else:
            raise Exception("Invalid yaml, missing 'Deployment' spec")

    def set_agent_image(self, image):
        yaml_set(self.deployment_spec,
                              ["spec", "template", "spec", "containers"],
        [{
            "command": ["/mssql-server-k8s-operator"],
            "env": [{
                "name": "MSSQL_K8S_NAMESPACE",
                "valueFrom": {
                    "fieldRef": {
                        "fieldPath": "metadata.namespace"
                    }
                }
            }],
            "image": image,
            "name": "mssql-operator",
        }])


class AgServiceYaml:
    """
    Represents an AG Service
    spec.selector: Should look like the following:
        type: sqlservr
        role.ag.mssql.microsoft.com/{{.AgName}}: secondary
        mode.ag.mssql.microsoft.com/{{.AgName}}: synchronousCommit
    spec.type: Can be 'NodePort' or 'LoadBalancer'


    Call self.create() to create the service YAML
    """

    def __init__(self, data):
        self.data = data

    def set_namespace(self, namespace):
        yaml_set(self.data, ("metadata", "namespace"), namespace)

    def set_service_type(self, service_type):
        yaml_set(self.data, ("spec", "type"), service_type)

    def copy(self):
        return AgServiceYaml(deepcopy(self.data))

    def create(self, ag, role, mode, annotations):
        """
        Create a concrete service.
        """
        name = ("{}-{}".format(ag, role.value) +
                ("-" + mode.name.lower() if role == AgRole.SECONDARY else ""))
        self.name = name
        yaml_set(self.data, ["metadata", "name"], name)
        yaml_set(self.data, ["metadata", "annotations"], annotations)
        role_key = "role.ag.mssql.microsoft.com/{}".format(ag)
        yaml_set(self.data, ["spec", "selector", role_key], role.value)
        if role == AgRole.PRIMARY:
            yaml_set(self.data, ["spec", "ports", 0, "targetPort"], 1433)
        elif role == AgRole.SECONDARY:
            mode_key = "mode.ag.mssql.microsoft.com/{}".format(ag)
            yaml_set(self.data, ["spec", "selector", mode_key], mode.value)

    @classmethod
    def create_ag_service(cls, service_type, data, namespace, ag, role, mode,
            annotations=None):
        """Create an AG Service.
        Specify service_type = 'NodePort' or 'LoadBalancer'
        """
        service = cls(data)
        service.set_service_type(service_type)
        if namespace is not None or namespace != "":
            service.set_namespace(namespace)

        service.create(ag, role, mode, annotations)
        return service


class FailoverYaml:
    def __init__(self, data):
        self.data = list(data)

    def set_namespace(self, namespace):
        for doc in self.data:
            yaml_set(doc, ["metadata", "namespace"], namespace)

    def set_config_map_name(self, config_map_name):
        role_doc = self._get_doc("Role")
        for rule in role_doc["rules"]:
            if "configmaps" in rule["resources"]:
                config_map_rule = rule
                break
        else:
            raise Exception("Failover Role missing 'configmaps' rule: " +
                            str(role_doc))
        config_map_rule["resourceNames"] = [config_map_name]

    def set_endpoint_name(self, endpoint_name):
        role_doc = self._get_doc("Role")
        for rule in role_doc["rules"]:
            if "endpoints" in rule["resources"]:
                endpoint_rule = rule
                break
        else:
            raise Exception("Failover Role missing 'endpoints' rule: " +
                            str(role_doc))
        endpoint_rule["resourceNames"] = [endpoint_name]

    def set_failover_container(self, agent_image, ag, new_primary):
        job_doc = self._get_doc("Job")
        yaml_set(job_doc, ["spec", "template", "spec", "containers"], [{
            "name":
            "manual-failover",
            "image": agent_image,
            "command": ["/mssql-server-k8s-failover"],
            "env": [{
                "name": "MSSQL_K8S_AG_NAME",
                "value": ag
            }, {
                "name": "MSSQL_K8S_NEW_PRIMARY",
                "value": new_primary
            }, {
                "name": "MSSQL_K8S_NAMESPACE",
                "valueFrom": {
                    "fieldRef": {
                        "fieldPath": "metadata.namespace"
                    }
                }
            }]
        }])

    def _get_doc(self, doc_kind):
        for doc in self.data:
            if doc["kind"] == doc_kind:
                return doc
        else:
            raise Exception(
                "Failover YAML missing {} document kind: {}".format(
                    doc_kind, self.data))


# YAML helpers
def yaml_set(data, key, val):
    obj = data
    for k in key[:-1]:
        obj = obj[k]
    if isinstance(obj, list):
        obj.append(None)
    obj[key[-1]] = val


def yaml_multi_set(data, val, keys):
    for key in keys:
        yaml_set(data, key, val)


def yaml_get(data, key):
    obj = data
    for k in key:
        obj = obj[k]
    return obj
