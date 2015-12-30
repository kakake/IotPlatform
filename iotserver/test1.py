#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'一个测试模块'

__author__ = 'kakake'

import sys

def test(args):
    if len(args)==1:
            print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test(sys.argv)
    input()