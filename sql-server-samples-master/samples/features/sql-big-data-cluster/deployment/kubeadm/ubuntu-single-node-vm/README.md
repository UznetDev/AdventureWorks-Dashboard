
# Deploy a SQL Server big data cluster on single node Kubernetes cluster (kubeadm)

Using this sample bash script, you will deploy a single node Kubernetes cluster using  kubeadm and a SQL Server big data cluster on top of it. The script must be run from the VM you are planning to use for your kubeadm deployment.

## Pre-requisites

1. A vanilla Ubuntu 16.04 or 18.04 virtual or physical machine. All dependencies will be setup by the script. Using Azure Linux VMs is not yet supported.
1. Machine should have at least 8 CPUs, 64GB RAM and 100GB disk space. After installing the images you will be left with 50GB for data/logs across all components.
1. Update existing packages using commands below to ensure that the OS image is up to date

``` bash
sudo apt update&&sudo apt upgrade -y
sudo systemctl reboot
```

## Recommended Virtual Machine settings

1. Use static memory configuration for the virtual machine. For example, in hyper-v installations do not use dynamic memory allocation but instead allocate the recommended 64 GB or higher.

1. Use checkpoint or snapshot capability in your hyper visor so that you can rollback the virtual machine to a clean state.

## Instructions to deploy SQL Server big data cluster

1. Download the script on the VM you are planning to use for the deployment

``` bash
curl --output setup-bdc.sh https://raw.githubusercontent.com/microsoft/sql-server-samples/master/samples/features/sql-big-data-cluster/deployment/kubeadm/ubuntu-single-node-vm/setup-bdc.sh
```

2. Make the script executable

``` bash
chmod +x setup-bdc.sh
```

3. Run the script (make sure you are running with sudo)

``` bash
sudo ./setup-bdc.sh
```

4. Refresh alias setup for azdata

``` bash
source ~/.bashrc
```

When prompted, provide your input for the password that will be used for all external endpoints: controller, SQL Server master and gateway. The password should be sufficiently complex based on existing rules for SQL Server password. The controller username is defaulted to *admin*.

## Cleanup

1. The [cleanup-bdc.sh](cleanup-bdc.sh/) script is provided as convenience to reset the environment in case of errors. However, we recommend that you use a virtual machine for testing purposes and use the snapshot capability in your hyper-visor to rollback the virtual machine to a clean state.
