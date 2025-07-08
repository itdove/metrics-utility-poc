import json

from kubernetes import client, config
from datetime import datetime
from typing import List


class Node:
    name: str
    cpu: int
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu
        
    def to_dict(self):
        return {"name":self.name, "cpu": self.cpu}
class Nodes:
    total: int
    timestamp: datetime
    nodes: List[Node]

    def __init__(self, total, timestamp, nodes):
        self.total = total
        self.timestamp = timestamp
        self.nodes = nodes

    def to_dict(self):
        return {"total":self.total, 
                "timestamp":self.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
                "nodes": self.nodes
                }
    
def describe_kubernetes_node():
    """
    Retrieves detailed information about a specific Kubernetes node,
    similar to 'kubectl describe node <node-name>'.
    """
    try:
        try:
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config()
            except config.ConfigException:
                raise Exception("Could not configure Kubernetes Python client")
        # Create a CoreV1Api client
        api_instance = client.CoreV1Api()

        nodes = api_instance.list_node()

        calculated_nodes = calculate_total_cpu(nodes)

        calculated_nodes_json = json.dumps(calculated_nodes, default=lambda o: o.to_dict())

        print(calculated_nodes_json)
        # # Get the current date and time
        # now = datetime.now()
        
        # print(f"total cpu at {}: {total}")

        # for node_info in nodes.items:
        #     # Read the node details
        #     # node_info = api_instance.read_node(name=node)

        #     # Print relevant information (customize as needed)
        #     print(f"Node Name: {node_info.metadata.name}")
        #     print(f"Kubernetes Version: {node_info.status.node_info.kubelet_version}")
        #     print(f"OS Image: {node_info.status.node_info.os_image}")
        #     print(f"Architecture: {node_info.status.node_info.architecture}")
        #     print("\nAddresses:")
        #     for address in node_info.status.addresses:
        #         print(f"  {address.type}: {address.address}")
        #     print("\nCapacity:")
        #     for resource, value in node_info.status.capacity.items():
        #         print(f"  {resource}: {value}")
        #     print("\nConditions:")
        #     for condition in node_info.status.conditions:
        #         print(f"  {condition.type}: {condition.status} (Reason: {condition.reason}, Message: {condition.message})")
            
        # You can access other fields like events, volumes, etc., from node_info
        
    except client.ApiException as e:
        print(f"Error describing node: {e}")
    except config.ConfigException as e:
        print(f"Error loading Kubernetes config: {e}")

def calculate_total_cpu(nodes) -> Nodes:
    total = 0
    nodes_cpu = []
    for node_info in nodes.items:
        for resource, value in node_info.status.capacity.items():
            if resource == 'cpu':
                nodes_cpu.append(Node(node_info.metadata.name, int(value)))
                total += int(value)
 
    now = datetime.now()
 
    return Nodes(total, now, nodes_cpu)

if __name__ == "__main__":
    describe_kubernetes_node()
