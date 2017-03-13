# [<img src="docs/images/MultiQC_logo.png" width="250" title="MultiQC">](https://github.com/ewels/MultiQC) [<img src="docs/images/clarity_logo.png" width="250" title="Clarity LIMS">](https://www.genologics.com/clarity-lims/)

**MultiQC_Clarity is a plugin for MultiQC, able to insert project-level and sample-level
metadata from the BaseSpace Clarity LIMS into MultiQC Reports**

For more information about MultiQC, see http://multiqc.info

For more information about BaseSpace Clarity LIMS, see https://www.genologics.com/clarity-lims/

> **NB:** This package is currently under development and not yet ready for general use.

## Description

## Installation

## Configuration
Before MultiQC_Clarity will work with MultiQC, you need to tell it what information
to retrieve from the LIMS. Unfortunately, as every Clarity installation is different
from the next, this cannot be automated.

To do this, you need to add to your MultiQC configuration. See the
[main MultiQC documentation](http://multiqc.info/docs/#configuring-multiqc)
for more information on how to do this. For a single run, you can just create
a file called `multiqc_config.yaml` in the working directory.

MultiQC clarity expects a config structure that looks something like this:

```yaml
clarity:
    <report section>:
        <process>:
            '<udf>':
```

See the bundled [`multiqc_config_example.yaml`](multiqc_config_example.yaml)
file to see a real-life example of this.

One special config param not usually available is `multiply_by`.
For example, to display a count in for Millions, set `multiply_by: 0.000001`.
To display a fraction as a percent, set `multiply_by: 100`.

## Usage

### Contributors
MultiQC_Clarity lead and main author: [@Galithil](https://github.com/Galithil)

MultiQC lead and main author: [@ewels](https://github.com/ewels)

MultiQC_Clarity code contributions and testing help from:
[@ewels](https://github.com/ewels)