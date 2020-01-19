# We are going to use phosphositeplus to mine phosphosites and their info
# PSP doesn't have easy programmatic access to their datasets so this was downloaded directly


# Open our file (saved in the working directory) and read it into python.
f = open("Kinase_Substrate_Dataset", 'r')
dataset = f.readlines()
f.close()

# Save the header line as header
header = [dataset[3].replace('\t',',')]

# Pull out all the human phosphosites
kinsubs = ""
for ll in dataset:
    if 'human' in ll:
        kinsubs += str(ll.replace('\t', ','))
        
# Make a list of phosposites with a header
linklist = []
linklist += kinsubs.split("\n")
linklist = header + linklist

outf = open("kinasesubstrates.csv", "w+")
for ll in linklist:
    outf.write(ll + '\n')
outf.close()