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
    G = Digraph(format='png',engine='sfdp')
    def RemindStack(filename,ParentStackName,depth=0):
        target_file = open(filename)
        array = yaml.load(target_file)
        stacks = []
        G.attr('node',shape="box",style="filled",color="#f75d89",fillcolor = "#f75d89",fontcolor="black")
        G.node(ParentStackName)
        for stack in array["Resources"]:
            stacks.append(str(stack))
        for i in range(len(stacks)):
            if "AWS::CloudFormation::Stack" == array["Resources"][stacks[i]]["Type"]:
                G.attr('node',shape="box",style="filled",color="#8be268",fillcolor = "#8be268",fontcolor="black")
                G.edge(ParentStackName,str(stacks[i]))
                nested_cfn_filepath = os.path.dirname(filename)+str("/")+array["Resources"][stacks[i]]["Properties"]["TemplateURL"]
                RemindStack(nested_cfn_filepath,str(stacks[i]),depth+1)
            else:
                if depth < 2:
                    G.attr('node',style="filled",color="#4286f4",fillcolor = "#4286f4",fontcolor="white")
                    G.edge(ParentStackName,str(stacks[i]))

    RemindStack(input_filename,"Parent")
    # G.render(output_filename)


if __name__ == '__main__':
    args = parser.parse_args()
    output_filename = "chasers"+os.path.basename(args.file)
    if args.output_file:
        output_filename = args.output_file
    if args.prefix:
        output_filename = args.prefix + output_filename
    ChasingStack(args.file,output_filename)
