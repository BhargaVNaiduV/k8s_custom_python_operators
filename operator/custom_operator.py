import kopf
import kubernetes.client as k8s_client
from kubernetes import config, client

# Load the in-cluster Kubernetes configuration
config.load_incluster_config()

# Define the Kubernetes API clients
api = client.CoreV1Api()
apps_api = client.AppsV1Api()

@kopf.on.create('example.com', 'v1', 'curljobs')
def create_fn(spec, **kwargs):
    url = spec['url']
    
    # Define the pod template
    pod_template = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'curl-job-pod'
        },
        'spec': {
            'containers': [{
                'name': 'curl-container',
                'image': 'ubuntu',
                'command': ['bash', '-c', f'while true; do curl {url}; sleep 10; done']
            }],
            'restartPolicy': 'Never'
        }
    }
    
    # Create the pod
    api.create_namespaced_pod(namespace='default', body=pod_template)
    
    # Log creation
    kopf.info(body=pod_template, reason='Created', message=f'Pod created to curl {url}')

@kopf.on.delete('example.com', 'v1', 'curljobs')
def delete_fn(spec, **kwargs):
    # Delete the pod when the custom resource is deleted
    api.delete_namespaced_pod(name='curl-job-pod', namespace='default')
    
    # Log deletion
    kopf.info(body=spec, reason='Deleted', message='Pod deleted')

if __name__ == '__main__':
    # Run the operator
    kopf.run()
