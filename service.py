from k8s_client import K8s
class VIcsnf:
  def __init__(self):
    self.k8s = K8s()
  def create(self, params):
    return self.k8s.create_pod()
