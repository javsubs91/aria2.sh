import os
from sys import exit as exx
import time
import uuid
import re
from subprocess import Popen,PIPE

HOME = os.path.expanduser("~")
CWD = os.getcwd()
tokens = {}

def installArgoTunnel():
    if checkAvailable(f"{HOME}/tools/argotunnel/cloudflared"):
        return
    else:
        import os
        from shutil import unpack_archive
        from urllib.request import urlretrieve
        
        os.makedirs(f'{HOME}/tools/argotunnel/', exist_ok=True)
        aTURL = findPackageR("cloudflare/cloudflared", "cloudflared-linux-amd64")
        urlretrieve(aTURL, f'{HOME}/tools/argotunnel/cloudflared')
        # unpack_archive('cloudflared.tgz',
        #   f'{HOME}/tools/argotunnel')
        os.chmod(f'{HOME}/tools/argotunnel/cloudflared', 0o755)
        # os.unlink('cloudflared.tgz')

class ArgoTunnel:
  def __init__(self, port, proto='http', metrics=49589, interval=30, retries=30):
    import os
    filePath = "/usr/local/sessionSettings/argotunnelDB.json"
    if not os.path.exists(filePath):
      os.makedirs(filePath[:-17], exist_ok=True)
      open(filePath, 'w').close()
    
    #Installing argotunnel
    installArgoTunnel()

    self.connection=None
    self.proto=proto
    self.port=port
    self.metricPort=metrics
    self.interval=interval
    self.retries=retries

  # def start(self):
  #   if self.connection:self.connection.kill()
  #   # self.connection=Popen(f"ssh -R 80:localhost:{self.port} {self.id}@ssh.localhost.run -o StrictHostKeyChecking=no".split(), stdout=PIPE, stdin=PIPE)
  #   self.connection=Popen(f"/content/tools/argotunnel/cloudflared tunnel --url {self.proto}://0.0.0.0:{self.port} --logfile cloudflared.log".split(), stdout=PIPE, stdin=PIPE)
  #   try:
  #     return re.findall("https://(.*?.trycloudflare.com)",self.connection.stdout.readline().decode("utf-8"))[0]
  #   except:
  #     raise Exception(self.connection.stdout.readline().decode("utf-8"))

  def keep_alive(self):
    # if self.connection:self.connection.kill()
    import urllib, requests, re
    from urllib.error import HTTPError
    
    try:
      argotunnelOpenDB = dict(accessSettingFile("argotunnelDB.json", v=False))
    except TypeError:
      argotunnelOpenDB = dict()

    if findProcess("cloudflared", f"localhost:{self.metricPort}"):
      try:
        oldAddr = argotunnelOpenDB[str(self.port)]
        if requests.get("http://"+oldAddr).status_code == 200:
          return oldAddr
      except:
        pass

    self.connection=Popen(f"{HOME}/tools/argotunnel/cloudflared tunnel --url {self.proto}://0.0.0.0:{self.port} --logfile {HOME}/tools/argotunnel/cloudflared_{self.port}.log --metrics localhost:{self.metricPort}".split(),
      stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    
    time.sleep(5)

    hostname = None
    for i in range(20):
      try:
        with urllib.request.urlopen(f"http://127.0.0.1:{self.metricPort}/metrics") as response:
            hostname = re.search(r'userHostname=\"https://(.+)\"',
             response.read().decode('utf-8'), re.MULTILINE)
            if not hostname:
              time.sleep(1)
              continue
            hostname = hostname.group(1)
            break
      except HTTPError:
        time.sleep(2)
        
    if not hostname:
      raise RuntimeError("Failed to get user hostname from cloudflared")
    
    argotunnelOpenDB[str(self.port)] = hostname
    accessSettingFile("argotunnelDB.json" , argotunnelOpenDB, v=False)
    return hostname

  def kill(self):
    self.connection.kill()


    elif self.SERVICE == "argotunnel":
        con=self.connections[name]
        port=con["port"]
        proto=con["proto"]
        if v:
          clear_output()
          loadingAn(name="lds")
          textAn("Starting Argo Tunnel ...", ty="twg")
        data = dict(url="https://"+ArgoTunnel(port, proto, closePort(self.config[1])).keep_alive())
        if displayB:
          displayUrl(data, btc)
        return data
