#!/micropython
# -*- coding: utf-8 -*-
#
# Copyright 2020-2025 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2025-10-21
# modified: 2025-10-22

from colorama import Fore, Style

from core.logger import Logger, Level
from core.component import Component
from response import Response

class MotorController(Component):
    '''
    A controller for four brushless motors. This operates in both open- and
    closed loop mode, and optionally supports slew limiting and zero-crossing
    behaviours.

    Args:
        config:   application-level configuration
        level:    log level
    '''
    def __init__(self, config=None, level=Level.INFO):
        self._log = Logger('motor-ctrl', level=level)
        Component.__init__(self, self._log, suppressed=False, enabled=False)
        self._log.info('initialising motor controller…')
        if config is None:
            raise ValueError('no configuration provided.')
        self._config     = config
        self._pfwd = 0.0
        self._sfwd = 0.0
        self._paft = 0.0
        self._saft = 0.0
        self._debug = False
        self._log.info('ready.')

    def get_speeds(self):
        return ( self._pfwd, self._sfwd, self._paft, self._saft )

    def stop(self):
        '''
        Stop all motors immediately.
        '''
        if not self.enabled:
            return Response.FAIL
        if self._debug:
            self._log.info(Fore.RED + 'STOP')
        self._pfwd = 0.0
        self._sfwd = 0.0
        self._paft = 0.0
        self._saft = 0.0
        return Response.OKAY

    def go(self, pfwd, sfwd, paft, saft):
        '''
        Set the speeds of each of the four motors.
        '''
        if not self.enabled:
            return Response.FAIL
        if self._debug:
            self._log.info(Fore.GREEN + 'GO (pfwd={:.2f}, sfwd={:.2f}, paft={:.2f}, saft={:.2f})'.format(pfwd, sfwd, paft, saft))
        self._pfwd = pfwd
        self._sfwd = sfwd
        self._paft = paft
        self._saft = saft
        return Response.OKAY

    def enable(self):
        '''
        Enable the motor controller.
        '''
        if not self.enabled:
            Component.enable(self)
            if self._debug:
                self._log.info('enabled.')
            
    def disable(self):
        '''
        Disable the motor controller.
        '''
        if self.enabled:
            self.stop()
            Component.disable(self)
            if self._debug:
                self._log.info('disabled.')
            
    def close(self):
        if not self.closed:
            self.disable()
            Component.close(self)
            if self._debug:
                self._log.info('closed.')

#EOF
