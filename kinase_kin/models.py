from app import db

class KinaseInfo(db.Model):
    """"""
    __tablename__ = "KinaseInfo"
   
    Unique_ID = db.Column('Unique_ID', db.Integer, primary_key = True)
    Uniprot_Accession_Number = db.Column('Uniprot_Accession_Number', db.String)
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
    
class Substrate(db.Model):
    """"""
    __tablename__ = "Substrate"
    
    Substrate_ID = db.Column('Substrate_ID', db.Integer, primary_key = True)
    Kin_ACC_ID = db.Column('Kin_ACC_ID', db.String)
    Kin_Gene = db.Column('Kin_Gene', db.String)
    Kinase = db.Column('Kinase', db.String)
    Substrate = db.Column('Substrate', db.String)
    SubFamily = db.Column('SubFamily', db.String)
    Sub_ACC_ID = db.Column('Sub_Gene', db.String)
    Sub_Mod_Rsd = db.Column('Sub_Mod_Rsd', db.String)
    Site_AA = db.Column('Site_AA', db.String)
    Sub_Domain = db.Column('Sub_Domain', db.String)

class InhibitorInfo(db.Model):
    """"""
    Inhibitor_Name = db.Column('Inhibitor_Name', db.String, primary_key = True)
    CHEMBLID = db.Column('CHEMBLID', db.String)
    Kinase_Target = db.Column('Kinase_Target', db.String)
    Smiles = db.Column('Smiles', db.String)
    InCHI_Key = db.Column('InCHI_Key', db.String)
    RoF = db.Column('RoF', db.Integer)
    MW = db.Column('MW', db.Integer)
    LogP = db.Column('LogP', db.Integer)
    TPSA = db.Column('TPSA', db.Integer)
    HBA = db.Column('HBA', db.Integer)
    HBD = db.Column('HBD', db.Integer)      
    NRB = db.Column('NRB', db.Integer)  
    Kinase_Families = db.Column('Kinase_Families', db.String)
    Image_link = db.Column('Image_link', db.String)  
