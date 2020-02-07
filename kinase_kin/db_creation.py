import csv, sqlite3

# Create a database in RAM
con = sqlite3.connect('KinaseDatabasev1.db')

#A cursor object is required to pinpoint data in the database
cur = con.cursor()

print("Opened database successfully")

#######1: THE KINASE INFORMATION##########
# Creating the table for the general kinase inforamtion
cur.execute("CREATE TABLE KinaseInfo(Uniprot_Accession_Number TEXT PRIMARY KEY NOT NULL, Kinase_Symbol VARCHAR(20) NOT NULL, Kinase_Name VARCHAR(150) NOT NULL, Groups TEXT, Family VARCHAR(20), SubFamily VARCHAR(20), Synonym VARVHAR(100), Function TEXT, Genomic_Location TEXT, Subcellular_Location TEXT, PDB_Image_link TEXT):")
#Populating the general kinase inforamation table
with open ('KinaseInfoFINAL.csv', 'r') as KTable:
	dr_1 = csv.DictReader(KTable) # Uses first line in file as column headings
	to_db_1 = [(i['Uniprot_Accession_Number'],i['Kinase_Symbol '], i['Kinase_Name'],i['Groups '], i['Family'], i['Subfamily'],i['Synonym '], i['Function'], i['Genomic_location'],i['Subcellular_Location '], i['PDB_Image_link ']) for i in dr_1]    #These names must be the same as in the columns of the CSV table

cur.executemany("INSERT INTO KinaseInfo(Uniprot_Accession_Number ,Kinase_Symbol , Kinase_Name, Groups, Family, Subfamily, Synonym, Function, Genomic_location, Subcellular_Location, PDB_Image_link ) VALUES (?,?,?,?,?,?,?,?,?,?,?);", to_db_1)
con.commit() # saves the chages to the database

# Creating the table for the substrate information
cur.excute("CREATE TABLE SubstrateInfo(Substrate_ID PRIMARY KEY NOT NULL, Substrate_ID VARCHAR(50), Kin_ACC_ID TEXT NOT NULL, Kin_Gene TEXT,Kinase TEXT NOT NULL,Substrate_Symbol TEXT NOT NULL, Sub_ACC_ID TEXT NOT NULL,Sub_Gene  TEXT NOT NULL, Sub_Mod_Rsd TEXT NOT NULL,Site_AA VARCHAR(30),Sub_Domain TEXT, FOREIGN KEY (Kinase) REFERENCES KinaseInfo(Kinase_Symbol));")
#Populating the substrate table
with open ('Substrate_FINAL.csv', 'r') as STable:
    dr4 = csv.DictReader(STable) # Uses first line in file as column headings
    to_db4 = [(i['SUBSTRATE_ID'],i['KIN_ACC_ID'],i['KIN_GENE'],i['KINASE'],i['SUBSTRATE_SYMBOL'],i['SUB_ACC_ID'], i['SUB_GENE'], i['SUB_MOD_RSD'], i['SITE_+/-7_AA'], i['SUB_DOMAIN']) for i in dr4]

cur.executemany("INSERT INTO Substrate(Substrate_ID,Kin_ACC_ID,Kin_Gene,Kinase,Substrate_Symbol,Sub_ACC_ID,Sub_Gene,Sub_Mod_Rsd,Site_AA,Sub_Domain) VALUES (?,?,?,?,?,?,?,?,?,?);", to_db4)
con.commit() # saves the chages to the database

# Creating the table for the inhibtor reference
cur.execute("CREATE TABLE InhibitorRef(InhibitorRef_ID INTEGER PRIMARY KEY,CHEMBL_ID TEXT,Kinase_Target TEXT,FOREIGN KEY(Kinase_Target) REFERENCES KinaseInfo(Kinase_Symbol))")

#Populating the table for the inhibitor reference table
with open('Inhibitor_refFINAL.csv','r') as IRTable:
  dr2 = csv.DictReader(IRTable) # Uses first line in file as column headings
  to_db2 = [(i['Inhibitor_RefID'],i['CHEMBL_ID'],i['Kinase_Target']) for i in dr2]
    
cur.executemany("INSERT INTO InhibitorRef(InhibitorRef_ID,CHEMBL_ID,Kinase_Target) VALUES (?,?,?);", to_db2)

con.commit() # saves the chages to the database

#Creating the table for the information on the inhibitors
cur.execute("CREATE TABLE Inhibitor_Info(Inhibitor_Name TEXT PRIMARY KEY,CHEMBLID TEXT,Smiles TEXT,InCHI_Key TEXT,RoF INTEGER,MW NUMERIC,LogP NUMERIC,TPSA NUMERIC,HBA NUMERIC,HBD NUMERIC,NRB NUMERIC,Kinase_Families TEXT,Image_link TEXT,FOREIGN KEY(CHEMBLID) REFERENCES InhibitorRef(CHEMBL_ID))")

#Populating the Inhibitor_info table
with open('Inhibitor_InfoFINAL.csv','r') as IITable:
  dr3 = csv.DictReader(IITable) # Uses first line in file as column headings
  to_db3 = [(i['INN_Name'],i['CHEMBL_ID'],i['Smiles'],i['InChi_Key'],i['RoF'],i['MW'], i['LogP'], i['TPSA'], i['HBA'], i['HBD'], i['NRB'], i['Kinase families'], i['image_link']) for i in dr3]
    
cur.executemany("INSERT INTO Inhibitor_Info(Inhibitor_Name,CHEMBLID,Smiles,InCHI_Key,RoF,MW,LogP,TPSA,HBA,HBD,NRB,Kinase_Families,Image_link) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db3)

con.commit() # saves the chages to the database

#joining tables using the foreign key

cur.execute("SELECT Kinase_Symbol FROM KinaseInfo INNER JOIN Substrate ON Substrate.Kinase = KinaseInfo.Kinase_Symbol ;")
cur.execute("SELECT Kinase_Symbol FROM KinaseInfo INNER JOIN InhibitorRef ON InhibitorRef.Kinase_Target = KinaseInfo.Kinase_Symbol ;")
cur.execute("SELECT CHEMBL_ID FROM InhibitorRef INNER JOIN Inhibitor_Info ON Inhibitor_Info.CHEMBLID = InhibitorRef.CHEMBL_ID ;")

con.close() # Connection must be closed at the end

