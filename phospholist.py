# We are going to use phosphositeplus to mine phosphosites and their info
# PSP doesn't have easy programmatic access to their datasets so this was downloaded directly


# Open our file (saved in the working directory) and read it into python.
f = open("Phosphorylation_site_dataset", 'r')
dataset = f.readlines()
f.close()

# Save the header line as header
header = [dataset[3].replace('\t',',')]

# Pull out all the human phosphosites
phosites = ""
for ll in dataset:
    if 'human' in ll:
        phosites += str(ll.replace('\t', ','))
        
# Make a list of phosposites with a header
pholist = []
pholist += phosites.split("\n")
pholist = header + pholist
pholist.pop(1)

outf = open("phospholist.csv", "w+")
for ll in pholist:
    outf.write(ll + '\n')
outf.close()