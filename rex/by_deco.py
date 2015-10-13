from functools import wraps
import re
from texts import *
from inspect import getmro, getmembers
from logging import debug as D

class Stack(list):

    push = list.append

    def __call__(self):
        return self[-1]


def rex(pattern):
    def handle_args(fn):
        fn._pattern = pattern
        return fn
    return handle_args


class PatternHook(type):

    def __new__(metacls, name, bases, attrs):
        newcls = type.__new__(metacls, name, bases, attrs)
        allre = {}
        mro = list(getmro(newcls))
        mro.reverse()
        for cls in mro:
            for key, obj in getmembers(cls):            
                try:
                    allre[key]="(?P<{}>{})".format(key, obj._pattern)
                except AttributeError:
                    pass
        allre = "|".join(allre.values())
        allre = re.compile(allre, re.MULTILINE)
        newcls.allre = allre
        return newcls



class State(metaclass=PatternHook):
    pass

    @classmethod
    def name(cls):
        return cls.__name__
        
class Frame: pass

class Parser:

    class Common(State):
    
        @rex(r'\n')
        def nl(self, mo):
            """ Count new lines """
            self.linecount += 1

        @rex(r'^[ \t]*$')
        def empty(self, mo):
            D("%s empty %r", self.stack_names(), mo)
            
        def nomatch(self, text):
            D("%s nomatch %r", self.stack_names(), text)
            self.buffer().append(text)
            
        def eot(self):
            D("%s eot, popping stack", self.stack_names())
            while self.frames:
                self.pop()

        @rex(r'\[\[')
        def link_start(self, mo):
            self.push(self.Link)

            
    class Start(Common):
    
        @rex(r'^@@')
        def txt(self, mo):
            print("txt", self.linecount)

        def nomatch(self, text):
            D("%s nomatch %r", self.stack_names(), text)
            self.push(self.Para)
            self.buffer().append(text)

    class Para(Common):

        def empty(self, mo):
            D("%s empty %r", self.stack_names(), mo)
            self.state.pop()

            
    class Link(Common):
        
        @rex(r'\]\]')
        def link_end(self, mo):
            frame = self.pop()
            self.buffer().append(frame.buffer)

    
    def __init__(self):
        self.linecount = 1 # starts from 1
        self.pos_start = 0
        self.pos_end = 0
        self.frames = Stack()
        
                
    def push(self, state):
        frame = Frame()
        frame.state = state
        frame.buffer = []
        self.frames.push(frame)

    def pop(self):
        frame = self.frames.pop()
        D("%r %r", frame.state, frame.buffer)
        return frame

    def state(self):
        return self.frames().state
    
    def buffer(self):
        return self.frames().buffer
    
    def parse_text(self, text):
        self.push(self.Start)
        while True:
            # guard if next end_pos excess text
            if self.pos_end > len(text):
                # D("==> end, match over text <==")
                break
    
            # D("search %r-%r => %r", self.pos_start, self.pos_end, len(text))
            mo = self.state().allre.search(text, self.pos_end)
            if mo:
                # D("==> nomatch(%r-%r) %r <==", self.pos_end, mo.start(), mo)
                #

                if mo.start() > self.pos_end:
                    self.state().nomatch(self, text[self.pos_end:mo.start()])
                #
                
                getattr(self.state(), mo.lastgroup)(self, mo)
                
                #
                if len(mo.group()) == 0:  # empty match
                    self.pos_end += 1
                    self.pos_start = self.pos_end
                else:
                    self.pos_start = mo.start()
                    self.pos_end = mo.end()
            else:
                # D("==> end <==")
                self.state().nomatch(self, text[self.pos_end:])
                break
    
        # signal end of text
        self.state().eot(self)

    def stack_names(self):
        return "[" + "/".join([i.state.name() for i in self.frames]) + "]"

import logging
logging.basicConfig(level=logging.DEBUG)
Parser().parse_text(text03)
