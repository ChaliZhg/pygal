# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Pie chart

"""

from __future__ import division
from pygal.util import decorate
from pygal.graph.graph import Graph
from math import pi


class Pie(Graph):
    """Pie graph"""

    def slice(self, serie_node, start_angle, serie, total):
        """Make a serie slice"""

        slices = self.svg.node(serie_node['plot'], class_="slices")
        serie_angle = 0
        original_start_angle = start_angle
        center = ((self.width - self.margin.x) / 2.,
                  (self.height - self.margin.y) / 2.)
        radius = min(center)
        for i, val in enumerate(serie.values):
            perc = val / total
            angle = 2 * pi * perc
            serie_angle += angle
            val = '{0:.2%}'.format(perc)
            metadata = serie.metadata[i]
            slice_ = decorate(
                self.svg,
                self.svg.node(slices, class_="slice"),
                metadata)
            if len(serie.values) > 1:
                small_radius = radius * .9
            else:
                radius = radius * .9
                small_radius = 0

            self.svg.slice(serie_node,
                slice_, radius, small_radius, angle, start_angle, center, val)
            start_angle += angle

        if len(serie.values) > 1:
            self.svg.slice(serie_node,
                slice_, radius * .9, 0, serie_angle,
                original_start_angle, center, val)
        return serie_angle

    def _compute(self):
        for serie in self.series:
            serie.values = map(lambda x: max(x, 0), serie.values)
        return super(Pie, self)._compute()

    def _plot(self):
        total = sum(map(sum, map(lambda x: x.values, self.series)))

        if total == 0:
            return
        current_angle = 0
        for serie in self.series:
            angle = self.slice(
                self._serie(serie.index), current_angle, serie, total)
            current_angle += angle