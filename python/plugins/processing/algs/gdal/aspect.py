# -*- coding: utf-8 -*-

"""
***************************************************************************
    aspect.py
    ---------------------
    Date                 : October 2013
    Copyright            : (C) 2013 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'October 2013'
__copyright__ = '(C) 2013, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from PyQt4.QtGui import QIcon

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.core.parameters import ParameterRaster
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterNumber
from processing.core.outputs import OutputRaster
from processing.algs.gdal.GdalUtils import GdalUtils

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class aspect(GdalAlgorithm):

    INPUT = 'INPUT'
    BAND = 'BAND'
    COMPUTE_EDGES = 'COMPUTE_EDGES'
    ZEVENBERGEN = 'ZEVENBERGEN'
    TRIG_ANGLE = 'TRIG_ANGLE'
    ZERO_FLAT = 'ZERO_FLAT'
    OUTPUT = 'OUTPUT'

    #def getIcon(self):
    #    return QIcon(os.path.join(pluginPath, 'images', 'gdaltools', 'dem.png'))

    def defineCharacteristics(self):
        self.name, self.i18n_name = self.trAlgorithm('Aspect')
        self.group, self.i18n_group = self.trAlgorithm('[GDAL] Analysis')
        self.addParameter(ParameterRaster(self.INPUT, self.tr('Input layer')))
        self.addParameter(ParameterNumber(
            self.BAND, self.tr('Band number'), 1, 99, 1))
        self.addParameter(ParameterBoolean(
            self.COMPUTE_EDGES, self.tr('Compute edges'), False))
        self.addParameter(ParameterBoolean(self.ZEVENBERGEN,
                                           self.tr("Use Zevenbergen&Thorne formula (instead of the Horn's one)"),
                                           False))
        self.addParameter(ParameterBoolean(self.TRIG_ANGLE,
                                           self.tr('Return trigonometric angle (instead of azimuth)'), False))
        self.addParameter(ParameterBoolean(self.ZERO_FLAT,
                                           self.tr('Return 0 for flat (instead of -9999)'), False))

        self.addOutput(OutputRaster(self.OUTPUT, self.tr('Aspect')))

    def getConsoleCommands(self):
        arguments = ['aspect']
        arguments.append(unicode(self.getParameterValue(self.INPUT)))
        output = unicode(self.getOutputValue(self.OUTPUT))
        arguments.append(output)

        arguments.append('-of')
        arguments.append(GdalUtils.getFormatShortNameFromFilename(output))

        arguments.append('-b')
        arguments.append(unicode(self.getParameterValue(self.BAND)))

        if self.getParameterValue(self.COMPUTE_EDGES):
            arguments.append('-compute_edges')

        if self.getParameterValue(self.ZEVENBERGEN):
            arguments.append('-alg')
            arguments.append('ZevenbergenThorne')

        if self.getParameterValue(self.TRIG_ANGLE):
            arguments.append('-trigonometric')

        if self.getParameterValue(self.ZERO_FLAT):
            arguments.append('-zero_for_flat')

        return ['gdaldem', GdalUtils.escapeAndJoin(arguments)]
