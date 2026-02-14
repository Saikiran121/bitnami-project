# Budget Analyzer - GitOps with Sealed Secrets

This project demonstrates a Budget Analyzer application deployed via Argo CD using Bitnami Sealed Secrets.

## Project Structure
- `app.py`: Flask application.
- `templates/`: HTML interface.
- `Dockerfile`: Container image definition.
- `k8s/`: Kubernetes manifests.
  - `deployment.yaml`: Application deployment.
  - `service.yaml`: Service exposure.
  - `secret.yaml`: **TEMPORARY** secret file (To be sealed).
- `argo-app.yaml`: Argo CD Application manifest.

## How to Seal your Secrets

The `k8s/secret.yaml` file contains sensitive information in plain text (encoded in base64 if using `data`, or plain string if using `stringData`). **Do not commit this file to Git.**

Follow these steps to create a `SealedSecret`:

1.  **Ensure `kubeseal` is installed** and you have access to your cluster where the Sealed Secrets controller is running.
2.  **Generate the SealedSecret**:
    ```bash
    kubeseal --format=yaml < k8s/secret.yaml > k8s/sealed-secret.yaml
    ```
3.  **Delete the plain secret**:
    ```bash
    rm k8s/secret.yaml
    ```
4.  **Commit and Push**:
    Only commit `k8s/sealed-secret.yaml` (and other files) to your repository.
5.  **Argo CD Sync**:
    Argo CD will pick up the `SealedSecret`. The controller in the cluster will automatically decrypt it and create a standard `Secret` named `budget-secrets`.

## Application Access
Once deployed, the application will be available via the `budget-analyzer-service`. If using Port-Forwarding:
```bash
kubectl port-forward svc/budget-analyzer-service 8080:80 -n budget-app
```
Then visit `http://localhost:8080`.
