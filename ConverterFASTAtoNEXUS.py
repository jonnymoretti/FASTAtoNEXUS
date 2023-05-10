import sys

def ReadFileFasta(filename):
    """ 
    - Read the .fasta file
    - Store in a dictionary the sequence names and their respective sequences
    - Adjust the lines to the right
    - Save the dictionary in a .txt file
    """
    filefasta = open(filename, "r")
    dic = {}
    for row in filefasta:
        if row.startswith(">"):
            names = row.strip()
            names = names[:99]
            dic[names] = ""
        else:
            dic[names] += row.strip() #Remove the "\n" character from dictionary values
    
    max_width = max(len(key) for key in dic.keys()) + 1 #Defines the maximum width of the keys

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
    - Count how many sequence names the .fasta file has
    """
    count = 0
    for key in dic:
        if key.startswith(">"):
            count +=1
    print(count)
    return count


def NCHARValues(dic):
    """
    - Count how many characters each string has
    - If any sequence does not have the same number of characters it will print "Missmatch sequence".
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
    - Fetches the outgroup from the dictionary as an argument
    - If the outgroup is not in the dictionary it will print that it does not exist
    """
    outgroup = None
    for key in dic:
        if key.startswith(">"):
            outgroup = outgroupname[1:]
            break
    if outgroup is None:
        print("There is no outgroup with that name in the file")
    return outgroup


def NGENValue(ngen):
    """
    - Will return the value of ngen
    """
    return ngen


def NexusFile(dic,count,first_lenght,otg_name,ng):
    """
    - Will open the text file in which the dictionary is contained
    - Will print the whole str from a NEXUS file with the values given as arguments
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
    with open("ficheiro_nexus.nex", "w") as file:
        file.write(nexus)