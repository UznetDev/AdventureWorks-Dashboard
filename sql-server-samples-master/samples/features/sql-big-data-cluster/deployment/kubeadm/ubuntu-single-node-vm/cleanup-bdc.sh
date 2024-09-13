#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
DIR_PREFIX=$1

kubeadm reset --force

systemctl stop kubelet
rm -rf /var/lib/cni/
rm -rf /var/lib/etcd/
rm -rf /run/flannel/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
rm -rf /etc/kubernetes/

ip link set cni0 down
#brctl delbr cni0
ip link set flannel.1 down
#brctl delbr flannel.1
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X

# Remove azdata
#
apt-get remove -y azdata-cli
rm /etc/apt/sources.list.d/azdata-cli.list
rm /etc/apt/trusted.gpg.d/dpgswdist.v1.asc.gpg
apt autoremove

# Remove mounts.
#
SERVICE_STOP_FAILED=0

systemctl | grep "/var/lib/kubelet/pods" | while read -r line; do

    # Retrieve the mount path
    #
    MOUNT_PATH=`echo "$line"  | grep -v echo | egrep -oh -m 1 "(/var/lib/kubelet/pods).+"`

    if [ -z "$MOUNT_PATH" ]; then
        continue
    fi

    if [[ ! -d "$MOUNT_PATH" ]] && [[ ! -f "$MOUNT_PATH" ]]; then

        SERVICE=$(echo $line | cut -f1 -d' ')

        echo "Mount "$MOUNT_PATH" no longer exists."
        echo "Stopping orphaned mount service: '$SERVICE'"

        systemctl stop $SERVICE

        if [ $? -ne 0 ]; then
            SERVICE_STOP_FAILED=1
        fi

        echo ""
    fi
done

if [ $SERVICE_STOP_FAILED -ne 0 ]; then
    echo "Not all services were stopped successfully. Please check the above output for more inforamtion."
else
    echo "All orphaned services successfully stopped."
fi

# Clean the mounted volumes.
#

for i in $(seq 1 30); do

  vol="vol$i"

  sudo umount /mnt/local-storage/$vol

  sudo rm -rf /mnt/local-storage/$vol

done

# Reset kube
#
sudo apt-get purge -y kubeadm --allow-change-held-packages
sudo apt-get purge -y kubectl --allow-change-held-packages
sudo apt-get purge -y kubelet --allow-change-held-packages
sudo apt-get purge -y kubernetes-cni --allow-change-held-packages
sudo apt-get purge -y kube* --allow-change-held-packages
sudo apt -y autoremove
sudo rm -rf ~/.kube
