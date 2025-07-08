from kubernetes import client, config
from openshift.dynamic import DynamicClient

def describe_kubernetes_node(node_name):
    """
    Retrieves detailed information about a specific Kubernetes node,
    similar to 'kubectl describe node <node-name>'.
    """
    try:
        # Load Kubernetes configuration
        k8s_client = config.new_client_from_config()

        # Create a CoreV1Api client
        api_instance = client.CoreV1Api()

        # Read the node details
        node_info = api_instance.read_node(name=node_name)

        # Print relevant information (customize as needed)
        print(f"Node Name: {node_info.metadata.name}")
        print(f"Kubernetes Version: {node_info.status.node_info.kubelet_version}")
        print(f"OS Image: {node_info.status.node_info.os_image}")
        print(f"Architecture: {node_info.status.node_info.architecture}")
        print("\nAddresses:")
        for address in node_info.status.addresses:
            print(f"  {address.type}: {address.address}")
        print("\nCapacity:")
        for resource, value in node_info.status.capacity.items():
            print(f"  {resource}: {value}")
        print("\nConditions:")
        for condition in node_info.status.conditions:
            print(f"  {condition.type}: {condition.status} (Reason: {condition.reason}, Message: {condition.message})")
        
        # You can access other fields like events, volumes, etc., from node_info
        
    except client.ApiException as e:
        print(f"Error describing node: {e}")
    except config.ConfigException as e:
        print(f"Error loading Kubernetes config: {e}")

if __name__ == "__main__":
    # Replace 'your-node-name' with the actual name of your Kubernetes node
    node_to_describe = "ip-10-0-10-50.ec2.internal"

    describe_kubernetes_node(node_to_describe)
