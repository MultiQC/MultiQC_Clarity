
from genologics.lims import Lims
from genologics.config import BASEURI, USERNAME, PASSWORD

from multiqc.utils import report, config
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import table

from collections import OrderedDict
import logging
import re

class MultiQC_clarity_metadata(BaseMultiqcModule):
    def __init__(self):

        self.log = logging.getLogger('multiqc')

        # Check that this plugin hasn't been disabled
        if config.kwargs.get('disable_clarity', False) is True:
            self.log.info("Skipping MultiQC_Clarity as disabled on command line")
            return None
        if getattr(config, 'disable_clarity', False) is True:
            self.log.debug("Skipping MultiQC_Clarity as specified in config file")
            return None

        super(MultiQC_clarity_metadata, self).__init__(name='Clarity LIMS', anchor='clarity')

        self.intro = '''<p>The <a href="https://github.com/MultiQC/MultiQC_Clarity" target="_blank">MultiQC_Clarity</a>
            plugin fetches data from a specified
            <a href="https://www.genologics.com/clarity-lims/" target="_blank">Basespace Clarity LIMS</a> instance.</p>'''

        self.lims = Lims(BASEURI, USERNAME, PASSWORD)
        self.metadata = {}
        self.header_metadata = {}
        self.general_metadata = {}
        self.tab_metadata = {}
        self.samples = []

        self.schema = getattr(config, 'clarity', None)
        if self.schema is None:
            self.log.debug("No config found for MultiQC_Clarity")
            return None

        self.name_edit_regex = self.schema.get("name_edit_regex")

        self.get_samples()
        self.get_metadata('report_header_info')
        self.get_metadata('general_stats')
        self.get_metadata('clarity_module')
        self.update_multiqc_report()
        self.make_sections()
        report.modules_output.append(self)


    def get_samples(self):
        if config.kwargs.get('clarity_project'):
            pj = self.lims.get_projects(name=config.kwargs['clarity_project'])
            if len(pj) > 1:
                self.log.error("Found multiple match projects in Clarity.")
            elif len(pj) < 1:
                self.log.error("Could not identify project in Clarity.")
            else:
                self.samples = self.lims.get_samples(projectlimsid=pj[0].id)
        else:
            names = set()
            for x in report.general_stats_data:
                names.update(x.keys())
            for d in report.saved_raw_data.values():
                try:
                    self.names.update(d.keys())
                except AttributeError:
                    pass
            if not config.kwargs.get('clarity_skip_edit_names'):
                names = self.edit_names(names)

            self.log.info("Looking into Clarity for samples {}".format(", ".join(names)))
            found = 0
            try:
                for name in names:
                    matching_samples = self.lims.get_samples(name=name)
                    if not matching_samples:
                        self.log.error("Could not find a sample matching {0}, skipping.".format(name))
                        continue
                    if len(matching_samples) > 1:
                        self.log.error("Found multiple samples matching {0}, skipping".format(name))
                        continue
                    found += 1
                    self.samples.append(matching_samples[0])
            except Exception as e:
                self.log.warn("Could not connect to Clarity LIMS: {}".format(e))
                return None
            self.log.info("Found {} out of {} samples in LIMS.".format(found, len(names)))


    def edit_names(self, names):
        if self.name_edit_regex:
            return self.edit_names_with_regex(names)

        edited=[]
        for name in names:
            if name.endswith("_1") or name.endswith("_2"):
                edited.append(name[:-2])
            elif name.endswith("_R1") or name.endswith("_R2"):
                edited.append(name[:-3])
            else:
                edited.append(name)

        return edited

    def edit_names_with_regex(self, names):
        edited = []
        for name in names:
            matches = re.search(re.compile(self.name_edit_regex), name)
            edited.append(matches.group(1))
        return edited

    def flatten_metadata(self, metadata):
        for first_level in metadata:
            for second_level in metadata[first_level]:
                if isinstance(metadata[first_level][second_level], set) or isinstance(metadata[first_level][second_level], list):
                    metadata[first_level][second_level] = ", ".join(metadata[first_level][second_level])

        return metadata

    def get_project_metadata(self, udfs):
        project_metadata={}
        for sample in self.samples:
            project_metadata[sample.project.name]={}
            for udf in udfs:
                if udf in sample.project.udf:
                    try:
                        project_metadata[sample.project.name][udf].add(str(sample.project.udf[udf]))
                    except:
                        project_metadata[sample.project.name][udf] = set()
                        project_metadata[sample.project.name][udf].add(str(sample.project.udf[udf]))

        return self.flatten_metadata(project_metadata)

    def get_sample_metadata(self, udfs):
        sample_metadata={}
        for sample in self.samples:
            sample_metadata[sample.name]={}
            for udf in udfs:
                if udf in sample.udf:
                    try:
                        sample_metadata[sample.name][udf].add(str(sample.udf[udf]))
                    except:
                        sample_metadata[sample.name][udf] = set()
                        sample_metadata[sample.name][udf].add(str(sample.udf[udf]))

        return self.flatten_metadata(sample_metadata)


    def get_metadata(self, part):
        for key in self.schema[part]:
            if key == 'Project':
                metadata = self.get_project_metadata(self.schema[part]['Project'])
            elif key == 'Sample':
                metadata =self.get_sample_metadata(self.schema[part]['Sample'])
            else:
                metadata = self.get_artifact_metadata(self.schema[part])

            if part == "report_header_info":
                self.header_metadata.update(metadata)
            elif part == "general_stats":
                self.general_metadata.update(metadata)
            else:
                self.tab_metadata.update(metadata)


    def get_artifact_metadata(self, pt_to_udfs):
        artifact_metadata={}
        for sample in self.samples:
            artifact_metadata[sample.name]={}
            for process_type in pt_to_udfs:
                if process_type == 'Sample':
                    continue
                if process_type == 'Project':
                    continue
                artifacts = self.lims.get_artifacts(sample_name=sample.name, process_type=process_type)
                for udf_name in pt_to_udfs[process_type].get("outputs", []):
                    values = []
                    for artifact in artifacts:
                        if udf_name in artifact.udf:
                            values.append(str(artifact.udf[udf_name]))

                    artifact_metadata[sample.name][udf_name]=values

                processes = set([art.parent_process for art in artifacts])
                inputs=[]
                for p in processes:
                    inputs.extend([art for art in p.all_inputs() if sample.name in [s.name for s in art.samples]])
                for udf_name in pt_to_udfs[process_type].get("inputs", []):
                    values = []
                    for artifact in inputs:
                        if udf_name in artifact.udf:
                            values.append(str(artifact.udf[udf_name]))

                    artifact_metadata[sample.name][udf_name]=values

        return self.flatten_metadata(artifact_metadata)


    def update_multiqc_report(self):
        if config.report_header_info is None:
            config.report_header_info = []
        for first_level in self.header_metadata:
            d = {}
            for key in self.header_metadata[first_level]:
                d[key] = self.header_metadata[first_level][key]
            config.report_header_info.append(d)

        headers = {}
        for first_level in self.schema["general_stats"]:
            for header in self.schema["general_stats"][first_level]:
                headers[header] = {}
                if isinstance(self.schema["general_stats"][first_level][header], dict):
                    for subsubkey, cfg in self.schema["general_stats"][first_level][header].items():
                        if subsubkey == 'multiply_by':
                            mby = str(cfg)[:]
                            headers[header]['modify'] = lambda x: float(x) * float(mby)
                        else:
                            headers[header][subsubkey] = cfg
                headers[header]['description'] = headers[header].get('description', '{} - {}'.format(first_level, header))
                headers[header]['namespace'] = headers[header].get('namespace', 'Clarity LIMS')
                headers[header]['scale'] = headers[header].get('scale', 'YlGn')

        report.general_stats_headers.append(headers)
        report.general_stats_data.append(self.general_metadata)

    def make_sections(self):
        headers = OrderedDict()
        for first_level in self.tab_metadata:
            for header in self.tab_metadata[first_level]:
                desc = header
                if header not in headers:
                    headers[header] = {}
                    for key in self.schema['clarity_module']:
                        if header in self.schema['clarity_module'][key]:
                            desc = key
                        elif isinstance(self.schema['clarity_module'][key], dict):
                            for subkey, val in self.schema['clarity_module'][key].items():
                                # print(val)
                                if val is None:
                                    break
                                elif header in val:
                                    desc = key
                                    if isinstance(val[header], dict):
                                        for subsubkey, cfg in val[header].items():
                                            if subsubkey == 'multiply_by':
                                                mby = str(cfg)[:]
                                                headers[header]['modify'] = lambda x: float(x) * float(mby)
                                            else:
                                                headers[header][subsubkey] = cfg

                    headers[header]['namespace'] = headers[header].get('namespace', desc)
                    headers[header]['title'] = headers[header].get('title', header)
                    headers[header]['description'] = headers[header].get('description', header)

        self.intro += table.plot(self.tab_metadata, headers)


