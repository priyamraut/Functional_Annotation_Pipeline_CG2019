#!usr/bin/python 3
import sys,re
from subprocess import Popen,PIPE,call

def read_reference(filename):
    list_filenames = []
    with open(filename,'r') as f:
        for line in f:
            list_filenames.append(line.strip())
    f.close()
    return list_filenames

def make_reference_dic(filename):
    dic_signature_desc = {}
    with open(filename,'r') as f:
        for line in f:
            if re.match('>',line):
                dic_signature_desc[line.split()[0][1:]] = []
    f.close()
    return dic_signature_desc


def make_signature_desc(filename,dic):
    with open(filename,'r') as f:
        for line in f:
            if re.search("signature_desc",line.split('\t')[-1]):
                start = re.search("signature_desc",line.split('\t')[-1]).start()
                end = re.search(";Name",line.split('\t')[-1]).start()
                dic[line.split('\t')[0]].append(line.split('\t')[-1][start+15:end])    

def replace_header(filename,dic):

    new_file = filename[:-4] + '_annotated.fasta'
    process = Popen(args = ['cp',filename,new_file],stdout = PIPE, stderr = PIPE)
    stdout, stderr = process.communicate()
    del stdout,stderr
    for key in dic:
        sed_cmd = 's/' + key + '/' + dic[key] + '/1'
        call(['sed','-i',"''",sed_cmd,new_file])


def main():

    file_reference = sys.argv[1]
    path = './'
    file_fastas = sys.argv[2]

    list_filenames = read_reference(file_reference)
    list_fastas = read_reference(file_fastas)

    for i in range(len(list_filenames)):
        file_r = list_filenames[i]
        file_f = list_fastas[i]
        nfile = path + file_r
        dic_signature_desc = make_reference_dic(file_f)
        make_signature_desc(nfile,dic_signature_desc)
        for key,value in dic_signature_desc.items():
            if value == []:
                dic_signature_desc[key].append("Hypothetical protein")
            dic_signature_desc[key] = key + ' ' + ';'.join(value)
        replace_header(file_f,dic_signature_desc)

    
if __name__ == '__main__':
    main()

