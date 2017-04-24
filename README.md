# [<img src="docs/images/MultiQC_logo.png" width="250" title="MultiQC">](https://github.com/ewels/MultiQC) [<img src="docs/images/clarity_logo.png" width="250" title="Clarity LIMS">](https://www.genologics.com/clarity-lims/)

**MultiQC_Clarity is a plugin for MultiQC, able to insert project-level and sample-level metadata from the BaseSpace Clarity LIMS into MultiQC Reports**

For more information about MultiQC, see [http://multiqc.info](http://multiqc.info)

For more information about BaseSpace Clarity LIMS, see [https://www.genologics.com/clarity-lims/](https://www.genologics.com/clarity-lims/)

## Description
MultiQC_Clarity connects to your Clarity LIMS installation using the API. MultiQC runs as normal, generating a list of sample names based on the contents of the files found. These sample names are passed to the MultiQC_Clarity plugin, which searches your Clarity LIMS installation for matching sample names. If exact matches are found, then the metadata configured in the config file is retrieved and entered into the report.

## Installation

### Plugin Installation
This plugin will hopefully soon be available on the Python Package Index. Until then, you can install it from GitHub directly using `pip`:

```bash
pip install --upgrade --force-reinstall git+https://github.com/MultiQC/MultiQC_Clarity.git
```

Alternatively, you can download or clone this repository and install it manually:

```bash
python setup.py install
```

### Genologics Package
The MultiQC_Clarity plugin uses the Genologics Python package, available on PyPI. This needs to be configured first. Create a file called `.genologicsrc` in your user's home directory that looks as follows:

```
[genologics]
BASEURI=https://your.installation.com
USERNAME=[YOUR-USERNAME]
PASSWORD=[YOUR-PASSWORD]
```

## Configuration
Before MultiQC_Clarity will work with MultiQC, you need to tell it what information to retrieve from the LIMS. Unfortunately, as every Clarity installation is different from the next, this cannot be automated.

To do this, you need to add to your MultiQC configuration. See the
[main MultiQC documentation](http://multiqc.info/docs/#configuring-multiqc)
for more information on how to do this. For a single run, you can just create
a file called `multiqc_config.yaml` in the working directory.

See the bundled [`multiqc_config_example.yaml`](multiqc_config_example.yaml)
file to see a real-life example of this.

There are three parts in the MultiQC report where you can add content - the report header (typically project-level information), the _General Statistics_ table and as a section in the report. The required configuration is broken into the same three sections.

Next, you need to specify which Clarity LIMS entity you want to retrieve information from. This can be `Project`, `Sample` or the name of a step.

If `Project` or `Sample`, the next level of configuration is the UDF name that you want to load. If it's a step, you need to specify either `outputs` or `inputs`.

For example, a basic setup with minimal configuration could be:

```yaml
clarity:
    report_header_info:
        Project:
            'custom UDF name':
            'another custom UDF':
    general_stats:
        Sample:
            'a custom UDF':
    clarity_module:
        'custom step name':
            'inputs':
                'your UDF name':
```

The final level of configuration configures how MultiQC handles the data itself. You can read the main [MultiQC documentation](http://multiqc.info/docs/) for more details, or see the above example for more information.

One special config param not usually available is `multiply_by`.
For example, to display a count in for Millions, set `multiply_by: 0.000001`.
To display a fraction as a percent, set `multiply_by: 100`.

## Usage
Once installed and configured the plugin should run automtically.

### `--clarity_project`
If you know the project for this run, you can specify its LUID manually to MultiQC_Clarity. This then ignores the samples found in the report and just grabs data from all samples in the specified project.

### `--clarity_skip_name_editing`
By default, MultiQC_Clarity removes the following strings from sample names before searching for them in the LIMS: `_1`, `_2`, `_R1`, `_R2`. Use this command line flag to disable this behaviour.

### `--disable_clarity`
This command line flag prevents the MultiQC_Clarity plugin from running on this MultiQC run.


## Contributors
* MultiQC_Clarity lead and main author: [@Galithil](https://github.com/Galithil)
* MultiQC lead and main author: [@ewels](https://github.com/ewels)
* MultiQC_Clarity code contributions and testing help from:
[@ewels](https://github.com/ewels)
