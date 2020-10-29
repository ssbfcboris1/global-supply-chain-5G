#!/usr/bin/env python
# coding: utf-8

# ## Tools and resources
# 
# - An open-source [graph database](https://neo4j.com/developer/get-started/?ref=footer)
# 
# - An open-source [data souce](https://permid.org/)
# 

# In[1]:


from OpenPermID import OpenPermID
from neo4j import GraphDatabase
import rdflib


# ![image.png](attachment:image.png)

# In[2]:


"""
Before uploading this notebook to GitHub, replace API Key string 
with "<API Key>".
"""
opid = OpenPermID()
opid.set_access_token("zS54mFFZvrTd8Eu8gyxwkGVfaTQQfp0M")


# In[3]:


# API call to obtain www.permID.org data on companies in 5G supply chain
output,err = opid.matchFile("./data/Global_Supply_Chain_Players_5G.csv")


# In[4]:


output.head()


# In[5]:


# drop rows with Null values (corporate entities without 
# record on www.permID.org.) 
output = output[output['Input_LocalID'].notna()]


# In[6]:


# Select relevant fields from return from the API call.
players_df = output[['Input_Name', 
                     'Match OpenPermID', 
                     'Match OrgName', 
                     'Match Score', 
                     'Match Level']]


# In[7]:


# Eliminate low "Match Score" players
high_score_companies = (players_df['Match Score']
                        .apply(lambda x: int(x[:-1])) > 50)
players_5G_df = players_df[high_score_companies]
players_5G_df


# ### For demo purposes, here I use the permid.org API to read a news item in text string format.
# 
# In production, the Python driver can upload a query to www.permid.org in the form of "PDF, XML or RDF files, OR even a folder."
# 
# https://permid.org/onecalaisViewer

# In[8]:


raw_text = """
Apple gets into 5G race; acquires Intel phone
modem business for $1 billion
Apple will hold over 17,000 wireless technology patents, ranging from protocols for cellular standards to
modem architecture and modem operation
IANS | San Francisco July 26, 2019 Last Updated at 09:58 IST
American technology company Apple has announced the acquisition of
chip-maker Intel's smartphone modem business for $1 billion.
Approximately 2,200 Intel employees will join Apple, along with intellectual property, equipment and leases,
the Cupertino-based iPhone maker said in a statement late Thursday.
The transaction is expected to close in the fourth quarter of 2019.
"This agreement enables us to focus on developing technology for the 5G network while retaining critical
intellectual property and modem technology that our team has created," said Intel CEO Bob Swan.
"We're looking forward to putting our full effort into 5G where it most closely aligns with the needs of our
global customer base, including network operators, telecommunications equipment manufacturers and cloud
service providers," he added.
7/13/2020 https://www.business-standard.com/article/printer-friendly-version?article_id=119072600214_1
https://www.business-standard.com/article/printer-friendly-version?article_id=119072600214_1 2/2
Apple will hold over 17,000 wireless technology patents, ranging from protocols for cellular standards to
modem architecture and modem operation.
Intel will retain the ability to develop modems for non-smartphone applications, such as PCs, internet-of-things
devices and autonomous vehicles.
Johny Srouji, Apple's senior vice president of Hardware Technologies said that Apple is excited to have
excellent engineers join its growing cellular technologies group.
"They, together with our significant acquisition of innovative IP, will help expedite our development on future
products and allow Apple to further differentiate moving forward," he added.
Apple has been working on its own chips for quite some time. Acquiring Intel's technology could help the
iPhone maker accelerate its plans.
Apple may have paid chip-maker Qualcomm somewhere between $5 billion-$6 billion for an agreement to
dismiss all ongoing litigations, including those with Apple's contract manufacturers.
Intel had been working on a chipset for the iPhone maker, with the chip expected to be part of iPhones by 2020.
"""


# In[9]:


# Store the return of the permID.org API call, which includes 
# "intelligent tags" of corporate entities and their relationships.
output,err = opid.calais(raw_text, outputFormat='rdf')


# ### Brief intro of the RDF files, mentioning the Python eco-system has taken note of RDF, as evidences as a package dealing with RDF:
# 
# https://rdflib.readthedocs.io/en/stable/index.html

# In[10]:


# analyze the return of the API call with the Python rdflib library
g = rdflib.Graph()

# which includes parsing the Resource Description Format (RDF) triples.parse a RDF file 
result = g.parse(output)

# loop through each triple in the graph (subj, pred, obj)
for subj, pred, obj in g:
    # check if there is at least one triple in the Graph
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")

# print the number of "triples" in the Graph
print("graph has {} statements.".format(len(g)))
# prints graph has 86 statements.

# print out the entire Graph in the RDF Turtle format
print(g.serialize(format="turtle").decode("utf-8"))


# - Next, read the RDF files into a neo4j instance to develop a knowledge graph ("property graph" in Neo4j parlance).
# 
# - See a separate notebook with a script written in Neo4j's Cypher language (a SQL-like graph database query language).  
# 
# https://neo4j.com/docs/api/python-driver/current/api.html

# In[ ]:




