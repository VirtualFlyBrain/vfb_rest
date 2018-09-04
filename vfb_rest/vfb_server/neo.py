import os
import re

from vfb.uk.ac.ebi.vfb.neo4j.KB_tools import kb_writer, iri_generator, KB_pattern_writer
from vfb.uk.ac.ebi.vfb.neo4j.neo4j_tools import results_2_dict_list


class irigen:
    def __init__(self):
        # os.environ["KBserver"] = "http://localhost:7474"
        # os.environ["KBuser"] = "neo4j"
        # os.environ["KBpassword"] = "neo4j/neo"
        kb = os.getenv('KBserver')
        user = os.getenv('KBuser')
        password = os.getenv('KBpassword')
        q_test='MATCH (n:Individual) RETURN n LIMIT 1'

        self.iri_generator = iri_generator(kb, user, password)
        self.iri_generator.set_default_config()

    def getVFBIds(self):
        return self.iri_generator.id_name

class neo:
    def __init__(self):
        #os.environ["KBserver"] = "http://localhost:7474"
        #os.environ["KBuser"] = "neo4j"
        #os.environ["KBpassword"] = "neo4j/neo"
        kb = os.getenv('KBserver')
        user = os.getenv('KBuser')
        password = os.getenv('KBpassword')
        self.nc = kb_writer(kb, user, password)
        self.pattern_writer = KB_pattern_writer(kb,user,password)
        self.orcid_pattern="^\s*(?:(?:https?://)?orcid.org/)?([0-9]{4})\-?([0-9]{4})\-?([0-9]{4})\-?([0-9]{4})\s*$"

    def create_or_get_dataset(self,name,license='',short_form='',description=''):
        print('Getting or creating dataset %s' % name)
        vid = self.get_datasetid_if_exists(short_form)

        if vid:
            print('DataSet exists!')
            n = self.getDatasetMetadata(vid)
            n['created'] = False
            return n
        else:
            # if it does not exist, generate it
            print('DataSet does not exist!')
            pw = self.pattern_writer
            try:
                pw.add_dataSet(short_form=short_form, name=name, license=license)
                pw.commit()
                vid = self.get_datasetid_if_exists(short_form)
                n = self.getDatasetMetadata(vid)
                n['created'] = True
                return n
            except:
                print("An unexpected error occurred")
                raise

    def create_or_get_person(self,orcid):
        print('Getting or creating person %s' % orcid)
        if not self.valid_orcid(orcid):
            raise Exception('Person was not successfully created. Invalid orcid: ' + orcid+'. Should look similar to http://orcid.org/0000-0000-0000-0001')
        vid = self.get_person_if_exists(orcid)

        if vid:
            print('Person exists!')
            n = self.getPersonMetadata(vid)
            n['created']=False
            return n
        else:
            # if it does not exist, generate it
            print('Person does not exist!')
            pw = self.pattern_writer
            try:
                pw.ni.add_node(labels=["Person",],IRI=orcid)
                pw.ni.commit()
                n = self.getPersonMetadata(orcid)
                n['created'] = True
                return n
            except:
                print("An unexpected error occurred")
                raise

    def valid_orcid(self,orcid):
        return re.match(self.orcid_pattern,orcid)

    def create_or_get_neuron(self, primary_name, alternative_names, external_identifier, orcid, datasetid, anatomical_type, project, classification_comment):
        print('Getting or creating ID %s' % primary_name)
        #Check if the combination of label and dataset already exists.
        did = self.dataset_exists(datasetid)

        if not did:
            raise Exception('VFB identifier was not successfully created. Unknown dataset id '+datasetid)

        ds = self.getDatasetMetadata(datasetid)
        ds_sf = ds['short_form']
        imaging_type = 'SB-SEM'
        label = primary_name + ' of ' + ds['label']

        vid = self.get_vfbid_if_exists(label,datasetid)

        if vid:
            print('Identifier exists!')
            n = self.getNeuronMetadata(vid)
            n['created'] = False
            return n
        else:
            #if it does not exist, generate it
            print('Identifier does not exist!')
            pw = self.pattern_writer
            try:
                if not self.node_exists(anatomical_type,on='short_form'):
                    print('Anatomical type does not exist, setting NEURON')
                    anatomical_type = 'FBbt_00005106'

                sf_template = ''
                dbxrefs = dict()
                print('ORCID: '+orcid)
                orcid = self.get_short_form(orcid)

                if project == "L1EM_Cardona":
                    sf_template = "VFBc_00050000"
                    dbxrefs['VFBsite_catmaid_l1em'] = external_identifier
                elif project == "FAFB":
                    sf_template = "VFBc_00017894"
                    #dbxrefs['VFBsite_catmaid_l1em'] = external_identifier
                else:
                    raise Exception('VFB identifier was not successfully created. Unknown project ' + project)

                #self.get_short_form(iri='http://virtualflybrain.org/reports/VFBc_00017894')
                anatomy_attributes = dict()
                anatomy_attributes['synonyms'] = alternative_names.split('|')

                start = 98989

                print("Dataset: " + ds_sf)
                print("LABEL: " + label)
                print("Anatomical Type: " + anatomical_type)
                print("Imaging Type: " + imaging_type)
                print("START: " + str(start))
                print("TEMPLATE: " + sf_template)
                print("ANATOMY_ATTRIBUTE: " + str(anatomy_attributes))
                print("ORCID: " + str(orcid))
                print("DBXREFS: " + str(dbxrefs))


                pw.add_anatomy_image_set(dataset=ds_sf,label=label,anatomical_type=anatomical_type,imaging_type=imaging_type,start=start,template=sf_template, anatomy_attributes=anatomy_attributes,orcid=orcid, dbxrefs=dbxrefs, hard_fail=True)
                pw.commit()
                vid = self.get_vfbid_if_exists(label, datasetid)
                print(":::Y:::"+str(vid))
                if vid:
                    n = self.getNeuronMetadata(vid)
                    print(":::Z:::")
                    n['created'] = True
                    return n
                else:
                    raise Exception('VFB identifier was not successfully created.')
            except Exception as e:
                raise Exception("Neuron creation failed: "+str(e))


    def get_vfbid_if_exists(self, primary_name, datasetid):
        q = "MATCH (n:Individual {label: '%s'})-[:has_source]-(p {iri:'%s'}) RETURN n,p" % (primary_name, datasetid)
        result = self.query(q)
        if result:
            for n in result:
                iri = n['n']['iri']
                print(iri)
                return iri
        else:
            return False

    def get_short_form(self,iri):
        q = "MATCH (n {iri: '%s'}) RETURN n" % iri
        result = self.query(q)
        if result:
            for n in result:
                sf = n['n']['short_form']
                return sf
        else:
            return False

    def get_datasetid_if_exists(self, short_form):
        q = "MATCH (n:DataSet {short_form: '%s'}) RETURN n" % (short_form)
        print(q)
        result = self.query(q)
        if result:
            for n in result:
                iri = n['n']['iri']
                print(iri)
                return iri
        else:
            return False

    def get_person_if_exists(self, orcid):
        q = "MATCH (n:Person {iri: '%s'}) RETURN n" % (orcid)
        print(q)
        result = self.query(q)
        if result:
            for n in result:
                iri = n['n']['iri']
                print(iri)
                return iri
        else:
            return False

    def dataset_exists(self, id):
        q = "MATCH (n:DataSet {iri: '%s'}) RETURN n" % (id)
        print(q)
        result = self.query(q)
        if result:
            return True
        else:
            return False

    def node_exists(self, id,on='iri'):
        q = "MATCH (n {%s: '%s'}) RETURN n" % (on,id)
        print(q)
        result = self.query(q)
        if result:
            return True
        else:
            return False

    def getNeuronMetadata(self, iri):
        q = "MATCH (n:Individual {iri: '%s'})-[:has_source]-(p) MATCH (n)-[:Annotation]-(o) MATCH (n)-[:INSTANCEOF]-(c:Class) MATCH (n)-[:database_cross_reference]-(d) RETURN n,p,c,o,d" % (iri)
        #q = "MATCH (n:Individual {iri: '%s'})-[:has_source]-(p) RETURN n,p" % (iri)
        result = self.query(q)
        if result:
            for n in result:
                print('ahsiahj')
                print(n['n'])
                n = {
                    'vfbid': '%s' % n['n']['iri'],
                    'primary_name': '%s' % n['n']['label'],
                    'neuron_type': '%s' % n['c']['iri'],
                    'alternative_names': '%s' % "|".join(n['n']['synonyms']),
                    'orcid': '%s' % n['o']['iri'],
                    'datasetid': '%s' % n['p']['iri'],
                    'external_identifiers': '%s' % n['d']['short_form'],
                    'classification_comment': '%s' % 'not implemented'
                }
                return n
        else:
            return False

    def getPersonMetadata(self, iri):
        q = "MATCH (n:Person {iri:'%s'}) RETURN n" % (iri)
        result = self.query(q)
        if result:
            for n in result:
                print('ahsiahj')
                print(n['n'])
                n = {
                    'orcid': '%s' % iri,
                }
                return n
        else:
            return False

    def getDatasetMetadata(self, iri):
        q = "MATCH (n:DataSet {iri: '%s'}) RETURN n" % (iri)

        result = self.query(q)
        if result:
            for n in result:
                iri = n['n']['iri']
                print(iri)
                n = {
                    'datasetid': '%s' % n['n']['iri'],
                    'label': '%s' % n['n']['label'],
                    'short_form': '%s' % n['n']['short_form']
                }
                return n
        else:
            return False


    def query(self, q):
        print(q)
        return results_2_dict_list(self.nc.nc.commit_list([q]))
