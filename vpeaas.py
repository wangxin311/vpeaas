#! /usr/bin/env python3

import sys
from datetime import datetime
from netmiko import ConnectHandler
from device import *
from optparse import OptionParser

def provision(device, config_file):
    start_time=datetime.now()
    nc = ConnectHandler(**device)
    with open(config_file) as f:
        commands = f.read().splitlines()
        nc.send_config_set(commands, exit_config_mode=False)
        if device['device_type'] == 'juniper':
            nc.commit()
        nc.disconnect()
    end_time = datetime.now()
    print("Total provision time on [ {device:^28} ] : {time:^2} Seconds".format(device=device['ip'], time=(end_time - start_time).seconds))

def reset(device, config):
    start_time = datetime.now()
    nc = ConnectHandler(**device)
    if device['device_type'] == 'juniper':
        command = 'load override ' + str(config)
        print(command)
        nc.send_config_set([command])
        nc.commit()
    elif device['device_type'] == 'arista_eos_ssh':
        command = 'config replace flash:' + str(config)
        print(command)
        nc.send_command(command)
    else:
        print("Device has to be Juniper or Arista")
    end_time = datetime.now()
    print("Total Configuration Reset time on [ {device:^28} ] : {time:^2} Seconds".format(device=device['ip'], time=(end_time - start_time).seconds))

def startProvision():
    # Create VPE for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision VPE for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_veos_r1, "config/1.create_vpe_tenant_a_vpe_veos_r1.cfg")
    provision(vpe_veos_r2, "config/1.create_vpe_tenant_a_vpe_veos_r2.cfg")
    provision(vpe_veos_r6, "config/1.create_vpe_tenant_a_vpe_veos_r6.cfg")
    provision(vpe_vmx_r7, "config/1.create_vpe_tenant_a_vpe_vmx_r7.cfg")
    provision(vpe_vmx_r12, "config/1.create_vpe_tenant_a_vpe_vmx_r12.cfg")
    input("VPE Provision for TENANT-A is completed, Press ENTER continue to Create Subnets and attach VM for TENANT-A...")

    # Create Subnets for TENANT-A and Create VM in the Subnet
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision Subnets and attach VM into subnets for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_veos_r1, "config/2.create_subnet_tenant_a_vpe_veos_r1.cfg")
    provision(vpe_veos_r2, "config/2.create_subnet_tenant_a_vpe_veos_r2.cfg")
    provision(vpe_veos_r6, "config/2.create_subnet_tenant_a_vpe_veos_r6.cfg")
    input("Subnets Provision and VM attachment for TENANT-A is completed, Press ENTER continue to Create Peering Gateway for TENANT-A...")

    # Create Peering Gateway for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision Peering Gateway for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vmx_r11, "config/3.create_peering_gateway_tenant_a_vpe_vmx_r11.cfg")
    provision(vpe_vmx_r17, "config/3.create_peering_gateway_tenant_a_vpe_vmx_r17.cfg")
    # input("Peering Gateway Provision for TENANT-A is completed, Press ENTER continue to Attach Peering Gateway to VPE Router for TENANT-A...")

    # Attach Peering Gateway to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Attach Peering Gateway to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vmx_r7, "config/3.attach_peering_gateway_tenant_a_vpe_vmx_r7.cfg")
    provision(vpe_vmx_r12, "config/3.attach_peering_gateway_tenant_a_vpe_vmx_r12.cfg")
    provision(vpe_vmx_r11, "config/3.attach_peering_gateway_tenant_a_vpe_vmx_r11.cfg")
    provision(vpe_vmx_r17, "config/3.attach_peering_gateway_tenant_a_vpe_vmx_r17.cfg")
    input("Attach PGW to VPE Router for TENANT-A is completed, Press ENTER continue to Create IGW for TENANT-A Public BM...")

    # Create IGW and attach to VPE Router for TENANT-A Public BM
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision Internet GW and attach it to VPE Router for TENANT-A Public BM (vpe-vm1) ]'))
    print("=" * 128)
    provision(vpe_vsrx_r9, "config/4.create_attach_internet_gateway_tenant_a_vpe_vsrx_r9.cfg")
    provision(vpe_vmx_r7, "config/4.create_attach_internet_gateway_tenant_a_vpe_vmx_r7.cfg")
    input("Create IGW and attach it to VPE Router for TENANT-A Public BM is completed, Press ENTER continue to Create NAT GW for TENANT-A...")


    # Create NAT GW and attach to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision NAT GW and attach it to VPE Router for TENANT-A Private BM (vpe-vm2 and vpe-vm3) ]'))
    print("=" * 128)
    provision(vpe_vsrx_r9, "config/5.create_attach_nat_gateway_tenant_a_vpe_vsrx_r9.cfg")
    input("Create NAT GW and attach it to VPE Router for TENANT-A Private BM is completed, Press ENTER continue to Create VGW for TENANT-A...")


    # Create VGW for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision VPN GW for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vsrx_r8, "config/6.create_vpn_gateway_tenant_a_vpe_vsrx_r8.cfg")
    # input("Create VGW for TENANT-A Private BM is completed, Press ENTER continue to Attach VGW to VPE Router for TENANT-A...")

    # Attach VGW to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Attach VPN GW to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vsrx_r8, "config/6.attach_vpn_gateway_tenant_a_vpe_vsrx_r8.cfg")
    provision(vpe_vmx_r7, "config/6.attach_vpn_gateway_tenant_a_vpe_vmx_r7.cfg")
    input("Attach VGW to VPE Router for TENANT-A is completed, Press ENTER continue to Create EGW for TENANT-A...")


    # Create EGW for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision Endpoint GW for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vsrx_r10, "config/7.create_endpoint_gateway_tenant_a_vpe_vsrx_r10.cfg")
    # input("Create EGW for TENANT-A is completed, Press ENTER continue to Attach EGW to VPE Router for TENANT-A...")

    # Attach EGW to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Attach Endpoint GW to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vsrx_r10, "config/7.attach_endpoint_gateway_tenant_a_vpe_vsrx_r10.cfg")
    provision(vpe_vmx_r7, "config/7.attach_endpoint_gateway_tenant_a_vpe_vmx_r7.cfg")
    input("Attach EGW to VPE Router for TENANT-A is completed, Press ENTER continue to Create LB for TENANT-A...")

    # Create LB for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Load Balancer is pre-provsioned for TENANT-A, skip LB creation ]'))
    print("=" * 128)
    # input("Create LB for TENANT-A is skipped, Press ENTER continue to attach LB to VPE Router for TENANT-A...")

    # Attach LB to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Attach Load Balancer to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vmx_r7, "config/8.attach_load_balancer_tenant_a_vpe_vmx_r7.cfg")
    input("Attach LB to VPE Router for TENANT-A is completed, Press ENTER continue to Create Network Edge for TENANT-A...")

    # Create Network Edge for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Network Edge is created in Fabric portal and owned by Customer, so no need to create it, skip creation ]'))
    print("=" * 128)
    # input("Network Edge for TENANT-A creation is skipped, Press ENTER continue to attach Network Edge to VPE Router for TENANT-A...")

    # Attach Network Edge to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Attach Network Edge to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_vmx_r12, "config/9.attach_network_edge_tenant_a_vpe_vmx_r12.cfg")
    input("Attach Network Edge to VPE Router for TENANT-A is completed, Press ENTER continue to Create Cloud GW for TENANT-A...")

    # Create Cloud GW for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Provision Cloud GW for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_veos_r20, "config/10.create_cloud_gateway_tenant_a_vpe_veos_r20.cfg")
    # input("Create Cloud GW for TENANT-A is completed, Press ENTER continue to Attach Cloud GW to VPE Router for TENANT-A...")

    # Attach Cloud GW to VPE Router for TENANT-A
    print("=" * 128)
    print('{:^128}'.format('[ Start Attach Cloud GW to VPE Router for TENANT-A ]'))
    print("=" * 128)
    provision(vpe_veos_r20, "config/10.attach_cloud_gateway_tenant_a_vpe_veos_r20.cfg")
    provision(vpe_vmx_r12, "config/10.attach_cloud_gateway_tenant_a_vpe_vmx_r12.cfg")
    input("Attach Cloud GW to VPE Router for TENANT-A is completed, Press ENTER exit the script...")
    # input("Attach Cloud GW to VPE Router for TENANT-A is completed, Press ENTER continue to for TENANT-B...")

    # # Create VPE for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Provision VPE for TENANT-B ]'))
    # print("=" * 128)
    # provision(vpe_veos_r1, "config/1.create_vpe_tenant_b_vpe_veos_r1.cfg")
    # provision(vpe_vmx_r7, "config/1.create_vpe_tenant_b_vpe_vmx_r7.cfg")
    # input("VPE Provision for TENANT-B is completed, Press ENTER continue to Create Subnets and attach VM...")
    #
    # # Create Subnets and Attach VM for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Provision Subnets for TENANT-B ]'))
    # print("=" * 128)
    # provision(vpe_veos_r1, "config/2.create_subnet_tenant_b_vpe_veos_r1.cfg")
    # input("Subnets Provision and VM attachment for TENANT-B is completed, Press ENTER continue to Create IGW and attach to VPE Router...")
    #
    # # Create IGW and attach to VPE Router for TENANT-B Public BM
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Provision IGW and attach it to VPE Router for TENANT-B Public BM (vpe-vm9) ]'))
    # print("=" * 128)
    # provision(vpe_vsrx_r9, "config/4.create_attach_internet_gateway_tenant_b_vpe_vsrx_r9.cfg")
    # provision(vpe_vmx_r7, "config/4.create_attach_internet_gateway_tenant_b_vpe_vmx_r7.cfg")
    # input("Create IGW and attach it to VPE Router for TENANT-B Public BM is completed, Press ENTER continue to Create VGW for TENANT-B...")
    #
    # # Create VGW for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Provision VGW for TENANT-B ]'))
    # print("=" * 128)
    # provision(vpe_vsrx_r8, "config/6.create_vpn_gateway_tenant_b_vpe_vsrx_r8.cfg")
    # input("Create VGW for TENANT-B is completed, Press ENTER continue to Attach VGW to VPE Router for TENANT-B...")
    #
    # # Attach VGW to VPE Router for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Attach VGW to VPE Router for TENANT-B ]'))
    # print("=" * 128)
    # provision(vpe_vsrx_r8, "config/6.attach_vpn_gateway_tenant_b_vpe_vsrx_r8.cfg")
    # provision(vpe_vmx_r7, "config/6.attach_vpn_gateway_tenant_b_vpe_vmx_r7.cfg")
    # input("Attach VGW to VPE Router for TENANT-B is completed, Press ENTER continue to Create LB for TENANT-B...")
    #
    # # Create LB for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Load Balancer is pre-provisioned for TENANT-B, skip creation ]'))
    # print("=" * 128)
    # input("Create LB for TENANT-B is skipped, Press ENTER continue to attach LB to VPE Router for TENANT-B...")
    #
    # # Attach LB to VPE Router for TENANT-B
    # print("=" * 128)
    # print('{:^128}'.format('[ Start Attach LB to VPE Router for TENANT-B ]'))
    # print("=" * 128)
    # provision(vpe_vmx_r7, "config/8.attach_load_balancer_tenant_b_vpe_vmx_r7.cfg")
    # input("Attach LB to VPE Router for TENANT-B is completed, All Steps are Done! Press ENTER to exit...")

def resetToBase():
    # Reset to BASE configuration
    print("=" * 128)
    print('{:^128}'.format('[ Start Reset all network devices to BASE Configuration ]'))
    print("=" * 128)
    reset(vpe_veos_r1, "VPEaaS-BASE-vEOS-R1-01182021.cfg")
    reset(vpe_veos_r2, "VPEaaS-BASE-vEOS-R2-01182021.cfg")
    reset(vpe_veos_r6, "VPEaaS-BASE-vEOS-R6-01182021.cfg")
    reset(vpe_veos_r20, "VPEaaS-BASE-vEOS-R20-01252021.cfg")
    reset(vpe_vmx_r7, "VPEaaS-BASE-vMX-R7-01182021-NATIVE.cfg")
    reset(vpe_vmx_r12, "VPEaaS-BASE-vMX-R12-01182021-NATIVE.cfg")
    reset(vpe_vmx_r11, "VPEaaS-BASE-vMX-R11-01182021-NATIVE.cfg")
    reset(vpe_vmx_r17, "VPEaaS-BASE-vMX-R17-01182021-NATIVE.cfg")
    reset(vpe_vsrx_r8, "VPEaaS-BASE-vSRX-R8-VGW-01182021-NATIVE.cfg")
    reset(vpe_vsrx_r9, "VPEaaS-BASE-vSRX-R9-IGW-NGW-01182021-NATIVE.cfg")
    reset(vpe_vsrx_r10, "VPEaaS-BASE-vSRX-R10-EGW-01182021-NATIVE.cfg")
    print("=" * 128)
    print('{:^128}'.format('[ BASE Configuration Reset Done, Ready For Provision ]'))
    print("=" * 128)

def setToFinal():
    # Reset to FINAL configuration
    print("=" * 128)
    print('{:^128}'.format('[ Start Reset all network devices to FINAL Configuration ]'))
    print("=" * 128)
    reset(vpe_veos_r1, "VPEaaS-FINAL-vEOS-R1-01292021-Symmetric-IRB.cfg")
    reset(vpe_veos_r2, "VPEaaS-FINAL-vEOS-R2-01292021-Symmetric-IRB.cfg")
    reset(vpe_veos_r6, "VPEaaS-FINAL-vEOS-R6-01202021-Symmetric-IRB.cfg")
    reset(vpe_veos_r20, "VPEaaS-FINAL-vEOS-R20-CGW-01252021.cfg")
    reset(vpe_vmx_r7, "VPEaaS-FINAL-vMX-R7-01292021-NATIVE-SymmetricIRB.cfg")
    reset(vpe_vmx_r12, "VPEaaS-FINAL-vMX-R12-01252021-Symmetric-IRB-NATIVE.cfg")
    reset(vpe_vmx_r11, "VPEaaS-FINAL-vMX-R11-01252021-NATIVE.cfg")
    reset(vpe_vmx_r17, "VPEaaS-FINAL-vMX-R17-01252021-NATIVE.cfg")
    reset(vpe_vsrx_r8, "VPEaaS-FINAL-vSRX-R8-VGW-01252021-NATIVE.cfg")
    reset(vpe_vsrx_r9, "VPEaaS-FINAL-vSRX-R9-IGW-NGW-01252021-NATIVE.cfg")
    reset(vpe_vsrx_r10, "VPEaaS-FINAL-vSRX-R10-EGW-01252021-NATIVE.cfg")
    print("=" * 128)
    print('{:^128}'.format('[ FINAL Configurations are pushed, Ready For Verification ]'))
    print("=" * 128)

def parse_args(argv):
    parser = OptionParser()
    parser.add_option('-p', '--provision', action='store_true', dest='provision',help='Start provision devices')
    parser.add_option('-r', '--reset', action='store_true',dest='reset' ,help='Reset all network device to Base Configuration')
    parser.add_option('-f', '--final', action='store_true',dest='final', help='Reset all network device to Final Configuration')
    (options, args) = parser.parse_args()

    if options.provision:
        startProvision()
    elif options.reset:
        resetToBase()
    elif options.final:
        setToFinal()

def main():
    if len(sys.argv) != 2:
        print("No parameter or too many parameter given, use 'vpeaas.py -h' to check available parameter")
        sys.exit(1)
    parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()

    # devices = [vpe_veos_r1, vpe_veos_r2]
    # for device in devices:
    #     nc = ConnectHandler(**vpe_veos_r1)
    #     # output = nc.send_command('show version')
    #     # nc.send_config_set(['config', 'interface Management1', 'description test, 'end'])
    #     # configfile=open("config.txt")
    #     # nc.send_config_set(['interface management 1', 'description test'], exit_config_mode=False)
    #     # configfile.close()
    #     with open("config.txt") as f:
    #         commands=f.read().splitlines()
    #     print(commands)
    #     nc.send_config_set(commands, exit_config_mode=False)
    #     nc.disconnect()


    # devices = [vpe_vmx_r7]
    # for device in devices:
    #     nc = ConnectHandler(**vpe_vmx_r7)
    #     output = nc.send_command('show version')
    #     print(output)
    #     # config_commands = ['set interfaces ge-0/0/1 unit 0 description "Test Config"']
    #     # nc.send_config_set(config_commands, exit_config_mode=False)
    #     # output = nc.commit()
    #     # print(output)
    #     config_commands = ['delete interfaces ge-0/0/1 unit 0']
    #     nc.send_config_set(config_commands, exit_config_mode=False)
    #     output = nc.commit()
    #     nc.disconnect()