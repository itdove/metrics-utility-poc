import json

from kubernetes import client, config
from datetime import datetime, timezone
from typing import List


class Node:
  def __init__(self, name: str, cpu: int):
      self.name = name
      self.cpu = cpu
  
  def __repr__(self):
      return f"Node(name='{self.name}', cpu={self.cpu})"

class Nodes:
  def __init__(self, total: int, timestamp: datetime, nodes: List[Node]):
      self.total = total
      self.timestamp = timestamp
      self.nodes = nodes
  
  def __repr__(self):
      return f"Nodes(total={self.total}, timestamp={self.timestamp}, nodes={self.nodes})"

class NodesJSONEncoder(json.JSONEncoder):
  """Custom JSON encoder for Nodes objects"""
  
  def default(self, obj):
      if isinstance(obj, datetime):
          return obj.isoformat()
      elif isinstance(obj, Node):
          return {
              'name': obj.name,
              'cpu': obj.cpu
          }
      elif isinstance(obj, Nodes):
          return {
              'total': obj.total,
              'timestamp': obj.timestamp,
              'nodes': obj.nodes
          }
      return super().default(obj)

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

        # calculated_nodes_json = json.dumps(calculated_nodes, default=lambda o: o.to_dict())
        calculated_nodes_json = json.dumps(calculated_nodes, cls=NodesJSONEncoder)

        print(calculated_nodes_json)
        
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
 
    return Nodes(total, now, nodes_cpu).to_json()

def describe_kubernetes_node_no_class():
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

    now = datetime.now(timezone.utc)

    info = {"cluster_name":"TOBEADDED",
            "timestamp": now.isoformat(),
            "nodes": []}
    cluster_vcpu = 0
    for node_info in nodes.items:
        for resource, value in node_info.status.capacity.items():
            if resource == 'cpu':
                info["nodes"].append({node_info.metadata.name: int(value)})
                cluster_vcpu += int(value)
    
    info["cluster_vcpu"] = cluster_vcpu

    print(json.dumps(info, indent=2))
  except client.ApiException as e:
      print(f"Error describing node: {e}")
  except config.ConfigException as e:
      print(f"Error loading Kubernetes config: {e}")


if __name__ == "__main__":
    describe_kubernetes_node_no_class()
    # nodeslist = [Node(name="n1",cpu=4),Node(name="n2",cpu=3)]
    # nodes = Nodes(total=4, timestamp=datetime.now(), nodes=None)
    # print(json.dumps(nodes, cls=NodesJSONEncoder))
    # # Create sample data
    # nodes_data = Nodes(
    #     total=12,
    #     timestamp=datetime.now(),
    #     nodes=[
    #         Node("worker-1", 4),
    #         Node("worker-2", 8)
    #     ]
    # )
    
    # # Serialize using custom encoder
    # json_data = json.dumps(nodes_data, cls=NodesJSONEncoder, indent=2)
    # print("Serialized with custom encoder:")
    # print(json_data)
