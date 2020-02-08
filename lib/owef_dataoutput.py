#!/bin/python3
import os
import json


class OUTPUT:

    def __init__(self, file=None, path=None, mode='w', status=None):
        self.root = os.getcwd()
        self.mode = mode
        self.filehandler = None
        if path:
            full_path = self.root + '/data/' + path
            if os.path.exists(full_path):
                pass
            else:
                os.mkdir(full_path)
        self.path = full_path
        if file:
            self.file = self.path+'/'+file    
            if status==None:
                with open(self.file, "w") as f:
                    f.write("")


    def set_path(self, path):
        if path:
            full_path = self.root + '/data/' + path
            if os.path.exists(full_path):
                pass
            else:
                os.mkdir(full_path)
        self.path = full_path

    def get_file(self, file):
        _file = ""
        if file == None:
            _file = self.file
        else:
            _file = self.path + '/' + file
        return _file

    def write_file(self, file=None):
        _file = self.get_file(file)
        if self.path:
            self.filehandler = open(_file, self.mode, encoding="utf-8")
        else:
            self.filehandler = open(self.path + '/' + _file, self.mode, encoding="utf-8")

    def read_file(self, file=None):
        if self.filehandler:
            return
        _file = self.get_file(file)
        if self.path:
            self.filehandler = open(_file, 'r', encoding="utf-8")
        else:
            self.filehandler = open(self.path + '/' + _file, 'r', encoding="utf-8")

    def write_data(self, data):
        self.write_file()
        self.filehandler.writeline(data)
        self.filehandler.close()

    def write_datas(self, datas):
        self.write_file()
        self.filehandler.writelines(datas)
        self.filehandler.close()

    def write_code(self, Contract_Source_Code, Contract_ABI, Contract_Creation_Code_16,
                   Contract_Creation_Opcode, Label, address):
        data = {"Contract Adress": address, "Label": Label, "Contract_Source_Code": Contract_Source_Code,
                "Contract_ABI": Contract_ABI, "Contract_Creation_Code_16": Contract_Creation_Code_16,
                "Contract_Creation_Opcode": Contract_Creation_Opcode}
        json.dump(data, self.filehandler)


        # self.filehandler.write("Contract Adress: " + address + '\r\n')
        # self.filehandler.write("Label: " + Label + '\r\n')
        # self.filehandler.write("Contract_Source_Code: \r\n")
        # self.filehandler.write(Contract_Source_Code)
        # self.filehandler.write('\r\n')
        # self.filehandler.write('Contract_ABI:\r\n')
        # self.filehandler.write(Contract_ABI)
        # self.filehandler.write("\r\n")
        # self.filehandler.write('Contract_Creation_Code_16:\r\n')
        # self.filehandler.write(Contract_Creation_Code_16)
        # self.filehandler.write('\r\n')
        # self.filehandler.write('Contract_Creation_Opcode:\r\n')
        # self.filehandler.write(Contract_Creation_Opcode)
        # self.filehandler.write('\r\n')
        # self.filehandler.write("\r\n\r\n")
