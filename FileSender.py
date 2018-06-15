import paramiko
import os


def find_file(file_list, search_file):
    for remoteFile in file_list:
        if remoteFile.filename == search_file:
            return remoteFile
    return None

class FileSender:
    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.socket = None
        self.date = None


    def connect(self, username, password, hostname, port):
        self.ssh = paramiko.Transport(hostname, port)
        self.ssh.connect(username=username, password=password)
        self.sftp = paramiko.SFTP.from_transport(self.ssh)


    def moveFromServer(self,local_path, remote_path, date):
        sent = []
        remote_folder = self.sftp.listdir_attr(remote_path)

        for remoteFile in remote_folder:
           # filename, file_extension = os.path.splitext(remoteFile)
            #file_stat = os.stat(os.path.join(local_path, remoteFile))
            if date> remoteFile.st_mtime :
                local_file_path = local_path + "\\" + remoteFile.filename#os.path.join(local_path, remoteFile)
                remote_file_path = remote_path + "/" + remoteFile.filename
                self.sftp.get( remote_file_path,local_file_path)
                self.sftp.remove(remote_file_path)
                sent.append(remoteFile)
            else:
               continue
        return sent



    def disonnect(self):
        self.sftp.close()
        self.ssh.close()

