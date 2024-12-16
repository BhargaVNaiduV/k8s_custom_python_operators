# Custom Kubernetes Operator for Curl Jobs

This repository contains a custom Kubernetes operator built using **Kopf (Kubernetes Operator Python Framework)**. The operator listens for the creation and deletion of a custom resource definition (CRD) called `curljobs` and manages pods that periodically execute `curl` commands against a specified URL.

---

## How It Works

1. **CRD Creation**:
   - When a `curljobs` resource is created, the operator:
     - Reads the URL specified in the resource.
     - Creates a pod that executes a `curl` command to the given URL every 10 seconds.

2. **CRD Deletion**:
   - When the `curljobs` resource is deleted, the operator:
     - Deletes the pod created for the corresponding `curljobs` resource.

---

## Prerequisites

1. A Kubernetes cluster with appropriate permissions to:
   - Manage custom resource definitions (CRDs).
   - Create and delete pods.

2. Install the required Python dependencies:
   - Install Kopf: `pip install kopf`
   - Install Kubernetes Python client: `pip install kubernetes`

---

## Setup Instructions

### 1. Define the Custom Resource Definition (CRD)

Apply the following YAML to your cluster to define the `curljobs` CRD:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: curljobs.example.com
spec:
  group: example.com
  names:
    kind: CurlJob
    listKind: CurlJobList
    plural: curljobs
    singular: curljob
  scope: Namespaced
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              url:
                type: string
                description: The URL to be periodically curled.
