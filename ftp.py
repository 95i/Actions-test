from ftplib import FTP,error_perm  # 加载ftp模块
import os

class FTPSync(object):
    conn = FTP()

    def __init__(self,host,port=21):
        self.conn.connect(host,port)

    def login(self,username,password):
        self.conn.login(username,password)
        self.conn.encoding = "GB2312"
        self.conn.set_debuglevel(2)             #打开调试级别2，显示详细信息
        self.conn.set_pasv(True)
        #0主动模式 1 #被动模式
        print(self.conn.welcome)

    def _ftp_list(self,line):
        li = line.split(' ')
        if self.ftp_dir_name == li[-1] and "<DIR>" in li:
            self._is_dir = True

    def _is_ftp_file(self, ftp_path):
        try:
            if ftp_path in self.conn.nlst(os.path.dirname(ftp_path)):
                return True
            else:
                return False
        except error_perm as e:
            return False

    def _is_ftp_dir(self,ftp_path):
        """
        用来判断所给的路径是文件还是文件夹
        """
        ftp_path = ftp_path.rstrip('/')
        ftp_parent_path = os.path.dirname(ftp_path)
        self.ftp_dir_name = os.path.basename(ftp_path)
        self._is_dir = False
        if ftp_path == '.' or ftp_path == './' or ftp_path == '':
            self._is_dir = True
        else:
            try:
                self.conn.cwd(ftp_path)
                self._is_dir = True
                # self.conn.retrlines('LIST %s' %ftp_parent_path,self._ftp_list)
            except error_perm as e:
                return self._is_dir
        return self._is_dir


    def get_file(self,ftp_path="",local_path="."):
        print(ftp_path)
        ftp_path = ftp_path.rstrip('/')

        file_name = os.path.basename(ftp_path)

        # 如果本地路径是目录，下载文件到该目录
        if os.path.isdir(local_path):
            file_handler = open(os.path.join(local_path,file_name),'wb')
            self.conn.retrbinary("RETR %s"%(ftp_path),file_handler.write)
            file_handler.close()

        # 如果本地路径不是目录，但上层目录存在，则按照本地路径的文件名作为下载的文件名称
        elif os.path.isdir(os.path.dirname(local_path)):
            file_handler = open(local_path,'wb')
            self.conn.retrbinary("RETR %s"%(ftp_path),file_handler.write)
            file_handler.close()
        # 如果本地路径不是目录，且上层目录不存在，则退出
        else:
            print('EROOR:The dir:%s is not exist' %os.path.dirname(local_path))


    def get_dir(self,ftp_path,local_path=".",begin=True):

        if not self._is_ftp_dir(ftp_path):
            self.get_file(ftp_path=ftp_path, local_path=local_path)
            return

        if begin:
            local_path = os.path.join(local_path, os.path.basename(ftp_path))

        #如果本地目录不存在，则创建目录
        if not os.path.isdir(local_path):
            os.mkdir(local_path)

        #进入ftp目录，开始递归查询
        self.conn.cwd(ftp_path)

        ftp_files = self.conn.nlst()

        for file in ftp_files:
            local_file = os.path.join(local_path, file)
            #如果file ftp路径是目录则递归上传目录（不需要再进行初始化begin的标志修改为False）
            #如果file ftp路径是文件则直接上传文件
            if self._is_ftp_dir(file):
                self.get_dir(file, local_file, False)
            elif "idea" in file:
                pass
            else:
                self.get_file(ftp_path=file, local_path=local_file)

        #如果当前ftp目录文件已经遍历完毕返回上一层目录
        self.conn.cwd("..")

    def get_all_dir(self):
        ftp_files = self.conn.nlst()
        for file in ftp_files:
            self.get_dir(file,"D:\\ftp",True)

    def put_file(self,local_path,ftp_path="."):
        ftp_path = ftp_path.rstrip('/')
        if os.path.isfile(local_path):
            file_handler = open(local_path,'rb')
            local_file_name = os.path.basename(local_path)

            #如果远程路径是个目录，则上传文件到这个目录，文件名不变
            if self._is_ftp_dir(ftp_path):
                self.conn.storbinary('STOR %s'%os.path.join(ftp_path,local_file_name), file_handler)

            #如果远程路径的上层是个目录，则上传文件，文件名按照给定命名
            elif self._is_ftp_dir(os.path.dirname(ftp_path)):
                print('STOP %s'%ftp_path)
                self.conn.storbinary('STOR %s'%ftp_path, file_handler)
            #如果远程路径不是目录，且上一层的目录也不存在，则提示给定远程路径错误
            else:
                print('STOR %s'%ftp_path, file_handler)

    def put_dir(self,local_path,ftp_path=".",begin=True):
        ftp_path = ftp_path.rstrip('/')

        if not os.path.isdir(local_path):
            print('ERROR:The dir:%s is not exist' %local_path)
            return

        #当本地目录存在时上传
        #上传初始化：如果给定的ftp路径不存在需要创建，同时将本地的目录存放在给定的ftp目录下。
        # 本地目录下文件存放的路径为ftp_path = ftp_path + os.path.basename(local_path)
        #例如，将本地的文件夹a上传到ftp的a/b目录下，则本地a目录下的文件将上传的ftp的a/b/a目录下
        if begin:
            if not self._is_ftp_dir(ftp_path):
                try:
                    self.conn.mkd(ftp_path)
                except Exceptione:
                    pass
            ftp_path = os.path.join(ftp_path,os.path.basename(local_path))

        # 如果上传路径是文件夹，则创建目录
        if not self._is_ftp_dir(ftp_path):
            try:
                self.conn.mkd(ftp_path)
            except Exceptione:
                pass

        #进入本地目录，开始递归查询
        os.chdir(local_path)
        local_files = os.listdir('.')
        for file in local_files:
            ftp_file = os.path.join(ftp_path,file)
            #如果file本地路径是目录则递归上传文件（不需要再进行初始化begin的标志修改为False）
            #如果file本地路径是文件则直接上传文件
            if os.path.isdir(file):
                self.put_dir(file,ftp_file,False)
            elif "idea" in file:
                pass
            else:
                self.put_file(file,ftp_path)

        #如果当前本地目录文件已经遍历完毕返回上一层目录
        os.chdir('..')

def ftp(localpath):
    ftp = FTPSync('ftpupload.net')
    ftp.login('epiz_30088209',"zhnFFiWyMhOZ")
    # ftp.get_file("ftppath")
    # ftp.get_dir("ftppath","localpath",True)
    # ftp.get_dir("","",True)
    # ftp.get_all_dir("")
    # ftp.put_file('/home/myscan/myscan/myscan/report_file/7/http___192.168.1.104_.html')
    ftp.put_dir(localpath, "/kanbi.ml/htdocs/videos",begin=True)

