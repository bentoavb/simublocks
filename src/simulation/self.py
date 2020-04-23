# MIT License
#
# Copyright (c) 2020 Anderson Vitor Bento
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
from src.element import Workspace
from src.simulation.tools import simulationTools
from src.simulation.plot import Plot

class Self(simulationTools):

    def __init__(self,T,tf):
        conns = Workspace.connections
        blocks = Workspace.blocks
        s = {
            't': np.arange(0,tf+T,T),
            'T': T,
            'inputs': {},
            'blocks': {}
        }

        exec(Workspace.importCode,s)
        s = self.loadBlocks(s)

        for i in s['inputs']:
            exec(s['inputs'][i].code,s)
            for k in range(len(s['t'])):
                s['inputs'][i].input[k] = s[s['inputs'][i].name](s['t'][k],k)
        
        for k in range(len(s['t']) -1):
            for i in s['blocks']:
                b = s['blocks'][i]
                if 'otherblock' in b.conn[0]:
                    first = b.conn[0]['otherblock']
                    b.u[k] = self.search(first, k)
                else:
                    b.u[k] = 0
                b.x[k+1] = b.ss[0]@b.x[k] + b.ss[1]*b.u[k]
        
        Plot.run(s)
        