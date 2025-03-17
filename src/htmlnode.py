from functools import reduce
from typing import List, Union

class HTMLNode:
    def __init__(self, tag = None, value= None, children= None, props= None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str | NotImplementedError | ValueError:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return reduce( lambda acc, item: acc + f' {item[0]}="{item[1]}"' , self.props.items() , "")
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, { self.children }, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,  tag, value, props=None) -> None:
        super().__init__(tag, value, props=props)
    
    def to_html(self) -> str | ValueError:
        if not self.value :
            raise ValueError("No value provided")
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)


    def to_html(self) -> str | ValueError:
        if not self.children :
            raise ValueError("No child(ren) provided")
        if not self.tag:
           raise ValueError("No tag provided")
        else:
            return f"<{self.tag}{self.props_to_html() if self.props else ""}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"