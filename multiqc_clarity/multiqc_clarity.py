
from genologics.lims import *
from genologics.config import BASEURI, USERNAME, PASSWORD

import logging
import yaml

class MultiQC_clarity_metadata(object):
    def __init__(self, conf_file, sample_names):
        self.conf_file = conf_file
        self.lims = Lims(BASEURI, USERNAME, PASSWORD)
        self.log = logging.getLogger('multiqc')
        self.metadata = {}
        self.names = sample_names
        with open(conf_file) as cf:
            self.schema = yaml.load(cf)


    def get_clarity_metadata(self):
        for sn in self.names:
            matching_samples = self.lims.get_samples(name=sn)
            if not matching_samples:
                self.log.error("Could not find a sample matching {0}, skipping.".format(sn))
                continue
            if len(matching_samples) > 1:
                self.log.error("Found multiple samples matching {0}, skipping".format(sn))
                continue
            sample = matching_samples[0]
            self.metadata[sn] = {}
            for process_type in self.schema:
                    artifacts = self.lims.get_artifacts(sample_name=sample.name, process_type=process_type)
                    for udf_name in self.schema[process_type].get("outputs", []):
                        values = []
                        for artifact in artifacts:
                            if udf_name in artifact.udf:
                                values.append(artifact.udf[udf_name])

                        self.metadata[sn][udf_name]=values

                    processes = set([art.parent_process for art in artifacts])
                    inputs=[]
                    for p in processes:
                        inputs.extend([art for art in p.all_inputs() if sample.name in [s.name for s in art.samples]])
                    for udf_name in self.schema[process_type].get("inputs", []):
                        values = []
                        for artifact in inputs:
                            if udf_name in artifact.udf:
                                values.append(artifact.udf[udf_name])

                        self.metadata[sn][udf_name]=values







if __name__=="__main__":
    k = MultiQC_clarity_metadata("../example.yaml", ["P5651_101", "P5651_102"])
    k.get_clarity_metadata()
    import pprint
    pprint.pprint(k.metadata)

