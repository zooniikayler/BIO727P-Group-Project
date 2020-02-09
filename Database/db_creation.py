import sqlite3,csv # Importing the required modules

conn = sqlite3.connect("KinaseDatabasev1.db") #Creates the databasefile in memory

c = conn.cursor() #cursor object that connects to the database

# Creating the table for the general kinase inforamtion
c.execute("""CREATE TABLE KinaseInfo(
          Uniprot_Accession_Number TEXT PRIMARY KEY NOT NULL,
          Kinase_Symbol VARCHAR(20) NOT NULL,
          Kinase_Name VARCHAR(150) NOT NULL,
          Groups TEXT,
          Family VARCHAR(20),
          SubFamily VARCHAR(20),
          Synonym VARVHAR(100),
          Function TEXT,
          Genomic_Location TEXT,
          Subcellular_Location TEXT,
          PDB_Image_link TEXT)
          """)

#Populating the general kinase inforamation table
with open('Kinase_InfoFINAL.csv','r') as KTable: 
    dr1 = csv.DictReader(KTable) # Uses first line in file as column headings
    to_db1 = [(i['Uniprot_Accession_Number'],
              i['Kinase_Symbol '],
              i['Kinase_Name'],
              i['Group'],
              i['Family'], 
              i['SubFamily'], 
              i['Synonym'], 
              i['Function'], 
              i['Genomic_location'], 
              i['Subcellular_location'], 
              i['PDB_image_link']) for i in dr1]
    
c.executemany("INSERT INTO KinaseInfo(Uniprot_Accession_Number,Kinase_Symbol,Kinase_Name, Groups, Family, SubFamily,Synonym,Function,Genomic_Location, Subcellular_Location, PDB_Image_link) VALUES (?,?,?,?,?,?,?,?,?,?,?);", to_db1)

conn.commit() # saves the chages to the database

# Creating the table for the inhibtor reference
c.execute("""CREATE TABLE InhibitorRef(
           InhibitorRef_ID INTEGER PRIMARY KEY,
           CHEMBL_ID TEXT,
           Kinase_Target TEXT,
           FOREIGN KEY(Kinase_Target) REFERENCES KinaseInfo(Kinase_Symbol)
           )""")

#Populating the table for the inhibitor reference table
with open('Inhibitor_refFINAL.csv','r') as IRTable:
    dr2 = csv.DictReader(IRTable) # Uses first line in file as column headings
    to_db2 = [(i['Inhibitor_RefID'],
               i['CHEMBL_ID'],
               i['Kinase_Target']) for i in dr2]
    
c.executemany("INSERT INTO InhibitorRef(InhibitorRef_ID,CHEMBL_ID,Kinase_Target) VALUES (?,?,?);", to_db2)

conn.commit() # saves the chages to the database

#Creating the table for the information on the inhibitors
c.execute("""CREATE TABLE Inhibitor_Info(
            Inhibitor_Name TEXT PRIMARY KEY,
            CHEMBLID TEXT,
            Smiles TEXT,
            InCHI_Key TEXT,
            RoF INTEGER,
            MW NUMERIC,
            LogP NUMERIC,
            TPSA NUMERIC,
            HBA NUMERIC,
            HBD NUMERIC,
            NRB NUMERIC,
            Kinase_Families TEXT,
            Image_link TEXT,
            FOREIGN KEY(CHEMBLID) REFERENCES InhibitorRef(CHEMBL_ID)
            )""")

#Populating the Inhibitor_info table
with open('Inhibitor_InfoFINAL.csv','r') as IITable:
    dr3 = csv.DictReader(IITable) # Uses first line in file as column headings
    to_db3 = [(i['INN_Name'],
               i['CHEMBL_ID'],
               i['Smiles'],
               i['InChi_Key'],
               i['RoF'],
               i['MW'], 
               i['LogP'], 
               i['TPSA'], 
               i['HBA'], 
               i['HBD'], 
               i['NRB'], 
               i['Kinase families'], 
               i['image_link']) for i in dr3]
    
c.executemany("INSERT INTO Inhibitor_Info(Inhibitor_Name,CHEMBLID,Smiles,InCHI_Key,RoF,MW,LogP,TPSA,HBA,HBD,NRB,Kinase_Families,Image_link) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db3)

conn.commit() # saves the chages to the database

# Creating the table for the substrate information
c.execute("""CREATE TABLE SubstrateInfo(
            Substrate_ID INTEGER PRIMARY KEY NOT NULL,
            Kin_ACC_ID TEXT NOT NULL,
            Kin_Gene TEXT,
            Kinase TEXT NOT NULL,
            Substrate_Symbol TEXT NOT NULL,
            Sub_ACC_ID TEXT NOT NULL,
            Sub_Gene TEXT NOT NULL,
            Sub_Mod_Rsd TEXT NOT NULL,
            Site_AA VARCHAR(30),
            Sub_Domain TEXT,
            Chromosome INTEGER,
            Leg TEXT,
            FOREIGN KEY (Kinase) REFERENCES KinaseInfo(Kinase_Symbol)
            )""")

#Populating the substrate table
with open('Substrate_FINAL.csv','r') as STable:
    dr4 = csv.DictReader(STable) # Uses first line in file as column headings
    to_db4 = [(i['SUBSTRATE_ID'],
               i['KIN_ACC_ID'],
               i['KIN_GENE'],
               i['KINASE'],
               i['SUBSTRATE_SYMBOL'],
               i['SUB_ACC_ID'], 
               i['SUB_GENE'], 
               i['SUB_MOD_RSD'], 
               i['SITE_AA'], 
               i['SUB_DOMAIN'],
               i['CHROMOSOME'],
               i['LEG']) for i in dr4]
    
c.executemany("INSERT INTO SubstrateInfo(Substrate_ID,Kin_ACC_ID,Kin_Gene,Kinase,Substrate_Symbol,Sub_ACC_ID,Sub_Gene,Sub_Mod_Rsd,Site_AA,Sub_Domain,Chromosome,Leg) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", to_db4)

conn.commit() # saves the chages to the database

#joining tables using the foreign key

c.execute("SELECT Kinase_Symbol FROM KinaseInfo INNER JOIN SubstrateInfo ON SubstrateInfo.Kinase = KinaseInfo.Kinase_Symbol ;")
c.execute("SELECT Kinase_Symbol FROM KinaseInfo INNER JOIN InhibitorRef ON InhibitorRef.Kinase_Target = KinaseInfo.Kinase_Symbol ;")
c.execute("SELECT CHEMBL_ID FROM InhibitorRef INNER JOIN Inhibitor_Info ON Inhibitor_Info.CHEMBLID = InhibitorRef.CHEMBL_ID ;")

conn.close() # Connection must be closed at the end