"""Calculating \\(\\pi\\) the simple way, but this is called
dummypi to avoid conflict with simplepi in the databench_examples repo."""

import math
from time import sleep
from random import random

import databench


class Dummypi(databench.Analysis):

    def on_connect(self):
        self.data['samples'] = 500

    def on_run(self):
        """Run when button is pressed."""

        inside = 0
        for i in range(self.data['samples']):
            sleep(0.001)
            r1, r2 = (random(), random())
            if r1*r1 + r2*r2 < 1.0:
                inside += 1

            if (i+1) % 100 == 0:
                draws = i+1
                self.emit('log', {
                    'draws': draws,
                    'inside': inside,
                    'r1': r1,
                    'r2': r2,
                })

                p = float(inside)/draws
                uncertainty = 4.0*math.sqrt(draws*p*(1.0 - p)) / draws
                self.data['pi'] = {
                    'estimate': 4.0*inside/draws,
                    'uncertainty': uncertainty,
                }

        self.emit('log', {'action': 'done'})

    def on_test_fn(self, first_param, second_param=100):
        """Echo params."""
        print(first_param, second_param)
        self.emit('test_fn', {
            'first_param': first_param,
            'second_param': second_param,
        })


META = databench.Meta('dummypi', Dummypi)
