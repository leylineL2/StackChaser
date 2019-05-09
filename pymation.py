from yaml import *

def construct_aws_ref(self,node):
    node.value = "!Ref "+node.value
    # print(node)
    return self.construct_yaml_str(node)


def construct_aws_sub(self,node):
    # print(self.construct_yaml_seq(node))
    # print(node)
    if isinstance(node, ScalarNode):
        node.value = "!Sub "+node.value
        # print(node)
        self.construct_yaml_str(node)
        # print(self.construct_scalar(node))
    elif isinstance(node, SequenceNode):
        # print(node.value)
        return [self.construct_object(child, deep=True)
                for child in node.value]
    else:
        raise ConstructorError(None, None,
                "expected a sequence node, but found %s" % node.id,
                node.start_mark)

def construct_aws_select(self,node):
            # print(node)
    return [self.construct_object(child, deep=True)
        for child in node.value]

def construct_aws_join(self,node):
            # print(node)
    return [self.construct_object(child, deep=True)
        for child in node.value]

constructor.Constructor.construct_aws_ref = construct_aws_ref
constructor.Constructor.construct_aws_sub = construct_aws_sub
constructor.Constructor.construct_aws_select = construct_aws_select
constructor.Constructor.construct_aws_join = construct_aws_join

constructor.Constructor.add_constructor(
        '!Ref',
        constructor.Constructor.construct_aws_ref)

constructor.Constructor.add_constructor(
        '!Sub',
        constructor.Constructor.construct_aws_sub)

constructor.Constructor.add_constructor(
        '!GetAtt',
        constructor.Constructor.construct_yaml_str)

constructor.Constructor.add_constructor(
        '!Select',
        constructor.Constructor.construct_aws_select)

constructor.Constructor.add_constructor(
        '!Join',
        constructor.Constructor.construct_aws_join)
