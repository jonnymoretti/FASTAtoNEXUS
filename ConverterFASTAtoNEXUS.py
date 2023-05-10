import sys

def ReadFileFasta(filename):
    """ 
    - Ler o ficheiro .fasta
    - Arquivar num dicionario os nomes da sequencia e as suas sequncias respetivas
    - Ajustar as linhas à direita
    - Gravar o dicionario num ficheiro .txt
    """
    filefasta = open(filename, "r")
    dic = {}
    for row in filefasta:
        if row.startswith(">"):
            names = row.strip()
            names = names[:99]
            dic[names] = ""
        else:
            dic[names] += row.strip() #Remover o carcter "\n" dos values do dicionario
    
    max_width = max(len(key) for key in dic.keys()) + 1 #Define a largura máxima das chaves

    with open("dicionario.txt" , "w")as file:
        s = ""
        for key, value in dic.items():
            if key.startswith(">"):
                line = " "  + key
            s += f"{line.rjust(max_width)}  {value}\n"
        file.write(s)
    return dic


def NTAXValues(dic):
    """
    - Contar quantos nomes de sequencia o arquivo .fasta possui
    """
    count = 0
    for key in dic:
        if key.startswith(">"):
            count +=1
    print(count)
    return count


def NCHARValues(dic):
    """
    - Contar quantos caracteres as cada sequencia possui
    - Se alguma sequencia não tiver o mesmo número de caracteres irá printar "Missmatch sequence"
    """
    first_lenght = None
    for key, value in dic.items():
        if key.startswith(">"):
            if first_lenght is None:
                first_lenght = len(value)
            elif len(value) != first_lenght:
                print("Missmatch sequence")
                return
    print(first_lenght)
    return first_lenght
    

def OutgroupName(dic, outgroupname):
    """
    - Vai buscar o outgroup pelo dicionario como argumento
    - Se  o outgroup não estiver no dicionario ele vai printar que não existe
    """
    outgroup = None
    for key in dic:
        if key.startswith(">"):
            outgroup = outgroupname[1:]
            break
    if outgroup is None:
        print("Não existe nenhum outgroup com esse nome no ficheiro")
    return outgroup


def NGENValue(ngen):
    """
    - Vai retornar o valor do ngen
    """
    return ngen


def NexusFile(dic,count,first_lenght,otg_name,ng):
    """
    - Vai abrir o ficheiro de texto no qual está contido o dicionario
    - Irá printar toda a str de um ficheiro NEXUS de com os valores determinados como argumentos
    """
    with open("dicionario.txt", "r") as file:
        dic = file.read()

    nexus_str = f"""#NEXUS\nBEGIN DATA;\nDIMENSIONS NTAX = {count} NCHAR = {first_lenght};\nFORMAT DATATYPE=DNA MISSING=N GAP=-;\n
MATRIX\n{dic}"""
    nexus_str2 = f"""  ;\nEND;\nbegin mrbayes;
    set autoclose=yes;
    outgroup {otg_name}
    mcmcp ngen = {ng} printfreq=1000 samplefreq=100 diagnfreq=1000 nchains=4 savebrlens=yes filename=MyRun01;
    mcmc;
    sumt filename=MyRun01;
end;"""
    nexus_totalstr = nexus_str + nexus_str2
    return nexus_totalstr


if __name__ == "__main__":
    dicio_fasta = ReadFileFasta(sys.argv[1])
    out_group = OutgroupName(dicio_fasta,sys.argv[2])
    nngen = NGENValue(sys.argv[3])
    ntax = NTAXValues(dicio_fasta)
    nchar = NCHARValues(dicio_fasta)
    nexus = NexusFile(dicio_fasta,ntax,nchar,out_group,nngen)
    print(nexus)
    with open("ficheiro_nexus.nex", "w") as file:
        file.write(nexus)