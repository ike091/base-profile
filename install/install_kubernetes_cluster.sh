#!/bin/bash

# Automatically sets up the master node of a K8s cluster to be used on SLATE (CentOS 7)
# A MetalLB configMap will still need to be provided
# 
# https://slateci.io/docs/cluster/index.html

# Disable SELinux
sudo setenforce 0
sudo sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

# Disable swap
sudo swapoff -a
sudo sed -e '/swap/s/^/#/g' -i /etc/fstab

# Disable firewalld
sudo systemctl disable --now firewalld

# Use iptables for bridged network traffic
sudo cat <<EOF >  /etc/sysctl.d/k8s.conf 
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

# Add Docker stable repo to Yum
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install the latest version of DockerCE and containerd 
sudo yum install docker-ce docker-ce-cli containerd.io -y

# Enable Docker on reboot through systemctl
sudo systemctl enable --now docker

# Add kubernetes repository
sudo cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

# Install the three necessary Kubernetes components
sudo yum install -y kubeadm kubectl kubelet --disableexcludes=kubernetes

# Enable Kubelet through systemctl.
sudo systemctl enable --now kubelet

kubeadm init --pod-network-cidr=192.168.0.0/16

sudo export KUBECONFIG=/etc/kubernetes/admin.conf

kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.1/manifests/metallb.yaml

# Remove master taint to allow user pods to run on master node
kubectl taint nodes --all node-role.kubernetes.io/master-
