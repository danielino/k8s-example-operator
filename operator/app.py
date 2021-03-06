#!/usr/bin/env python
import kopf
import kubernetes
import yaml

CURRENT_API_VERSION = "v1alpha1"


def get_deployment_template(name, namespace, app):
    return {
        'apiVersion': 'apps/v1',
        'metadata': {
            'name': name,
            'namespace': namespace,
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'app': app
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': app
                    }
                },
                'spec': {
                    'containers': [
                        {
                            'image': 'exampleapp:latest',
                            'imagePullPolicy': 'IfNotPresent',
                            'name': 'controller'
                        }
                    ],
                }
            },
        }
    }


@kopf.on.resume("example.com", CURRENT_API_VERSION, "controllers")
@kopf.on.create("example.com", CURRENT_API_VERSION, "controllers")
def create_controller(body, spec, **kwargs):
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    app = body['metadata']['labels']['app']

    deployment = get_deployment_template(name, namespace, app)

    kopf.adopt(deployment, owner=body)

    apps = kubernetes.client.AppsV1Api()

    obj = apps.create_namespaced_deployment(namespace, deployment)

    return {'message': "created successfully"}
