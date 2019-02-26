#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import argparse
import os
from pprint import pprint

parser = argparse.ArgumentParser(
        prog="stackchaser.py",
        description="Write png for CFn Relation",
        add_help=True,
        )
subparsers = parser.add_subparsers(help='string help')
parser.add_argument("-f","--file", help="import parent cloudformation file",required=True)
parser.add_argument("-p","--prefix", help="add prefix string for output file",required=False)
parser.add_argument("-o","--output-file", help="output filename",required=False)

def RemindStack(filename,depth=0):
    target_file = open(filename)
    array = yaml.load(target_file)
    Nest = []
    stacks = []
    for stack in array["Resources"]:
        stacks.append(str(stack))
    for i in range(len(stacks)):
        if "AWS::CloudFormation::Stack" == array["Resources"][stacks[i]]["Type"]:
            Nest.append({stacks[i]:RemindStack(os.path.dirname(filename)+str("/")+array["Resources"][stacks[i]]["Properties"]["TemplateURL"],depth+1)})
        else:
            if depth < 2:
                Nest.append(str(stacks[i]))
    return Nest


def CreateGraphviz(StackList,filename):
    from graphviz import Digraph

    G = Digraph(format='png',engine='fdp')
    def CreateNode(StackList,ParentStackName):

        for Stack in StackList:
            if type(Stack) is str:
                G.node(Stack)
            elif type(Stack) is dict:
                key = list(Stack.keys())[0]
                CreateNode(Stack[key],key)
                G.edge(ParentStackName,str(key))
    CreateNode(StackList,"Parent")
    G.render(filename)

if __name__ == '__main__':
    args = parser.parse_args()
    StackList = RemindStack(args.file)
    # pprint(StackList)
    filename = "chasers"+os.path.basename(args.file)
    if args.output_file:
        filename = args.output_file
    if args.prefix:
        filename = args.prefix + filename
    CreateGraphviz(StackList,filename)
