# -*- coding: utf-8 -*-

"""# Functions for getting and setting style DEPEDENDENCIES, organized into sections:

I. General functions for getting and setting dependencies
II. Specific functions for setting particular dependencies

License:
    Copyright 2020 The Cytoscape Consortium

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
    documentation files (the "Software"), to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions
    of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# External library imports
import sys
import time

# Internal module imports
from . import commands
from . import styles

# Internal module convenience imports
from .exceptions import CyError
from .py4cytoscape_utils import *
from .py4cytoscape_logger import cy_log
from .py4cytoscape_tuning import MODEL_PROPAGATION_SECS



# ==============================================================================
# I. General Functions
# ------------------------------------------------------------------------------

def get_style_dependencies(style_name='default', base_url=DEFAULT_BASE_URL):
    """Get the values of dependencies in a style.

    Args:
        style_name (str): Name of style; default is "default" style
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of py4cytoscape.

    Returns:
        dict: contains all dependencies and their current boolean value

    Raises:
        CyError: if style name doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> get_style_dependencies(style_name='galFiltered Style')
        {'arrowColorMatchesEdge': False, 'nodeCustomGraphicsSizeSync': True, 'nodeSizeLocked': True}
        >>> get_style_dependencies()
        {'arrowColorMatchesEdge': False, 'nodeCustomGraphicsSizeSync': True, 'nodeSizeLocked': False}
    """
    # launch error if visual style name is missing
    if style_name not in styles.get_visual_style_names(base_url=base_url):
        error = 'Error in py4cytoscape:get_style_dependencies. No visual style named "' + style_name + '"'
        # TODO: R version of this error has the wrong text
        sys.stderr.write(error)
        raise CyError(error)
    #        return None
    # TODO: Is this what we want to return here?

    res = commands.cyrest_get('styles/' + style_name + '/dependencies', base_url=base_url)

    # make it a dict
    dep_list = {dep['visualPropertyDependency']: dep['enabled'] for dep in res}
    return dep_list


def set_style_dependencies(style_name='default', dependencies={}, base_url=DEFAULT_BASE_URL):
    """Set the values of dependencies in a style, overriding any prior setting.

    Args:
        style_name (str): Name of style; default is "default" style
        dependencies (dict): A ``list`` of style dependencies, see Available Dependencies below. Note: each dependency
            is set by a boolean, True or False
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of py4cytoscape.

    Returns:
        dict: contains the ``views`` property with a value of the current view's SUID (e.g., {'views': [275240]})

    Raises:
        CyError: if style name doesn't exist
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >>> set_style_dependencies(dependencies={'arrowColorMatchesEdge': True}, style_name='galFiltered Style')
        {'views': [275240]}
        >>> get_style_dependencies(dependencies={'arrowColorMatchesEdge': True, 'nodeCustomGraphicsSizeSync': False})
        {'views': [275240]}

    Available Dependencies:
        arrowColorMatchesEdge
        nodeCustomGraphicsSizeSync
        nodeSizeLocked
    """
    # launch error if visual style name is missing
    if style_name not in styles.get_visual_style_names(base_url=base_url):
        error = 'Error in py4cytoscape:set_style_dependencies. No visual style named "' + style_name + '"'
        # TODO: R version of this error has the wrong text
        sys.stderr.write(error)
        raise CyError(error)
        # return None
        # TODO: Is this what we want to return here?

    dep_list = [{'visualPropertyDependency': dep, 'enabled': val}    for dep, val in dependencies.items()]

    res = commands.cyrest_put('styles/' + style_name + '/dependencies', body=dep_list, base_url=base_url, require_json=False)
    res = commands.commands_post('vizmap apply styles="' + style_name + '"')
    # TODO: Do we really want to lose the first res value?
    return res




def lock_node_dimensions(new_state, style_name='default', base_url=DEFAULT_BASE_URL):
    toggle = 'true' if new_state else 'false'

    res = set_style_dependencies(style_name=style_name, dependencies={'nodeSizeLocked': toggle}, base_url=base_url)

    return res
