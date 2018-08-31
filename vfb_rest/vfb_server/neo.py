import os
from vfb.uk.ac.ebi.vfb.neo4j.KB_tools import kb_writer, iri_generator, KB_pattern_writer
from vfb.uk.ac.ebi.vfb.neo4j.neo4j_tools import results_2_dict_list



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
        self.iri_generator = iri_generator(kb,user,password)
        self.iri_generator.set_default_config()

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
                vid = self.get_datasetid_if_exists(short_form)
                n = self.getDatasetMetadata(vid)
                n['created'] = True
                return n
            except OSError as err:
                print("OS error: {0}".format(err))
            except:
                print("An unexpected error occurred")
                raise

    def create_or_get_neuron(self, primary_name, alternative_names, external_identifiers, orcid, datasetid, anatomical_type):
        print('Getting or creating ID %s' % primary_name)
        #Check if the combination of label and dataset already exists.
        vid = self.get_vfbid_if_exists(primary_name,datasetid)
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
                imaging_type='SB-SEM'
                pw.add_anatomy_image_set(dataset=datasetid,label=primary_name,anatomical_type=anatomical_type,imaging_type=imaging_type,start=98989,template='http://virtualflybrain.org/reports/VFBc_00017894')
                vid = self.get_vfbid_if_exists(primary_name, datasetid)
                if vid:
                    n = self.getNeuronMetadata(vid)
                    n['created'] = True
                    return n
                else:
                    raise Exception('VFB identifier was not successfully created.')
            except OSError as err:
                print("OS error: {0}".format(err))
            except:
                print("An unexpected error occurred")
                raise

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

    def get_datasetid_if_exists(self, short_form):
        q = "MATCH (n:DataSet {short_form: '%s'}) RETURN n" % (short_form)
        print(q)
        result = self.query(q)
        print(result)
        print(type(result))
        if result:
            print("result:true")
            for n in result:
                iri = n['n']['iri']
                print(iri)
                return iri
        else:
            return False

    def getVFBIds(self):
        return self.iri_generator.id_name

    def getNeuronMetadata(self, iri):
        q = "MATCH (n:Individual {iri: '%s'})-[:has_source]-(p) RETURN n,p" % (iri)
        result = self.query(q)
        if result:
            for n in result:
                print(n['n'])
                n = {
                    'vfbid': '%s' % n['n']['iri'],
                    'primary_name': '%s' % n['n']['label'],
                    'neuron_type': '%s' % 'not implemented',
                    'alternative_names': '%s' % 'not implemented',
                    'orcid': '%s' % 'not implemented',
                    'datasetid': '%s' % n['p']['iri'],
                    'external_identifiers': '%s' % 'not implemented'
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
