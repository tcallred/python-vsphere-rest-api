#!/usr/bin/env python

from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
import atexit

"""
Takes: ESX host name, username, password, virtual machine name
Returns: Dict containing the name of the machine, cpu and memory usage as %
"""


def specific_vm_perf(host, user, password, vm_name):

    # Connect to the host without SSL signing
    try:
        si = SmartConnectNoSSL(
            host=host,
            user=user,
            pwd=password)
        atexit.register(Disconnect, si)
    except AttributeError:
        raise IOError("Could not connect to ESX host. Verify IP address.")

    content = si.RetrieveContent()
    perf_manager = content.perfManager

    # create a mapping from performance stats to their counter_ids
    # counter_info: [performance stat => counterId]
    # performance stat example: cpu.usagemhz.LATEST
    # counterId example: 6
    counter_info = {}
    for c in perf_manager.perfCounter:
        full_name = c.groupInfo.key + "." + c.nameInfo.key + "." + c.rollupType
        counter_info[full_name] = c.key

    # create a list of vim.VirtualMachine objects so
    # that we can query them for statistics
    container = content.rootFolder
    view_type = [vim.VirtualMachine]
    recursive = True

    container_view = content.viewManager.CreateContainerView(container, view_type, recursive)
    children = container_view.view
    our_vm = None

    # Loop through all the VMs
    for child in children:
        if child.summary.config.name == vm_name:
            our_vm = child
    if our_vm is None:
        raise AssertionError("Virtual machine not found")
    # Get all available metric IDs for this VM
    counter_ids = [m.counterId for m in perf_manager.QueryAvailablePerfMetric(entity=our_vm)]

    # Using the IDs form a list of MetricId
    # objects for building the Query Spec
    metric_ids = [vim.PerformanceManager.MetricId(counterId=c, instance="*") for c in counter_ids]

    # Build the specification to be used
    # for querying the performance manager
    spec = vim.PerformanceManager.QuerySpec(maxSample=1,
                                            entity=our_vm,
                                            metricId=metric_ids)
    # Query the performance manager
    # based on the metrics created above
    result = perf_manager.QueryStats(querySpec=[spec])
    # result[0].value is the list of perf metrics
    # Loop through the results and return the output

    output = {'name': our_vm.summary.config.name}
    for val in result[0].value:
        if counter_info.keys()[counter_info.values().index(val.id.counterId)] == "cpu.usage.average":
            output['cpu'] = str(val.value[0])
        elif counter_info.keys()[counter_info.values().index(val.id.counterId)] == "mem.usage.average":
            output['mem'] = str(val.value[0])

    return output


def main():
    try:
        print(str(specific_vm_perf('151.155.216.206', 'root', 'R))Tr0x', 'eDir-st8123')))
    except IOError as e:
        print(e)
    except AssertionError as e:
        print(e)


if __name__ == "__main__":
    main()
