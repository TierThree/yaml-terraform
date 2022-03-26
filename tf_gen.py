class TerraformGeneration:

    yaml_config = ""
    file_output = ""

    def __init__(self, yaml_config):
        self.yaml_config = yaml_config

        if "output_location" not in yaml_config["metadata"].keys():
            self.file_output = "/tmp/output.tf"
        else:
            self.file_output = yaml_config["metadata"]["output_location"]

    def terraform_gen(self):
        provider_block = self._provider_block_gen(self.yaml_config["provider"])
        datacenter_block = self._datacenter_block_gen(self.yaml_config["spec"]["datacenter"])
        cluster_block = self._cluster_block_gen(self.yaml_config["spec"]["cluster"])
        network_block, network_resource_block = self._network_block_gen(self.yaml_config["spec"]["network"])
        clone_block = self._clone_block_gen(self.yaml_config["spec"]["clone"]["template"])
        resource_block = self._resource_block_gen(self.yaml_config["metadata"], \
                                                   self.yaml_config["spec"], \
                                                   network_resource_block)

        with open(self.file_output, 'a+') as f:
            f.write(f'''{provider_block}
                        {datacenter_block}
                        {cluster_block}
                        {network_block}
                        {clone_block}
                        {resource_block}''')

    def _provider_block_gen(self, provider):
        return f'provider "{provider["name"]}" {{ \n \
                    user = var.vpshere_user \n \
                    password = var.vsphere_password \n \
                    vsphere_server = var.vsphere_server \n \
                    \
                    allow_unverified_ssl = true \n \
        }}'

    def _datacenter_block_gen(self, datacenter):
        return f'data "vsphere_datacenter" "datacenter" {{ \n \
                    name = "{datacenter}" \n }}'

    def _datastore_block_gen(self, datastore):
        return f'data "vsphere_datastore" "datastore" {{ \n \
                    name = "{datastore}" \n }}'

    def _cluster_block_gen(self, cluster):
        return f'data "vsphere_compute_cluster" "cluster" {{ \n \
                    name = "{cluster}" \n }}'

    def _network_block_gen(self, networks):
        string_return = ""
        resource_block = ""

        for network in networks:
            string_return += f'data "vsphere_network" "network" {{ \n \
                                    name = {network["portgroup"]}  \n }} \n'
            resource_block += f'network_interface {{ \n network_id = data.vsphere_network.network.id \n }}'

        return string_return, resource_block

    def _disk_block_gen(self, disks):
        resource_block = ""
        
        for index, disk in enumerate(disks):
            resource_block += f'disk {{ \n \
                                    label = disk{index} \n \
                                    size = {disk["size"]} \n \
                                    thin_provisioned = data.vsphere_virtual_machine.template.disks.{index}.thin_provisioned \n \
                                }}'

        return resource_block

    def _clone_block_gen(self, clone):
        return f'data "vsphere_virtual_machine" "template" {{ \n \
            name = "{clone}" \n \
            datacenter_id = data.vsphere_datacenter.datacenter.id \n }}'

    def _resource_block_gen(self, metadata, spec, network_block):
        vmname = metadata["name"]
        folder = metadata["folder"]

        cpu_count = spec["cpu"]
        memory = spec["memory"]

        disk_block = self._disk_block_gen(spec["disks"])

        return f'resource "vsphere_virtual_machine" "vm" {{ \n \
            name = {vmname} \n \
            folder = "{folder}" \n \
            resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id \n \
            datastore_id = data.vsphere_datastore.datastore.id \n \
            num_cpus = {cpu_count} \n \
            memory = {memory} \n \
            guest_id = data.vsphere_virtual_machine.template.guest_id \n \
            scsi_type = data.vsphere_virtual_machine.template.scsi_type \n \
            {network_block} \n \
            {disk_block} \n \
            clone {{ \n \
                template_uuid = data.vsphere_virtual_machine.template.id \n }} \n }}'