#!/usr/bin/env python
""" MultiQC command line options - we tie into the MultiQC
core here and add some new command line parameters. """

import click

c_disable = click.option('--disable_clarity',
    is_flag = True,
    default = False,
    help = "Disable the MultiQC_Clarity plugin on this run"
)
c_pname = click.option('--clarity_project',
    type = str,
    help = 'Manually specify a project name in Clarity Lims instead of automatically matching sample names'
)
c_edit_patterns = click.option('--clarity_skip_name_editing',
    is_flag = True,
    default = False,
    help = "Do not edit the sample names to remove suffixes like _1, _2, _R1, _R2."
)
