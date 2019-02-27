#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import argparse
import os
from pprint import pprint
from graphviz import Digraph

parser = argparse.ArgumentParser(
        prog="stackchaser.py",
        description="Write png for CFn Relation",
        add_help=True,
        )
subparsers = parser.add_subparsers(help='string help')
parser.add_argument("-f","--file", help="import parent cloudformation file",required=True)
parser.add_argument("-p","--prefix", help="add prefix string for output file",required=False)
parser.add_argument("-o","--output-file", help="output filename",required=False)

def ChasingStack(input_filename,output_filename):
    G = Digraph(format='png',engine='fdp')
    def RemindStack(filename,ParentStackName,depth=0):
        target_file = open(filename)
        array = yaml.load(target_file)
        stacks = []
        for stack in array["Resources"]:
            stacks.append(str(stack))
        for i in range(len(stacks)):
            print(G)
            if "AWS::CloudFormation::Stack" == array["Resources"][stacks[i]]["Type"]:
                G.edge(ParentStackName,str(stacks[i]))
                RemindStack(os.path.dirname(filename)+str("/")+array["Resources"][stacks[i]]["Properties"]["TemplateURL"],str(stacks[i]),depth+1)
            else:
                if depth < 2:
                    print(stacks[i])
                    G.edge(ParentStackName,str(stacks[i]))
    RemindStack(input_filename,"Parent")
    G.render(output_filename)


if __name__ == '__main__':
    args = parser.parse_args()
    output_filename = "chasers"+os.path.basename(args.file)
    if args.output_file:
        output_filename = args.output_file
    if args.prefix:
        output_filename = args.prefix + output_filename
    ChasingStack(args.file,output_filename)
