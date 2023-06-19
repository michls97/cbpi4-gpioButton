
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

@parameters([Property.Actor(label="Actor",  description="Select the actor that will be switched on/off when GPIO button is pressed."),
            Property.Select(label="GPIO", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="GPIO [BMC numbering] that will toggle the Actor")])
            #Property.Select(label="GPIOstate", options=["High", "Low"],description="High: Actor toggles on GPIO high; Low: Actor switches off on GPIO low"),
            #Property.Select(label="notification", options=["Yes", "No"], description="Will show notification when GPIO button is pressed")])

class gpioButton(CBPiActor):

    async def toggleActor(self):
        if self.cbpi.actor.find_by_id(self.base).instance.get_state():
            await self.cbpi.actor.off(self.base)
        else:
            await self.cbpi.actor.on(self.base)

    def measure(self, channel):
        asyncio.run(self.toggleActor())

    def on_start(self):
        self.state = True
        self.base = self.props.get("Actor", None)
        try:
            self.name = (self.cbpi.actor.find_by_id(self.base).name)
        except:
            self.name = ""
        self.ActorDependency = self.props.get("GPIO", None)
        #self.dependency_type = self.props.get("GPIOstate", "High")
        self.notification = self.props.get("notification", "Yes")
        self.interrupt = False
        mode = GPIO.getmode()
        logging.info(mode)
        if (mode == None):
            GPIO.setmode(GPIO.BCM)
        if self.ActorDependency is not None:
            GPIO.setup(int(self.ActorDependency), GPIO.IN, pull_up_down = GPIO.PUD_UP)
        else:
            pass
        pass

    async def on(self, power=0):
        GPIO.add_event_detect(int(self.ActorDependency), GPIO.FALLING, callback=self.measure, bouncetime=600)
        self.state = True

    async def off(self):
        GPIO.remove_event_detect(int(self.ActorDependency))
        self.state = False

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("GPIO Button", gpioButton)
    pass


