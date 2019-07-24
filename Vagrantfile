# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# Vagrantfile --- LDAP Development Environment
#
# Extras: Postgresql client
#

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", inline: $shell
  config.vm.provision "shell", path: "get-requirements.bash"
end

$shell = <<-"CONTENTS"
  apt-get update
  apt-get install -y python3-pip
CONTENTS
