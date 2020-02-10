from kinase_kin.app import db

class KinaseInfo(db.Model):
    """"""
    __tablename__ = "KinaseInfo" #Selects the the KinaseInfo table from the db
   
    Uniprot_Accession_Number = db.Column('Uniprot_Accession_Number', db.String, primary_key = True)
    Kinase_Symbol = db.Column('Kinase_Symbol', db.String)
    Kinase_Name = db.Column('Kinase_Name', db.String)
    Groups = db.Column('Groups', db.String)
    Family = db.Column('Family', db.String)
    SubFamily = db.Column('SubFamily', db.String)
    Synonym = db.Column('Synonym', db.String)
    Function = db.Column('Function', db.String)
    Genomic_location = db.Column('Genomic_Location', db.String)
    Subcellular_Location = db.Column('Subcellular_Location', db.String)
    PDB_Image_link = db.Column('PDB_Image_link', db.String)
    
class SubstrateInfo(db.Model):
    """"""
    __tablename__ = "SubstrateInfo" #Selects the the SubstrateInfo table from the db
    
    Substrate_ID = db.Column('Substrate_ID', db.Integer, primary_key = True)
    Kin_ACC_ID = db.Column('Kin_ACC_ID', db.String)
    Kin_Gene = db.Column('Kin_Gene', db.String)
    Kinase = db.Column('Kinase', db.String)
    Substrate_Symbol = db.Column('Substrate_Symbol', db.String)
    Sub_ACC_ID = db.Column('Sub_ACC_ID', db.String)
    Sub_Gene = db.Column('Sub_Gene', db.String)
    Sub_Mod_Rsd = db.Column('Sub_Mod_Rsd', db.String)
    Site_AA = db.Column('Site_AA', db.String)
    Sub_Domain = db.Column('Sub_Domain', db.String)
    Chromosome = db.Column('Chromosome', db.Integer)
    Leg = db.Column('Leg', db.String)

class InhibitorInfo(db.Model): 
    """"""
    __tablename__ = "Inhibitor_Info" #Selects the the Inhibitor_Info table from the db
    
    Inhibitor_Name = db.Column('Inhibitor_Name', db.String, primary_key = True)
    CHEMBLID = db.Column('CHEMBLID', db.String)
    Smiles = db.Column('Smiles', db.String)
    Brand_Name = db.Column('Brand_Name', db.String)
    Phase = db.Column('Phase', db.String)
    InCHI_Key = db.Column('InCHI_Key', db.String)
    LigID = db.Column('LigID', db.String)
    PDBID = db.Column('PDBID', db.String)
    Type = db.Column('Type', db.String)
    RoF = db.Column('RoF', db.Integer)
    MW = db.Column('MW', db.Integer)
    LogP = db.Column('LogP', db.Integer)
    TPSA = db.Column('TPSA', db.Integer)
    HBA = db.Column('HBA', db.Integer)
    HBD = db.Column('HBD', db.Integer)      
    NRB = db.Column('NRB', db.Integer)  
    Kinase_Families = db.Column('Kinase_Families', db.String)
    Chirality = db.Column('Chirality', db.String)
    Inhibitor_Synonyms = db.Column('Inhibitor_Synonyms', db.String)
    Image_link = db.Column('Image_link', db.String)
    

class InhibitorRef(db.Model):
    """"""
    __tablename__ = "InhibitorRef" #Selects the the InhibitorRef table from the db
    
    CHEMBL_ID = db.Column("CHEMBL_ID", db.String, primary_key = True)
    Kinase_Target = db.Column('Kinase_Target', db.String)
