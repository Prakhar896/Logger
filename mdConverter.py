import markdown
from pygments.formatters import HtmlFormatter

def convert(markdownCode):
    formatter = HtmlFormatter(style='emacs', full=True, cssclass='codehilite')
    css_string = formatter.get_style_defs()
    md_css_string = '<style>' + css_string + '</style>'
    md_template_string = markdown.markdown(markdownCode, output_format='html5', extensions=["fenced_code", "codehilite"])
    md_template = md_css_string + md_template_string
    return md_template