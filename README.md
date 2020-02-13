Team Zoonii - QMUL MSc Bioinformatics
Kinase Kinpendium: Software Group Development Project
Kinase Kinpendium was developed by Team Zoonii – a group of 3 students that are part of the MSc Bioinformatics Programme at Queen Mary University of London, under the supervision of Professor Conrad Bessant and Dr Fabrizio Smeraldi.

Kinase Kinpendium is a database that allows the user to explore kinase-substrate relationships, kinase-inhibitor relationships, and the neighboring genetic environment of phosphosites. Additionally, Kinase Kinpendium includes a data analysis tool that allows the user to upload experimental phosphoproteomics data and produces several visualisations to represent kinase activity. 

Website Link
http://Kinase-Kinpendium.us-east-2.elasticbeanstalk.com

Getting Started
To run on your localhost please download the directory 'kinase_kin'.

Once downloaded please open and run the 'db_creation.py' to create and populate the database called 'KinaseDatabaseV1.db'.

The packages required
Python                             3.7.0
Flask                              1.1.1
Flask-SQLAlchemy                   2.4.1
Flask-Table                        0.5.0
Flask-WTF                          0.14.2
Jinja2                             2.10.3
jupyter                            1.0.0
pandas                             0.25.1
requests                           2.21.0
beautifulsoup4                     4.8.0
bokeh                              1.3.4

To install these:

pip install Python                       
pip install Flask                          
pip install Flask-SQLAlchemy                  
pip install Flask-Table                     
pip install Flask-WTF                      
pip install Jinja2                             
pip install jupyter                            
pip install pandas                            
pip install requests                      
pip install beautifulsoup4                    
pip install bokeh                              

Running the website
In your commandline open the 'kinase_kin' directory and run the following command:

python export FLASK_APP=main.py
python flask run
Copy the localhost URL and paste it into your browser.

This would lead you to the homepage of 'Kinase Kinpendium'. For full instructions read our documentation. 

Authors
Mohomed Ali - MuhammadAli-ai
Numaan Akbar Iqbar - Numzy97
Zoonii Kayler - zooniikayler
Raz - 

Acknowledgments
Thank you to Professor Conrad Bessant and Dr Fabrizio Smeraldi for your support.
