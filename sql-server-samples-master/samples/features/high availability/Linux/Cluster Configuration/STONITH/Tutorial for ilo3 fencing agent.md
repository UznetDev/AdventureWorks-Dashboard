# Configure STONITH with ilo3 fencing agent
## Test all the Agents before configuring Stonith

```bash
sudo fence_ilo3 -a dl380g7-07-ilo -l Administrator -p 'Password!12' --action=status –verbose
sudo fence_ilo3 -a dl380g7-08-ilo -l Administrator -p 'Password!12' --action=status –verbose
sudo fence_ilo3 -a dl380g7-09-ilo -l Administrator -p 'Password!12' --action=status –verbose
```

>[!NOTE]
>Check whether the password and user name for the device include any special characters that could be misinterpreted by the bash shell. Making sure that you enter passwords and user names surrounded by quotation marks could address this issue.

## Create the Stonith fencing

```bash
sudo pcs stonith create fence_dl380g7-07 fence_ilo3  ipaddr=dl380g7-07-ilo login="Administrator" passwd='Password!12' pcmk_host_list=dl380g7-07
sudo pcs stonith create fence_dl380g7-08 fence_ilo3  ipaddr=dl380g7-08-ilo login="Administrator" passwd='Password!12' pcmk_host_list=dl380g7-08
sudo pcs stonith create fence_dl380g7-09 fence_ilo3  ipaddr=dl380g7-09-ilo login="Administrator" passwd='Password!12' pcmk_host_list=dl380g7-09
```

## Enable fencing

```bash
sudo pcs property set stonith-enabled=true
```

## Check fencing configuration

```bash
sudo pcs stonith --full
```

The following shows the output:
```
Resource: fence_dl380g7-08 (class=stonith type=fence_ilo3)
  Attributes: ipaddr=dl380g7-08-ilo login=Administrator passwd=Password!12
  Operations: monitor interval=60s (fence_dl380g7-08-monitor-interval-60s)
Resource: fence_dl380g7-09 (class=stonith type=fence_ilo3)
  Attributes: ipaddr=dl380g7-09-ilo login=Administrator passwd=Password!12 pcmk_host_list=dl380g7-09
  Operations: monitor interval=60s (fence_dl380g7-09-monitor-interval-60s)
Resource: fence_dl380g7-07 (class=stonith type=fence_ilo3)
  Attributes: ipaddr=dl380g7-07-ilo login=Administrator passwd=Password!12 pcmk_host_list=dl380g7-07
  Operations: monitor interval=60s (fence_dl380g7-07-monitor-interval-60s)
```

## Test the configuration

1. Fence a node with `pcs stonith fence <nodeName>`

    ```bash
    pcs stonith fence dl380g7-09
    ```

    ```bash
    sudo pcs status
    ```

    The following shows the output:
    ```
    Cluster name: sqlcluster
    Stack: corosync
    Current DC: dl380g7-08 (version 1.1.15-11.el7_3.4-e174ec8) - partition with quorum
    Last updated: Fri May 12 09:46:58 2017          Last change: Fri May 12 09:46:55 2017 by root via cibadmin on dl380g7-08

    3 nodes and 7 resources configured

    Online: [ dl380g7-07 dl380g7-08 ]
    OFFLINE: [ dl380g7-09 ]

    Full list of resources:

    Master/Slave Set: ag_cluster-master [ag_cluster]
        Masters: [ dl380g7-08 ]
        Slaves: [ dl380g7-07 ]
        Stopped: [ dl380g7-09 ]
    virtualip      (ocf::heartbeat:IPaddr2):       Started dl380g7-08
    fence_dl380g7-08       (stonith:fence_ilo3):   Started dl380g7-07
    fence_dl380g7-09       (stonith:fence_ilo3):   Started dl380g7-07
    fence_dl380g7-07       (stonith:fence_ilo3):   Started dl380g7-08
    ```

2. Crash a node using `echo c>>/proc/sysrq-trigger`

    ```bash
    sudo pcs status
    ```

    The following shows the output:
    ```
    Cluster name: sqlcluster
    Stack: corosync
    Current DC: dl380g7-08 (version 1.1.15-11.el7_3.4-e174ec8) - partition with quorum
    Last updated: Fri May 12 10:00:52 2017          Last change: Fri May 12 09:58:01 2017 by root via cibadmin on dl380g7-08

    3 nodes and 7 resources configured

    Online: [ dl380g7-07 dl380g7-08 ]
    OFFLINE: [ dl380g7-09 ]

    Full list of resources:

    Master/Slave Set: ag_cluster-master [ag_cluster]
        Masters: [ dl380g7-08 ]
        Slaves: [ dl380g7-07 ]
        Stopped: [ dl380g7-09 ]
    virtualip      (ocf::heartbeat:IPaddr2):       Started dl380g7-08
    fence_dl380g7-08       (stonith:fence_ilo3):   Started dl380g7-08
    fence_dl380g7-09       (stonith:fence_ilo3):   Started dl380g7-07
    fence_dl380g7-07       (stonith:fence_ilo3):   Started dl380g7-08
    ```

    ```bash
    sudo cat /var/log/messages
    ```

    The following shows the output:
    ```
    May 12 09:58:38 dl380g7-08 pengine[30024]: warning: Node dl380g7-09 will be fenced because the node is no longer part of the cluster
    May 12 09:58:38 dl380g7-08 pengine[30024]: warning: Action fence_dl380g7-09_stop_0 on dl380g7-09 is unrunnable (offline)
    May 12 09:58:38 dl380g7-08 pengine[30024]:  notice: Move    fence_dl380g7-09#011(Started dl380g7-09 -> dl380g7-07)
    May 12 09:58:38 dl380g7-08 crmd[30025]:  notice: Initiating start operation fence_dl380g7-09_start_0 on dl380g7-07
    May 12 09:58:38 dl380g7-08 stonith-ng[30021]:  notice: Client crmd.30025.62ff454d wants to fence (reboot) 'dl380g7-09' with device '(any)'
    May 12 09:58:39 dl380g7-08 stonith-ng[30021]:  notice: fence_dl380g7-07 can not fence (reboot) dl380g7-09: static-list
    May 12 09:58:39 dl380g7-08 stonith-ng[30021]:  notice: fence_dl380g7-09 can fence (reboot) dl380g7-09: static-list
    May 12 09:58:40 dl380g7-08 crmd[30025]:  notice: Initiating monitor operation fence_dl380g7-09_monitor_60000 on dl380g7-07
    ```

3. Take down the network between nodes and appropriate network cards

    ```bash
    sudo if down eth0
    ```