# Copyright (c) 2000-2002 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
utilities functions to generate file readable with Georg Sander's vcg
(Visualization of Compiler Graphs).

You can download vcg at http://rw4.cs.uni-sb.de/~sander/html/gshome.html
Note that vcg exists as a debian package.

See the documentation of vcg for explanation about the different value that
maybe used for the functions parameters
"""

__revision__ = "$Id: vcgutils.py,v 1.2 2004-10-26 14:18:34 fabioz Exp $"

import string

ATTRS_VAL = {
    'algos':       ('dfs', 'tree', 'minbackward',
                    'left_to_right','right_to_left',
                    'top_to_bottom','bottom_to_top',
                    'maxdepth', 'maxdepthslow', 'mindepth', 'mindepthslow',
                    'mindegree', 'minindegree', 'minoutdegree',
                    'maxdegree','maxindegree', 'maxoutdegree'),
    'booleans':    ('yes', 'no'),
    'colors':      ('black', 'white', 'blue', 'red', 'green', 'yellow',
                    'magenta', 'lightgrey',
                    'cyan', 'darkgrey', 'darkblue', 'darkred', 'darkgreen',
                    'darkyellow', 'darkmagenta', 'darkcyan', 'gold',
                    'lightblue', 'lightred', 'lightgreen', 'lightyellow',
                    'lightmagenta', 'lightcyan', 'lilac', 'turquoise',
                    'aquamarine', 'khaki', 'purple', 'yellowgreen', 'pink',
                    'orange', 'orchid'),
    'shapes':      ('box', 'ellipse', 'rhomb', 'triangle'),
    'textmodes':   ('center', 'left_justify', 'right_justify'),
    'arrowstyles': ('solid', 'line', 'none'),
    'linestyles':  ('continuous', 'dashed', 'dotted', 'invisible'),
    }

# meaning of possible values:
#   O    -> string
#   1    -> int 
#   list -> value in list
GRAPH_ATTRS = {
    'title' :              0,
    'label' :              0,
    'color':               ATTRS_VAL['colors'],
    'textcolor':           ATTRS_VAL['colors'],
    'bordercolor':         ATTRS_VAL['colors'],
    'width':               1,
    'height':              1,
    'borderwidth':         1,
    'textmode':            ATTRS_VAL['textmodes'],
    'shape':               ATTRS_VAL['shapes'],
    'shrink':              1,
    'stretch':             1,
    'orientation':         ATTRS_VAL['algos'],
    'vertical_order':      1,
    'horizontal_order':    1,
    'xspace':              1,
    'yspace':              1,
    'layoutalgorithm' :    ATTRS_VAL['algos'],
    'late_edge_labels' :   ATTRS_VAL['booleans'],
    'display_edge_labels': ATTRS_VAL['booleans'],
    'dirty_edge_labels' :  ATTRS_VAL['booleans'],
    'finetuning':          ATTRS_VAL['booleans'],
    'manhattan_edges':     ATTRS_VAL['booleans'],
    'smanhattan_edges':    ATTRS_VAL['booleans'],
    'port_sharing':        ATTRS_VAL['booleans'],
    'edges':               ATTRS_VAL['booleans'],
    'nodes':               ATTRS_VAL['booleans'],
    'splines':             ATTRS_VAL['booleans'],
    }
NODE_ATTRS = {
    'title' :              0,
    'label' :              0,
    'color':               ATTRS_VAL['colors'],
    'textcolor':           ATTRS_VAL['colors'],
    'bordercolor':         ATTRS_VAL['colors'],
    'width':               1,
    'height':              1,
    'borderwidth':         1,
    'textmode':            ATTRS_VAL['textmodes'],
    'shape':               ATTRS_VAL['shapes'],
    'shrink':              1,
    'stretch':             1,
    'vertical_order':      1,
    'horizontal_order':    1,
    }
EDGE_ATTRS = {
    'sourcename' :         0,
    'targetname' :         0,
    'label' :              0,
    'linestyle' :          ATTRS_VAL['linestyles'],
    'class' :              1,
    'thickness' :          0,
    'color':               ATTRS_VAL['colors'],
    'textcolor':           ATTRS_VAL['colors'],
    'arrowcolor':          ATTRS_VAL['colors'],
    'backarrowcolor':      ATTRS_VAL['colors'],
    'arrowsize':           1,
    'backarrowsize':       1,
    'arrowstyle':          ATTRS_VAL['arrowstyles'],
    'backarrowstyle':      ATTRS_VAL['arrowstyles'],
    'textmode':            ATTRS_VAL['textmodes'],
    'priority':            1,
    'anchor':              1,
    'horizontal_order':    1,
    }


# Misc utilities ###############################################################

def latin_to_vcg(st):
    """convert latin characters using vcg escape sequence
    """
    for char in st:
        if char not in string.ascii_letters:
            try:
                num = ord(char)
                if num >= 192:
                    st = st.replace(char, r'\fi%d'%ord(char))
            except:
                pass
    return st


class VCGPrinter:
    """a vcg graph writer
    """
    
    def __init__(self, output_stream):
        self._stream = output_stream
        self._indent = ''

    def open_graph(self, **args):
        """open a vcg graph
        """
        self._stream.write('%sgraph:{\n'%self._indent)
        self._inc_indent()
        self._write_attributes(GRAPH_ATTRS, **args)

    def close_graph(self):
        """close a vcg graph
        """
        self._dec_indent()
        self._stream.write('%s}\n'%self._indent)


    def node(self, title, **args):
        """draw a node
        """
        self._stream.write('%snode: {title:"%s"' % (self._indent, title))
        self._write_attributes(NODE_ATTRS, **args)
        self._stream.write('}\n')


    def edge(self, from_node, to_node, edge_type='', **args):
        """draw an edge from a node to another.
        """
        self._stream.write(
            '%s%sedge: {sourcename:"%s" targetname:"%s"' % (
            self._indent, edge_type, from_node, to_node))
        self._write_attributes(EDGE_ATTRS, **args)
        self._stream.write('}\n')


    # private ##################################################################
    
    def _write_attributes(self, attributes_dict, **args):
        """write graph, node or edge attributes
        """
        for key, value in args.items():
            try:
                _type =  attributes_dict[key]
            except KeyError:
                raise Exception('''no such attribute %s
possible attributes are %s''' % (key, attributes_dict.keys()))

            if not _type:
                self._stream.write('%s%s:"%s"\n' % (self._indent, key, value))
            elif _type == 1:
                self._stream.write('%s%s:%s\n' % (self._indent, key,
                                                  int(value)))
            elif value in _type:
                self._stream.write('%s%s:%s\n' % (self._indent, key, value))
            else:
                raise Exception('''value %s isn\'t correct for attribute %s
correct values are %s''' % (value, key, _type))
    
    def _inc_indent(self):
        """increment indentation
        """
        self._indent = '  %s' % self._indent
        
    def _dec_indent(self):
        """decrement indentation
        """
        self._indent = self._indent[:-2]
