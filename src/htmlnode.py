class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_text = ""
        for p in self.props:
            html_text += " " + p + '="' + self.props[p] + '"'
        return html_text

    def __repr__(self):
        return f"Tag: {self.tag} /n Value: {self.value} /n Children: {self.children} /n Props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No Value : Invalid Node")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Tag: {self.tag} /n Value: {self.value} /n Props: {self.props}"
